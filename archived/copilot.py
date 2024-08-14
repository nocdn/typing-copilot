import asyncio
import httpx
import json
import pyperclip
import time
from pynput.keyboard import Controller, Listener, HotKey, Key
import sys
import argparse
import os
from dotenv import load_dotenv
import signal

def clear():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")

def signal_handler(sig, frame):
    clear()  # Your custom clear function
    print("Safely terminated program.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

load_dotenv()

def load_config(file_path='config.json'):
    with open(file_path, 'r') as file:
        return json.load(file)

config = load_config()

argParser = argparse.ArgumentParser()

argParser.add_argument("--tokens", help="the maximum tokens to generate", default=32)
argParser.add_argument("--schema", help="choose a model schema from openAI, fireworks or openrouter, paste in a model string from the platforms", default="gpt-3.5-turbo")
argParser.add_argument("--temp", help="the model temperature to use", default=0)
argParser.add_argument("--context", help="max amount of words to give the model from the input field", default=76)
argParser.add_argument("--delay", help="delay between the operations like cmd+a and cmd+c in seconds, eg: 0.15 is 150ms", default=0.2)

args = argParser.parse_args()

globalMaxTokens = int(args.tokens) if args.tokens else config['defaults']['tokens']
globalTemperature = float(args.temp) if args.temp else config['defaults']['temperature']
globalContext = int(args.context) if args.context else config['defaults']['context']
globalDelay = float(args.delay) if args.delay else config['defaults']['delay']
modelChoice = args.schema if args.schema else config['defaults']['model']
schema = "groq"
modelChoice = "mixtral-8x7b-32768"
keyboardShortcut = config['keyboard_shortcuts']['activate']

# Network configurations
max_retries = config['network']['max_retries']
retry_delay = config['network']['retry_delay']



clear()

if args.tokens:
    globalMaxTokens = int(args.tokens)
    print(f"Chosen {globalMaxTokens} tokens")

if args.temp:
    globalTemperature = args.temp
    print(f"Chosen {globalTemperature} temperature")

if args.context:
    globalContext = args.context
    print(f"Chosen {globalContext} context length")

if args.delay:
    globalDelay = args.delay
    print(f"Chosen {globalDelay} delay")

if args.schema:
    if args.schema == "gpt-3.5-turbo":
        modelChoice = "gpt-3.5-turbo"
        try:
            OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
        except KeyError:
            OPENAI_API_KEY = input("Please enter your OpenAI API key, will be saved as env variable: ")
            if not OPENAI_API_KEY:
                print("Please set the OPENAI_API_KEY environment variable manually")
                sys.exit()

            # Add the API key to the .zshrc file
            line_to_add = f'export OPENAI_API_KEY={OPENAI_API_KEY}\n'
            zshrc_path = os.path.expanduser('~/.zshrc')
            with open(zshrc_path, 'a') as file:
                file.write(line_to_add)

            print(f"Added line to {zshrc_path}: {line_to_add}")

    elif args.schema == "openrouter":
        modelChoice = input("Please paste in the model string from openrouter.ai: ")
        schema = "openrouter"
        try:
            OPENROUTER_API_KEY = os.environ['OPENROUTER_API_KEY']
        except KeyError:
            OPENROUTER_API_KEY = input("Please enter your OpenRouter API key, will be saved as env variable: ")
            if not OPENROUTER_API_KEY:
                print("Please set the OPENROUTER_API_KEY environment variable manually")
                sys.exit()

            # Add the API key to the .zshrc file
            line_to_add = f'export OPENROUTER_API_KEY={OPENROUTER_API_KEY}\n'
            zshrc_path = os.path.expanduser('~/.zshrc')
            with open(zshrc_path, 'a') as file:
                file.write(line_to_add)

            print(f"Added line to {zshrc_path}: {line_to_add}")

    elif args.schema == "fireworks":
        modelChoice = input("Please paste in the model string from fireworks.ai: ")
        schema = "fireworks"
        try:
            FIREWORKS_API_KEY = os.environ['FIREWORKS_API_KEY']
        except KeyError:
            FIREWORKS_API_KEY = input("Please enter your Fireworks API key, will be saved as env variable: ")
            if not FIREWORKS_API_KEY:
                print("Please set the FIREWORKS_API_KEY environment variable manually")
                sys.exit()

            # Add the API key to the .zshrc file
            line_to_add = f'export FIREWORKS_API_KEY={FIREWORKS_API_KEY}\n'
            zshrc_path = os.path.expanduser('~/.zshrc')
            with open(zshrc_path, 'a') as file:
                file.write(line_to_add)

            print(f"Added line to {zshrc_path}: {line_to_add}")

    elif args.schema == "pplx":
        modelChoice = input("Please paste in the model string from perplexity.ai: ")
        schema = "pplx"
        try:
            PPLX_API_KEY = os.environ['PPLX_API_KEY']
        except KeyError:
            PPLX_API_KEY = input("Please enter your Perplexity API key, will be saved as env variable: ")
            if not PPLX_API_KEY:
                print("Please set the PPLX_API_KEY environment variable manually")
                sys.exit()

            # Add the API key to the .zshrc file
            line_to_add = f'export PPLX_API_KEY={PPLX_API_KEY}\n'
            zshrc_path = os.path.expanduser('~/.zshrc')
            with open(zshrc_path, 'a') as file:
                file.write(line_to_add)

            print(f"Added line to {zshrc_path}: {line_to_add}")

    elif args.schema == "groq":
        modelChoice = "mixtral-8x7b-32768"
        schema = "groq"
        try:
            GROQ_API_KEY = os.environ['GROQ_API_KEY']
        except KeyError:
            GROQ_API_KEY = input("Please enter your Groq API key, will be saved as env variable: ")
            if not GROQ_API_KEY:
                print("Please set the GROQ_API_KEY environment variable manually")
                sys.exit()

            # Add the API key to the .zshrc file
            line_to_add = f'export GROQ_API_KEY={GROQ_API_KEY}\n'
            zshrc_path = os.path.expanduser('~/.zshrc')
            with open(zshrc_path, 'a') as file:
                file.write(line_to_add)

            print(f"Added line to {zshrc_path}: {line_to_add}")

    else:
        print("Please choose a valid model schema from openAI, fireworks or openrouter")
        sys.exit()
    print(f"Chosen {modelChoice} model")



c = Controller()

total_start_time = 0

def press_callback():
    try:
        global total_start_time
        total_start_time = time.time()
        
        c.press(Key.cmd)
        c.press('a')
        c.release('a')
        c.release(Key.cmd)
        c.press(Key.cmd)
        c.press('c')
        c.release('c')
        c.release(Key.cmd)
        c.press(Key.down)
        c.release(Key.down)

        time.sleep(globalDelay)
        prompt_text = pyperclip.paste()
        # time.sleep(globalDelay)
        prompt_text = prompt_text.split(" ")[-globalContext:]
        prompt_text = " ".join(prompt_text)
        if prompt_text and prompt_text[-1] != ' ':
            c.press(' ')
            c.release(' ')
        # time.sleep(globalDelay)
        if prompt_text and prompt_text[-1] != ' ':
            prompt_text += ' '
        
        clear()
        print(f"Prompt text being passed:\n\n{prompt_text}")

        asyncio.run(fetch_chat_generic(prompt_text))
    except AttributeError:
        pass

def typeReceivedText(text):
    c.type(text)


fetchURLs = {
    "openai": "https://api.openai.com/v1/chat/completions",
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    "fireworks": "https://api.fireworks.ai/inference/v1/chat/completions",
    "pplx": "https://api.perplexity.ai/chat/completions",
    "groq": "https://api.groq.com/openai/v1/chat/completions"
}

fetchAPIKeys = {
    "openai": os.environ['OPENAI_API_KEY'],
    "openrouter": os.environ.get('OPENROUTER_API_KEY'),
    "fireworks": os.environ.get('FIREWORKS_API_KEY'),
    "pplx": os.environ.get('PPLX_API_KEY'),
    "groq": os.environ.get('GROQ_API_KEY')
}


async def fetch_chat_generic(prompt):
    attempt = 0
    while attempt < max_retries:
        try:
            response_start_time = time.time()
            url = fetchURLs[schema]
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {fetchAPIKeys[schema]}"
            }
            data = {
                "model": modelChoice,
                "messages": [
                {
                    "role": "system",
                    "content": "Continue the provided text, DO NOT output or repeat the provided text, just continue writing based on the context you have."
                },
                {
                    "role": "user",
                    "content":  prompt
                }],
                "max_tokens": globalMaxTokens,
                "temperature": globalTemperature,
                "stream": True
            }
            async with httpx.AsyncClient() as client:
                async with client.stream("POST", url, headers=headers, data=json.dumps(data)) as response:
                    async for line in response.aiter_lines():
                        if line.strip():  # Check if line is not empty
                            try:
                                # Process each line received from the stream
                                json_data = line.strip().replace('data: ', '')
                                completion_data = json.loads(json_data)
                                # Check if the data contains 'choices' and process accordingly
                                if 'choices' in completion_data and len(completion_data['choices']) > 0:
                                    # Extract the 'content' from the delta object
                                    content_chunks = completion_data['choices'][0]['delta'].get('content', '')
                                    if content_chunks:
                                        typeReceivedText(content_chunks)
                            except json.JSONDecodeError:
                                print(f"\nReceived end of response: {line}\n")
                                
            typeReceivedText(" ")
            
            response_end_time = time.time()
            
            elapsed_response_time = response_end_time - response_start_time
            elapsed_total_time = response_end_time - total_start_time
            print(f"\nTime for full response: {elapsed_response_time:.2f}s")
            print(f"Time for total operation: {elapsed_total_time:.2f}s")
            break

        except httpx.ConnectError as e:
            attempt += 1
            print(f"Failed to connect (attempt {attempt}/{max_retries}): {e}")
            if attempt > max_retries:
                print("Maximum retry attempts reached. Exiting.")
                sys.exit(1)  # Exit the program after the final attempt
            else:
                await asyncio.sleep(retry_delay)

def for_canonical(f):
    return lambda k: f(l.canonical(k))


hk = HotKey(HotKey.parse(keyboardShortcut), on_activate=press_callback)

with Listener(on_press=for_canonical(hk.press), on_release=for_canonical(hk.release)) as l:
    l.join()