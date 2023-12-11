import httpx
import asyncio
import json
import pyautogui
import sys
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

async def fetch_completion_async(prompt):
    url = "https://api.openai.com/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "model": "gpt-3.5-turbo-instruct",
        "prompt": prompt,
        "max_tokens": 32,
        "temperature": 0,
        "stream": True
    }
    async with httpx.AsyncClient() as client:
        async with client.stream("POST", url, headers=headers, data=json.dumps(data)) as response:
            async for line in response.aiter_lines():
                if line.strip():  # Check if line is not empty
                    try:
                        # Strip 'data: ' prefix before JSON parsing
                        json_data = line.strip().replace('data: ', '')
                        completion_data = json.loads(json_data)
                        if 'choices' in completion_data and len(completion_data['choices']) > 0:
                            text_chunk = completion_data['choices'][0]['text']
                            pyautogui.write(text_chunk, interval=0.0001)
                    except json.JSONDecodeError:
                        print("Received non-JSON line: ", line)

def run_script_with_input(input_text):
    asyncio.run(fetch_completion_async(input_text))

if __name__ == "__main__":
    # Get input from command line arguments
    input_text = ' '.join(sys.argv[1:])
    run_script_with_input(input_text)
