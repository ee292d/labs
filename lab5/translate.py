import argparse
import sys

import ctranslate2
import transformers

from flores import name_to_flores_200_code

def translate(source, tgt_lang_code, tokenizer, translator):
    tokens = tokenizer.convert_ids_to_tokens(
        tokenizer.encode(source))
    results = translator.translate_batch(
        [tokens], target_prefix=[[tgt_lang_code]])
    target_tokens = results[0].hypotheses[0][1:]
    target_text = tokenizer.decode(
        tokenizer.convert_tokens_to_ids(target_tokens))
    return target_text

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_file",
        default="../models/nllb/nllb-200-distilled-600M",
        help="Translation model")
    parser.add_argument(
        "--target_language",
        default="English",
        help="Language to translate to")

    args = parser.parse_args()

    tokenizer = transformers.AutoTokenizer.from_pretrained(args.model_file)
    translator = ctranslate2.Translator(args.model_file)

    target_code = name_to_flores_200_code(args.target_language)

    print(f"Translating to {args.target_language}")
    print("Enter text to be translated")
    
    for line in sys.stdin:
        result = translate(line.strip(), target_code, tokenizer, translator)
        result = result.replace('<unk>', '')
        print(result)
