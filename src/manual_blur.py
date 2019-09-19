# author: Asmaa Mirkhan ~ 2019

import os
import argparse
import cv2 as cv


def blurBoxes(image, boxes):
    for box in boxes:
        x,y,w,h = [d for d in box]
        sub = image[y:y+h, x:x+w]
        blur = cv.GaussianBlur(sub, (23,23), 30)
        image[y:y+h, x:x+w] = blur
    return image


def main(args):
    image = cv.imread(args.input_image)
    temp_image = image.copy()
    ROIs = []
    while True:
        box = cv.selectROI('blur', temp_image, fromCenter=False)
        ROIs.append(box)
        cv.rectangle(temp_image, (box[0],box[1]), (box[0]+box[2], box[1]+box[3]), (0,255,0), 3)
        print('ROI is saved, press q to stop capturing, press any other key to select other ROI')
        key = cv.waitKey(0)
        if key & 0xFF == ord('q'):
            break
        
    image = blurBoxes(image, ROIs)

    if args.output_image:
        cv.imwrite(args.output_image,image)
    cv.imshow('blurred',image)
    cv.waitKey(0)
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Image blurring parameters')
    parser.add_argument('-i', '--input_image',
                        help='Path to your image', type=str, required=True)
    parser.add_argument('-o', '--output_image',
                        help='Output file path', type=str)
    args = parser.parse_args()
    assert os.path.isfile(args.input_image), 'Invalid input file'
    if args.output_image:
        assert os.path.isdir(os.path.dirname(
            args.output_image)), 'No such directory'

    main(args)