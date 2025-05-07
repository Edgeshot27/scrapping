import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_olx_car_covers():
    base_url = "https://www.olx.in/items/q-car-cover"
    
    response = requests.get(base_url)

    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    items = []
    listings = soup.find_all('li', class_='EIR5N')  
    for listing in listings:
        title = listing.find('span')
        price = listing.find('span', {'class': '_89yzn'})

        title_text = title.text.strip() if title else "N/A"
        price_text = price.text.strip() if price else "N/A"

        items.append({'Title': title_text, 'Price': price_text})

    df = pd.DataFrame(items)
    df.to_csv('olx_car_covers.csv', index=False)
    print("Scraped data saved to olx_car_covers.csv")

if __name__ == "__main__":
    scrape_olx_car_covers()
