#!/usr/bin/bash

DEST_FOLDER="../models"
mkdir -p $DEST_FOLDER
cd $DEST_FOLDER
wget https://storage.googleapis.com/download.usefulsensors.com/models/nllb-200-distilled-600M-int8.zip
unzip nllb-200-distilled-600M-int8.zip
rm -rf nllb-200-distilled-600M-int8.zip