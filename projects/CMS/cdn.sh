#!/bin/bash

# CDN Cache Refresh Script
# This script reads URLs from a file and hits them to refresh CDN caches

# Configuration
URL_FILE="${1:-/home/ansarimn/Downloads/essays/public/links.txt}"
LOG_FILE="/home/ansarimn/Downloads/tools-2025/projects/CMS/cdn_refresh.log"
TIMEOUT=30         # Timeout per request in seconds





# Function to log messages with timestamp
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to hit a single URL
hit_url() {
    local url="$1"
    local start_time=$(date +%s)
    
    # Use curl to hit the URL and capture HTTP code directly
    local http_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time "$TIMEOUT" --connect-timeout 10 "$url" 2>/dev/null)
    local curl_exit_code=$?
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    if [[ $curl_exit_code -eq 0 && -n "$http_code" ]]; then
        if [[ "$http_code" =~ ^[2-3][0-9][0-9]$ ]]; then
            log_message "SUCCESS: $url (HTTP $http_code) - ${duration}s"
        else
            log_message "WARNING: $url returned HTTP $http_code - ${duration}s"
        fi
    else
        log_message "ERROR: Failed to reach $url - ${duration}s"
    fi
}

# Main execution
main() {
    log_message "Starting CDN cache refresh"
    
    # Check if URL file exists
    if [[ ! -f "$URL_FILE" ]]; then
        log_message "ERROR: URL file '$URL_FILE' not found"
        exit 1
    fi
    
    # Count total URLs
    local total_urls=$(grep -c '^[^#]' "$URL_FILE" 2>/dev/null || echo 0)
    log_message "Processing $total_urls URLs from $URL_FILE"
    
    if [[ $total_urls -eq 0 ]]; then
        log_message "No URLs found in file"
        exit 0
    fi
    
    # Process all URLs in parallel
    local count=0
    local pids=()
    
    while IFS= read -r url || [[ -n "$url" ]]; do
        # Skip empty lines and comments
        [[ -z "$url" || "$url" =~ ^[[:space:]]*# ]] && continue
        
        # Trim whitespace
        url=$(echo "$url" | xargs)
        [[ -z "$url" ]] && continue
        
        # Start background job for each URL
        hit_url "$url" &
        pids+=($!)
        ((count++))
        
    done < "$URL_FILE"
    
    log_message "Started $count parallel requests"
    
    # Wait for all jobs to complete
    for pid in "${pids[@]}"; do
        wait "$pid"
    done
    
    log_message "Completed processing $count URLs"
}

# Run main function
main "$@"
