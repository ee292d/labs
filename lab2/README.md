# Fine-tuning an Image Model

This lab will show you how to run an image classification model on your Pi, and
fine-tune it to recognize different kinds of objects.

## Train your Model

We'll be training our models on a cloud server, using Google's free Colab 
service. [Open the notebook](https://colab.research.google.com/github/ee292d/labs/blob/main/lab2/notebook.ipynb)
and follow the directions until you have a `best_int8.tflite` file downloaded
onto your laptop.

## Upload your Model to the Pi

You should be remotely connected to your Pi through VS Code, with this 
repository open. In the file explorer, open up the `models` folder.

On your laptop, rename the `best_int8.tflite` file to `flower_model.tflite`.
Then drag the file into the `models` folder in VS Code. It should upload the
model to your board, looking like this:

<image src="doc_images/flower_model_upload.png" width="344px"/>

The name is only grayed out because I've set up our `.gitignore` file to avoid
storing this particular file.

## Install TensorFlow Lite

We'll be using the TensorFlow Lite inference engine to run the model, so you'll
need to install the Python module.

```bash
pip install --break-system-packages tflite-runtime
```

## Test the Model

This lab includes an example image of a dandelion that we can test the model on 
with this command:

```bash
python lab2/classify_image.py --image=images/dandelion.jpg --model=models/flower_model.tflite --label_file=models/flower_labels.txt
```

The three arguments are the image to run the model on, the path to the model 
file, and the path to a labels file. I've prebuilt the labels file for this 
model, but in general it should be a text file containing an alphabetical list
of the class names from your dataset, each on a new line.

## Install the Camera

To take real advantage of an edge device like the Pi, we need local sensors to
run our models on. To do this with the flower model we've just trained, I'll
show you how to install a standard Raspberry Pi camera module.

### Requirements

You'll need these two pieces of hardware:
 - [Raspberry Pi Camera Module v2](https://www.raspberrypi.com/products/camera-module-v2/)
 - [Raspberry Pi Mini to Standard Camera Cable](https://www.raspberrypi.com/products/camera-cable/). Unfortunately the Pi 5 introduced a new camera connector, so you'll need this adaptor.

If you're an EE292D student, you should already have received these.

### Installation

I've found the installation process to be confusing and error-prone (I've
destroyed at least one cable myself) so here are the steps I've found to be
most reliable:

Power down your Pi.

Remove the standard cable from the camera module. The module ships with a cable
that doesn't work with the Pi 5, so we need to swap it out. There is a small
black tab that holds the cable in place, you'll need to use your fingernails to
pop it open. You should then find that the cable comes out easily. Insert the
larger end of the adapter cable into the slot, and push the tab back down.
You'll need to make sure that the metallic contacts on the cable are facing
toward the board.