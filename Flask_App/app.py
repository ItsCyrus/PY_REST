from flask import Flask, request, jsonify, Blueprint, render_template
import json
from model import Item
from blueprints.home import home_bp

app = Flask(__name__)

app.register_blueprint(home_bp)

db = 'Flask_App/data/db.json'

def load_data():
    try:
        with open(db, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data(data):
    with open(db, 'w') as file:
        json.dump(data, file, indent=4)

items = load_data()

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify([item.serialize() for item in items])

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()

    required_fields = ['model', 'specs', 'color', 'availability', 'image']
    if not all(key in data for key in required_fields):
        return jsonify({'error': 'Missing fields'}), 400
    
    if not isinstance(data['model'], str) or \
       not isinstance(data['specs'], str) or \
       not isinstance(data['color'], str) or \
       not isinstance(data['availability'], bool) or \
       not isinstance(data['image'], str):
        return jsonify({'error': 'Invalid data types in payload'}), 400

    new_item = Item(data['model'], data['specs'], data['color'], data['availability'], data['image'])
    items.append(new_item)
    save_data([item.serialize() for item in items])
    return jsonify(new_item.serialize()), 201

# @app.route("/")
# def homepage():
#     return "THE HOMEPAGE"

if __name__ == '__main__':
    app.run(debug=True)