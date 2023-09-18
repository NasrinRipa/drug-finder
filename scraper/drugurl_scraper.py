import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome WebDriver instance
driver = webdriver.Chrome()

# base URL
base_url = 'https://www.drugs.com/alpha'


csv_filename = 'drug_url_index.csv'
csv_file = open(csv_filename, 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Page Name', 'URL'])


def scrape_page():
    page_elements = driver.find_elements(By.CSS_SELECTOR, 'li a[aria-label^="Browse drugs starting with"]')
    for element in page_elements:
        page_name = element.text.strip()
        page_url = element.get_attribute('href')
        csv_writer.writerow([page_name, page_url])

# Loop through pages
for page_letter in 'abcdefghijklmnopqrstuvwxyz0123456789':
    page_url = f'{base_url}/{page_letter}.html'
    
    try:
        # Retry page load if it fails
        for _ in range(3):  # You can adjust the number of retries
            try:
                driver.get(page_url)
                break  # Exit the retry loop if successful
            except Exception as e:
                print(f"Page load error: {str(e)}")
                continue
        
        # Wait for the pagination buttons to be clickable
        paging_buttons = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'ddc-paging'))
        )

        # Click on each pagination button to navigate through the pages
        for button in paging_buttons:
            button.click()
            scrape_page()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Close the CSV file and the WebDriver
csv_file.close()
driver.quit()
