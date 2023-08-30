import requests
from bs4 import BeautifulSoup
import pandas as pd
import string
from tqdm import tqdm
from urllib.parse import urljoin

def scrape_drug_urls(base_url):
    alphabet = list(string.ascii_lowercase)
    drug_urls = []

    for letter in tqdm(alphabet):
        page_url = f"{base_url}#{letter}"
        response = requests.get(page_url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            rows = soup.find_all('a', class_='css-1hacg05')
            
            for row in rows:
                name = row.text
                relative_url = row['href']
                absolute_url = urljoin(base_url, relative_url)  
                drug_urls.append({
                    "name": name,
                    "url": absolute_url
                })
        else:
            print(f"Failed to fetch data for letter {letter}")

    return drug_urls

if __name__ == "__main__":
    base_url = "https://www.healthline.com/drugs"
    drug_urls = scrape_drug_urls(base_url)

    if drug_urls:
        df = pd.DataFrame(data=drug_urls, columns=drug_urls[0].keys())
        df.to_csv("drug_urls.csv", index=False)
    else:
        print("No drug URLs found.")





