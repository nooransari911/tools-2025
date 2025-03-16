#!/bin/bash

set -euo pipefail

log_message() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# --- Safety Checks ---
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  log_message "ERROR: Not inside a Git repository.  Exiting."
  exit 1
fi

# --- Get Commit Message ---
log_message "Hi $(git config user.name)! You've successfully authenticated."
read -r -p "Enter commit message: " commit_message
commit_message="${commit_message:-Default commit message}"

# --- Stage Changes ---
git add -A

# --- Check if there's anything to commit *before* fetching ---
if ! git diff-index --quiet --cached HEAD --; then
    log_message "Starting commit..."
    git commit -m "$commit_message"
else
    log_message "No changes to commit."
fi

# --- Fetch and Update ---
log_message "Fetching latest changes from remote..."
git fetch origin

current_branch=$(git rev-parse --abbrev-ref HEAD)

if ! git show-ref --verify --quiet "refs/remotes/origin/$current_branch"; then
    log_message "ERROR: Branch '$current_branch' does not exist on the remote (origin)."
    log_message "This likely means you need to push the branch for the first time:"
    log_message "  git push -u origin $current_branch"
    exit 1
fi

# --- Attempt a Fast-Forward Merge (Safest) ---
log_message "Updating local branch '$current_branch'..."

# Use git merge --ff-only to try a fast-forward *first*.
if ! git merge --ff-only "origin/$current_branch"; then
  log_message "Fast-forward merge failed. Attempting a regular merge..."

  # If ff-only fails, attempt a regular merge (with potential conflicts).
  if ! git merge "origin/$current_branch"; then
    log_message "ERROR: Merge failed. You have conflicts to resolve."
    log_message "Resolve the conflicts, then run 'git add .' and 'git commit'."
    log_message "After resolving the conflicts, you can run 'git push origin $current_branch'."
    exit 1
  fi
fi

# --- Push ---
log_message "Starting push..."
git push origin HEAD:"$current_branch"

log_message "Push successful!"

exit 0
