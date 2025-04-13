#!/usr/bin/env python

# Demonstrates how to run an large language model locally on a Raspberry Pi 5.
# You'll need to follow the configuration steps in the README.md file before
# you can run this.

from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='gemma3:1b', messages=[
  {
    'role': 'user',
    'content': 'In one sentence, why are puppies so cute?',
  },
])

print(response.message.content)