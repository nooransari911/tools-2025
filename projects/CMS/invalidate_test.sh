#!/bin/bash
# New, more robust version

# Read the API key from the first command-line argument
API_KEY="$1"

# Check if the key was provided
if [ -z "$API_KEY" ]; then
    echo "Error: API Key was not provided as an argument."
    exit 1
fi

# Use the key from the argument
curl -X POST "https://z8sw7kg1o2.execute-api.us-west-2.amazonaws.com/v1-initial/AWSCloudFrontInvalidateAll" -H "x-api-key: $API_KEY"
