import sys
import logging

sys.path.append("./app-automl")
from lib import prediction, upload, insert

request_id = "test"
file_path = "./tests/test_image.jpeg"
file_name = "test_image.jpeg"
bucket = "xray-uploads"
gcs_path = gcs_path = "gs://{}/{}".format(bucket, file_name)


def test_prediction():
    try:
        prediction.make_prediction(file_path)
    except Exception as e:
        logging.error(e)
    return


def test_upload():
    upload.upload_image(file_path, file_name, bucket)
    return


def test_insert():
    insert.insert_data(
        request_id,
        file_name,
        gcs_path,
        "test",
        "test",
        40,
        "test@test.com",
        "tx",
        91602,
        5,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
    )
    return
