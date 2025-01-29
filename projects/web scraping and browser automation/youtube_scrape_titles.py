# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os, json, csv, time

import googleapiclient.discovery

def fetch_title (id_list):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    API_KEY = "AIzaSyAE0E5_14qSagw-4fl_yiM1LlvJ4VGhra4"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = API_KEY)



    all_responses = []  # List to hold all responses from different API calls

    # Loop through the video IDs in chunks of 20
    chunk_size = 10
    for i in range(0, len(id_list), chunk_size):
        video_ids_chunk = id_list[i:i + chunk_size]  # Get the chunk of 20 video IDs
        video_ids_str = ",".join(video_ids_chunk)

        request = youtube.videos().list(
            part="snippet",
            id=video_ids_str
        )
        response = request.execute()

        # Collect the response from each API call into the all_responses list
        all_responses.append(response)

        # Add a small delay to avoid hitting rate limits
        time.sleep(1)  # Sleep for 1 second (adjust as needed)

    # Now process all collected responses after all API calls
    for response in all_responses:
        # Loop through each response's 'items' and print the video titles
        for item in response.get("items", []):
            print(item["snippet"]["title"])

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



if __name__ == "__main__":
    # Path to your CSV file
    csv_file_path = "/home/ansarimn/Downloads/archive/youtube-playlists/Watch later-videos.csv"

    # Get the first 200 video IDs from the CSV
    id_list = get_ids_from_csv(csv_file_path, limit=200)
    # print (id_list)

    # id_list = ["Czk_co-2m4I", "DDScZ_uq6hs", "8x7-BRuwu38", "Qqpb_JrxnVc"]
    fetch_title (id_list)
