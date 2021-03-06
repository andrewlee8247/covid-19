import logging
from google.cloud import storage
from google.cloud.storage import Blob

cloud_logger = logging.getLogger("cloudLogger")
cloud_logger.setLevel(logging.DEBUG)


def upload_image(file_path, filename, bucket_name):
    # Uploads file to cloud storage and returns file path
    # Set variables
    project_id = "msds498-covid"

    storage_client = storage.Client(project=project_id)
    bucket = storage_client.get_bucket(bucket_name)

    try:
        # Upload file
        blob = Blob(filename, bucket)
        with open(file_path, "rb") as file_content:
            blob.upload_from_file(file_content)
        gcs_path = "gs://{}/{}".format(bucket_name, filename)
        cloud_logger.info("File uploaded successfully to %s", gcs_path)
        return

    except Exception as e:
        raise Exception(e)
        return
