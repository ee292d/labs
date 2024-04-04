#!/usr/bin/env bash

cd ../models

YOLOV8_MODEL_URL="https://storage.googleapis.com/download.usefulsensors.com/models/yolov8n_int8.tflite.zip"
curl -L -O ${YOLOV8_MODEL_URL}
unzip -q yolov8n_int8.tflite.zip
rm -rf yolov8n_int8.tflite.zip
rm -rf __MACOSX

AFRICAN_WILDLIFE_MODEL_URL="https://storage.googleapis.com/download.usefulsensors.com/models/african_wildlife.tflite.zip"
curl -L -O ${AFRICAN_WILDLIFE_MODEL_URL}
unzip -q african_wildlife.tflite.zip
rm -rf african_wildlife.tflite.zip
rm -rf __MACOSX