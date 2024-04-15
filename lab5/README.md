# Translate Languages

This lab will show you how to translate text from one language into another.

## Installation

We'll be using the [NLLB (No Language Left Behind) model from Meta](https://huggingface.co/facebook/nllb-200-distilled-600M)
which is available under a Creative Commons CC-BY-NC-4.0. To get this model 
you'll need to run the download script. [It's over 500 megabytes in size](https://forum.opennmt.net/t/nllb-200-with-ctranslate2/5090),
so this may take some time.

```bash
cd ~/labs/lab5
./download_model.sh
```

Once the model is downloaded, you'll need to install the Python dependencies
for running it.

```bash
pip install --break-system-packages ctranslate2 transformers sentencepiece
```

## Translating

The translation script takes in a line of text at a time as input, and
translates from a given source language to the target language you specify.
There are [over 200 languages supported](https://github.com/facebookresearch/flores/blob/main/flores200/README.md#languages-in-flores-200)
and you pass them in with the `--source_language` and `--target_language` 
command-line arguments. Here's an example that will translate from English to
Spanish:

```bash
python translate.py --source_language=english --target_language=spanish
```

You should see output like this:

```bash
Translating from english to spanish
Enter text to be translated
```

Type in "Hello, how are you?" and press return.

After a couple of seconds, you should see:

```bash
Hola, ¿cómo estás?
```

You can translate between any pairs of the 200 languages supported, though some
of the languages have less data than others and so the model can be less 
accurate for those. For example, try running Spanish to Arabic:

```bash
python translate.py --source_language=spanish --target_language=arabic
```

Paste in "Hola, ¿cómo estás?" and you should see this result:

```bash
مرحبا, كيف حالك؟
```

You can also read in text files and the script will translate line by line.

```bash
python translate.py --source_language=chinese --target_language=english < ../text/chinese_example.txt
```

## Next Steps

The NLLB model from Meta is only licensed for non-commercial use, but the recent [MADLAD model from Google](https://huggingface.co/docs/transformers/en/model_doc/madlad-400)
offers similar functionality without those restrictions, and is also available [in quantized form](https://huggingface.co/Heng666/madlad400-3b-mt-ct2-int8). 
It's a bit larger though, so it won't run as quickly.

You could look at translating speech into text using the script from Lab 4, and
then feed the results into the translator to convert it into another language.