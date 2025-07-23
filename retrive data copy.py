import requests
import os
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

PAT = os.getenv('CONFLUENCE_PASSWORD')
BASE_URL = "https://confluence.sierrawireless.com"
PAGE_ID = "442173464"

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

    for tr in table.find_all('tr')[1:]:
        cells = tr.find_all(['td', 'th'])
        if not cells:
            continue

        row_data = []
        for cell in cells:
            # Handle special <ac:link><ri:page ri:content-title="..."/> cases
            ri_page = cell.find('ri:page')
            if ri_page and ri_page.has_attr('ri:content-title'):
                value = ri_page['ri:content-title']
            else:
                # Default fallback to regular text
                value = cell.get_text(separator=' ', strip=True)
            row_data.append(value)

        # Safely zip headers with row values
        row_dict = {}
        for i in range(min(len(headers), len(row_data))):
            row_dict[headers[i]] = row_data[i]
        rows.append(row_dict)

    if rows:
        tables.append(rows)

    # Save to JSON
    with open('confluence_data.json', 'w', encoding='utf-8') as f:
        json.dump(tables, f, indent=4)

    print("✅ Tables extracted and saved to confluence_data.json")
else:
    print(f"❌ Failed to retrieve page. Status: {response.status_code}")
