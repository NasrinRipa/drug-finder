import csv
import requests
from bs4 import BeautifulSoup

# Read the CSV file with Drug Name and URL columns
input_csv_filename = 'filtered_drug_names_urls.csv'
output_csv_filename = 'drug_info_beatiful.csv'

# Create a CSV file to save the extracted data
csv_file = open(output_csv_filename, 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Drug Name', 'Uses', 'Dosage', 'Side Effects'])

# Function to extract drug information from a URL
def extract_drug_info(url, drug_name):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        uses = None
        dosage = None
        side_effects = None

        # Extract Uses
        uses_elements = soup.find_all('h2', id='uses', class_='ddc-anchor-offset')
        if uses_elements:
            uses = '\n'.join([element.find_next('p').text.strip() for element in uses_elements])

        # Extract Dosage
        dosage_elements = soup.find_all('h2', id='dosage', class_='ddc-anchor-offset')
        if dosage_elements:
            dosage = '\n'.join([element.find_next('p').text.strip() for element in dosage_elements])

        # Extract Side Effects
        side_effects_elements = soup.find_all('h2', id='side-effects', class_='ddc-anchor-offset')
        if side_effects_elements:
            side_effects = '\n'.join([element.find_next(['p', 'ul', 'li']).text.strip() for element in side_effects_elements])

        return drug_name, uses, dosage, side_effects
    else:
        return None, None, None, None

# Loop through the URLs and extract drug information
with open(input_csv_filename, 'r', encoding='utf-8') as input_csv:
    csv_reader = csv.DictReader(input_csv)
    for row in csv_reader:
        drug_name = row['Drug Name']
        page_url = row['URL']

        try:
            drug_name, uses, dosage, side_effects = extract_drug_info(page_url, drug_name)
            if drug_name is not None:
                csv_writer.writerow([drug_name, uses, dosage, side_effects])
                print(f"Extracted information for {drug_name}")
        except Exception as e:
            print(f"An error occurred while extracting information for {drug_name}: {str(e)}")

# Close the CSV file
csv_file.close()
