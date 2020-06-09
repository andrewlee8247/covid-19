import sys
import os
from werkzeug.datastructures import FileStorage
from werkzeug.test import EnvironBuilder, run_wsgi_app

sys.path.append("./app-keras")
from web import app
from lib import secrets


def test_frontend():
    with app.test_client() as c:
        response = c.get("/")
        assert response.status_code == 200


def test_api():
    with app.test_client() as c:
        response = c.get("/api/")
        assert response.status_code == 200


def test_upload():
    token = secrets.access_token()
    test_image = os.path.join("./tests/test_image.jpeg")
    test_file = FileStorage(
        stream=open(test_image, "rb"),
        filename="test_image.jpeg"
    )
    builder = EnvironBuilder(
        path="/api/prediction",
        method="POST",
        data={"payload": test_file},
        headers={"Content-type": "multipart/form-data", "x-access-token": token}
    )
    env = builder.get_environ()
    (app_iter, status, headers) = run_wsgi_app(app.wsgi_app, env)
    assert status == "200 OK"
    assert headers["Content-Type"] == "application/json"
    assert int(headers["Content-Length"]) > 47
