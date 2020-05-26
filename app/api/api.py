import os
import uuid
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flasgger import Swagger
from flasgger import swag_from
from google.cloud import logging as cloudlogging
import logging
from lib import prediction

log_client = cloudlogging.Client()
log_handler = log_client.get_default_handler()
cloud_logger = logging.getLogger("cloudLogger")
cloud_logger.setLevel(logging.INFO)
cloud_logger.addHandler(log_handler)

UPLOAD_FOLDER = "/tmp"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SWAGGER"] = {
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/api/apispec_1.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/api/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/",
}

# Setup template for Swagger UI
template = {
    "swagger": "2.0",
    "info": {
        "title": "Computer Vision API: COVID-19",
        "description": "API Documentation for COVID-19 Classification Based on X-Ray Imaging",
        "version": "1.0",
        "schemes": ["http", "https"],
    },
}

Swagger(app, template=template)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api/prediction", methods=["POST"])
@swag_from("apidocs.yml")
def prediction_payload():
    if request.method == "POST":
        try:
            # Check if the post request has the payload part
            if "payload" not in request.files:
                raise Exception("Input name must be payload")
            file = request.files["payload"]
            # If user does not select file exception is raised
            if file.filename == "":
                raise Exception("No selected file")
            if file and allowed_file(file.filename):
                request_id = str(uuid.uuid4())
                filename = "{}_{}".format(request_id, secure_filename(file.filename))
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                response = prediction.make_prediction("/tmp/", filename)
                os.remove("/tmp/" + filename)
                if list(response.keys())[0] == "error":
                    raise Exception(response)
                else:
                    cloud_logger.info({"payload": filename, "prediction": response})
                    return jsonify(response)
            else:
                raise Exception("File extension not allowed")
        except Exception as e:
            cloud_logger.error({"error": "{}".format(e)})
            error = {"error": "{}".format(e)}
            return jsonify(error)


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port="8080")
