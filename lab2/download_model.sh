#!/usr/bin/env bash

FLOWER_MODEL_URL="https://storage.googleapis.com/download.usefulsensors.com/models/flower_model.tflite.zip"
cd ../models
curl -L -O ${FLOWER_MODEL_URL}
unzip -q flower_model.tflite.zip
rm -rf flower_model.tflite.zip
rm -rf __MACOSX