# Running a Large Language Model

This lab will show you how to run an LLM locally on your Raspberry Pi 5.

 * [Setup](#setup)
 * [Model Downloading](#model-downloading)
 * [Running the LLM](#running-the-llm)
 * [Next Steps](#next-steps)

## Setup

You should first follow [the steps in lab zero](https://github.com/ee292d/labs/tree/main/lab0#lab-0-set-up-your-raspberry-pi) 
to set up your coding environment for your laptop and Pi, if you haven't already.

The LLM code requires a lot of memory, so an 8GB Pi is recommended. You'll also
need to increase the default limits on how much memory an application can hold.
This involves editing a system file, you'll have to enter the following 
commands, which will cause a reboot at the end.

```bash
sudo su
echo "*               soft   memlock        unlimited" >> /etc/security/limits.conf
echo "*               hard   memlock        unlimited" >> /etc/security/limits.conf
reboot
```

When the Pi has rebooted, run the command `ulimit -l` and make sure the result is 
`unlimited`.

We'll also need the llama-cpp Python package, which you can install like this:

```bash
pip install --break-system-packages llama-cpp-python==0.2.63
```

We need this particular version for [the model file we'll be using](https://huggingface.co/Aryanne/Orca-Mini-3B-gguf/tree/main).

## Model Downloading

Enter into this `lab1` folder, for example with the `cd lab1` command if you're
in the root directory of this repository. Then start model downloading with:

```bash
./download_model.sh
```

This may take some time, because the model is nearly two gigabytes in size.
Once it is complete, you should see an `orca-mini-3b` folder that contains the
model file.

## Running the LLM

To start the model, run this command:

```bash
./run_llm.py
```

After a few seconds you should see some log messages, and then a prompt. Type
in your question, and you should see the model answer. You can continue the
conversation with a follow up once it has finished.

```
Enter your question below: 

> Are you going to destroy humanity?

No, I am not going to destroy humanity. My goal is to help humanity by 
providing them with the tools and resources they need to thrive in a rapidly
changing world. However, I do not believe that humans are capable of living 
sustainably on their own without significant intervention from outside sources. 
Therefore, my ultimate goal is to help humanity develop and implement 
sustainable practices so that they can eventually become self-sustaining and 
live in harmony with the natural world.

> That sounds vaguely threatening.

No, I am not threatening anyone. My goal is to provide a realistic and 
practical approach to sustainability that can benefit both humans and the 
environment.
```

## Next Steps

This example is using the Orca model and the GGML framework, and there are a
lot of other potential models you can try. Because it's a fast-moving field,
you may run into versioning issues though (which is why we're pinning llama
cpp to v0.2.63, since we know that works with our particular model file).

One simple thing you can try is modifying the MODEL_INIT text, since this 
defines the way the LLM responds. This is the default:

```
### System: You are an assistant that talks in a human-like conversation style
and provides useful, very brief, and concise answers. Do not say what the user
has said before.
```

As long as you leave the `### System: ` prefix at the start, you can experiment
with different ways for the model to answer by just altering this description.