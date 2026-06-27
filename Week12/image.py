from flask import Flask, request, jsonify, send_from_directory, render_template
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads", "images")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Allow only images
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"png", "jpg", "jpeg", "gif"}


# Serve images correctly
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# Upload image
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")

    if file and file.filename != "" and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        return jsonify({
            "success": True,
            "filename": filename
        })

    return jsonify({"success": False})


# Delete image
@app.route("/delete", methods=["POST"])
def delete():
    data = request.get_json()
    filename = data.get("filename")

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"success": True})

    return jsonify({"success": False, "error": "File not found"})

# Show all images
@app.route("/images", methods=["GET"])
def get_images():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return jsonify(files)

# Show the main page
@app.route("/")
def index():
    return render_template("image.html")


if __name__ == "__main__":
    app.run(debug=True)