from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

import os

from image_upload import handle_files,fetch_image#
from profile_name import add_name,init_db,show_name#

from multiple import fetch_images_with_discount#
from multiple import get_images_with_50_discount#
from multiple import get_images_with_20_discount#
from samecolour import fetch_images_with_matching_colour#
from multiple import get_images_with_30_discount#
from multiple import get_images_with_40_discount#
from brand import fetch_images_by_brand#
from brand import get_images_by_brand#
from orderbase import init_order_db,add_order,get_orders#

app = Flask(__name__)
CORS(app)

init_db()
init_order_db()



@app.route('/image', methods=['POST'])
def senddata():
    try:
        print("Headers:", request.headers)
        print("Files:", request.files)
        print("Form Data:", request.form)

        if 'file' not in request.files or 'user_id' not in request.form:
            return jsonify({'message': 'No file part in the request'}), 400

        image_file = request.files['file']
        user_id = request.form['user_id']

        if image_file.filename == '':
            return jsonify({'message': 'No selected file'}), 400

        
        filename = handle_files()
        
        return jsonify({'message': f'File uploaded successfully as {filename}'}), 200

    except Exception as e:
        # Log the error for debugging
        print("Error:", str(e))
        return jsonify({'message': 'File upload failed', 'error': str(e)}), 500


@app.route('/add', methods=['POST'])
def add_name_route():
    try:
        print("Headers:", request.headers)
        print("Files:", request.files)
        print("Form Data:", request.form)

        # Get the JSON data from the request
        data = request.get_json()

        user_id = data.get('user_id')
        name = data.get('name')

        if not user_id or not name:
            return jsonify({"message": "user_id and name are required"}), 400

        # Call add_name with parameters
        add_name()  # Pass user_id and name as arguments
        
        return jsonify({'message': 'Name uploaded successfully'}), 200
    except Exception as e:
        # Log the error for debugging
        print("Error:", str(e))
        return jsonify({'message': 'Name upload failed', 'error': str(e)}), 500


#Streaming part starts here so lookout from here

SORTED_FOLDER = r"C:\Users\Admin\Desktop\flutterprojects\test\data\sorted_data"

@app.route('/get_images_by_colour', methods=['GET'])
def get_images_by_colour():
    genders = request.args.get("genders", "")  
    articles = request.args.get("articles", "")
    return jsonify(fetch_images_with_matching_colour(genders, articles, 0.5))

@app.route('/get_images', methods=['GET'])
def get_images_with_50_discount():
    genders = request.args.get("genders", "")  
    articles = request.args.get("articles", "")
    return jsonify(fetch_images_with_discount(genders, articles, 0.5))



@app.route('/get_images', methods=['GET'])
def get_images_with_50():
    genders = request.args.get("genders", "")  
    articles = request.args.get("articles", "")
    return jsonify(fetch_images_with_discount(genders, articles, 0.5))


@app.route('/get_images_20', methods=['GET'])
def get_images_with_20():
    genders = request.args.get("genders", "")  
    articles = request.args.get("articles", "")
    return jsonify(fetch_images_with_discount(genders, articles, 0.2))


@app.route('/images/<gender>/<article>/<filename>')
def get_image(gender, article, filename):
    image_path = os.path.join(SORTED_FOLDER, gender, article)
    if not os.path.exists(os.path.join(image_path, filename)):
        return jsonify({"error": "Image not found"}), 404
    return send_from_directory(image_path, filename)


@app.route('/get_images_30', methods=['GET'])
def get_images_with_30():
    genders = request.args.get("genders", "")  
    articles = request.args.get("articles", "")
    return jsonify(fetch_images_with_discount(genders, articles, 0.3))

@app.route('/get_images_40', methods=['GET'])
def get_images_with_40():
    genders = request.args.get("genders", "")  
    articles = request.args.get("articles", "")
    return jsonify(fetch_images_with_discount(genders, articles, 0.4))

@app.route('/get_by_brand', methods=['GET'])
def get_brand():
    genders = request.args.get("genders", "")  
    articles = request.args.get("articles", "")
    brand = request.args.get("brand", "")
    return jsonify(fetch_images_by_brand(genders, articles, brand))

######
"profile and user name starts here"

@app.route('/cat', methods=['POST'])
def ball():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({"message": "User ID is required"}), 400

        # Call show_name to fetch the name for the user_id
        response = show_name(user_id=user_id)  # This function should return the user's name
        
        return response

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500


@app.route('/test/<user_id>', methods=['GET'], endpoint='get_image_route')
def get_image(user_id):
    try:
        image = fetch_image(user_id)  # Assuming this function fetches the image based on the user_id
        return image
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

    

















############
"order work start here"
############
@app.route('/add_order_path', methods=['POST'])
def add_order_route():
    try:
        data = request.get_json()
        user_id = data.get('user_id')  # Firebase UID from the frontend
        items = data.get('items')  # List of items in the order
        total_price = data.get('total_price')  # Total price of the order
        payment_method = data.get('payment_method')  # Payment method (e.g., 'Credit Card')

        if not user_id or not items or total_price is None or not payment_method:
            return jsonify({"message": "User ID, Items, Total Price, and Payment Method are required"}), 400

        # Call the add_order function to store the order in the database
        return add_order()

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "Error while placing order", "error": str(e)}), 500



@app.route('/get_orders', methods=['GET'])
def get_orders_route():
    """Endpoint to retrieve all orders from the database."""
    try:
        return get_orders()  # Call the function to fetch all orders

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "Error fetching orders", "error": str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)    
