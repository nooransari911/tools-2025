import requests
import json


domain = "http://localhost:3000"



# List of URLs to fetch data from
urls = [
    f"{domain}/jet/post_user_profile?id=45&phone=fg&name=my&dept=sales",
    f"{domain}/jet/post_user_profile?id=45&phone=fg&name=my",
    f"{domain}/jet/post_user_profile?id=45&phone=85&name=my&dept=sales",
    f"{domain}/jet/nz",
    f"{domain}/jet/viet",
    f"{domain}/jet/france",
    f"{domain}/jet/china"
]

# Open HTML file to write the results
with open("./src/output.md", "w") as file:
    # Write the title of the report
    file.write("<h1>API Response Report</h1>\n")

    # Loop through each URL and fetch the response
    for url in urls:
        response = requests.get(url)
        
        # Try to parse and print the response as JSON
        try:
            response_json = response.json()
            response_content = json.dumps(response_json, indent=4)
        except ValueError:
            response_json = None
            response_content = response.text
        
        # Write each URL section
        file.write(f"<h1>URL: {url}</h1>\n")
        file.write(f"<h2>Status Code: {response.status_code}</h2>\n")
        
        # Display the response (formatted JSON or raw text)
        file.write(f"<pre>{response_content}</pre>\n")
