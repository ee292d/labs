# Fine-tune and Deploy a Large Language Model

This lab will show you how to efficiently fine-tune a large language model, then prepare it for deployment on a Raspberry Pi.

- [Fine-Tuning and Preparing a Model](#fine-tuning-and-preparing-a-model)
- [Deploying](#deploying)
- [Next Steps](#next-steps)

## Fine-tuning and Preparing a Model

Follow the instructions in `notebook.ipynb` to fine-tune a small base model on a chat dataset, then prepare the fine-tuned weights for deployment on your Raspberry Pi. You should [open this notebook in Colab](https://colab.research.google.com/github/ee292d/labs/blob/main/lab6/notebook.ipynb).

## Deploying

Once you've downloaded the prepared weights from your Colab instance, you'll need to transfer them to your Pi. If your development computer is a Linux/Unix machine, you can do this with `scp`, like so:

``` bash
scp phi-2-chat.gguf your-username@192.168.0.1:~/labs/lab6/
```

where `your-username` is the username you chose when you set up your Pi, `192.168.0.1` is the IP address of the Pi on your local network, and `~/labs/lab6/` is the path to the directory containing the `run_phi_chat.py` file included with this lab.

Once you've copied the weights over, double check that you have `llama-cpp` installed on the Pi (as in Lab 1):

``` bash
pip install --break-system-packages llama-cpp-python==0.1.77
```

Finally, you can run this in the `lab6` directory of your Pi to chat with your fine-tuned model:

``` bash
python run_phi_chat.py
```

## Next Steps

You can probably imagine all the great things we can do relatively cheaply and quickly with fine-tuning! The first step might be to build a multi-turn chat application with your model, or to train a model for new tasks like following instructions.
