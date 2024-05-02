# Understand Your Data

This lab will show you how to find and understand the datasets you'll need to
train your own models.

Improving the size and quality of your training data is the easiest way to make
any ML application better, but that can be tough to do in practice. This lab
will be a bit different from the previous workshops, with less coding and more
exploration of the options, since exactly what you'll need to do for your 
project will depend a lot on what your application needs.

## FiftyOne

The standard tool for downloading and analyzing image datasets is [FiftyOne](https://voxel51.com/fiftyone/).
It's a desktop tool and also has a Python interface. To get started I recommend
installing it on your laptop through `pip`.

```bash
python -m pip install fiftyone
```

If you have trouble installing it, you can try the [online version](https://try.fiftyone.ai/datasets/example/samples)
instead.

You can start the desktop app by running this command:

```bash
python run_fiftyone.py
```

To understand how this can be useful, try to find the images with the lowest
predicted people scores.

 - Click "Add Stage" in the top left.
 - Choose "Sort By".
 - Enter "predictions.confidence" as the first argument.
 - Change the second argument (sorting order) to False.
 - The view should update.
 - In the filter side panel to the left, open "Labels".
 - Choose "Ground Truth"
 - In the "Filter by label" text box, enter "Person".
 - Click on the cowboy photo that should be the top entry.
 - Find the bounding box labeled "Person" with the lowest score.

This is the kind of exploration that can be very useful when analyzing your own
datasets, since it uncovers common problems.

## Navigu

For another way to explore your data, go to [navigu.net/#imagenet](https://navigu.net/#imagenet). 
Search for "seat belt" in the Synset box (not the Text Search Input). Search 
for "oxygen mask" in synsets. What do most of the images have in common?

## Homebrewed Data

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

## Crawling the Web

One of the most common approaches to gathering more data for training is to
fetch examples from public websites. This can be effective, but there are a lot
of potential problems to look out for. You're using other people's resources
every time you send a request to a web server, so you need to do so in a polite
and rule-abiding way. A complete introduction to responsible web crawling is
beyond the scope of this guide, but at a minimum you should always check the
`robots.txt` file on any website to ensure your access is permitted, and have 
your email address for contact in the user agent string. Many people are 
rightly concerned about their creative work being used in unwelcome ways, so 
even these rules set up for the web search era may not be enough in the future,
since the law around copyright and other intellectual property rights for this
data is still being contested.

## Prepared Datasets

As an alternative to raw web crawling, there are a lot of collections of 
samples available for download from research organizations and companies. These
are often sourced from the web, but are at least easier to process than plain 
HTML content and may come with ground truth labels. Many of them are not 
suitable for production deployment though, for either license or content 
reasons, so you still need to be careful. I'll list a few I recommend for each
common media type, along with notes on others that are popular but problematic.

### Images

You can [download nearly 9 million images](https://github.com/cvdfoundation/open-images-dataset#download-full-dataset-with-google-storage-transfer),
with labels and bounding boxes, as part of Google's Open Images dataset. This
is the largest collection of annotated Creative Commons-licensed images
available, though [COCO comes close](https://viso.ai/computer-vision/coco-dataset/)
with 2.5 million and a clear license.

I do not recommend [LAION](https://laion.ai/) because it only contains URLs 
pointing to images, so you still need to fetch the images separately, the
content hasn't been well-screened, and the labels are from alt-text, not any
manual process. [This article has a good explanation](https://knowingmachines.org/models-all-the-way)
of some of the issues involved.

You also need to be careful of datasets like [ImageNet](https://image-net.org/download),
because while you can download them with images included, you need to agree to
a research-only license to do so. This is a something that applies to a lot of
image datasets, so you should always verify that what you're using allows
production usage.

Once you have images downloaded, you'll also want to inspect the content. The
simplest approach is to pick some files at random and open them on your desktop
for inspection. This can often help you find obvious issues like corruption,
unexpected image sizes, or poor compression quality. Another important step is
to scan for problematic content, using something like [this NSFW model](https://github.com/LAION-AI/CLIP-based-NSFW-Detector)
to make sure you're training on appropriate material.

### Text

The oldest and largest collection of pages crawled from the web is [Common Crawl](https://commoncrawl.org/get-started),
but for practical purposes I recommend the [Colossal Cleaned Common Crawl](https://github.com/allenai/allennlp/discussions/5056),
a version that is easier to download and with duplicates and other data issues fixed.

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



MADLAD 400

https://huggingface.co/datasets/allenai/MADLAD-400

Mozilla Common Voice

https://huggingface.co/datasets/mozilla-foundation/common_voice_17_0

LibriSpeech

https://www.openslr.org/12

