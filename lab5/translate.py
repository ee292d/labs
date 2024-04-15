import argparse
import sys
import time

import ctranslate2
import sentencepiece as spm

from flores import name_to_flores_200_code, print_known_languages

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_file",
        default="../models/nllb-200-distilled-600M-int8/",
        help="Translation model")
    parser.add_argument(
        "--sp_file",
        default="../models/nllb-200-distilled-600M-int8/flores200_sacrebleu_tokenizer_spm.model",
        help="Tokenization model")
    parser.add_argument(
        "--source_language",
        default="Spanish",
        help="Language to translate from")
    parser.add_argument(
        "--target_language",
        default="English",
        help="Language to translate to")
    parser.add_argument(
        "--beam_size",
        type=int,
        default=1,
        help=f"How wide an array to use for the beam search. Smaller is faster but less accurate.")
    parser.add_argument(
        "--list_languages",
        type=bool,
        default=False,
        help="Show supported languages")

    args = parser.parse_args()

    if args.list_languages:
        print_known_languages()
        exit(0)

    sp = spm.SentencePieceProcessor()
    sp.load(args.sp_file)

    translator = ctranslate2.Translator(args.model_file)

    src_lang = name_to_flores_200_code(args.source_language)
    tgt_lang = name_to_flores_200_code(args.target_language)
    
    if src_lang is None or tgt_lang is None:
        exit(1)

    target_prefix = [[tgt_lang]]

    print(f"Translating from {args.source_language} to {args.target_language}")
    print("Enter text to be translated")
    
    for line in sys.stdin:
        subworded = sp.encode_as_pieces(line.strip())
        subworded = [[src_lang] + subworded + ["</s>"]]

        translation_result = translator.translate_batch(subworded, batch_type="tokens", max_batch_size=2024, beam_size=args.beam_size, target_prefix=target_prefix)
        translation = translation_result[0].hypotheses[0]

        if tgt_lang in translation:
            translation.remove(tgt_lang)

        translation_text = sp.decode(translation)

        print(translation_text)
