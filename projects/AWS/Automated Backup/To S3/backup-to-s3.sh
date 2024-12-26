# 700,000 Objects in ~/Downloads/
# 1000 objects to actually backup to S3

#!/bin/bash

# Set log file
LOG_FILE=~/Downloads/backup/s3-backup.log

# Function for logging with generous newlines
log() {
  timestamp=$(date +"%Y-%m-%d %H:%M:%S")
  echo -e "\n$timestamp - $1\n" | tee -a "$LOG_FILE"  # Append to log file and print to stdout
}

# Default local directory to sync
DEFAULT_LOCAL_DIR="/home/ansarimn/Downloads/backup/all-dirs-backup/"


# Enable path autocompletion
log "Enabling path autocompletion..."
if [ -z "$BASH_VERSION" ]; then
  log "Not running in a Bash shell. Aborting."
  exit 1
fi

shopt -s direxpand  # Expand directory paths
shopt -s progcomp   # Enable programmable completion



# Get local directory from user input or use default
read -e -rp "Enter the local directory to sync [default: $DEFAULT_LOCAL_DIR]: " local_dir
local_dir="${local_dir:-$DEFAULT_LOCAL_DIR}"
log "Local directory to sync: $local_dir"

# Check if local directory exists
if [[ ! -d "$local_dir" ]]; then
  log "Local directory '$local_dir' does not exist. Aborting."
  exit 1
fi

# Change to the backup directory
cd /home/ansarimn/Downloads/backup/ || { log "Failed to change directory"; exit 1; }
log "Changed directory to /home/ansarimn/Downloads/backup/"

# Ask the user if they want to run the snapshot script
read -rp "Do you want to run the snapshot script before syncing? (yes/no): " run_snapshot
log "User chose to run snapshot script: $run_snapshot"





if [[ "$run_snapshot" == "yes" ]]; then
  log "Running snapshot DRY RUN script quiet-snapshot-script-dry.sh...."
  /home/ansarimn/Downloads/backup/quiet-snapshot-script-dry.sh # Assuming you have a dry run version
  log "Snapshot DRY RUN script completed."

  # Ask if they want to proceed with the actual snapshot
  read -rp "Do you want to proceed with the actual snapshot script quiet-snapshot-script.sh? (yes/no): " run_snapshot_actual
  log "User chose to run actual snapshot script: $run_snapshot_actual"

  if [[ "$run_snapshot_actual" == "yes" ]]; then
    log "Running actual snapshot script..."
    /home/ansarimn/Downloads/backup/quiet-snapshot-script.sh
    log "Snapshot script completed."
  else
    log "Skipping actual snapshot script."
  fi
else
  log "Skipping snapshot script."
fi




# Test S3 sync with dry run
log "Testing S3 sync with dry run..."
upload_count=$(aws s3 sync "$local_dir" s3://ansarimn-fedora-backup-us-west-2/all-dirs-backup/ --dryrun | grep 'upload' | wc -l)
log "Number of files to be uploaded: $upload_count"

# Ask the user if they want to proceed
read -rp "Do you want to proceed with the actual S3 sync? (yes/no): " user_response
log "User response: $user_response"





# Check the user's response
if [[ "$user_response" != "yes" ]]; then
  log "Aborting S3 sync."
  exit 0
fi

# Proceed with the actual S3 sync
log "Starting actual S3 sync..."
aws s3 sync "$local_dir" s3://ansarimn-fedora-backup-us-west-2/all-dirs-backup/ --delete
log "S3 sync completed."
