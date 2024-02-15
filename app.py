from flask import Flask
import jsonify

app = Flask(__name__)

@app.route("/")
def homepage():
    return "THE HOMEPAGE"

@app.route("/api/about")
def about_list():
    return jsonify()

if __name__ == "__main__":
    app.run(host='0.0.0.0')