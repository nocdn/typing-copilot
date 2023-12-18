## Welcome to General Copilot 👋

### What is this project about?

Well, I loved how Github Copilot finished code and sentences for me, but it only works in IDEs. I wanted something that would work wherever I was typing, so I made this. It's a simple Python script that uses the OpenAI API (specifically gpt-3.5-turbo-instruct) to complete the text based on the context you provide in the prompt. It's not perfect, but it's pretty good :)

### How do I use it? 🤔

1. Clone the repo (I recommend doing this in a new virtual environment to prevent any issues with dependencies)
2. Install the requirements with `pip install -r requirements.txt`
3. Export the OpenAI API key to an environment variable called `OPENAI_API_KEY` with `export OPENAI_API_KEY="<Your-API-Key>"` (see below for how to get an API key)
   1. Alternatively, you can just paste your API key into the `copilotNonAsync.py` file if you don't want to use an environment variable
4. Run the script with `python copilotNonAsync.py` (the main file)
5. Copy whatever you want to complete (so it is stored in the clipboard) then press the hotkey (default is `ctrl+option+f` or `ctrl+alt+f` on Windows) to complete the text
   1. You can change the hotkey in the `copilotNonAsync.py` file
6. The text should get typed out in a few moments (it will be typed out wherever your cursor is)

#### How do I get an API key? 🔑

1. Go to https://platform.openai.com/api-keys
2. Sign up if you haven't already.
3. Add billing to your account.
4. Generate a new API key and use that for the `OPENAI_API_KEY` environment variable.
   1. If you know your API key already, you don't have to generate a new one. You can just use the one you already have.

#### To-do 🚧

- [ ] Add a way to change the hotkey without editing the file
- [ ] Add a way to send the text to complete without having to copy it to the clipboard
- [ ] Add a command line argument to specify the API call details like the temperature, max tokens, etc.
- [ ] Remove the space that the model adds to the beginning of each response

##### Disclaimer ⚠️

I am not responsible for any misuse of this software. Please don't use it for anything bad. I made it for fun, not for evil :)
