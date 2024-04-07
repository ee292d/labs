
import argparse
import shutil
import time

import numpy as np
from PIL import Image, ImageDraw

from picamera2 import Picamera2, Preview

import easyocr


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument(
      "-i",
      "--image",
      default="../images/bus.jpg",
      help="Input image")
  parser.add_argument(
      "--camera", default=None, type=int, help="Pi camera device to use")
  parser.add_argument(
      "--save_input", default=None, help="Image file to save model input to")
  parser.add_argument(
      "--save_output", default=None, help="Image file to save model output to")
  parser.add_argument(
      "--languages",
      default="en",
      help="Languages to look for"
  )

  args = parser.parse_args()

  if args.camera is not None:
    picam2 = Picamera2(camera_num=args.camera)
    picam2.start_preview(Preview.NULL)
    config = picam2.create_preview_configuration({
        "size": (320, 240),
        "format": "BGR888"
    })
    picam2.configure(config)

    picam2.start()

  reader = easyocr.Reader(args.languages.split(","))
  
  while True:
    if args.camera is None:
      img = Image.open(args.image)
    else:
      img = Image.fromarray(picam2.capture_array())

    if args.save_input is not None:
      img.save("new_" + args.save_input)
      # Do a file move to reduce flicker in VS Code.
      shutil.move("new_" + args.save_input, args.save_input)

    start_time = time.time()
    results = reader.readtext(image=img)
    stop_time = time.time()

    print(results)

    if args.save_output is not None:
      img_draw = ImageDraw.Draw(img)

    if args.save_output is not None:
      img.save("new_" + args.save_output)
      shutil.move("new_" + args.save_output, args.save_output)

    print("time: {:.3f}ms".format((stop_time - start_time) * 1000))

    if args.camera is None:
      break
