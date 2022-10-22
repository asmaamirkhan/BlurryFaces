# author: Asmaa Mirkhan ~ 2019

import os
import argparse
import cv2
from DetectorAPI import Detector


def blurBoxes(image, boxes, blur_strength, extend_selection):
    """
    Argument:
    image -- the image that will be edited as a matrix
    boxes -- list of boxes that will be blurred each element must be a dictionary that has [id, score, x1, y1, x2, y2] keys

    Returns:
    image -- the blurred image as a matrix
    """

    for box in boxes:
        # unpack each box
        x1, y1 = box["x1"], box["y1"]
        x2, y2 = box["x2"], box["y2"]

        height, width, _ = image.shape

        x1 = max(0, x1 - extend_selection)
        x2 = min(width, x2 + extend_selection)
        y1 = max(0, y1 - extend_selection)
        y2 = min(height, y2 + extend_selection)

        # crop the image due to the current box
        sub = image[y1:y2, x1:x2]

        # apply GaussianBlur on cropped area
        blur = cv2.blur(sub, (blur_strength, blur_strength))

        # paste blurred image on the original image
        image[y1:y2, x1:x2] = blur

    return image


def main(args):
    # assign model path and threshold
    model_path = args.model_path
    threshold = args.threshold
    blur_strength = args.blur_strength
    extend_selection = args.extend_selection

    # create detection object
    detector = Detector(model_path=model_path, name="detection")

    # open video
    capture = cv2.VideoCapture(args.input_video)

    # video width = capture.get(3)
    # video height = capture.get(4)
    fps = capture.get(5)

    if args.output_video:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        output = cv2.VideoWriter(
            args.output_video, fourcc, fps, (int(
                capture.get(3)), int(capture.get(4)))
        )

    frame_counter = 0
    while True:
        # read frame by frame
        _, frame = capture.read()
        frame_counter += 1

        # the end of the video?
        if frame is None:
            break

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        # real face detection
        faces = detector.detect_objects(frame, threshold=threshold)

        # apply blurring
        frame = blurBoxes(frame, faces, blur_strength, extend_selection)

        # show image
        cv2.imshow('blurred', frame)

        # if image will be saved then save it
        if args.output_video:
            output.write(frame)
            print('Blurred video has been saved successfully at',
                  args.output_video, 'path')

    # when any key has been pressed then close window and stop the program

    cv2.destroyAllWindows()


if __name__ == "__main__":
    # creating argument parser
    parser = argparse.ArgumentParser(description='Image blurring parameters')

    # adding arguments
    parser.add_argument('-i',
                        '--input_video',
                        help='Path to your video',
                        type=str,
                        required=True)
    parser.add_argument('-m',
                        '--model_path',
                        help='Path to .pb model',
                        type=str,
                        required=True)
    parser.add_argument('-o',
                        '--output_video',
                        help='Output file path',
                        type=str)
    parser.add_argument('-t',
                        '--threshold',
                        help='Face detection confidence',
                        default=0.7,
                        type=float)
    parser.add_argument('-s',
                        '--blur_strength',
                        help='Blur strength, default 25',
                        default=25,
                        type=int)
    parser.add_argument('-e',
                        '--extend_selection',
                        help='Extend the selected area by x amount of pixels',
                        default=0,
                        type=int)
    args = parser.parse_args()

    # if input image path is invalid then stop
    assert os.path.isfile(args.input_video), 'Invalid input file'

    # if output directory is invalid then stop
    if args.output_video:
        assert os.path.isdir(os.path.dirname(
            args.output_video)), 'No such directory'

    main(args)
