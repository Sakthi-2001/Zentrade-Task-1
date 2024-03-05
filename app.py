from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    url = "https://s3.amazonaws.com/open-to-cors/assignment.json"
    response = requests.get(url)
    if response.status_code != 200:
        return "Failed to fetch data"
    
    try:
        data = response.json()
    except json.decoder.JSONDecodeError as e:
        return f"Failed to decode JSON: {e}"
    
    products = data.get('products')
    
    if not products or not isinstance(products, dict):
        return "Product data is not in the expected format"
    product_list = [product for product_id, product in products.items()]
    
    sorted_products = sorted(product_list, key=lambda x: int(x.get('popularity', 0)), reverse=True)
    print(sorted_products[1:10])

    return render_template('index.html', products=sorted_products)

if __name__ == '__main__':
    app.run(debug=True)
