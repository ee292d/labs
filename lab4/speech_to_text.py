import argparse
import numpy as np
import sys
import time

from faster_whisper import WhisperModel, available_models
import sounddevice as sd

# Input to the speech model.
SAMPLE_RATE = 16000
CHANNELS = 1
AUDIO_BUFFER_DURATION_S = 30.0
AUDIO_BUFFER_DURATION_MS = int(AUDIO_BUFFER_DURATION_S * 1000)
AUDIO_BUFFER_SAMPLES = int(AUDIO_BUFFER_DURATION_S * SAMPLE_RATE)

def run_model(model, audio_input, beam_size, vad_parameters=None, verbose=True):
    transcribe_start_time = time.time()
    segments, info = model.transcribe(audio_input, beam_size=beam_size, vad_parameters=vad_parameters)
    transcribe_end_time = time.time()
    transcribe_duration = transcribe_end_time - transcribe_start_time
    
    if verbose:
        print("Transcribe time: {:.3f}ms".format(transcribe_duration * 1000))
        print("Detected language '%s' with probability %f" %
                (info.language, info.language_probability))

    all_text = ""
    segment_start_time = time.time()
    for segment in segments:
        if verbose:
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        else:
            all_text += segment.text
    segment_end_time = time.time()
    segment_duration = segment_end_time - segment_start_time
    if verbose:
        print("Segment time: {:.3f}ms".format(segment_duration * 1000))
    else:
        print(all_text)
        
def update_audio_buffer(indata, outdata, frames, time, status):
    global audio_buffer
    if status:
        print("Sound device error: ", status, file=sys.stderr)
    indata_len = indata.shape[0]
    indata_f32 = indata.flatten()
    audio_buffer = np.concatenate((audio_buffer, indata_f32)).flatten()
    audio_buffer = audio_buffer[indata_len:]


if __name__ == "__main__":

    AVAILABLE_MODELS = available_models()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--audio_file",
        default="../audio/two_cities.wav",
        help="File to use as input")
    parser.add_argument(
        "--microphone",
        default=None,
        help="Which microphone to use as input")
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
    
    if args.microphone is not None:
        sd.default.samplerate = SAMPLE_RATE
        sd.default.channels = CHANNELS

    if args.microphone is None:
        run_model(model, args.audio_file, args.beam_size)
    else:
        audio_buffer = np.zeros((AUDIO_BUFFER_SAMPLES), dtype=np.float32)
        
        sd.default.samplerate = SAMPLE_RATE
        sd.default.channels = CHANNELS
        with sd.Stream(channels=CHANNELS, callback=update_audio_buffer):
            while True:
                sd.sleep(1000)
                run_model(model, audio_buffer, args.beam_size, 
                          vad_parameters={
                              "threshold": 0.0,
                              "min_silence_duration_ms": AUDIO_BUFFER_DURATION_MS,
                              "min_speech_duration_ms": AUDIO_BUFFER_DURATION_MS
                              },
                          verbose=False)