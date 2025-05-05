# Understand Speech

This lab will show you how to recognize speech from an audio file or microphone
using Useful Sensors' Moonshine model.

 - [Installation](#installation)
 - [Transcribing an Audio File](#transcribing-an-audio-file)
 - [Transcribing Live Audio from a Microphone](#transcribing-live-audio-from-a-microphone)
 - [Trying Different Models](#trying-different-models)
 - [Next Steps](#next-steps)

## Installation

We'll be using the [Moonshine](https://github.com/usefulsensors/moonshine)
open source project to recognize speech. It's trained from scratch, and is
comparable in accuracy to the [Whisper model from OpenAI](https://openai.com/research/whisper)
but has been optimized to run much faster and with fewer resources.

To install the ONNX version of this framework, run:

```bash
python3 -m pip install --break-system-packages useful-moonshine-onnx@git+https://git@github.com/usefulsensors/moonshine.git#subdirectory=moonshine-onnx
```

To check that his has installed correctly, and cache the model files we'll 
need, run:

```bash
python3 -c "import moonshine_onnx; print(moonshine_onnx.transcribe(moonshine_onnx.ASSETS_DIR / 'beckett.wav', 'moonshine/tiny'))"
```

This will transcribe an audio file included with the framework, and should show
you:

```bash
['Ever tried ever failed, no matter try again, fail again, fail better.']
```

To access the microphone we'll also need the [PortAudio](https://www.portaudio.com/)
system package and the [Python sounddevice](https://python-sounddevice.readthedocs.io/en/0.4.6/)
library. To install these, connect to your Pi, open a terminal, and run:

```bash
sudo apt install -y libportaudio2
pip install --break-system-packages sounddevice
```

## Transcribing an Audio File

To get the text from an audio file containing speech, run the 
`speech_to_text.py` script. This will automatically download the Whisper model
on the first run, and then output information about the text. We'll be using a
file I recorded earlier for testing, but you can replace `--audio_file` with a
WAV you supply to run on other inputs.

```bash
cd ~/labs/lab4
python speech_to_text.py --audio_file=../audio/two_cities.wav
```

You should see something like this:

```bash
Transcribe time: 8296ms
['It was the best of times, it was the worst of times. It was the age of wisdom, it was the age of foolishness. It was the epoch of belief, it was the epoch of incredulity. It was the season of light, it was the season of darkness. It was the spring of hope, it was the winter of despair. We had everything before us, we had nothing before us. We were all going direct to heaven, we were all going direct the other way. In short, the period was so far like the present period that some of its noisiest authorities insisted on its being received for good or for evil in the superlative degree of comparison only. The first thing that was the first time that was done was the first time that was done.']
```
The transcription took about 8 seconds, and since the original audio file is 40 seconds
long, this means we're able to run at about five times real time.

You should also see that the model has transcribed me pretty accurately. There
are some errors towards the end between this and [the original](https://www.gutenberg.org/files/98/98-h/98-h.htm#link2H_4_0002)
but overall it has caught most of the words correctly.

## Transcribing Live Audio from a Microphone

The model doesn't have to be run on a pre-recorded audio file, we can also 
transcribe from live audio. For this you'll need a USB microphone attached to
your Pi. I like to use [this Jounivo model](https://www.amazon.com/JOUNIVO-Microphone-Adjustable-Noise-Canceling-Technology/dp/B07N2WRHMY/)
but most USB microphones should work. To make sure it's showing up on your
system run this command:

```bash
python3 -m sounddevice
```

If the microphone has been detected, you should see it in the list, something
like this:

```bash
  0 JOUNIVO JV601: USB Audio (hw:2,0), ALSA (2 in, 0 out)
  1 pulse, ALSA (32 in, 32 out)
* 2 default, ALSA (32 in, 32 out)
```

If not, debugging the Linux sound system is too large a topic to cover in this
tutorial unfortunately, but I recommend trying different microphones as a first
step.

To run transcription on live audio, use this command:

```bash
python live_captions.py
```

You can replace the microphone name with anything you saw in the device list,
but "default" is a good place to start for most setups.

Here's some example output from me speaking into the microphone:

```bash
Loading Moonshine model 'moonshine/base' (using ONNX runtime) ...
Press Ctrl+C to quit live captions.

t the moonshine. Speech to text, Model Uh and it seems to be working fairly well
```

## Trying different models

There is also a "moonshine/base" model available, which is slower but more
accurate than the default "moonshine/tiny". To use it, run:

```bash
python speech_to_text.py --model_name "moonshine/base"
```

You should see output like this:

```bash
encoder_model.onnx: 100%|██████████████████████████████████████████████████████| 80.8M/80.8M [00:14<00:00, 5.49MB/s]
decoder_model_merged.onnx: 100%|█████████████████████████████████████████████████| 166M/166M [00:27<00:00, 5.95MB/s]
Transcribe time: 13155ms
['It was the best of times, it was the worst of times. It was the age of wisdom, it was the age of foolishness. It was the epoch of belief, it was the epoch of incredulity. It was the season of light, it was the season of darkness. It was the spring of hope, it was the winter of despair. We had everything before us, we had nothing before us. We were all going direct to heaven, we were all going direct the other way. In short, the period was so far like the present period that some of its noisiest authorities insisted on its being received for good or for evil in the superlative degree of comparison only. The first time I saw this was a very important time.']
```

In this case we've gone from nine seconds to thirteen, so it's slower than
before but still faster than realtime. This makes it a good choice if you 
aren't as worried about latency and need improved accuracy.

You can also look at the OpenAI Whisper model itself, since it has features
like multilingual support and larger model sizes with more accuracy, as well
as a thriving community of people optimizing runtimes for the model family.

You might be able to speed up your results by ensuring that your Pi has
active cooling, like a fan and metal case, or even try out overclocking, 
though this is unlikely to make a big difference.

## Next Steps

The results you get from running the script on a live microphone should be good
enough for some simple interactive applications.

If you are interested in a fully voice-driven application, I've found the
[Piper package](https://github.com/rhasspy/piper) to be a great text-to-speech
complement to Whisper's speech recognition model. There are some other 
fantastic TTS tools out there like [Bark](https://github.com/suno-ai/bark) but
for simple, understandable speech output Piper has been great and very fast.