import argparse
import numpy as np
import time
import librosa

from moonshine_onnx import MoonshineOnnxModel, load_tokenizer

if __name__ == "__main__":

    AVAILABLE_MODELS = ["moonshine/tiny", "moonshine/base"]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--audio_file",
        default="../audio/two_cities.wav",
        help="File to use as input")
    parser.add_argument(
        "--model_name",
        default="moonshine/tiny",
        help=f"Model to use, can be one of {', '.join(AVAILABLE_MODELS)}")
    parser.add_argument(
        "--model_precision",
        default="quantized",
        help="Model precision to use, can be one of 'float32', 'quantized'")

    args = parser.parse_args()

    model = MoonshineOnnxModel(model_name=args.model_name, model_precision=args.model_precision)
    tokenizer = load_tokenizer()

    loaded_audio, _ = librosa.load(args.audio_file, sr=16_000)
    batched_audio = loaded_audio[np.newaxis, :].astype(np.float32)

    transcribe_start_time = time.time()
    tokens = model.generate(batched_audio)
    transcribe_end_time = time.time()
    transcribe_duration = transcribe_end_time - transcribe_start_time

    print("Transcribe time: {:.0f}ms".format(transcribe_duration * 1000))

    text = tokenizer.decode_batch(tokens)[0]

    print(text)
