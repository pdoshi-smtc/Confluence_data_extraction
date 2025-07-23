import requests
import os
from dotenv import load_dotenv
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Load variables from .env
load_dotenv()

# Fetch PAT from environment (stored in CONFLUENCE_PASSWORD)
PAT = os.getenv('CONFLUENCE_PASSWORD')

# Constants
CONFLUENCE_BASE_URL = "https://confluence.sierrawireless.com"
PAGE_ID = "442173464"

# Set up the API URL
url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{PAGE_ID}?expand=body.storage"

# Use Bearer token with PAT
headers = {
    "Authorization": f"Bearer {PAT}",
    "Content-Type": "application/json"
}

# Make the request
response = requests.get(url, headers=headers, verify=False)


# Check and display result
if response.status_code == 200:
    data = response.json()
    title = data['title']
    html_content = data['body']['storage']['value']

    print(f"Title: {title}")
    print("\n--- Page Content (HTML) ---\n")
    print(html_content)
else:
    print(f"❌ Failed to retrieve page. Status code: {response.status_code}")
    print("Response:", response.text)
