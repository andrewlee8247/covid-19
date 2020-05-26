import logging
from google.cloud import automl
from lib import upload

cloud_logger = logging.getLogger("cloudLogger")
cloud_logger.setLevel(logging.INFO)


def make_prediction(file_dir, filename):
    # Makes single prediction from AutoML
    # Set variables
    project_id = "msds498-covid"
    model_id = "covid-model-v.1"

    try:
        file_path = "{}{}".format(file_dir, filename)
        upload.upload_image(file_dir, filename)
        prediction_client = automl.PredictionServiceClient()

        # Get the full path of the model.
        model_full_id = prediction_client.model_path(
            project_id, "us-central1", model_id
        )

        # Read the file.
        with open(file_path, "rb") as content_file:
            content = content_file.read()

        image = automl.types.Image(image_bytes=content)
        payload = automl.types.ExamplePayload(image=image)

        # params is additional domain-specific parameters.
        # score_threshold is used to filter the result
        # https://cloud.google.com/automl/docs/reference/rpc/google.cloud.automl.v1#predictrequest
        params = {"score_threshold": "0.8"}

        response = prediction_client.predict(model_full_id, payload, params)
        for result in response.payload:
            predicted_class = result.display_name
            predicted_class_score = result.classification.score
        prediction = {
            "predicted_class": predicted_class,
            "score": predicted_class_score,
        }
        cloud_logger.info(
            "results: %s",
            {"predicted_class": predicted_class, "score": predicted_class_score},
        )
        return prediction

    except Exception as e:
        raise Exception(e)
        return
