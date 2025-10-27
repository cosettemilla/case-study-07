from flask import Flask, request, jsonify, render_template
from azure.storage.blob import BlobServiceClient, PublicAccess, ContentSettings
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

bsc = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
IMAGES_CONTAINER = "images-demo"

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/api/v1/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/api/v1/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    img_blob = f"{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}-{file.filename}"
    img_bc = bsc.get_blob_client(IMAGES_CONTAINER, img_blob)
    img_bc.upload_blob(
        file.stream,
        overwrite=True,
        content_settings=ContentSettings(content_type="image/jpeg")
    )
    return jsonify({"message": "File uploaded successfully"})

if __name__ == "__main__":
    app.run(debug=True)
