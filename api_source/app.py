from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/market-data", methods=["GET"])
def market_data():
    response = requests.get("https://dummyjson.com/products", timeout=30)
    response.raise_for_status()
    products = response.json().get("products", [])

    transformed = []
    for product in products[:20]:
        transformed.append({
            "external_product_id": product["id"],
            "product_name": product["title"],
            "category": product["category"],
            "price": product["price"],
            "rating": product["rating"],
            "brand": product.get("brand", "unknown")
        })

    return jsonify(transformed)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)