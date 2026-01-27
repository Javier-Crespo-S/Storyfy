from flask import Flask, jsonify, request
from config import Config
from extensions import db, CORS
from models import User, Story
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
CORS(app)
app.config["JWT_SECRET_KEY"] = "secret_key_storyfy" 
jwt = JWTManager(app)


@app.route("/")
def home():
    return jsonify({"message": "Storyfy backend running"})


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Faltan datos"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Usuario ya existe"}), 409

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Usuario creado correctamente"}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Faltan datos"}), 400

    user = User.query.filter_by(username=username, password=password).first()

    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify({"message": "Login correcto", "token": access_token}), 200
    else:
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401


@app.route("/api/stories", methods=["POST"])
@jwt_required()
def create_story():
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"error": "Faltan datos"}), 400

    user_id = get_jwt_identity()
    story = Story(title=title, content=content, user_id=user_id)
    db.session.add(story)
    db.session.commit()

    return jsonify({"message": "Historia publicada correctamente"}), 201


@app.route("/api/stories", methods=["GET"])
def get_stories():
    stories = Story.query.order_by(Story.id.desc()).all()
    result = []
    for story in stories:
        result.append({
            "id": story.id,
            "title": story.title,
            "content": story.content,
            "author": story.user.username
        })
    return jsonify(result), 200


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
