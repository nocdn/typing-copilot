from pynput import keyboard
import requests
import json
import pyperclip
import keyboard as kb
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

output_file_path = "/Users/bartek/scripts/general-copilot/buffer.txt"

def start_keystroke_listener():
    def on_press(key):
        try:
            with open(output_file_path, "r+") as f:
                if key == keyboard.Key.space:
                    f.seek(0, os.SEEK_END)  # Move to the end of file
                    f.write(' ')
                elif key == keyboard.Key.backspace:
                    f.seek(0, os.SEEK_END)
                    if f.tell() > 0:
                        f.seek(-1, os.SEEK_END)
                        f.truncate()
                elif hasattr(key, 'char') and key.char:
                    f.seek(0, os.SEEK_END)
                    f.write(key.char)
        except AttributeError:
            pass  # Special keys can be handled here if needed

    listener = keyboard.Listener(on_press=on_press)
    listener.start()



def fetch_last_64_words():
    with open(output_file_path, "r") as f:
        text = f.read()
    words = text.split()
    return ' '.join(words[-64:])


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
    prompt_text = fetch_last_64_words()
    fetch_completion(prompt_text)

def main():
    # Clear the contents of the file at the start
    open(output_file_path, "w").close()


    start_keystroke_listener()
    with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+f': on_activate}) as h:
        h.join()

if __name__ == "__main__":
    main()

