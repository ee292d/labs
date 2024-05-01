# Understand Your Data

This lab will show you how to find and understand the datasets you'll need to
train your own models.

Improving the size and quality of your training data is the easiest way to make
any ML application better, but that can be tough to do in practice. This lab
will be a bit different from the previous workshops, with less coding and more
exploration of the options, since exactly what you'll need to do for your 
project will depend a lot on what your application needs.

## Sourcing Data

The best source of training data for your application is the platform that 
you'll be deploying on. This is because you can minimize "skew" between the 
kind of samples that you'll be running on at the end, and the sort of data that
the model sees during training. Skew is any difference in the distribution of
characteristics between sets of samples. One common way this shows up in 
computer vision is with field-of-view, since training images are often captured
using cameras optimized for photography, but robots and similar devices often
use fisheye lens to see more of their surroundings. Since models haven't seen
images with this kind of distortion during training, they perform poorly
compared to what you'd expect from the training evaluation metrics. Other 
frequent sources of image skew include framing (people take photos with objects
centered, but autonomous cameras will often crop subjects), light response,
environmental conditions like dust, steam, or smoke, resolution, and lighting.

Text samples can be skewed by punctuation, formality, case differences, 
dialects, slang, and many other differences. Audio can be affected by 
compression algorithms, background noise, accents, microphones, post
processing, and room acoustics.

All of these variables mean that the best data you can get are samples that
you've gathered using the same hardware you'll be deploying on, in the same
environments your device will exist in. The problem is that the deep learning
techniques we're using require large datasets to be effective, and collecting
the tens or hundreds of thousands of samples required from a real device will
probably cost too much or take too long to be realistic. We've discussed ways
of training faster, using less data, like LoRA or transfer learning, but even
these benefit from increasing the amount of data. In practice you're likely to
need to supplement data you gather and label yourself with external datasets.

### Crawling the Web

One of the most common approaches to gathering more data for training is to
fetch examples from public websites. 


## Finding Datasets




Data Curation by Poking Around

Finding Problematic Samples

 - Sort by (compressed) file size.


## FiftyOne

```bash
python3 -m pip install fiftyone
```

Find the images with the lowest predicted people scores.

## Navigu

Go to [navigu.net/#imagenet](https://navigu.net/#imagenet). Search for "seat belt" in the Synset box (not the Text Search Input). Search for "oxygen mask" in synsets. What do most of the images have in common?

## LLM Detection

https://arxiv.org/abs/2403.16887

| Adjectives | Adverbs | Controls |
|------------|---------|----------|
| commendable | meticulously | consider |
| innovative | reportedly | conclusion |
| meticulous | lucidly | furthermore | 
| intricate | innovatively | relative | 
| notable | aptly | technical |
| versatile | methodically | blue |
| noteworthy | excellently | red |
| invaluable | compellingly | yellow |
| pivotal | impressively | before |
| potent | undoubtedly | after |
| fresh | scholarly | earlier | 
| ingenious | strategically | later |

"As an AI language model"

## PII

https://github.com/Poogles/piiregex

## Adult Content

https://github.com/LAION-AI/CLIP-based-NSFW-Detector

## Right to Use

Respect robots.txt.
Always supply a user agent when crawling, containing an email contact.

## Data Sources

Google Open Images

https://github.com/cvdfoundation/open-images-dataset#download-full-dataset-with-google-storage-transfer

LAION

https://laion.ai/blog/laion-400-open-dataset/

Only URLs.

https://knowingmachines.org/models-all-the-way

ImageNet 1k

https://image-net.org/download

Research-only license.

Common Crawl

https://commoncrawl.org/get-started

MADLAD 400

https://huggingface.co/datasets/allenai/MADLAD-400

Mozilla Common Voice

https://huggingface.co/datasets/mozilla-foundation/common_voice_17_0

LibriSpeech

https://www.openslr.org/12

