#!/bin/bash

# --- Configuration ---
# Directories to watch
SOURCE_DIR_A="/home/ansarimn/Pictures/Screenshots/"
OUTPUT_DIR="/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/py_practice/cheatv2/output files/"

# S3 Bucket Configuration
S3_BUCKET="ansarimn-public-ssg-bucket" 

# --- SCRIPT PATHS AND MODULES ---
AI_WORKING_DIR="/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/"

# Path for scripts that can be run directly
GEMINI_OCR_SCRIPT="$AI_WORKING_DIR/single Doc processor.py"
ACTION_A_COPY_SCRIPT="$AI_WORKING_DIR/py_practice/cheat/action_A.py"
# NEW: Path to the CloudFront invalidation script
CLOUDFRONT_INVALIDATE_SCRIPT="~/Downloads/tools-2025/projects/CMS/invalidate_test.sh"

# Python module path for the Fireworks script
FIREWORKS_MODULE_PATH="src.fireworks_chatbot"

# Configs and Prompts (using absolute paths to be safe)
GEMINI_OUTPUT_CONFIG="$AI_WORKING_DIR/data/output_file_version alt.json"
OCR_PROMPT_FILE="$AI_WORKING_DIR/prompt files/ocr_prompt.md"
ANALYSIS_PROMPT_FILE="$AI_WORKING_DIR/prompt files/solve test q.md"

# Trigger Count
TRIGGER_COUNT=4

# --- State ---
declare -a SCREENSHOT_QUEUE=()
declare -a OCR_FILE_QUEUE=()

echo "--- Solution Starting: Two-Script Orchestration with Invalidation ---"
echo "1. Watching Screenshots Dir: '$SOURCE_DIR_A'"
echo "2. Watching Gemini Output Dir: '$OUTPUT_DIR'"
echo "Press Ctrl+C to stop."
echo "---------------------------"

# Ensure all necessary directories exist
mkdir -p "$SOURCE_DIR_A" "$OUTPUT_DIR"

# Main watch loop
inotifywait -m -e create --format '%w%f' "$SOURCE_DIR_A" "$OUTPUT_DIR" | while read -r NEW_FILE; do
    echo
    echo "[Monitor] Event detected: New file '$NEW_FILE'"

    # --- TRIGGER 1: New screenshots arrive -> Call Gemini Script ---
    if [[ "$NEW_FILE" == "$SOURCE_DIR_A"* ]]; then
        SCREENSHOT_QUEUE+=("$NEW_FILE")
        echo "[Chain] Screenshot added to queue. Queue size: ${#SCREENSHOT_QUEUE[@]}"

        if (( ${#SCREENSHOT_QUEUE[@]} >= TRIGGER_COUNT )); then
            echo ">>> TRIGGER A MET: 4 screenshots detected. Starting Gemini OCR..."
            
            echo "--> Copying files..."
            python3 "$ACTION_A_COPY_SCRIPT" "${SCREENSHOT_QUEUE[@]}"
            
            echo "--> Calling Gemini OCR script..."
            python3 "$GEMINI_OCR_SCRIPT" \
                flash paid \
                "$OCR_PROMPT_FILE" \
                -i "$AI_WORKING_DIR/img/test/" \
                -o "$GEMINI_OUTPUT_CONFIG"
            
            if [ $? -ne 0 ]; then
                echo ">>> ERROR: Gemini OCR script failed."
            else
                echo "--> Gemini OCR call complete. Waiting for output file to trigger next step."
            fi
            SCREENSHOT_QUEUE=()
        fi

    # --- TRIGGER 2: New OCR markdown file arrives -> Call Fireworks Script ---
    elif [[ "$NEW_FILE" == *chain_output-*.md ]]; then
        OCR_FILE_QUEUE+=("$NEW_FILE")
        echo "[Chain] OCR file detected and added to queue. Queue size: ${#OCR_FILE_QUEUE[@]}"

        while (( ${#OCR_FILE_QUEUE[@]} > 0 )); do
            OCR_FILE_TO_PROCESS="${OCR_FILE_QUEUE[0]}"
            OCR_FILE_QUEUE=("${OCR_FILE_QUEUE[@]:1}")
            
            echo ">>> TRIGGER B MET: Processing OCR file '$OCR_FILE_TO_PROCESS'"

            BASENAME=$(basename "$OCR_FILE_TO_PROCESS" .md)
            FINAL_OUTPUT_FILE="$OUTPUT_DIR/final-analysis-$(echo $BASENAME | grep -o '[0-9]*$').md"
            
            # Run Fireworks script as a module from the project root
            (
                echo "--> Changing to AI working directory to run Fireworks script as a module..."
                cd "$AI_WORKING_DIR" || exit 1

                python3 -m "$FIREWORKS_MODULE_PATH" \
                    --headless \
                    file \
                    "$ANALYSIS_PROMPT_FILE" \
                    "$OCR_FILE_TO_PROCESS" \
                    "$FINAL_OUTPUT_FILE"
            )
            
            if [ $? -ne 0 ]; then
                echo ">>> ERROR: Fireworks analysis script failed for '$OCR_FILE_TO_PROCESS'."
                continue
            fi

            echo "--> Fireworks analysis complete. Preparing for S3 upload..."
            
            if [ ! -f "$FINAL_OUTPUT_FILE" ]; then
                echo ">>> CRITICAL ERROR: Could not find the final output file to upload: '$FINAL_OUTPUT_FILE'"
                continue
            fi
            
            S3_TARGET="s3://$S3_BUCKET/test/md/latestq.md"
            echo "--> Uploading '$FINAL_OUTPUT_FILE' to the static target: '$S3_TARGET'..."

            if aws s3 cp "$FINAL_OUTPUT_FILE" "$S3_TARGET"; then
                echo ">>> S3 Upload successful."
                
                                # --- CORRECTED: Robust call to the invalidation script ---
                echo "--> Invalidating CloudFront cache..."
                # 1. Ensure the script is executable (safe to run multiple times)
                chmod +x "$CLOUDFRONT_INVALIDATE_SCRIPT"
                # 2. Call it with bash
                if bash "$CLOUDFRONT_INVALIDATE_SCRIPT"; then
                    echo ">>> CloudFront invalidation request sent successfully."
                else
                    echo ">>> ERROR: CloudFront invalidation script failed. Check its permissions and internal logic."
                fi
                # --- END OF CORRECTION ---
                
            else
                echo ">>> ERROR: S3 upload failed for '$FINAL_OUTPUT_FILE'."
            fi
            
            echo "---------------------------"
        done
    fi
done

# --- NEW, CRITICAL BLOCK: Explicitly ignore the final analysis file to prevent loops ---
elif [[ "$NEW_FILE" == *final-analysis-*.md ]]; then
    echo "[Monitor] Final analysis file created. IGNORING to prevent infinite loop."
    echo "---------------------------"
