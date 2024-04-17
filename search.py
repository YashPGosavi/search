from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Static outbound IP addresses
static_ip_addresses = [
    "44.226.145.213",
    "54.187.200.255",
    "34.213.214.55",
    "35.164.95.156",
    "44.230.95.183",
    "44.229.200.200"
]

def scrape_flipkart(product_name, source_address):
    products = []
    flipkart_url = f"https://www.flipkart.com/search?q={product_name}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(flipkart_url, headers=headers, source_address=(source_address, 0))
        response.raise_for_status()  # Raise exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')
        product_cards = soup.find_all("div", class_="_1AtVbE")
        for card in product_cards:
            title_element = card.find("div", class_="_4rR01T")
            if title_element:
                title = title_element.text.strip()
                image_url = card.find("img")['src']
                product_link = "https://www.flipkart.com" + card.find("a")['href']
                products.append({"title": title, "image_url": image_url, "product_link": product_link})
    except requests.RequestException as e:
        # Handle request exception
        print("Error during request:", e)
    except Exception as e:
        # Handle other exceptions
        print("An error occurred:", e)
    return products

@app.route('/search', methods=['POST'])
def search_products():
    data = request.get_json()
    product_name = data.get('product_name')
    if not product_name:
        return jsonify({"error": "Product name is required"}), 400
    
    # Choose one of the static IP addresses
    source_address = static_ip_addresses[0]
    
    products = scrape_flipkart(product_name, source_address)
    return jsonify({"products": products})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
