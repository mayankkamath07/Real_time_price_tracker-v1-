import requests
from bs4 import BeautifulSoup

def get_price(url):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    try:

        response = requests.get(url, headers=headers)
        
        
        soup = BeautifulSoup(response.content, "html.parser")
        
       
        price_tag = soup.find("p", class_="price_color")

        if price_tag:
                price_text = price_tag.text 
    
   
        clean_price = price_text.replace("£", "").replace(",", "").strip()
    
        return float(clean_price)

    except Exception as e:
        print(f"Scraping error: {e}")
        return None

if __name__ == "__main__":
    test_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    print(f"Price found: {get_price(test_url)}")