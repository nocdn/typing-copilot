## Welcome to General Copilot 👋

### What is this project about?

Well, I loved how Github Copilot finished code and sentences for me, but it only works in IDEs. I wanted something that would work wherever I was typing, so I made this. It's a simple Python script that uses LLM APIs, like OpenAI, or OpenRouter to complete the text based on the context you provide in the prompt. It's not perfect, but it's pretty good :)

### How do I use it? 🤔

1. Clone the repo (I recommend doing this into a new virtual environment to prevent any issues with dependencies)
2. Install the requirements with `pip install -r requirements.txt`
3. Export the API keys for the platforms that you would like to use to corresponding environment variables, `OPENAI_API_KEY`, `OPENROUTER_API_KEY`, or `FIREWORKS_API_KEY`. Example syntax: `export OPENAI_API_KEY=<Your-API-Key>` (see below for how to get an API key)
   1. Alternatively, you can just paste your API key into the `copilotNonAsync.py` file if you don't want to use an environment variable
   2. I do recommend editing the .env file to not have to enter the variables every launch
   3. You could also edit the ~/.zshrc file to export the variables to make them persist
4. Open the virtual environment and run the script with `python copilot.py`
5. Press the keyboard shortcut (ctrl+optn+f by default) to get the completion
6. The completion is typed from where the caret is, so make sure to place it where you want the completion to be inserted.
   1. Remember that the model will press the combination cmd+a and cmd+c to copy all the text in the input field to pass to the model as context.

#### How do I get an OpenAI API key? 🔑

1. Go to https://platform.openai.com/api-keys
2. Sign up if you haven't already.
3. Add billing to your account.
4. Generate a new API key and use that for the `OPENAI_API_KEY` environment variable.
   1. If you know your API key already, you don't have to generate a new one. You can just use the one you already have.

#### How do I get a Fireworks AI API key? 🔑

1. Go to https://fireworks.ai/users/
2. Sign up if you haven't already, or just log in.
3. Go to the API Keys section and generate a new API key, or use an existing one.

#### How do I get an OpenRouter API key? 🔑

1. Go to https://openrouter.ai/
2. Sign up in the top right corner if you haven't already, or just log in.
3. Go to the account section next to the profile picture (top right) then 'Keys' from the drop-down
4. Generate a new API key, or use an existing one if you know it.

#### How do I get a Perplexity AI API key? 🔑

1. Go to https://www.perplexity.ai/
2. Sign in or sign up, if you haven't already
3. Go to the account settings in the bottom left
4. Top right, go to API tab
5. Under API Keys, either copy the key or generate a new one
   1. You must have some credits added, the minimum is $3 I believe.

#### To-do 🚧

 - [ ] Add support for ~/.bashrc for env variables

##### Disclaimer ⚠️

I am not responsible for any misuse of this software. Please don't use it for anything bad. I made it for fun, not for evil :)
