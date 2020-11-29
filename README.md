# 🕵️‍♀️ Blurry Faces
A tool to blur faces or other regions in photos and videos 🕵️‍

## 🙌 Available Codes
1. [auto_blur_image](./src/auto_blur_image.py): Detects and blurs faces _(or objects)_ in a given image automatically due to a Tensorflow model
2. [auto_blur_video](./src/auto_blur_video.py): Detects and blurs faces _(or objects)_ in a given video due to a Tensorflow model
3. [manual_blur_image](./src/manual_blur_image.py): Blurs manually selected faces _(or objects)_


## 🔧🔩 Usage 
1. Clone or download this repo
2. Open [src](/src) folder in CMD
3. Install required packages
   ```bash
   pip install -r requirements.txt
   ```

#### For `auto_blur_image.py`:
4. Run:
   ```bash
   python auto_blur_image.py --input_image <PATH_TO_INPUT_JPG_FILE> --output_image <PATH_TO_OUTPUT_JPG_FILE>  --model_path <PATH_TO_INPUT_PB_FILE> --threshold <THRESHOLD>
   ```

#### For `auto_blur_video.py`:
4. Run:
   ```bash
   python auto_blur_video.py --input_video <PATH_TO_INPUT_MP4_FILE> --output_video <PATH_TO_OUTPUT_MP4_FILE> --model_path  <PATH_TO_INPUT_PB_FILE>  --threshold <THRESHOLD>
   ```

#### For `manual_blur_image.py`:
4. Run:
   ```bash
   python manual_blur_image.py --input_image <PATH_TO_INPUT_JPG_FILE> --output_image <PATH_TO_OUTPUT_JPG_FILE>
   ```
    * Select your ROI (Region of Interest)
    * Press <kbd>Enter</kbd>
    * Press <kbd>Q</kbd> to finish **or** any key to select another ROI

5. To see running options run _for all codes_:
   ```bash
   python manual_blur_image.py --help
   ```

6. TADAA 🎉 It's done 🤗

## 🤗 Examples

#### For `auto_blur_image.py`:
<img src="./outputs/auto_blur_image.jpg" width="600"  />

> Threshold = 0.4

#### For `auto_blur_video.py`:
![](./outputs/auto_blur_video.gif)

> Threshold = 0.4

#### For `manual_blur_image.py`:
![](./outputs/manual_blur_image.gif)

## 📍 Note
I am using face detection model in [face_model](./face_model) folder that can detects faces but codes are valid for any `.pb` object detection model.

## 📖 References 
* [Face Detection Model](https://github.com/yeephycho/tensorflow-face-detection)
* [Original Video of Imitation Game Trailer](https://www.youtube.com/watch?v=j2jRs4EAvWM)

## 🦸‍♀️ Project's Core Codes
- [📍 TensorFlow Object Detection:](https://github.com/asmaamirkhan/TFObjectDetection) check out this repo in case that you want to use the core code for other purpose 

## 💼 Contact
Find me on [LinkedIn](https://www.linkedin.com/in/asmaamirkhan/) and feel free to mail me, [Asmaa 🦋](mailto:asmaamirkhan.am@gmail.com)
