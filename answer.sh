#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Run Copilot Query
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🤖

# Documentation:
# @raycast.author Kayetic
# @raycast.authorURL https://raycast.com/Kayetic

# Copy the selected text to the clipboard (Cmd+C)
osascript -e 'tell application "System Events" to keystroke "c" using command down'

# Wait a moment to ensure the clipboard is updated
sleep 0.1

# Get the clipboard content into a variable
selected_text=$(pbpaste)

# Make a curl request with the selected text
response=$(curl -s -X POST "https://api.groq.com/openai/v1/chat/completions" \
     -H "Authorization: Bearer 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" \
     -H "Content-Type: application/json" \
     -d '{
           "messages": [
               {"role": "system", "content": "answer the user'\''s query concisely"},
               {"role": "user", "content": "'"${selected_text//\"/\\\"}"'"}
           ],
           "model": "llama-3.1-8b-instant"
         }'
)

# Extract the assistant's response from the JSON response using jq
response_text=$(echo "$response" | jq -r '.choices[0].message.content')

# Type the response
osascript -e "tell application \"System Events\" to keystroke \"${response_text//\"/\\\"}\""
