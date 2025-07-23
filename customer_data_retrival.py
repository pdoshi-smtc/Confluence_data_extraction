import requests
import os
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

PAT = os.getenv('CONFLUENCE_PASSWORD')
BASE_URL = "https://confluence.sierrawireless.com"
PAGE_ID = "466383617"

url = f"{BASE_URL}/rest/api/content/{PAGE_ID}?expand=body.storage"

headers = {
    "Authorization": f"Bearer {PAT}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers, verify=False)

if response.status_code == 200:
    data = response.json()
    html_content = data['body']['storage']['value']

    soup = BeautifulSoup(html_content, 'html.parser')

    tables = []
    for table in soup.find_all('table'):
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        rows = []

        for tr in table.find_all('tr')[1:]:  # Skip header
            cells = tr.find_all(['td', 'th'])
            row = [cell.get_text(strip=True) for cell in cells]
            row_dict = {}
            for i in range(min(len(headers), len(row))):
                row_dict[headers[i]] = row[i]
            rows.append(row_dict)

        tables.append(rows)

    # Save to JSON
    with open('customer_data.json', 'w', encoding='utf-8') as f:
        json.dump(tables, f, indent=4)

    print("✅ Tables extracted and saved to customer_data.json")
else:
    print(f"❌ Failed to retrieve page. Status: {response.status_code}")
