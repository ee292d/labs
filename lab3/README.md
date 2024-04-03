# Locate People and Objects

This lab will show you how to run pretrained models to locate people and 
objects in images, optimize their latency, and train on custom classes.

## Train your Model

Just like in Lab 2, we'll be training our models on a cloud server, using
Google's free Colab service. [Open the notebook](https://colab.research.google.com/github/ee292d/labs/blob/main/lab2/notebook.ipynb)
and follow the directions until you have completed the [Download a Model](https://colab.research.google.com/github/ee292d/labs/blob/main/lab3/notebook.ipynb#scrollTo=8Ne3OOfjut-F&line=6&uniqifier=1)
step and have the `yolov8n_in8.tflite` file downloaded.

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
person: 0.92 (585, 374) 110x289
person: 0.92 (224, 375) 96x268
person: 0.90 (115, 386) 146x301
bus: 0.88 (321, 289) 631x307
person: 0.65 (28, 422) 57x189
time: 375.521ms
```

This shows fairly accurate results, but it took nearly 400 milliseconds to run!
That's because the default YOLOv8 model runs on 640x640 images, but luckily we
can modify it pretty easily to run on smaller inputs. If you [return to the Colab notebook at the step "Shrink the Input Size"](https://colab.research.google.com/github/ee292d/labs/blob/main/lab3/notebook.ipynb#scrollTo=91BhuyoqxEZ7&line=5&uniqifier=1)
I'll show you how to create a much faster model.

Once you have retrained that model and uploaded it to the Pi, you should be able
to run it using:

```bash
python locate_objects.py \
  --model_file=../models/yolov8n_224_int8.tflite \
  --label_file=../models/yolov8_labels.txt \
  --image=../images/bus.jpg
```

This should give similar results to the larger model, but with an inference time
that's more like 25 milliseconds instead of 375. To have some fun with it, you
can also take live camera input and output the results to an image you can view
in VS Code, with this command:

```bash
python locate_objects.py \
  --model_file=../models/yolov8n_224_int8.tflite \
  --label_file=../models/yolov8_labels.txt \
  --camera=0 \
  --save_output=output.png
```

## Next Steps

The Colab shows how you can train your own model for custom classes, and you
should be able to run it on your Pi by following the same exporting and uploading steps you did for the standard YOLOv8 models.
