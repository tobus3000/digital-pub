# digital-pub
Throw in a question and let the robots discuss it

## Overview

The `pub.py` script allows you to have a few robots discuss any topic you throw at them.  

## Requirements

This is using the `openai` library, so you'll either need a subscription at [openai](https://chat.openai.com/) **or** you install something locally, like LM Studio locally..

* [LM Studio](https://lmstudio.ai/)
  - Download a model. I use: `TheBloke - Mistral-7B-Instruct-v0.2-GGUF - mistral-7b-instruct-v0.2.Q3_K_M`
  - Run server in LM Studio. This exposes a local endpoint that uses port `1234` by default.
* Python package: `openai >= 1.12.0`

## Usage

```powershell
& C:/Python310/python.exe ./pub.py --help
usage: pub.py [-h] --topic TOPIC [--type {quiz,talk}]

Run a Digital Pub

options:
  -h, --help          show this help message and exit
  --topic TOPIC       Topic of the day or question for pub quiz.
  --type {quiz,talk}  Path to the output file
```