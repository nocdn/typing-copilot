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

def clear():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")

load_dotenv()

argParser = argparse.ArgumentParser()

argParser.add_argument("--tokens", help="the maximum tokens to generate", default=32)
argParser.add_argument("--model", help="choose a model schema from openAI, fireworks or openrouter, paste in a model string from the platforms", default="gpt-3.5-turbo")
argParser.add_argument("--temp", help="the model temperature to use", default=0)
argParser.add_argument("--context", help="max amount of words to give the model from the input field", default=128)
argParser.add_argument("--delay", help="delay between the operations like cmd+a and cmd+c in seconds, eg: 0.15 is 150ms", default=0.2)



globalMaxTokens = 32
globalTemperature = 0
globalContext = 128
globalDelay = 0.2
modelChoice = "gpt-3.5-turbo"
schema = "openai"

args = argParser.parse_args()

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

if args.model:
    if args.model == "gpt-3.5-turbo":
        modelChoice = "gpt-3.5-turbo"
        try:
            OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
        except KeyError:
            OPENAI_API_KEY = input("Please enter your OpenAI API key, will be saved as env variable: ")
            if not OPENAI_API_KEY:
                print("Please set the OPENAI_API_KEY environment variable manually")
                sys.exit()
            os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

    elif args.model == "openrouter":
        modelChoice = input("Please paste in the model string from openrouter.ai: ")
        schema = "openrouter"
        try:
            OPENROUTER_API_KEY = os.environ['OPENROUTER_API_KEY']
        except KeyError:
            OPENROUTER_API_KEY = input("Please enter your OpenRouter API key, will be saved as env variable: ")
            if not OPENROUTER_API_KEY:
                print("Please set the OPENROUTER_API_KEY environment variable manually")
                sys.exit()
            os.environ['OPENROUTER_API_KEY'] = OPENROUTER_API_KEY
    elif args.model == "fireworks":
        modelChoice = input("Please paste in the model string from fireworks.ai: ")
        schema = "fireworks"
        try:
            FIREWORKS_API_KEY = os.environ['FIREWORKS_API_KEY']
        except KeyError:
            FIREWORKS_API_KEY = input("Please enter your Fireworks API key, will be saved as env variable: ")
            if not FIREWORKS_API_KEY:
                print("Please set the FIREWORKS_API_KEY environment variable manually")
                sys.exit()
            os.environ['FIREWORKS_API_KEY'] = FIREWORKS_API_KEY
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
        time.sleep(globalDelay)
        if prompt_text and prompt_text[-1] != ' ':
            c.press(' ')
            c.release(' ')
        time.sleep(globalDelay)
        if prompt_text and prompt_text[-1] != ' ':
            prompt_text += ' '
        
        clear()
        print(f"Prompt text being passed:\n\n{prompt_text}")

        if schema == "openai":
            asyncio.run(fetch_chat_openai(prompt_text))
        elif schema == "openrouter":
            asyncio.run(fetch_chat_openrouter(prompt_text))
        elif schema == "fireworks":
            asyncio.run(fetch_chat_fireworks(prompt_text))
        else:
            asyncio.run(fetch_chat_openai(prompt_text))
    except AttributeError:
        pass

def typeReceivedText(text):
    c.type(text)


async def fetch_chat_openai(prompt):
    response_start_time = time.time()
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "model": modelChoice,
        "messages": [
        {
        "role": "system",
        "content": "Continue the provided text, do not output the provided text, just continue writing based on the context you have."
        },
        {
        "role": "user",
        "content":  prompt}],
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
    print(f"Time for full response: {elapsed_response_time:.2f}s")
    print(f"Time for total operation: {elapsed_total_time:.2f}s")

async def fetch_chat_openrouter(prompt):
    response_start_time = time.time()
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
    }
    data = {
        "model": modelChoice,
        "messages": [
        {
        "role": "system",
        "content": "Continue the provided text, do not output the provided text, just continue writing based on the context you have."
        },
        {
        "role": "user",
        "content":  prompt}],
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
    print(f"Time for full response: {elapsed_response_time:.2f}s")
    print(f"Time for total operation: {elapsed_total_time:.2f}s")

async def fetch_chat_fireworks(prompt):
    response_start_time = time.time()
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {FIREWORKS_API_KEY}"
    }
    data = {
        "model": modelChoice,
        "messages": [
        {
        "role": "system",
        "content": "Continue the provided text, do not output the provided text, just continue writing based on the context you have."
        },
        {
        "role": "user",
        "content":  prompt}],
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
    print(f"Time for full response: {elapsed_response_time:.2f}s")
    print(f"Time for total operation: {elapsed_total_time:.2f}s")



def for_canonical(f):
    return lambda k: f(l.canonical(k))


hk = HotKey(HotKey.parse('<ctrl>+<alt>+f'), on_activate=press_callback)

with Listener(on_press=for_canonical(hk.press), on_release=for_canonical(hk.release)) as l:
    l.join()