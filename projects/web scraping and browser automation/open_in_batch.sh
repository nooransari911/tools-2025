#!/bin/bash

input_file="../../../misc.txt"        # Replace with your input file name if different
block_size=5             # Number of lines per batch
state_file=".last_batch_processed" # File to store the last processed batch number

# Get the last processed batch number from the state file
if [ -f "$state_file" ]; then
  current_batch=$(cat "$state_file")
else
  current_batch=0 # Start from batch 0 if no state file exists
fi

start_line=$((current_batch * block_size + 1))
end_line=$(( (current_batch + 1) * block_size ))

# Extract the current block using sed  (NO PYTHON HERE!)
block_output=$(cat "$input_file" | awk -F ': ' '{print $NF}' | sed -n "${start_line},${end_line}p") # <--- CORRECTED: NO PYTHON HERE

# Check if there was any output from sed (i.e., if the batch exists)
if [[ -n "$block_output" ]]; then
  echo "Processing batch number: $current_batch (lines $start_line to $end_line)"
  echo "$block_output" | python3 open_select.py  # <--- CORRECT: PYTHON CALLED ONLY ONCE HERE, AFTER BLOCK IS EXTRACTED

  # Increment batch number for the next run and update the state file
  next_batch=$((current_batch + 1))
  echo "$next_batch" > "$state_file"
else
  echo "No more batches to process after batch number: $((current_batch - 1))"
  echo "State file '$state_file' will not be updated."
  # Optionally, you can remove the state file if you want to restart from batch 0 next time:
  # rm "$state_file"
fi

exit 0
