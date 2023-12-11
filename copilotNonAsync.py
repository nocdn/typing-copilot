from pynput import keyboard
import requests
import json
import pyperclip
import keyboard as kb

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def fetch_completion(prompt):
    url = "https://api.openai.com/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "model": "gpt-3.5-turbo-instruct",
        "prompt": prompt,
        "max_tokens": 32,
        "temperature": 0
        # Note: 'stream': True is removed as we are using synchronous requests
    }
    response = requests.post(url, headers=headers, json=data)
    completion_data = response.json()
    print(completion_data)

    if 'choices' in completion_data and len(completion_data['choices']) > 0:
        text_chunk = completion_data['choices'][0]['text']
        print(text_chunk)
        kb.write(text_chunk, 0.025)

def on_activate():
    prompt_text = pyperclip.paste()
    fetch_completion(prompt_text)

def main():
    with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+f': on_activate}) as h:
        h.join()

if __name__ == "__main__":
    main()
