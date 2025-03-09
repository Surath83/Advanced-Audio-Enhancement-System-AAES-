from flask import Flask, request, send_from_directory, jsonify # type: ignore
from flask_cors import CORS # type: ignore
import os
import shutil  # Used to copy files properly

app = Flask(__name__)
CORS(app)  # Allow requests from React frontend

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Simulate processing (replace with real enhancement logic)
    processed_filename = f"enhanced_{filename}"
    processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)
    
    shutil.copy(file_path, processed_path)  # Copy file as dummy processing

    # Construct full URL for React frontend to access
    processed_url = f"http://127.0.0.1:5000/download/{processed_filename}"

    return jsonify({
        "message": "File uploaded and processed successfully",
        "processed_file": processed_url
    })

@app.route("/download/<filename>", methods=["GET"])
def download_audio(filename):
    return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
