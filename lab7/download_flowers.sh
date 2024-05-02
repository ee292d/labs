#!/usr/bin/env bash

cd ../images/
curl -O http://download.tensorflow.org/example_images/flower_photos.tgz
tar xzf flower_photos.tgz
rm -rf flower_photos.tgz