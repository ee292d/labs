#!/usr/bin/env python

# Derived from Lab 1 run_llm.py, but with your own fine-tuned model.

# Demonstrates how to run a large language model locally on a Raspberry Pi 5.
# You'll need to follow the configuration steps in the README.md file from 
# Lab 1 before you can run this.

import llama_cpp

MODEL_PATH = "phi-2-chat.gguf"
MODEL_CONTEXT = 2048
MODEL_EPSILON = 1e-6
MODEL_RFB = 10000
MODEL_BATCH = 32
MODEL_THREADS = 4
MODEL_PREFIX = "### Human: "
MODEL_SUFFIX = "### Assistant: "
MODEL_INIT = ""

llm = llama_cpp.Llama(
    model_path=MODEL_PATH,
    n_ctx=MODEL_CONTEXT,
    rms_norm_eps=MODEL_EPSILON,
    rope_freq_base=MODEL_RFB,
    n_batch=MODEL_BATCH,
    n_threads=MODEL_THREADS,
    use_mlock=True,
    use_mmap=False,
    verbose=False)

print ("\nUser: ")

while True:
    user_prompt = input("\n> ")
    if (user_prompt.lower() == "quit") or (user_prompt.lower() == "exit"):
        break
    full_prompt = f"{MODEL_PREFIX}{user_prompt}\n{MODEL_SUFFIX}"
    ptokens = llm.tokenize(bytes(full_prompt, "utf-8"))
    resp_gen = llm.generate(
        ptokens,
        top_k=40,
        top_p=0.95,
        temp=0.25,
        repeat_penalty=1.1,
        reset=False,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        tfs_z=1.0,
        mirostat_mode=0,
        mirostat_tau=5.0,
        mirostat_eta=0.1,
        logits_processor=llama_cpp.LogitsProcessorList([]))

    for tok in resp_gen:
        if tok == llm.token_eos():
            break

        word = llm.detokenize([tok]).decode("utf-8", errors="ignore")
        print(word, end="", flush=True)
    print()