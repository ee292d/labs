
import argparse
import shutil
import time

import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite

from picamera2 import Picamera2, Preview

def load_labels(filename):
  with open(filename, "r") as f:
    return [line.strip() for line in f.readlines()]


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument(
      "-i",
      "--image",
      default="../images/dandelion.jpg",
      help="image to be classified")
  parser.add_argument(
      "-m",
      "--model_file",
      default="../models/flower_model.tflite",
      help=".tflite model to be executed")
  parser.add_argument(
      "-l",
      "--label_file",
      default="../models/flower_labels.txt",
      help="name of file containing labels")
  parser.add_argument(
      "--input_mean",
      default=0.0, type=float,
      help="input_mean")
  parser.add_argument(
      "--input_std",
      default=255.0, type=float,
      help="input standard deviation")
  parser.add_argument(
      "--num_threads", default=2, type=int, help="number of threads")
  parser.add_argument(
      "--camera", default=None, type=int, help="Pi camera device to use")
  parser.add_argument(
    "--save_input", default=None, help="Image file to save model input to")


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

  interpreter = tflite.Interpreter(
      model_path=args.model_file,
      num_threads=args.num_threads)
  interpreter.allocate_tensors()

  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()

  # check the type of the input tensor
  floating_model = input_details[0]["dtype"] == np.float32

  # NxHxWxC, H:1, W:2
  height = input_details[0]["shape"][1]
  width = input_details[0]["shape"][2]

  while True:
    if args.camera is None:
      img = Image.open(args.image).resize((width, height))
    else:
      img = Image.fromarray(picam2.capture_array()).resize(size=(width, height), resample=Image.Resampling.LANCZOS)

    if args.save_input is not None:
      img.save("new_" + args.save_input)
      # Do a file move to reduce flicker in VS Code.
      shutil.move("new_" + args.save_input, args.save_input)

    # add N dim
    input_data = np.expand_dims(img, axis=0)

    if floating_model:
      input_data = (np.float32(input_data) - args.input_mean) / args.input_std

    interpreter.set_tensor(input_details[0]["index"], input_data)

    start_time = time.time()
    interpreter.invoke()
    stop_time = time.time()

    output_data = interpreter.get_tensor(output_details[0]["index"])
    results = np.squeeze(output_data)

    top_k = results.argsort()[-5:][::-1]
    labels = load_labels(args.label_file)
    for i in top_k:
      if floating_model:
        print("{:08.6f}: {}".format(float(results[i]), labels[i]))
      else:
        print("{:08.6f}: {}".format(float(results[i] / 255.0), labels[i]))

    print("time: {:.3f}ms".format((stop_time - start_time) * 1000))

    if args.camera is None:
      break