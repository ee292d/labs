# Understand Your Data

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

