# Lab 1: Deploy a person detector on RPI

## Requirements

 - Raspberry Pi 5 8GB.
 - Raspberry Pi Camera
 - USB keyboard and mouse.
 - HDMI display.
 - Blank SD card.
 - SD card reader.
 - Laptop.

## Set up your Raspberry Pi

#### Flash an SD Card

On your laptop, download the Rapsberry Pi Imager tool for your operating system from [raspberrypi.com/software/](https://www.raspberrypi.com/software/).

Insert an SD card into the laptop's reader.

Open the Imager tool.

Select "Raspberry Pi 5", "Raspberry Pi OS (64-bit)", and the reader device.

Press "Write" and choose "Edit Settings".

Enter your preferred user name and password.

Enter the name and password of your Wifi network.

Choose "Yes" to apply the settings.

Writing will take a few minutes. Once it's complete, take the card from the reader and insert it into the Raspberry Pi. Make sure SD card is inserted so that its metal contacts are facing towards the board.

Plug the power supply into the wall, and then into the USB C plug on the Raspberry Pi.

#### Connect the Camera to the Pi

#### Connect the Display and Keyboard

#### Power up the Pi

#### Connect to Wifi

### Install VS Code on your Laptop

#### Download the App

#### Find the IP address of your Pi

#### Create a Remote Connection

#### Download this Repository

### Run an Image Labeling Model

#### Install TFLite

```bash
python3 -m pip install tflite-runtime
```

#### Make sure TFLite is Working

```bash
cd labs/lab1
python3 label_image.py
```
