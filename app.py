from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    # Fetch JSON data from the URL
    url = "https://s3.amazonaws.com/open-to-cors/assignment.json"
    response = requests.get(url)
    
    # Check if the response is successful
    if response.status_code != 200:
        return "Failed to fetch data"
    
    try:
        data = response.json()
    except json.decoder.JSONDecodeError as e:
        return f"Failed to decode JSON: {e}"
    
    # Extract product data from the 'products' key
    products = data.get('products')
    
    # Ensure product data is available and is a dictionary
    if not products or not isinstance(products, dict):
        return "Product data is not in the expected format"
    
    # Convert the dictionary to a list of products
    product_list = [product for product_id, product in products.items()]
    
    # Sort the products based on descending popularity
    sorted_products = sorted(product_list, key=lambda x: int(x.get('popularity', 0)), reverse=True)
    print(sorted_products[1:10])

    # Render the HTML template with sorted products
    return render_template('index.html', products=sorted_products)

if __name__ == '__main__':
    app.run(debug=True)
