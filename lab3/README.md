# Locate People and Objects

This lab will show you how to run pretrained models to locate people and 
objects in images, optimize their latency, and train on custom classes.

## Train your Model

Just like in Lab 2, we'll be training our models on a cloud server, using
Google's free Colab service. [Open the notebook](https://colab.research.google.com/github/ee292d/labs/blob/main/lab2/notebook.ipynb)
and follow the directions until you have completed the [Download a Model](https://colab.research.google.com/github/ee292d/labs/blob/main/lab3/notebook.ipynb#scrollTo=8Ne3OOfjut-F&line=6&uniqifier=1)
step and have the `yolov8n_int8.tflite` file downloaded.

## Upload your Model to the Pi

You should be remotely connected to your Pi through VS Code, with this 
repository open. In the file explorer, open up the `models` folder, and drag
the YOLO model file into it, as you did with the flower model on the previous
lab.

## Test the Model

This lab includes an example image of a bus with people in front that we can
test the model on using this command:

```bash
cd ~/labs/lab3
python locate_objects.py --model_file=../models/yolov8n_int8.tflite --label_file=../models/yolov8_labels.txt --image=../images/bus.jpg
```

The three arguments are the path to the model file, the path to a labels file,
and the image file to use as the input.

You should see something like this:

```bash
INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
person: 0.83 (39, 135) 51x108
bus: 0.82 (113, 100) 218x107
person: 0.72 (79, 130) 33x93
person: 0.66 (205, 123) 37x117
time: 24.521ms
```

To have some fun with it, you can also take live camera input and output the results to an image you can view in VS Code, with this command:

```bash
python locate_objects.py \
  --model_file=../models/yolov8n_224_int8.tflite \
  --label_file=../models/yolov8_labels.txt \
  --camera=0 \
  --save_output=output.png
```

You'll need to find the `output.png` image in the `labs3` folder in VS Code's
file explorer. Once you select that, you should see the camera input with
bounding boxes and labels overlaid.

## Train a Custom Model

The default YOLOv8 model is trained on the COCO2017 dataset, which contains 80
different categories of objects. It's likely that a real-world application will
need to recognize other classes though, so to complete this lab [return to the Colab to learn how to retrain a model to recognize custom categories](https://colab.research.google.com/github/ee292d/labs/blob/main/lab3/notebook.ipynb#scrollTo=ETE7JjEaAr-W&line=5&uniqifier=1).

## Run a Custom Model

Once you've completed the Colab, you should have a `african_wildlife.tflite`
file in the models folder. To test it out, run:

```bash
python locate_objects.py \
  --model_file=../models/african_wildlife.tflite \
  --label_file=../models/african_wildlife_labels.txt \
  --image=../images/zebra.jpeg
```

## Next Steps
