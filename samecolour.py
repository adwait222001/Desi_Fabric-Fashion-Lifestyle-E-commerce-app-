from flask import Flask, jsonify, send_from_directory, request
import os
import json
from collections import defaultdict
from itertools import zip_longest

app = Flask(__name__)

SORTED_FOLDER = r"C:\Users\Admin\Desktop\flutterprojects\cloth_project\data\sorted_data"

def fetch_images_with_matching_colour(genders, articles, discount):
    if not genders or not articles:
        return {"error": "Missing parameters"}, 400

    gender_list = genders.split(",")  # Convert CSV to list
    article_list = articles.split(",")

    colour_dict = defaultdict(lambda: defaultdict(list))  # {baseColour: {gender: [image_entries]}}

    for gender in gender_list:
        for article in article_list:
            article_path = os.path.join(SORTED_FOLDER, gender.strip(), article.strip())

            if not os.path.exists(article_path):
                continue  # Skip if folder doesn't exist

            for file in os.listdir(article_path):
                if file.endswith(('.jpg', '.png')):
                    img_name = os.path.splitext(file)[0]
                    json_file = os.path.join(article_path, f"{img_name}.json")

                    if os.path.exists(json_file):
                        with open(json_file, 'r', encoding='utf-8') as f:
                            json_content = json.load(f)
                            base_colour = json_content.get("data", {}).get("baseColour", "Unknown")

                            if base_colour == "Unknown":
                                continue  # Skip if baseColour is not found

                            original_price = json_content.get("data", {}).get("price", "N/A")
                            if original_price != "N/A":
                                try:
                                    original_price = float(original_price)
                                    discounted_price = original_price * (1 - discount)
                                except ValueError:
                                    discounted_price = "N/A"
                            else:
                                discounted_price = "N/A"

                            product_data = {
                                "price": original_price,
                                "discountedPrice": discounted_price,
                                "productName": json_content.get("data", {}).get("productDisplayName", "Unknown"),
                                "brand": json_content.get("data", {}).get("brandName", "Unknown"),
                                "baseColour": base_colour
                            }

                            server_host = request.host
                            image_entry = {
                                "image_url": f"http://{server_host}/images/{gender}/{article}/{file}",
                                "product_info": product_data
                            }

                            # Store images by colour and gender
                            colour_dict[base_colour][gender].append(image_entry)

    # 🏆 **New Logic: Interleave Across Genders**
    final_images = []
    for base_colour, gender_dict in colour_dict.items():
        # Extract lists of images per gender
        gender_lists = [gender_dict[gender] for gender in gender_list if gender in gender_dict]

        # Interleave images using zip_longest (fills missing slots with None)
        for items in zip_longest(*gender_lists, fillvalue=None):
            for item in items:
                if item:  # Avoid adding None values
                    final_images.append(item)

    return {"images": final_images}

@app.route('/get_images_by_colour', methods=['GET'])
def get_images_by_colour():
    genders = request.args.get("genders", "")  
    articles = request.args.get("articles", "")
    return jsonify(fetch_images_with_matching_colour(genders, articles, 0.5))

@app.route('/images/<gender>/<article>/<filename>')
def get_image(gender, article, filename):
    image_path = os.path.join(SORTED_FOLDER, gender, article)
    return send_from_directory(image_path, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
