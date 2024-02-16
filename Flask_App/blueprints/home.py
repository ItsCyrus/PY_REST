from flask import Blueprint, render_template
from model import Item
import json

home_bp = Blueprint('home', __name__,template_folder='templates')

@home_bp.route('/')
def index():
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
    return render_template('index.html', items=items)