from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def scrape_olx_car_covers():
    # Set up the Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode (no UI)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    base_url = "https://www.olx.in/items/q-car-cover"
    
    driver.get(base_url)
    
    # Wait for the element containing listings to appear
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'EIR5N'))
        )
    except TimeoutException:
        print("Timeout occurred while waiting for the listings to load.")
        driver.quit()
        return
    
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  

    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    items = []
    listings = soup.find_all('li', class_='EIR5N')  

    if not listings:
        print("No listings found.")
        driver.quit()
        return

    for listing in listings:
        
        title = listing.find('span')
        price = listing.find('span', {'class': '_89yzn'})
        
        
        title_text = title.text.strip() if title else "N/A"
        price_text = price.text.strip() if price else "N/A"
        
        items.append({'Title': title_text, 'Price': price_text})

   
    if items:
        df = pd.DataFrame(items)
        df.to_csv('olx_car_covers.csv', index=False)
        print("Scraped data saved to olx_car_covers.csv")
    else:
        print("No valid data to save.")
    
    driver.quit()

if __name__ == "__main__":
    scrape_olx_car_covers()
