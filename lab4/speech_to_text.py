import argparse
import time

from faster_whisper import WhisperModel, available_models

if __name__ == "__main__":

  AVAILABLE_MODELS = available_models()

  parser = argparse.ArgumentParser()
  parser.add_argument(
      "--audio_file",
      default="../audio/two_cities.wav",
      help="Input audio")
  parser.add_argument(
      "--model_size",
      default="tiny.en",
      help=f"Model to use, can be one of {', '.join(AVAILABLE_MODELS)}")
  parser.add_argument(
      "--compute_type",
      default="int8",
      help=f"Internal data type to use, can be one of int8, float16, float32, int8_float16")
  parser.add_argument(
      "--beam_size",
      type=int,
      default=5,
      help=f"How wide an array to use for the beam search (smaller is faster but less accurate)")

  args = parser.parse_args()

  model = WhisperModel(args.model_size, device="cpu",
                       compute_type=args.compute_type)

  transcribe_start_time = time.time()
  segments, info = model.transcribe(args.audio_file, beam_size=args.beam_size)
  transcribe_end_time = time.time()
  transcribe_duration = transcribe_end_time - transcribe_start_time
  print("Transcribe time: {:.3f}ms".format(transcribe_duration * 1000))

  print("Detected language '%s' with probability %f" %
        (info.language, info.language_probability))

  segment_start_time = time.time()
  for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
  segment_end_time = time.time()
  segment_duration = segment_end_time - segment_start_time
  print("Segment time: {:.3f}ms".format(segment_duration * 1000))
