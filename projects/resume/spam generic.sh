#!/bin/bash
# Spam any HTTP endpoint

# Function to validate the URL
validate_url() {
    if [[ $1 =~ ^(http|https):// ]]; then
        return 0  # Valid URL
    else
        return 1  # Invalid URL
    fi
}

# Default HTTP endpoint
default_endpoint="https://www.google.com/"
default_requests=100

# Print script start message with timestamp
echo -e "[$(date +'%Y-%m-%d %H:%M:%S')] - Script started\n"

# Prompt user for the HTTP endpoint
read -p "Enter the HTTP endpoint (including http:// or https://) [Default: $default_endpoint]: " endpoint

# Use default if input is empty
if [[ -z "$endpoint" ]]; then
    endpoint="$default_endpoint"
fi

# Validate the endpoint
if ! validate_url "$endpoint"; then
    echo -e "Invalid URL. Please enter a valid HTTP or HTTPS URL.\n"
    exit 1
fi

# Prompt user for the number of requests
read -p "Enter the number of requests to send [Default: $default_requests]: " total_requests

# Use default if input is empty
if [[ -z "$total_requests" ]]; then
    total_requests="$default_requests"
fi

# Initialize counters
success_count=0
total_time=0
times=()

# Send requests in parallel and capture responses with timing
response_data=$(seq 1 "$total_requests" | xargs -n1 -P100 bash -c "start=\$(date +%s.%N); code=\$(curl -s -o /dev/null -w \"%{http_code}\n\" \"$endpoint\"); end=\$(date +%s.%N); duration=\$(echo \"(\$end - \$start) * 1000\" | bc); echo \"\$code \$duration\"")

# Process response data
while read -r line; do
    code=$(echo "$line" | awk '{print $1}')
    duration=$(echo "$line" | awk '{print $2}')

    if [[ "$code" =~ ^2 ]]; then  # Check if the response code starts with 2
        ((success_count++))
        times+=("$duration")
        total_time=$(echo "$total_time + $duration" | bc)
    fi
done <<< "$response_data"

# Calculate min, max, and average times
if (( ${#times[@]} > 0 )); then
    min_time=$(printf '%s\n' "${times[@]}" | sort -n | head -n1)
    max_time=$(printf '%s\n' "${times[@]}" | sort -n | tail -n1)
    avg_time=$(echo "$total_time / ${#times[@]}" | bc -l)
else
    min_time=0
    max_time=0
    avg_time=0
fi

# Print the summary
echo -e "Total requests sent: $total_requests\n"
echo -e "Successful responses: $success_count\n"
echo -e "Total time taken: $total_time ms\n"
echo -e "Min response time: $min_time ms\n"
echo -e "Max response time: $max_time ms\n"
echo -e "Avg response time: $avg_time ms\n"
