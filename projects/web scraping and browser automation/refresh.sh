#!/bin/bash

# First, run the Python script
echo "Running Python script..."
date +"%Y-%m-%d %H:%M:%S"
python3 ./play_parallel.py

# Infinite loop to allow the user to select options indefinitely
while true; do
    # Display the menu for user selection
    echo ""
    echo ""
    echo "Select an option:"
    echo "1. Show New Posts"
    echo "2. Show All Posts"
    echo "3. Exit"
    read -p "Enter your choice (1, 2, or 3): " choice

    # Execute the appropriate awk command based on the user's choice
    case $choice in
        1)
            echo "Showing New Posts..."
            # Run awk command for new posts
            awk -f engg_app_filter.awk Iapplied.txt Ilist.txt | fzf -e -m | tee -a Iapplied.txt | awk -F ': ' '{print $NF}' | python3 open_select.py
            ;;


        2)
            echo "Showing All Posts..."
            # Run awk command for all posts
            awk -f engg_filter.awk Ilist.txt | fzf -e -m
            ;;
        3)
            echo "Exiting..."
            break  # Exit the loop and script
            ;;
        *)
            echo "Invalid choice. Please select 1, 2, or 3."
            ;;
    esac
done
