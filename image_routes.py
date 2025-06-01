from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from app import app, db, Notes  # Import the Notes model

image_bp = Blueprint("image", __name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Add image column to Notes model (Modify `models.py`)
class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), default="New Note")
    content = db.Column(db.Text, default=" ")
    notes_notebook = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), nullable=True)  # Store image filename

@image_bp.route("/note/<int:id>/upload-image", methods=["POST"])
def upload_image(id):
    note = Notes.query.get(id)
    if not note:
        return jsonify({"message": "Note not found"}), 404

    if "image" not in request.files:
        return jsonify({"message": "No image provided"}), 400

    image = request.files["image"]
    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    note.image = filename
    db.session.commit()
    return jsonify({"message": "Image uploaded successfully", "image_url": f"/static/uploads/{filename}"}), 201

@image_bp.route("/note/<int:id>/get-image", methods=["GET"])
def get_image(id):
    note = Notes.query.get(id)
    if not note or not note.image:
        return jsonify({"message": "Image not found"}), 404

    return jsonify({"image_url": f"/static/uploads/{note.image}"}), 200

@image_bp.route("/note/<int:id>/update-image", methods=["PUT"])
def update_image(id):
    note = Notes.query.get(id)
    if not note:
        return jsonify({"message": "Note not found"}), 404

    if "image" not in request.files:
        return jsonify({"message": "No image provided"}), 400

    # Delete old image if exists
    if note.image:
        old_image_path = os.path.join(app.config["UPLOAD_FOLDER"], note.image)
        if os.path.exists(old_image_path):
            os.remove(old_image_path)

    new_image = request.files["image"]
    filename = secure_filename(new_image.filename)
    new_image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    note.image = filename
    db.session.commit()
    return jsonify({"message": "Image updated successfully", "image_url": f"/static/uploads/{filename}"}), 200

@image_bp.route("/note/<int:id>/delete-image", methods=["DELETE"])
def delete_image(id):
    note = Notes.query.get(id)
    if not note:
        return jsonify({"message": "Note not found"}), 404

    if not note.image:
        return jsonify({"message": "No image to delete"}), 400

    image_path = os.path.join(app.config["UPLOAD_FOLDER"], note.image)
    if os.path.exists(image_path):
        os.remove(image_path)

    note.image = None
    db.session.commit()
    return jsonify({"message": "Image deleted successfully"}), 200
