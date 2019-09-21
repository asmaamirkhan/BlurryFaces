# author: Asmaa Mirkhan ~ 2019

import os
import argparse
import cv2 as cv
import tensorflow as tf
import numpy as np
import time

class DetectorAPI:
    def __init__(self, path_to_ckpt):
        self.path_to_ckpt = path_to_ckpt
 
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
 
        self.default_graph = self.detection_graph.as_default()
        self.sess = tf.Session(graph=self.detection_graph)
 
        # Definite input and output Tensors for detection_graph
        self.image_tensor = self.detection_graph.get_tensor_by_name(
            'image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        self.detection_boxes = self.detection_graph.get_tensor_by_name(
            'detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        self.detection_scores = self.detection_graph.get_tensor_by_name(
            'detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name(
            'detection_classes:0')
        self.num_detections = self.detection_graph.get_tensor_by_name(
            'num_detections:0')
 
    def processFrame(self, image):
        # Expand dimensions since the trained_model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image, axis=0)
        # Actual detection.
        start_time = time.time()
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores,
                self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})
        end_time = time.time()
 
        print("Elapsed Time:", end_time-start_time)
 
        im_height, im_width, _ = image.shape
        boxes_list = [None for i in range(boxes.shape[1])]
        for i in range(boxes.shape[1]):
            boxes_list[i] = (int(boxes[0, i, 1] * im_width),
                            int(boxes[0, i, 0] * im_height),
                             int(boxes[0, i, 3] * im_width),
                             int(boxes[0, i, 2] * im_height)
                             )
 
        return boxes_list, scores[0].tolist(), [int(x) for x in classes[0].tolist()], int(num[0])
 
    def close(self):
        self.sess.close()
        self.default_graph.close()

def blurBoxes(image, boxes):
    """
    Argument:
    image -- the image that will be edited as a matrix
    boxes -- list of boxes that will be blurred, each box must be int the format (x_top_left, y_top_left, width, height)
    
    Returns:
    image -- the blurred image as a matrix
    """
    
    for box in boxes:
        # unpack each box
        x,y,w,h = [d for d in box]
        
        # crop the image due to the current box
        sub = image[y:y+h, x:x+w]
        
        # apply GaussianBlur on cropped area
        blur = cv.GaussianBlur(sub, (23,23), 30)
        
        # paste blurred image on the original image
        image[y:y+h, x:x+w] = blur
        
    return image


def main(args):
    model_path = args.model_path
    odapi = DetectorAPI(path_to_ckpt=model_path)
    threshold = 0.7

    image = cv.imread(args.input_image)
    boxes, scores, classes, num = odapi.processFrame(image)
    boxes = boxes[0:num]
    boxes = [list(b) for b in boxes]
    boxes = [boxes[i] for i in range(0, num) if scores[i] > threshold]
    
    print(boxes)
    print(scores)
    print(classes)
    for i,box in enumerate(boxes):
        if scores[i] > 0.5:
            print(box)
            x1,y1,x2,y2 = [d for d in box]
            cv.rectangle(image, (x1, y1), (x2,y2), (255, 0, 0), 1)

    print(image.shape)
    cv.imshow('blurred',image)
    # apply blurring
    #image = blurBoxes(image, ROIs)
    
    # if image will be saved then save it
    if args.output_image:
        cv.imwrite(args.output_image,image)
    cv.imshow('blurred',image)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    

if __name__ == "__main__":
    # creating argument parser
    parser = argparse.ArgumentParser(description='Image blurring parameters')
    
    # adding arguments
    parser.add_argument('-i', '--input_image',
                        help='Path to your image', type=str, required=True)
    parser.add_argument('-m', '--model_path',
                        help='Path to .pb model', type=str, required=True)
    parser.add_argument('-o', '--output_image',
                        help='Output file path', type=str)
    args = parser.parse_args()
    
    # if input image path is invalid then stop
    assert os.path.isfile(args.input_image), 'Invalid input file'
    
    # if output directory is invalid then stop
    if args.output_image:
        assert os.path.isdir(os.path.dirname(
            args.output_image)), 'No such directory'

    main(args)
