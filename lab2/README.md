# Fine-tuning an Image Model

This lab will show you how to run an image classification model on your Pi, and
fine-tune it to recognize different kinds of objects.


```bash
pip install --break-system-packages tflite-runtime
```

## Install Ultralytics

```bash
pip install --break-system-packages ultralytics
echo "PATH=${PATH}:~/.local/bin" >> ~/.bashrc
source ~/.bashrc
```

## Run Image Classification

```bash
cd lab2
python
```

```python
from ultralytics import YOLO

model = YOLO("yolov8n-cls.pt")
_ = model("../images/grace_hopper.bmp")
```

```bash
curl -O http://download.tensorflow.org/example_images/flower_photos.tgz
tar xzf flower_photos.tgz
mkdir flower_photos/train
mkdir flower_photos/test
mv flower_photos/daisy flower_photos/train
mv flower_photos/dandelion flower_photos/train
mv flower_photos/roses flower_photos/train
mv flower_photos/sunflowers flower_photos/train
mv flower_photos/tulips flower_photos/train

mkdir flower_photos/test/daisy
mkdir flower_photos/test/dandelion
mkdir flower_photos/test/roses
mkdir flower_photos/test/sunflowers
mkdir flower_photos/test/tulips

mv flower_photos/train/daisy/9*.jpg flower_photos/test/daisy/
mv flower_photos/train/dandelion/9*.jpg flower_photos/test/dandelion/
mv flower_photos/train/roses/9*.jpg flower_photos/test/roses/
mv flower_photos/train/sunflowers/9*.jpg flower_photos/test/sunflowers/
mv flower_photos/train/tulips/9*.jpg flower_photos/test/tulips/
```

```python
from ultralytics import YOLO

model = YOLO("yolov8n-cls.pt")

freeze = [f'model.{x}.' for x in range(9)]
for k, v in model.named_parameters():
    v.requires_grad = True
    if any(x in k for x in freeze):
        print(f'freezing {k}')
        v.requires_grad = False

model.train(data="flower_photos")
```