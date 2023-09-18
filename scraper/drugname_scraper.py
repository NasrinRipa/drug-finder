import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a Chrome WebDriver instance 
driver = webdriver.Chrome()

# Define the base URL for drug pages
base_url = 'https://www.drugs.com'

# Read the URLs from the existing CSV file
input_csv_filename = 'drug_url_index.csv'
output_csv_filename = 'drug_names2.csv'

# Create a CSV file to save the data
csv_file = open(output_csv_filename, 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Drug Name', 'URL'])

# Function to scrape data from a drug page
def scrape_drug_page(url):
    driver.get(url)
    drug_elements = driver.find_elements(By.CLASS_NAME, 'ddc-list-column-2')
    for element in drug_elements:
        drug_name = element.text.strip()
        drug_url = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        csv_writer.writerow([drug_name, drug_url])
        print(drug_name)
        print(drug_url)

# Loop through the URLs from the input CSV file
with open(input_csv_filename, 'r', encoding='utf-8') as input_csv:
    csv_reader = csv.DictReader(input_csv)
    for row in csv_reader:
        page_name = row['Page Name']
        page_url = row['URL']
        #full_url = f"{base_url}{page_url}"
        
        try:
            # Scrape data from the drug page
            scrape_drug_page(page_url)
        except Exception as e:
            print(f"An error occurred while scraping {page_name}: {str(e)}")

# Close the CSV file and the WebDriver
csv_file.close()
driver.quit()
