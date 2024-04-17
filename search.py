from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def scrape_flipkart(product_name):
    products = []
    flipkart_url = f"https://www.flipkart.com/search?q={product_name}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(flipkart_url, headers=headers)
    logger.debug("Response status code: %s", response.status_code)  # Log response status code
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        product_cards = soup.find_all("div", class_="_1AtVbE")
        for card in product_cards:
            title_element = card.find("div", class_="_4rR01T")
            if title_element:
                title = title_element.text.strip()
                image_url = card.find("img")['src']
                product_link = "https://www.flipkart.com" + card.find("a")['href']
                products.append({"title": title, "image_url": image_url, "product_link": product_link})
    else:
        logger.error("Failed to fetch data from Flipkart. Status code: %s", response.status_code)
    return products

@app.route('/')
def index():
    return 'Welcome to the search web scraper service!'

@app.route('/search', methods=['POST'])
def search_products():
    data = request.json
    logger.debug("Received request data: %s", data)  # Log request data
    product_name = data.get('product_name')
    
    if not product_name:
        return jsonify({"error": "Product name not provided"}), 400

    products = scrape_flipkart(product_name)
    logger.debug("Scraped products: %s", products)  # Log scraped products
    return jsonify({"products": products})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
