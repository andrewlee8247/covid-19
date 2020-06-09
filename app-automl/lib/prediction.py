import logging
from google.cloud import automl

cloud_logger = logging.getLogger("cloudLogger")
cloud_logger.setLevel(logging.INFO)


def make_prediction(file_path):
    # Makes single prediction from AutoML
    # Set variables
    project_id = "msds498-covid"
    model_id = "ICN8802844023602544640"

    try:
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

        # Run prediction
        response = prediction_client.predict(model_full_id, payload, params)

        # Get classification and score
        for result in response.payload:
            predicted_class = result.display_name
            predicted_class_score = result.classification.score

        # Return prediction results
        prediction = {
            "predicted_class": predicted_class,
            "score": predicted_class_score,
        }
        cloud_logger.info(
            "results: %s",
            {"predicted_class": predicted_class, "score": predicted_class_score}
        )
        return prediction

    except Exception:
        raise Exception("Processing error. Please try again.")
        return
