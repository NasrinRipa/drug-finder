import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import time

def extract_section(driver, section_name):
    try:
        section_element = driver.find_element(By.CSS_SELECTOR, f'[data-testid="{section_name}"]')
        section_text = section_element.text if section_element else ""
        return section_text.strip()
    except:
        return ""

if __name__ == "__main__":
    df = pd.read_csv("drug_urls.csv")
    drug_urls = df.url.to_list()

    chrome_options = Options()
    chrome_options.add_argument
    service = Service("C:\Program Files (x86)\chromedriver.exe")  

    drug_data = []
    
    with webdriver.Chrome(service=service, options=chrome_options) as driver:
        for drug_url in tqdm(drug_urls):
            try:
                driver.get(drug_url)
                time.sleep(1)

                drug_name = drug_url.split("/")[-1]  

                # Extract "What it is" section
                what_it_is = extract_section(driver, "what-it-is")
                
                # Extract "Uses" section
                uses = extract_section(driver, "uses")
                
                # Extract "Dosage" section
                dosage = extract_section(driver, "dosage")
                
                # Extract "Side Effects" section
                side_effects = extract_section(driver, "side-effects")

                drug_data.append({
                    "name": drug_name,
                    "what_it_is": what_it_is,
                    "uses": uses,
                    "dosage": dosage,
                    "side_effects": side_effects
                })

                time.sleep(1)

            except Exception as e:
                print(f"Error for {drug_url}: {e}")
                time.sleep(1)

    if drug_data:  
        df = pd.DataFrame(data=drug_data, columns=drug_data[0].keys())
        df.to_csv("drug_features.csv", index=False)
    else:
        print("No drug data found.")













