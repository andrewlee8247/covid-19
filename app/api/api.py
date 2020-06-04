import os
import uuid
import jwt
from functools import wraps
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flasgger import Swagger
from flasgger import swag_from
from google.cloud import logging as cloudlogging
import logging
from lib import upload, insert, prediction, secrets

log_client = cloudlogging.Client()
log_handler = log_client.get_default_handler()
cloud_logger = logging.getLogger("cloudLogger")
cloud_logger.setLevel(logging.INFO)
cloud_logger.addHandler(log_handler)

UPLOAD_FOLDER = "/tmp"
BUCKET_NAME = "xray-uploads"
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


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = secrets.access_token
        # Check if token is in headers
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            cloud_logger.error('A valid token is missing')
            return jsonify({'error': 'A valid token is missing'})
        # Check if token is valid
        try:
            access = jwt.decode(token, "secret", algorithm='HS256')
        except Exception:
            cloud_logger.error('Token is invalid')
            return jsonify({'error': 'Token is invalid'})

        return f(access, *args, **kwargs)
    return decorator


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api/prediction", methods=["POST"])
@token_required
@swag_from("apidocs.yml")
def prediction_payload(access):
    if request.method == "POST":
        try:
            # Request data to insert to database
            request_id = str(uuid.uuid4())
            first_name = request.form.get("first_name", type=str)
            last_name = request.form.get("last_name", type=str)
            age = request.form.get("age", type=int)
            email = request.form.get("email", type=str)
            state = request.form.get("state", type=str)
            zip_code = request.form.get("zip_code", type=int)
            symptom_days = request.form.get("symptom_days", type=int)
            trouble_breathing = request.form.get("trouble_breathing", type=int)
            chest_pain = request.form.get("chest_pain", type=int)
            tiredness = request.form.get("tiredness", type=int)
            bluish_color = request.form.get("bluish_color", type=int)
            runny_nose = request.form.get("runny_nose", type=int)
            cough = request.form.get("cough", type=int)
            fever = request.form.get("fever", type=int)
            # Insert data to database, upload image to storage, and make prediction
            # Check if the post request has the payload part
            if "payload" not in request.files:
                raise Exception("Input name must be payload")
            file = request.files["payload"]
            # If user does not select file exception is raised
            if file.filename == "":
                raise Exception("No selected file")
            if file and allowed_file(file.filename):
                filename = "{}_{}".format(request_id, secure_filename(file.filename))
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                gcs_path = "gs://{}/{}".format(BUCKET_NAME, filename)
                # Submit prediction payload
                response = prediction.make_prediction("/tmp/", filename)
                # Insert data to database
                insert.insert_data(
                    request_id,
                    filename,
                    gcs_path,
                    first_name=first_name,
                    last_name=last_name,
                    age=age,
                    email=email,
                    state=state,
                    zip_code=zip_code,
                    symptom_days=symptom_days,
                    trouble_breathing=trouble_breathing,
                    chest_pain=chest_pain,
                    tiredness=tiredness,
                    bluish_color=bluish_color,
                    runny_nose=runny_nose,
                    cough=cough,
                    fever=fever,
                )
                # Upload image to cloud storage
                upload.upload_image("/tmp/", filename, BUCKET_NAME)
                os.remove("/tmp/" + filename)
                if list(response.keys())[0] == "error":
                    raise Exception(response)
                else:
                    cloud_logger.info({"payload": filename, "prediction": response})
                    return jsonify(response)
            else:
                raise Exception("File extension not allowed")
        except Exception as e:
            cloud_logger.error(e)
            error = {"error": "{}".format(e)}
            return jsonify(error)


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port="80")
