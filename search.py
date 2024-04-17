from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_flipkart(product_name):
    products = []
    flipkart_url = f"https://www.flipkart.com/search?q={product_name}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(flipkart_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_cards = soup.find_all("div", class_="_1AtVbE")
    for card in product_cards:
        title_element = card.find("div", class_="_4rR01T")
        if title_element:
            title = title_element.text.strip()
            image_url = card.find("img")['src']
            product_link = "https://www.flipkart.com" + card.find("a")['href']
            products.append({"title": title, "image_url": image_url, "product_link": product_link})
    return products


@app.route('/search/<product_name>')
def search_products(product_name):
    products = scrape_flipkart(product_name)
    return jsonify({"products": products})

if __name__ == '__main__':
    app.run(debug=True)
