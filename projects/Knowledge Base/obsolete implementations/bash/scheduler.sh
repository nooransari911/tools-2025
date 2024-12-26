#!/bin/bash

# Step 1: Read prompts interactively from the user
echo "Enter your prompts, one per line (type 'done' to finish):"
PROMPTS=()
while true; do
    read prompt
    if [ "$prompt" == "done" ]; then
        break
    fi
    PROMPTS+=("$prompt")
done

# Step 2: Export PROMPTS array so it can be accessed in the Python script
export PROMPTS

# Step 3: Use `xargs` to process each line in the file (input_file.txt) in parallel
# Without the -P flag, `xargs` will run as many processes as needed
cat links_base.md | xargs -I {} python3 gemini_generate_once.py {} "${PROMPTS[@]}"
