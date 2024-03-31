# Classify Images

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

You should see something like this:

```bash

```

## Install the Camera

To take real advantage of an edge device like the Pi, we need local sensors to
run our models on. To do this with the flower model we've just trained, I'll
show you how to install a standard Raspberry Pi camera module.

### Requirements

You'll need these two pieces of hardware:
 - [Raspberry Pi Camera Module v2](https://www.raspberrypi.com/products/camera-module-v2/)
 - [Raspberry Pi Mini to Standard Camera Cable](https://www.raspberrypi.com/products/camera-cable/). Unfortunately the Pi 5 introduced a new camera connector, so you'll need this adaptor.

If you're an EE292D student, you should already have received these.

### Physical Installation

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

<image src="doc_images/cam_cable1.jpg" width="400px"/>

You'll now need to insert the other end of the cable into one of the two camera
ports on the board. I find this very fiddly, since you first need to open the
tab on the port you'll be using with your fingernails, and then push the tab
back down while keeping the cable in position. The metallic contacts on the
cable should be facing towards the Ethernet port on the board.

<image src="doc_images/cam_cable2.jpg" width="400px"/>

### Check the Camera

Power the board up again, connect to it through VS Code, and then in the 
terminal run this command:

```bash
rpicam-hello --list-cameras
```

You should see results like this:

```bash
Available cameras
-----------------
0 : imx219 [3280x2464 10-bit RGGB] (/base/axi/pcie@120000/rp1/i2c@88000/imx219@10)
    Modes: 'SRGGB10_CSI2P' : 640x480 [206.65 fps - (1000, 752)/1280x960 crop]
                             1640x1232 [41.85 fps - (0, 0)/3280x2464 crop]
                             1920x1080 [47.57 fps - (680, 692)/1920x1080 crop]
                             3280x2464 [21.19 fps - (0, 0)/3280x2464 crop]
           'SRGGB8' : 640x480 [206.65 fps - (1000, 752)/1280x960 crop]
                      1640x1232 [83.70 fps - (0, 0)/3280x2464 crop]
                      1920x1080 [47.57 fps - (680, 692)/1920x1080 crop]
                      3280x2464 [21.19 fps - (0, 0)/3280x2464 crop]
```

If instead you see the error message `No available cameras` then the connection
hasn't worked. Power the Pi down again, and double check the orientation and
seating of the cable at both ends. Try opening the tabs, reseating the cable,
closing the tabs, and then checking again. Unfortunately I haven't found a 
robust way to debug the exact problem when things aren't working, other than
double-checking everything.