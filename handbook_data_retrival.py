
import requests
import os
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load PAT from .env
load_dotenv()
PAT = os.getenv("CONFLUENCE_PASSWORD")

# Page info
CONFLUENCE_BASE_URL = "https://confluence.sierrawireless.com"
PAGE_ID = "407798724"

# REST API URL
url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{PAGE_ID}?expand=body.storage"
headers = {
    "Authorization": f"Bearer {PAT}",
    "Content-Type": "application/json"
}

# Request
response = requests.get(url, headers=headers, verify=False)

if response.status_code == 200:
    data = response.json()
    html_content = data['body']['storage']['value']

    soup = BeautifulSoup(html_content, "html.parser")
    tables = soup.find_all("table")
    all_data = []

    for table in tables:
        headers = []
        rows_data = []
        for i, row in enumerate(table.find_all("tr")):
            cols = row.find_all(["th", "td"])
            cols_text = [col.get_text(strip=True) for col in cols]
            if i == 0:
                headers = cols_text
            else:
                row_dict = {headers[j]: cols_text[j] for j in range(len(cols_text))}
                rows_data.append(row_dict)
        all_data.append(rows_data)

    with open("handbook.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print("✅ Table data extracted and saved to 'handbook.json'")
else:
    print(f"❌ Failed to retrieve page. Status code: {response.status_code}")
    print("Response:", response.text)
