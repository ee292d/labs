#!/usr/bin/bash

DEST_FOLDER="../models/nllb/"
mkdir -p $DEST_FOLDER
cd $DEST_FOLDER
wget https://storage.googleapis.com/download.usefulsensors.com/ai_in_a_box/nllb-200-distilled-600M.tar.gz
tar -xf *.tar.gz
rm *.tar.gz
