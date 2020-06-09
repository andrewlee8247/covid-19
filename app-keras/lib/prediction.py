import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
from PIL import Image
import logging

cloud_logger = logging.getLogger("cloudLogger")
cloud_logger.setLevel(logging.INFO)


def make_prediction(file_dir, filename):
    # Load model
    model = load_model("./lib/models/model_v1")
    payload = pd.DataFrame([filename], columns=["filename"],)
    try:
        # Image preprocessing
        predict_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

        data_generator = predict_datagen.flow_from_dataframe(
            dataframe=payload,
            directory=file_dir,
            x_col="filename",
            y_col=None,
            target_size=(224, 224),
            color_mode="rgb",
            shuffle=False,
            class_mode=None,
            batch_size=1,
            validate_filenames=False,
        )

        # Run prediction
        predict = model.predict_generator(data_generator, 1 // 1)

        # Get classification and score
        classification = np.argmax(predict, axis=1)
        if classification == 0:
            predicted_class = "normal"
            predicted_class_score = round(predict[0][0], 5)
        elif classification == 1:
            predicted_class = "COVID-19"
            predicted_class_score = round(predict[0][1], 5)

        # Return prediction results
        prediction = {
            "predicted_class": predicted_class,
            "score": str(predicted_class_score),
        }
        cloud_logger.info(
            "results: %s",
            {"predicted_class": predicted_class, "score": predicted_class_score},
        )
        return prediction

    except Exception:
        raise Exception("Processing error. Please try again.")
        return
