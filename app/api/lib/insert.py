import logging
from datetime import datetime
from google.cloud import bigquery

cloud_logger = logging.getLogger("cloudLogger")
cloud_logger.setLevel(logging.INFO)


def insert_data(
    request_id,
    file_name,
    image_path,
    first_name=None,
    last_name=None,
    age=None,
    email=None,
    state=None,
    zip_code=None,
    symptom_days=None,
    trouble_breathing=None,
    chest_pain=None,
    tiredness=None,
    bluish_color=None,
    runny_nose=None,
    cough=None,
    fever=None,
):
    # Connect to database
    client = bigquery.Client(project="msds498-covid")
    table_id = "msds498-covid.covid_19.requests"
    table = client.get_table(table_id)

    try:
        # Raise exceptions
        if age is not None:
            if type(age) is not int:
                raise Exception("Age must be a number")
        if email is not None:
            if email.find("@") == -1:
                raise Exception("Must be a valid email address")
        if state is not None:
            if type(state) is not str:
                raise Exception("State must not be an integer")
            elif len(state) != 2:
                raise Exception("State must be abbreviated")
            else:
                state = state.lower()
        if zip_code is not None:
            if type(zip_code) is not int:
                raise Exception("ZIP Code must be a number")
            if len(str(zip_code)) != 5:
                raise Exception("ZIP Code must be 5 digits")
        if symptom_days is not None:
            if type(symptom_days) is not int:
                raise Exception("Symptom days must be a number")
        # For developer
        if trouble_breathing is not None:
            if trouble_breathing not in (0, 1):
                raise Exception("trouble_breathing must be 0 or 1")
        if chest_pain is not None:
            if chest_pain not in (0, 1):
                raise Exception("chest_pain must be 0 or 1")
        if tiredness is not None:
            if tiredness not in (0, 1):
                raise Exception("tiredness must be 0 or 1")
        if bluish_color is not None:
            if bluish_color not in (0, 1):
                raise Exception("bluish_color must be 0 or 1")
        if runny_nose is not None:
            if runny_nose not in (0, 1):
                raise Exception("runny_nose must be 0 or 1")
        if cough is not None:
            if cough not in (0, 1):
                raise Exception("cough must be 0 or 1")
        if fever is not None:
            if fever not in (0, 1):
                raise Exception("fever must be 0 or 1")

        # Insert data to table
        table = client.get_table(table_id)
        row_to_insert = [
            (
                "{}".format(request_id),
                datetime.now().timestamp(),
                file_name,
                image_path,
                first_name,
                last_name,
                age,
                email,
                state,
                "{}".format(zip_code),
                symptom_days,
                trouble_breathing,
                chest_pain,
                tiredness,
                bluish_color,
                runny_nose,
                cough,
                fever,
            )
        ]
        error = client.insert_rows(table, row_to_insert)

        if not error:
            cloud_logger.info("Insert job is done.")
        else:
            raise Exception(error)
        return

    except Exception as e:
        raise Exception(e)
        return
