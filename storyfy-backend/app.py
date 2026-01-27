from flask import Flask, jsonify
from config import Config
from extensions import db, CORS
from models import User

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "Storyfy backend running"})

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)