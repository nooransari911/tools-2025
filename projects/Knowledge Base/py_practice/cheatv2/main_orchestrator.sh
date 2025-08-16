#!/bin/bash

# --- Configuration ---
# Directories to watch
SOURCE_DIR_A="/home/ansarimn/Pictures/Screenshots/"
# The single output directory, which is also watched for the second trigger
OUTPUT_DIR="/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/py_practice/cheatv2/output files/"

# S3 Configuration for the final upload
S3_BUCKET="ansarimn-public-ssg-bucket" 
S3_FINAL_ANALYSIS_PATH="test"

# Script Paths and the SINGLE shared output config
ACTION_A_COPY_SCRIPT="/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/py_practice/cheat/action_A.py"
PROCESS_SCRIPT="/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/single Doc processor f.py"
AI_WORKING_DIR="/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/"
OUTPUT_CONFIG="$AI_WORKING_DIR/data/output_file_version.json" # Shared by both Gemini and Fireworks

# Trigger Count for Screenshots
TRIGGER_COUNT=4

# --- State ---
declare -a SCREENSHOT_QUEUE=()
declare -a OCR_FILE_QUEUE=()

echo "--- Solution Starting ---"
echo "Bash orchestrator is now watching for the AI chain reaction."
echo "1. Watching Screenshots Dir: '$SOURCE_DIR_A'"
echo "2. Watching Output Dir:      '$OUTPUT_DIR'"
echo "Press Ctrl+C to stop."
echo "---------------------------"

# Ensure all necessary directories exist
mkdir -p "$SOURCE_DIR_A" "$OUTPUT_DIR"

# Main watch loop now correctly monitors two distinct locations
inotifywait -m -e create --format '%w%f' "$SOURCE_DIR_A" "$OUTPUT_DIR" | while read -r NEW_FILE; do
    echo
    echo "[Monitor] Event detected: New file '$NEW_FILE'"

    # --- TRIGGER 1: New screenshots arrive ---
    # This block handles the first step of the chain: Screenshot -> Gemini OCR
    if [[ "$NEW_FILE" == "$SOURCE_DIR_A"* ]]; then
        SCREENSHOT_QUEUE+=("$NEW_FILE")
        echo "[Chain] Screenshot added to queue. Queue size: ${#SCREENSHOT_QUEUE[@]}"

        if (( ${#SCREENSHOT_QUEUE[@]} >= TRIGGER_COUNT )); then
            echo ">>> TRIGGER A MET: 4 screenshots detected. Starting Gemini OCR..."
            
            echo "--> Copying files to working directory..."
            python3 "$ACTION_A_COPY_SCRIPT" "${SCREENSHOT_QUEUE[@]}"
            if [ $? -ne 0 ]; then
                echo ">>> ERROR: File copy script failed. Resetting queue."
                SCREENSHOT_QUEUE=()
                continue
            fi
            
            echo "--> Calling AI script (GEMINI) for OCR..."
            AI_PROVIDER=gemini python3 "$PROCESS_SCRIPT" \
                flash paid \
                "$AI_WORKING_DIR/prompt files/ocr_prompt.md" \
                -i "$AI_WORKING_DIR/img/test/" \
                -o "$OUTPUT_CONFIG" # Use the shared output config
            
            if [ $? -ne 0 ]; then
                echo ">>> ERROR: Gemini OCR step failed."
            else
                echo "--> Gemini OCR call complete. Waiting for output file to trigger next step."
            fi
            SCREENSHOT_QUEUE=() # Reset queue after processing
        fi

    # --- TRIGGER 2: New OCR text file arrives from Gemini ---
    # This block handles the second and third steps: Gemini Output -> Fireworks -> S3 Upload
    elif [[ "$NEW_FILE" == "$OUTPUT_DIR"* ]]; then
        OCR_FILE_QUEUE+=("$NEW_FILE")
        echo "[Chain] OCR file detected and added to queue. Queue size: ${#OCR_FILE_QUEUE[@]}"

        # Process every file in the queue one by one
        while (( ${#OCR_FILE_QUEUE[@]} > 0 )); do
            OCR_FILE_TO_PROCESS="${OCR_FILE_QUEUE[0]}"
            # Remove the processed file from the queue
            OCR_FILE_QUEUE=("${OCR_FILE_QUEUE[@]:1}")
            
            echo ">>> TRIGGER B MET: Processing OCR file '$OCR_FILE_TO_PROCESS'"

            echo "--> Calling AI script (FIREWORKS) for final analysis..."
            AI_PROVIDER=fireworks python3 "$PROCESS_SCRIPT" \
                pro paid \
                "$AI_WORKING_DIR/prompt files/solve test q.md" \
                -i "$OCR_FILE_TO_PROCESS" \
                -o "$OUTPUT_CONFIG" # Use the same shared output config

            if [ $? -ne 0 ]; then
                echo ">>> ERROR: Fireworks analysis step failed for '$OCR_FILE_TO_PROCESS'."
                continue # Skip to the next file in the queue if any
            fi

            echo "--> Fireworks analysis complete. Preparing for S3 upload..."
            
            # Reliably find the filename that was just created by reading the updated config.
            # Your Python script updates the version *after* creating the file, so the version in the JSON
            # now points to the file that was just created.
            VERSION=$(grep -o '"version": [0-9]*' "$OUTPUT_CONFIG" | grep -o '[0-9]*')
            BASE_PATH=$(grep -o '"base_path": "[^"]*"' "$OUTPUT_CONFIG" | sed 's/"base_path": "//' | sed 's/"//')
            FINAL_FILE_TO_UPLOAD="latestq.md"

            if [ ! -f "$FINAL_FILE_TO_UPLOAD" ]; then
                echo ">>> CRITICAL ERROR: Could not find the final output file to upload: '$FINAL_FILE_TO_UPLOAD'"
                continue
            fi
            
            S3_TARGET="s3://$S3_BUCKET/$S3_FINAL_ANALYSIS_PATH/$(basename "$FINAL_FILE_TO_UPLOAD")"
            echo "--> Uploading '$FINAL_FILE_TO_UPLOAD' to '$S3_TARGET'..."

            aws s3 cp "$FINAL_FILE_TO_UPLOAD" "$S3_TARGET"
            if [ $? -eq 0 ]; then
                echo ">>> S3 Upload successful. Chain complete for this item."
            else
                echo ">>> ERROR: S3 upload failed for '$FINAL_FILE_TO_UPLOAD'."
            fi
            echo "---------------------------"
        done
    fi
done
