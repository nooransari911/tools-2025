#!/bin/bash



# --- Configuration ---
# 4 file trigger
SOURCE_DIR_A="/home/ansarimn/Pictures/Screenshots/"
# 1 file trigger
SOURCE_DIR_B="/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/output files/" 
S3_BUCKET="ansarimn-public-ssg-bucket" # <-- IMPORTANT: CHANGE THIS
S3_BUCKET_BASE_PATH="test/img"
S3_BUCKET_BASE_NAME_IMAGES="test-img"

# Scripts to be called
ACTION_A_COPY_SCRIPT="/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/py_practice/cheat/action_A.py"
ACTION_A_PROCESS_SCRIPT="/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/single Doc processor f.py"
AI_WORKING_DIR="/home/ansarimn/Downloads/tools-2025/projects/Knowledge Base/"



# Trigger for Directory A
TRIGGER_COUNT=4

# --- State ---
declare -a FILES_A=()

echo "--- Solution Starting ---"
echo "Bash orchestrator is now watching directories."
echo "DIR A:  '$SOURCE_DIR_A' (Triggers on $TRIGGER_COUNT files)"
echo "DIR B:  '$SOURCE_DIR_B' (Triggers on 1 file)"
echo "Press Ctrl+C to stop."
echo "---------------------------"

# Create directories if they don't exist
mkdir -p "$SOURCE_DIR_A" "$SOURCE_DIR_B" "scripts"

# Main watch loop
inotifywait -m -e create --format '%w%f' "$SOURCE_DIR_A" "$SOURCE_DIR_B" | while read -r NEW_FILE; do

    echo "[Monitor] Event detected: New file '$NEW_FILE'"

    # --- Orchestration Logic for Directory A ---
    if [[ "$NEW_FILE" == "$SOURCE_DIR_A"* ]]; then
        FILES_A+=("$NEW_FILE")
        echo "[Monitor] File added to Dir A queue. Queue size: ${#FILES_A[@]}"

        if (( ${#FILES_A[@]} >= TRIGGER_COUNT )); then
            echo
            echo ">>> TRIGGER A MET: Found ${#FILES_A[@]} files. Starting action chain..."
            
            # ACTION 1: Run the Python copy script. The 'if' statement checks its exit code.







            echo "--> Step 1: Executing file copy script..."
            python3 "$ACTION_A_COPY_SCRIPT" "${FILES_A[@]}"
            COPY_STATUS=$?

            if [ $COPY_STATUS -ne 0 ]; then
                echo ">>> ERROR: File copy script failed. Aborting processing."
                exit 1
            fi

            echo "--> Step 1.1: Uploading files to S3..."

            for i in "${!FILES_A[@]}"; do
                index=$((i + 1))
                file="${FILES_A[$i]}"

                if [ ! -f "$file" ]; then
                    echo ">>> WARNING: File not found: $file — skipping upload."
                    continue
                fi

                ext="${file##*.}"
                s3_target="s3://$S3_BUCKET/$S3_BUCKET_BASE_PATH/$S3_BUCKET_BASE_NAME_IMAGES-${index}.${ext}"

                echo "    Uploading $file to $s3_target"
                if ! aws s3 cp "$file" "$s3_target"; then
                    echo ">>> ERROR: Failed to upload $file to S3."
                    exit 1
                fi
            done

            echo "--> Step 2: Executing data processing script..."
            AI_PROVIDER=fireworks python3 "$ACTION_A_PROCESS_SCRIPT" \
                -i "$AI_WORKING_DIR/img/test/" pro paid \
                "$AI_WORKING_DIR/prompt files/solve test q.md" \
                -o "$AI_WORKING_DIR/data/output_file_version.json" \
                -u "$AI_WORKING_DIR/data/gemini_tokens_usage_free.json"

            PROCESS_STATUS=$?

            if [ $PROCESS_STATUS -ne 0 ]; then
                echo ">>> ERROR: Data processing script failed."
                exit 1
            fi

            echo ">>> Action chain for Trigger A complete."



           
            echo ">>> Resetting Trigger A queue."
            echo "---------------------------"
            FILES_A=() # Reset the queue regardless of success or failure
        fi

    # --- Orchestration Logic for Directory B ---
    elif [[ "$NEW_FILE" == "$SOURCE_DIR_B"* ]]; then
        echo
        echo ">>> TRIGGER B MET: New file in Dir B. Starting S3 upload..."

        aws s3 cp "$NEW_FILE" "s3://$S3_BUCKET/S3_BUCKET_BASE_PATH/md/latestq.md" --cache-control="max-age=10 public"
        
        if [ $? -eq 0 ]; then
            echo ">>> S3 Upload successful for '$NEW_FILE'."
        else
            echo ">>> ERROR: S3 upload failed for '$NEW_FILE'."
        fi
        echo "---------------------------"
    fi
done
