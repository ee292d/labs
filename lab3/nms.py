# Non-max suppression implementation.
# See https://petewarden.com/2022/02/21/non-max-suppressions-how-do-they-work/

import sys

NMS_UNSPECIFIED_OVERLAP_TYPE = 0
NMS_JACQUARD = 1
NMS_MODIFIED_JACCARD = 2
NMS_INTERSECTION_OVER_UNION = 3

NMS_DEFAULT = 0,
NMS_WEIGHTED = 1,

NUM_KEYPOINTS_PER_BOX = 0
NUM_COORDS_PER_KEYPOINT = 2

def rect_is_empty(rect):
  return rect["min_x"] > rect["max_x"] or rect["min_y"] > rect["max_y"]

def rect_intersects(a, b):
    return not (rect_is_empty(a) or 
                rect_is_empty(b) or 
                b["max_x"] < a["min_x"] or 
                a["max_x"] < b["min_x"] or
                b["max_y"] < a["min_y"] or
                a["max_y"] < b["min_y"])

def rect_empty():
  return {
    "min_x": sys.float_info.max,
    "min_y": sys.float_info.max,
    "max_x": sys.float_info.min,
    "max_y": sys.float_info.min,
  }

def rect_intersect(a, b):
  result = {
    "min_x": max(a["min_x"], b["min_x"]),
    "min_y": max(a["min_y"], b["min_y"]),
    "max_x": min(a["max_x"], b["max_x"]),
    "max_y": min(a["max_y"], b["max_y"]),
  }
  if result["min_x"] > result["max_x"] or result["min_y"] > result["max_y"]:
    return rect_empty()
  else:
    return result

def rect_union(a, b):
  return {
    "min_x": min(a["min_x"], b["min_x"]),
    "min_y": min(a["min_y"], b["min_y"]),
    "max_x": max(a["max_x"], b["max_x"]),
    "max_y": max(a["max_y"], b["max_y"]),
  }

def rect_width(rect):
  return rect["max_x"] - rect["min_x"]

def rect_height(rect):
  return rect["max_y"] - rect["min_y"]

def rect_area(rect):
  return rect_width(rect) * rect_height(rect)

def rect_from_coords(coords):
  return {
    "min_x": coords[0],
    "min_y": coords[1],
    "max_x": coords[2],
    "max_y": coords[3],
  }

def overlap_similarity(overlap_type, rect1, rect2):
  if not rect_intersects(rect1, rect2):
    return 0.0
  
  intersection = rect_intersect(rect1, rect2)
  intersection_area = rect_area(intersection)
  if overlap_type == NMS_JACQUARD:
    normalization = rect_area(rect_union(rect1, rect2))
  elif overlap_type == NMS_MODIFIED_JACCARD:
    normalization = rect_area(rect2);
  elif overlap_type == NMS_INTERSECTION_OVER_UNION:
    normalization = rect_area(rect1) + rect_area(rect2) - intersection_area;

  if normalization < 0.0:
    return 0.0
  else:
    return intersection_area / normalization

def unweighted_non_max_suppression(options, indexed_scores, coords, max_num_detections):
  detections = []
  for indexed_score in indexed_scores:
    candidate_coords_offset = indexed_score[0] * options["num_coords"]
    offset = candidate_coords_offset + options["box_coord_offset"]
    candidate_box_coords = coords[offset:offset+4]
    candidate_rect = rect_from_coords(candidate_box_coords)
    candidate_detection = {
      "rect": candidate_rect,
      "score": indexed_score[1],
    }
    if options["min_score_threshold"] > 0.0 and candidate_detection["score"] < options["min_score_threshold"]:
      break;
    suppressed = False
    for existing_detection in detections:
      similarity = overlap_similarity(
                options["overlap_type"],
                existing_detection["rect"],
                candidate_detection["rect"]);
      if similarity > options["min_suppression_threshold"]:
        suppressed = True;
        break;
  
    if not suppressed:
      detections.append(candidate_detection)
    if len(detections) >= max_num_detections:
      break
  return detections

def weighted_non_max_suppression(options, indexed_scores, coords, max_num_detections):
  num_keypoints = options["num_keypoints"]
  remained_indexed_scores = indexed_scores
  detections = []
  while len(remained_indexed_scores) > 0:
    indexed_score = remained_indexed_scores[0]
    original_indexed_scores_size = len(remained_indexed_scores)
    candidate_coords_offset = indexed_score[0] * options["num_coords"]
    offset = candidate_coords_offset + options["box_coord_offset"]
    candidate_box_coords = coords[offset:offset+4]
    candidate_rect = rect_from_coords(candidate_box_coords)
    candidate_keypoints_offset = candidate_coords_offset + options["keypoint_coord_offset"]
    candidate_keypoints_offset_end = candidate_keypoints_offset + num_keypoints * NUM_COORDS_PER_KEYPOINT
    candidate_keypoints_coords = coords[candidate_keypoints_offset:candidate_keypoints_offset_end]
    candidate_detection = {
      "rect": candidate_rect,
      "score": indexed_score[1],
      "keypoints": candidate_keypoints_coords,
    }
    if options["min_score_threshold"] > 0.0 and candidate_detection["score"] < options["min_score_threshold"]:
      break;
    remained = []
    candidates = []
    candidate_location = candidate_detection["rect"]
    for remained_indexed_score in remained_indexed_scores:
      remained_coords_offset = remained_indexed_score[0] * options["num_coords"]
      remained_offset = remained_coords_offset + options["box_coord_offset"]
      remained_box_coords = coords[remained_offset:remained_offset+4]
      remained_rect = rect_from_coords(remained_box_coords)
      similarity = overlap_similarity(options["overlap_type"], remained_rect, candidate_rect)
      if similarity > options["min_suppression_threshold"]:
        candidates.append(remained_indexed_score)
      else:
        remained.append(remained_indexed_score)
    if len(candidates) == 1:
      weighted_detection = candidate_detection
    else:
      keypoints = [0.0] * NUM_KEYPOINTS_PER_BOX * NUM_COORDS_PER_KEYPOINT
      w_xmin = 0.0
      w_ymin = 0.0
      w_xmax = 0.0
      w_ymax = 0.0
      total_score = 0.0
      for sub_indexed_score in candidates:
        sub_score = sub_indexed_score[1]
        total_score += sub_score
        sub_coords_offset = sub_indexed_score[0] * options["num_coords"]
        sub_offset = sub_coords_offset + options["box_coord_offset"]
        sub_box_coords = coords[sub_offset:sub_offset+4]
        sub_rect = rect_from_coords(sub_box_coords)
        w_xmin += sub_rect["min_x"] * sub_score
        w_ymin += sub_rect["min_y"] * sub_score
        w_xmax += sub_rect["max_x"] * sub_score
        w_ymax += sub_rect["max_y"] * sub_score

        sub_keypoints_offset = sub_coords_offset + options["keypoint_coord_offset"]
        sub_keypoints_offset_end = sub_keypoints_offset + num_keypoints * NUM_COORDS_PER_KEYPOINT
        sub_keypoints_coords = coords[sub_keypoints_offset:sub_keypoints_offset_end]
        for k in range(num_keypoints):
          keypoints[k * 2] += sub_keypoints_coords[k * 2] * sub_score;
          keypoints[(k * 2) + 1] += sub_keypoints_coords[(k * 2) + 1] * sub_score;
      
      weighted_detection = {
        "rect": {
          "min_x": w_xmin / total_score,
          "min_y": w_ymin / total_score,
          "max_x": w_xmax / total_score,
          "max_y": w_ymax / total_score,
          },
        "score": indexed_score[1],
      }
      weighted_detection["keypoints"] = [None] * num_keypoints * NUM_COORDS_PER_KEYPOINT
      for k in range(num_keypoints):
        weighted_detection["keypoints"][k * 2] = keypoints[k * 2] / total_score
        weighted_detection["keypoints"][(k * 2) + 1] = keypoints[(k * 2) + 1] / total_score

    detections.append(weighted_detection)
    if original_indexed_scores_size == len(remained):
      break
    else:
      remained_indexed_scores = remained

  return detections

def non_max_suppression_internal(options, scores, coords):
  indexed_scores = []
  for i in range(options["num_boxes"]):
    indexed_scores.append((i, scores[i]))
  indexed_scores.sort(key = lambda x: x[1], reverse=True)
  if options["max_num_detections"] < 0:
    max_num_detections = options["num_boxes"]
  else:
    max_num_detections = options["max_num_detections"]
  if options["algorithm"] == NMS_WEIGHTED:
    return weighted_non_max_suppression(options, indexed_scores, coords, max_num_detections)
  else:
    return unweighted_non_max_suppression(options, indexed_scores, coords, max_num_detections)

def box_to_nms_box(box):
  center_x = box[0]
  center_y = box[1]
  w = box[2]
  h = box[3]
  half_w = w / 2
  half_h = h / 2
  min_x = center_x - half_w
  min_y = center_y - half_h
  max_x = center_x + half_w
  max_y = center_y + half_h
  return [min_x, min_y, max_x, max_y]

def nms_detections_to_box(nms_detections, class_index):
  result = []
  for detection in nms_detections:
    rect = detection["rect"]
    min_x = rect["min_x"]
    min_y = rect["min_y"]
    max_x = rect["max_x"]
    max_y = rect["max_y"]
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    w = max_x - min_x
    h = max_y - min_y
    score = detection["score"]
    result.append([center_x, center_y, w, h, score, class_index])
  return result

def non_max_suppression(boxes, class_count):
  nms_options = {
    "max_num_detections": -1,
    "min_score_threshold": 0.1,
    "min_suppression_threshold": 0.1,
    "overlap_type": NMS_INTERSECTION_OVER_UNION,
    "algorithm": NMS_WEIGHTED,
    "num_coords": 4,
    "keypoint_coord_offset": 0,
    "num_keypoints": 0,
    "num_values_per_keypoint": 0,
    "box_coord_offset": 0,
  }
  result = []
  for class_index in range(class_count):
    class_boxes = []
    class_scores = []
    for box in boxes:
      current_class_index = box[5]
      if current_class_index != class_index:
        continue
      class_boxes = class_boxes + box_to_nms_box(box)
      class_scores.append(box[4])
    if len(class_scores) == 0:
      continue
    nms_options["num_boxes"] = len(class_scores)
    clean_class_detections = non_max_suppression_internal(nms_options, class_scores, class_boxes)
    result = result + nms_detections_to_box(clean_class_detections, class_index)
  result.sort(key=lambda box: box[4], reverse=True)
  return result