from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():

    product = None
    code = request.args.get('code')

    if code:

        url = f"https://world.openfoodfacts.org/api/v0/product/{code}.json"

        try:

            response = requests.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0"
                },
                timeout=5
            )

            data = response.json()

            if data.get("status") == 1:

                p = data["product"]

                product = {
                    "name": p.get("product_name", "Unknown Product"),
                    "ingredients": p.get("ingredients_text", "No ingredients found"),
                    "allergens": p.get("allergens", "No allergen info"),
                    "image": p.get("image_front_url", "")
                }

            else:

                product = {
                    "name": "Product not found",
                    "ingredients": "",
                    "allergens": "",
                    "image": ""
                }

        except Exception as e:

            print("ERROR:", e)

            product = {
                "name": "API error / no response",
                "ingredients": "",
                "allergens": "",
                "image": ""
            }

    return render_template(
        "index.html",
        product=product
    )

if __name__ == '__main__':
    app.run(debug=True)