#!/bin/bash

# Trap SIGCHLD to reap any background child processes
trap 'wait' SIGCHLD

# Set log file
LOG_FILE=~/Downloads/backup/ec2-backup.log

# Function for logging with generous newlines
log() {
  timestamp=$(date +"%Y-%m-%d %H:%M:%S")
  echo -e "\n$timestamp - $1\n" | tee -a "$LOG_FILE"  # Append to log file and print to stdout
}

# File containing the list of source directories
DIR_LIST_FILE=~/Downloads/backup/dir-list.md

# Destination directory on EC2
DEST_DIR=/home/ec2-user/fedora/

# Accept EC2 IP as input
read -p "Enter EC2 IP: " ec2_ip

# Log start of the backup operation
log "Starting EC2 backup operation..."

# Create the destination directory if it doesn't exist
log "Creating destination directory on EC2..."

if ssh -i ~/.ssh/aws_ec2.pem ec2-user@"$ec2_ip" "mkdir -p $DEST_DIR"; then
  log "Destination directory created successfully."
else
  log "Failed to create destination directory on EC2."
  exit 1
fi

# Log reading the directory list file
log "Reading directory list from $DIR_LIST_FILE..."

# Read each directory from the list file and create snapshots
while IFS= read -r dir; do
  # Skip empty lines and comments
  [[ -z "$dir" || "$dir" =~ ^# ]] && continue

  # Expand the directory path
  expanded_dir=$(eval echo "$dir")
  log "Processing directory: $expanded_dir..."

  # Extract the directory name
  dir_name=$(basename "$expanded_dir")
  dest_subdir="$DEST_DIR/$dir_name"

  # Check if it's a git repository
  if [ -d "$expanded_dir/.git" ]; then
    log "  -> Detected git repository: $expanded_dir"
    log "  -> Creating destination directory: $dest_subdir on EC2..."

    # Use git to get a list of files respecting .gitignore and rsync to copy
    if git -C "$expanded_dir" ls-files -z | rsync -av --delete --info=progress2 -e "ssh -i ~/.ssh/aws_ec2.pem" --files-from=- --from0 "$expanded_dir" "ec2-user@$ec2_ip:$dest_subdir/" > >(tee -a "$LOG_FILE"); then
      log "  -> Copy completed successfully for $expanded_dir"
    else
      log "  -> Copy failed for $expanded_dir"
      exit 1
    fi
  else
    log "  -> Not a git repository. Copying all files: $expanded_dir"
    log "  -> Creating destination directory: $dest_subdir on EC2..."

    # Copy entire directory as-is, with --delete to overwrite existing files
    if rsync -av --delete --info=progress2 -e "ssh -i ~/.ssh/aws_ec2.pem" "$expanded_dir/" "ec2-user@$ec2_ip:$dest_subdir/" > >(tee -a "$LOG_FILE"); then
      log "  -> Copy completed successfully for $expanded_dir"
    else
      log "  -> Copy failed for $expanded_dir"
      exit 1
    fi
  fi
done < "$DIR_LIST_FILE"

# SSH into EC2 instance and execute remote commands
ssh -i ~/.ssh/aws_ec2.pem ec2-user@"$ec2_ip" << 'ENDSSH' | tee -a "$LOG_FILE"

# Define a helper function for logging with newlines
log() {
  timestamp=$(date +"%Y-%m-%d %H:%M:%S")
  echo -e "\n$timestamp - $1\n"
}

log "Creating additional directories on EC2..."

mkdir -p /home/ec2-user/efs/

log "Listing contents of /home/ec2-user/fedora/..."

ls -al /home/ec2-user/fedora/

log "Listing contents of /home/ec2-user/efs/..."

ls -al /home/ec2-user/efs/

log "Mounting EFS..."

if sudo mount -t efs -o tls,iam fs-050286a440b03ab40.efs.ap-southeast-1.amazonaws.com /home/ec2-user/efs/; then
  log "EFS mounted successfully."
else
  log "Failed to mount EFS."
  exit 1
fi

log "Syncing files from /home/ec2-user/fedora/ to /home/ec2-user/efs/..."

if sudo rsync -av --info=progress2 /home/ec2-user/fedora/ /home/ec2-user/efs/; then
  log "File sync completed successfully."
else
  log "File sync failed."
  exit 1
fi

log "Final listing of contents in /home/ec2-user/fedora/..."

ls -al /home/ec2-user/fedora/

log "Final listing of contents in /home/ec2-user/efs/..."

ls -al /home/ec2-user/efs/

log ""
log ""
log "Final size of EFS FS at /home/ec2-user/efs/:"
du -sh /home/ec2-user/efs/

log ""
log ""
log "Unmounting /home/ec2-user/efs/..."
sudo umount /home/ec2-user/efs/

# Ensure clean exit from SSH session
exit 0
ENDSSH


log "Backup operation to EC2 completed successfully."
