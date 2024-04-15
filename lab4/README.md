# Understand Speech

This lab will show you how to recognize speech from an audio file or microphone
using OpenAI's Whisper model.

 - [Installation](#installation)
 - [Transcribing an Audio File](#transcribing-an-audio-file)
 - [Transcribing Live Audio from a Microphone](#transcribing-live-audio-from-a-microphone)
 - [Speeding up Transcription](#speeding-up-transcription)
 - [Next Steps](#next-steps)

## Installation

We'll be using the [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
open source project to recognize speech. It's based on the original release of
the [Whisper model from OpenAI](https://openai.com/research/whisper) but uses
the [CTranslate2 library](https://github.com/OpenNMT/CTranslate2) to run faster
than the reference implementation provided by OpenAI.

To access the microphone we'll also need the [PortAudio](https://www.portaudio.com/)
system package and the [Python sounddevice](https://python-sounddevice.readthedocs.io/en/0.4.6/)
library. To install these, connect to your Pi, open a terminal, and run:

```bash
sudo apt install -y libportaudio2
pip install --break-system-packages faster-whisper sounddevice
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
Transcribe time: 357ms
Detected language 'en' with probability 1.000000
[0.00s -> 5.08s]  It was the best of times, it was the worst of times.
[5.08s -> 8.88s]  It was the age of wisdom, it was the age of foolishness.
[8.88s -> 13.52s]  It was the epoch of belief, it was the epoch of incredulity.
[13.52s -> 17.60s]  It was the season of light, it was the season of darkness.
[17.60s -> 21.28s]  It was the spring of hope, it was the winter of despair.
[21.28s -> 24.68s]  We had everything before us, we had nothing before us.
[24.68s -> 29.16s]  We were all going direct to heaven, we were all going direct the other way.
[29.16s -> 34.00s]  In short, the period was so far like the present period, that some of its noisiest
[34.00s -> 40.12s]  authorities insisted on its being received, for good or for evil, in the superlative degree
[40.12s -> 41.64s]  of comparison only.
Segment time: 7708ms
```

You'll see the recognized text in the middle of these logs, together with a
guess at what language is being spoken (since Whisper is multilingual) and
timing information. There are two phases to running the model, the 
transcription, which took about 350ms, and the segment section which took 
almost eight seconds in total. Since the original audio file is 40 seconds
long, this means we're able to run at about five times real time.

You should also see that the model has transcribed me pretty accurately. There
are some minor differences in punctuation between this and [the original](https://www.gutenberg.org/files/98/98-h/98-h.htm#link2H_4_0002)
but overall it has caught all of the words correctly.

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
python speech_to_text.py --microphone=default
```

You can replace the microphone name with anything you saw in the device list,
but "default" is a good place to start for most setups.

Here's some example output from me speaking into the microphone:

```bash
Sound device error:  input underflow
Sound device error:  input underflow
Sound device error:  input underflow
 . . . . . . . . . . . . . .
 Hi, this is Pete Warden and I'm testing out the Python Speech to Text Lab. You'll start to see some output coming out, there's quite a time lag, so you might be waiting a little while unfortunately.
 Hi, this is Pete Warden, and I'm testing out the Python Speech-to-Text Lab. You'll start to see some output coming out. There's quite a time lag, so you might be waiting a little while, unfortunately. As you can see, there's quite a delay.
 coming out there's quite a time lag so you might be waiting a little while unfortunately. As you can see there's quite a delay but it should at least be working.
```

I'm not sure why the SoundDevice library gives me underflow errors initially,
but I've made sure they're printed to stderr so you can easily ignore them if
you're piping the command to a file or another process.
The other lines are all transcripts. Interestingly, the model hallucinates a
series of periods in this case for the first run of complete silence, but after
that each line is a snapshot of up to 30 seconds of transcription from the 
model. If you're trying this yourself, you'll see why I'm talking about the
lag, because there's a long delay of up to ten seconds between speaking and the
words appearing on-screen. In the next section I'll discuss how to reduce the
latency for applications that need more responsiveness.

## Speeding up Transcription

There are a [variety of models](https://github.com/SYSTRAN/faster-whisper/blob/master/faster_whisper/utils.py#L12)
available, but by default we're already using 'tiny.en' which should be the
fastest. We can speed things up a bit by using the `beam_search` argument,
which controls the algorithm used to assemble the model results. By setting
this to '1' you should see an overall speed-up of a few seconds:

```bash
python speech_to_text.py --audio_file=../audio/two_cities.wav --beam_size=1
```

```bash
Transcribe time: 357ms
Detected language 'en' with probability 1.000000
[0.00s -> 5.08s]  It was the best of times, it was the worst of times.
[5.08s -> 8.88s]  It was the age of wisdom, it was the age of foolishness.
[8.88s -> 13.52s]  It was the epoch of belief, it was the epoch of incredulity.
[13.52s -> 17.60s]  It was the season of light, it was the season of darkness.
[17.60s -> 21.28s]  It was the spring of hope, it was the winter of despair.
[21.28s -> 24.64s]  We had everything before us, we had nothing before us.
[24.64s -> 29.16s]  We were all going direct to heaven, we were all going direct the other way.
[29.16s -> 34.00s]  In short, the period was so far like the present period, that some of its noisiest
[34.00s -> 40.12s]  authorities insisted on its being received, for good, awful evil, in the superlative degree
[40.12s -> 41.64s]  of comparison only.
Segment time: 5874ms
```

In this case we've gone from eight seconds to six.

OpenAI only released pretrained weights for Whisper, so the architecture is
fixed. One of the consequences is that it always runs on 30 seconds of audio,
at least in the encoder stage, so there's a fixed cost associated with that.
However, the second decoder stage loops on the number of actual tokens found,
so for live audio we can speed things up a bit by reducing the length of the
non-silent input buffer. The default is the full 30 seconds that Whisper 
expects but here's how to run it with a five second input instead:

```bash
python speech_to_text.py --microphone=default --beam_size=1 --buffer_duration=5
```

Here are the logging results I see:

```bash
 Hi, I'm Pete Warden.
 Hi, I'm Pete Warden and I'm trying out reducing the
 I'm trying out reducing the buffer duration to see if I can actually get.
 duration to see if I can actually get faster results. And as you can see.
 of his faults and as you can see it's kind of working. But...
 kind of working, but there are some accuracy issues.
 ```

 If you run this yourself, you should hopefully see the log lines appearing
 much more frequently, every three or four seconds. You can also see in this
 example that the shorter input reduces the accuracy, since the model has less
 context to work with when trying to understand the speech.

 You might also be able to speed up your results by ensuring that your Pi has
 active cooling, like a fan and metal case, or even try out overclocking, 
 though this is unlikely to make a big difference.

 ## Next Steps

The results you get from running the script on a live microphone should be good
enough for some simple interactive applications. You can even prototype by
piping the output into `grep` to spot particular words or patterns.

To work with languages other than English you can experiment with the other
OpenAI models which have multilingual support.

If you are interested in a fully voice-driven application, I've found the
[Piper package](https://github.com/rhasspy/piper) to be a great text-to-speech
complement to Whisper's speech recognition model. There are some other 
fantastic TTS tools out there like [Bark](https://github.com/suno-ai/bark) but
for simple, understandable speech output Piper has been great and very fast.