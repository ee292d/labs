
import argparse
import shutil
import time

import numpy as np
from PIL import Image, ImageDraw
import tflite_runtime.interpreter as tflite

from picamera2 import Picamera2, Preview

from nms import non_max_suppression_yolov8

# How many coordinates are present for each box.
BOX_COORD_NUM = 4

# How to draw a skeleton from the keypoints.
POSE_LINES = [[0, 1], [0, 2], [1, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 6], [5, 7], [
    5, 11], [6, 8], [6, 12], [7, 9], [8, 10], [11, 12], [13, 11], [14, 12], [15, 13], [16, 14]]


def load_labels(filename):
  with open(filename, "r") as f:
    return [line.strip() for line in f.readlines()]


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument(
      "-i",
      "--image",
      default="../images/bus.jpg",
      help="Input image")
  parser.add_argument(
      "-m",
      "--model_file",
      default="../models/yolov8n_224_int8.tflite",
      help="TF Lite model to be executed")
  parser.add_argument(
      "-l",
      "--label_file",
      default="../models/yolov8_labels.txt",
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
  parser.add_argument(
      "--save_output", default=None, help="Image file to save model output to")
  parser.add_argument(
      "--score_threshold",
      default=0.6, type=float,
      help="Score level needed to include results")
  parser.add_argument(
      "--output_format",
      default="yolov8_detect",
      help="How to interpret the output from the model"
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

  interpreter = tflite.Interpreter(
      model_path=args.model_file,
      num_threads=args.num_threads)
  interpreter.allocate_tensors()

  class_labels = load_labels(args.label_file)

  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()

  # check the type of the input tensor
  floating_model = input_details[0]["dtype"] == np.float32

  # NxHxWxC, H:1, W:2
  input_height = input_details[0]["shape"][1]
  input_width = input_details[0]["shape"][2]

  max_box_count = output_details[0]["shape"][2]

  if args.output_format == "yolov8_detect":
    class_count = output_details[0]["shape"][1] - BOX_COORD_NUM
    keypoint_count = 0
  elif args.output_format == "yolov8_pose":
    class_count = 1
    box_num_values = output_details[0]["shape"][1]
    non_keypoint_values = (BOX_COORD_NUM + 1)
    keypoint_values = box_num_values - non_keypoint_values
    if (keypoint_values % 3) != 0:
      print(
          f"Unexpected number of values {keypoint_values} for format {args.output_format}")
      exit(0)
    keypoint_count = int(keypoint_values / 3)
  else:
    print(f"Unknown output format {args.output_format}")
    exit(0)

  if len(class_labels) != class_count:
    print("Model has %d classes, but %d labels" %
          (class_count, len(class_labels)))
    exit(0)

  while True:
    if args.camera is None:
      img = Image.open(args.image).resize((input_width, input_height))
    else:
      img = Image.fromarray(picam2.capture_array()).resize(
          size=(input_width, input_height), resample=Image.Resampling.LANCZOS)

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
    results = np.squeeze(output_data).transpose()

    # The detect output format is [x, y, width, height, class 0 score, class 1
    # score, ..., class n score]. So, if there are 80 classes, each box will be
    # an array containing 84 values (4 coords plus the 80 class scores).
    # The pose output format is similar, but instead of the class scores it has
    # a single score followed by n triples of keypoint coordinates. So if a box
    # has 17 keypoints, it will have 4 coords, plus one class score, plus 51
    # (17 * 3) keypoint coordinates, for 56 values in total.
    boxes = []
    for i in range(max_box_count):
      raw_box = results[i]
      center_x = raw_box[0]
      center_y = raw_box[1]
      w = raw_box[2]
      h = raw_box[3]
      if args.output_format == "yolov8_detect":
        class_scores = raw_box[BOX_COORD_NUM:]
        for index, score in enumerate(class_scores):
          if (score > args.score_threshold):
            boxes.append([center_x, center_y, w, h, score, index])
      else:
        score = raw_box[BOX_COORD_NUM]
        if (score > args.score_threshold):
          coords = [center_x, center_y, w, h, score, 0]
          keypoints = raw_box[BOX_COORD_NUM + 1:]
          boxes.append([*coords, *keypoints])

    # Clean up overlapping boxes. See
    # https://petewarden.com/2022/02/21/non-max-suppressions-how-do-they-work/
    clean_boxes = non_max_suppression_yolov8(
        boxes, class_count, keypoint_count)

    if args.save_output is not None:
      img_draw = ImageDraw.Draw(img)

    for box in clean_boxes:
      center_x = box[0] * input_width
      center_y = box[1] * input_height
      w = box[2] * input_width
      h = box[3] * input_height
      half_w = w / 2
      half_h = h / 2
      left_x = int(center_x - half_w)
      right_x = int(center_x + half_w)
      top_y = int(center_y - half_h)
      bottom_y = int(center_y + half_h)
      score = box[4]
      class_index = box[5]
      class_label = class_labels[class_index]
      print(
          f"{class_label}: {score:.2f} ({center_x:.0f}, {center_y:.0f}) {w:.0f}x{h:.0f}")
      if args.save_output is not None:
        img_draw.rectangle(((left_x, top_y), (right_x, bottom_y)), fill=None)
        img_draw.text((left_x, top_y), f"{class_label} {score:.2f}")
        if args.output_format == "yolov8_pose":
          for line in POSE_LINES:
            start_index = 6 + (line[0] * 3)
            end_index = 6 + (line[1] * 3)
            start_x = box[start_index + 0]
            start_y = box[start_index + 1]
            end_x = box[end_index + 0]
            end_y = box[end_index + 1]
            img_draw.line((start_x, start_y, end_x, end_y), fill="yellow")
          for i in range(keypoint_count):
            index = 6 + (i * 3)
            k_x = box[index + 0]
            k_y = box[index + 1]
            img_draw.arc((k_x - 1, k_y - 1, k_x + 1, k_y + 1),
                         start=0, end=360, fill="red")

    if args.save_output is not None:
      img.save("new_" + args.save_output)
      shutil.move("new_" + args.save_output, args.save_output)

    print("time: {:.3f}ms".format((stop_time - start_time) * 1000))

    if args.camera is None:
      break
