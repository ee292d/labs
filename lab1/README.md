```bash
sudo apt update
sudo apt upgrade
```

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

```bash
>>> Installing ollama to /usr/local
>>> Downloading Linux arm64 bundle
######################################################################## 100.0%
>>> Creating ollama user...
>>> Adding ollama user to render group...
>>> Adding ollama user to video group...
>>> Adding current user to ollama group...
>>> Creating ollama systemd service...
>>> Enabling and starting ollama service...
Created symlink /etc/systemd/system/default.target.wants/ollama.service → /etc/systemd/system/ollama.service.
>>> The Ollama API is now available at 127.0.0.1:11434.
>>> Install complete. Run "ollama" from the command line.
WARNING: No NVIDIA/AMD GPU detected. Ollama will run in CPU-only mode.
```

```bash
ollama --version
```

```bash
ollama version is 0.6.4
```

```bash
ollama pull gemma3:1b
```

800MB, so may take a while on a slow connection.

See https://ollama.com/library for all models.

```bash
ollama run gemma3:1b "Please tell me in one sentence what the most popular small-board comput
er brand is"
```

```bash
Raspberry Pi is the most popular small-board computer brand, known for its affordability and versatility.
```

```bash
ollama run gemma3:1b "What animal is in this image? images/zebra.jpeg"
```

```bash
The image shows a zebra! 😊 

It’s a beautiful picture of a zebra in a grassy field. 

Is there anything else you'd like to know about zebras or this image?
```

For interactive mode:

```bash
ollama run gemma3:1b
```

# Running a Large Language Model

This lab will show you how to run an LLM locally on your Raspberry Pi 5.

 * [Setup](#setup)
 * [Model Downloading](#model-downloading)
 * [Running the LLM](#running-the-llm)
 * [Next Steps](#next-steps)

## Setup

You should first follow [the steps in lab zero](https://github.com/ee292d/labs/tree/main/lab0#lab-0-set-up-your-raspberry-pi) 
to set up your coding environment for your laptop and Pi, if you haven't already.

The LLM code requires a lot of memory, so an 8GB Pi is recommended. You'll need
the Ollama package, which you install like this:

```bash
sudo apt update
sudo apt upgrade
curl -fsSL https://ollama.com/install.sh | sh
```

You should see log output like this:

```bash
>>> Installing ollama to /usr/local
>>> Downloading Linux arm64 bundle
######################################################################## 100.0%
>>> Creating ollama user...
>>> Adding ollama user to render group...
>>> Adding ollama user to video group...
>>> Adding current user to ollama group...
>>> Creating ollama systemd service...
>>> Enabling and starting ollama service...
Created symlink /etc/systemd/system/default.target.wants/ollama.service → /etc/systemd/system/ollama.service.
>>> The Ollama API is now available at 127.0.0.1:11434.
>>> Install complete. Run "ollama" from the command line.
WARNING: No NVIDIA/AMD GPU detected. Ollama will run in CPU-only mode.
```

To verify it has installed correctly, run Ollama to check the version:

```bash
ollama --version
```

You should see something like this (though the version number will change over time)

```bash
ollama version is 0.6.4
```

## Running LLMs

Before you run a model for the first time, I recommend that you download its
weights. This isn't strictly necessary, since they will be downloaded 
automatically the first time you run a command that uses a particular model,
but since the downloads can take a while for larger models, I prefer to do it
explicitly once.

In this case, we're going to be using the one billion parameter version of
Google's open-weights Gemma 3 model.

```bash
ollama pull gemma3:1b
```

This is 800MB in size, so may take a while on a slow connection. If you're
interested in other models, [the Ollama library](https://ollama.com/library)
has a lot more on offer. You will need to keep an eye on the model size if you
want to run with reasonable latency on a Pi though. Typically aiming for below
three billion parameters is a good tradeoff between accuracy and speed, though
your mileage may vary depending on your application.

Now you have the model downloaded locally, you can easily run it from the 
command line using Ollama. Here's how you can ask it a typical query:

```bash
ollama run gemma3:1b "Please tell me in one sentence what the most popular small-board comput
er brand is"
```

You'll see a spinner for a few seconds, followed by an answer written to the
terminal:

```bash
Raspberry Pi is the most popular small-board computer brand.
```

Gemma 3 is a multi-modal model, able to use image data as input, so you can
reference an image file on disk too:

```bash
cd ~/labs
ollama run gemma3:1b "What animal is in this image? images/zebra.jpeg"
```

The response should look something like this:

```bash
The image shows a zebra! 😊 

It’s a beautiful picture of a zebra in a grassy field. 

Is there anything else you'd like to know about zebras or this image?
```

You can start an interactive session with the model by leaving off the prompt:

```bash
ollama run gemma3:1b
```

If you want more statistics about the model and its execution, you can pass
`--verbose` to the command:

```bash
ollama run gemma3:1b "In one sentence, what is Stanford University known for?" --verbose
```

You'll see logging of the time taken to produce the results, below the main 
output:

```bash
Stanford University is renowned for its exceptional focus on research, particularly in computer science, biology, and 
medicine, as well as its globally recognized liberal arts education and entrepreneurial spirit.

total duration:       3.015430902s
load duration:        68.769712ms
prompt eval count:    20 token(s)
prompt eval duration: 352.448552ms
prompt eval rate:     56.75 tokens/s
eval count:           35 token(s)
eval duration:        2.593728836s
eval rate:            13.49 tokens/s
```

## Calling an LLM from Python

Ollama also has a Python library, which you can install with:

```bash
pip install --break-system-package ollama
```

### Why `--break-system-packages`?

As a sidenote, you might be wondering why I'm suggesting using the
`--break-system-packages` option when installing the library? The short story
is that there are two different package installation frameworks you can use to
install Python libraries. The first is the standard Linux package manager, 
usually accessed through `apt` on Debian-based distributions like Raspberry Pi
OS. This is how we typically install non-Python tools, like `git` or `curl`.
There's also a package manager built into Python called `pip`. Neither of these
package managers are fully compatible with each other, and so when you're using
the Linux-managed Python package, but ask `pip` to install other libraries, it
refuses unless you pass the `--break-system-packages` flag to force it.
Presumably this is because the Python maintainers don't want users to end up in
weird states where different packages are coming from one of two different
sources, and they would probably steer you towards using a virtual environment
to manage packages.

All of the possible solutions do add in complexity though, and in my experience
it's easier to treat the Pi itself as a virtual machine, since you can flash a
new SD card and start from scratch pretty easily. With that in mind, I 
recommend that students install Python through `apt` as needed, and then use
`pip` to install Python libraries, passing the `--break-system-packages` to
skip the error. There are a still a lot of opportunities to shoot yourself in
the foot with Python package installation and dependencies, so make sure you
have copies of any valuable data on the Pi, and be prepared to reinstall as
needed.