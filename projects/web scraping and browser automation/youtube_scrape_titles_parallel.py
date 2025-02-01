# -*- coding: utf-8 -*-

import os
import csv
import concurrent.futures
import googleapiclient.discovery
from dotenv import load_dotenv



load_dotenv()




def fetch_response_for_chunk(video_ids_chunk):
    api_service_name = "youtube"
    api_version = "v3"
    API_KEY = os.environ["API_KEY_GENERIC"]

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY)

    video_ids_str = ",".join(video_ids_chunk)
    request = youtube.videos().list(
        part="snippet",
        id=video_ids_str
    )
    response = request.execute()

    # Return the full response object
    return response

def get_ids_from_csv(file_path, limit=200):
    video_ids = []
    with open(file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header row
        for i, row in enumerate(csvreader):
            if i >= limit:  # Stop if we have processed 'limit' rows
                break
            if not row or not row[0]:  # Skip empty rows or rows with missing video ID
                continue
            video_ids.append(row[0])  # The video ID is in the first column
    return video_ids

def fetch_responses_parallel(id_list):
    # Set chunk size for parallel requests
    chunk_size = 10
    all_responses = []

    # Use ProcessPoolExecutor to parallelize API calls
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Split the list into chunks of video IDs
        chunks = [id_list[i:i + chunk_size] for i in range(0, len(id_list), chunk_size)]
        
        # Use map to fetch the responses for each chunk in parallel
        results = executor.map(fetch_response_for_chunk, chunks)
        
        # Collect all responses from the results
        for response in results:
            all_responses.append(response)

    return all_responses

def extract_titles_from_responses(responses):
    # Extract titles from the responses at the last step
    titles = []
    for response in responses:
        for item in response.get("items", []):
            titles.append(item["snippet"]["title"])
    return titles



def extract_title_with_link(responses):
    # Extract titles and their full YouTube link from the responses at the last step
    title_with_link = []
    for response in responses:
        for item in response.get("items", []):
            title = item["snippet"]["title"]
            video_id = item["id"]
            # Format: "title: full YouTube link"
            full_link = f"https://www.youtube.com/watch?v={video_id}"
            title_with_link.append(f"{title}: {full_link}")
    return title_with_link

if __name__ == "__main__":
    # Path to your CSV file
    csv_file_path = "/home/ansarimn/Downloads/archive/youtube-playlists/Watch later-videos.csv"

    # Get the first 200 video IDs from the CSV
    id_list = get_ids_from_csv(csv_file_path, limit=200)

    # Fetch all responses in parallel
    responses = fetch_responses_parallel(id_list)

    # Now extract titles from the responses at the very last step
    titles = extract_title_with_link(responses)

    # Print all the extracted titles
    for title in titles:
        print(title)
