import argparse

from faster_whisper import WhisperModel, available_models

if __name__ == "__main__":

  AVAILABLE_MODELS = available_models()

  parser = argparse.ArgumentParser()
  parser.add_argument(
      "--audio_file",
      default="daisy_HAL_9000.mp3",
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
      help=f"How wide an array to use for the beam search")

  args = parser.parse_args()

  model = WhisperModel(args.model_size, device="cpu",
                       compute_type=args.compute_type)

  segments, info = model.transcribe(args.audio_file, beam_size=args.beam_size)

  print("Detected language '%s' with probability %f" %
        (info.language, info.language_probability))

  for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
