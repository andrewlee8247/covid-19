import sys
from locust import HttpUser, TaskSet, task, between

sys.path.append("./app-automl")
from lib import secrets

token = secrets.access_token()


class UserBehavior(TaskSet):
    @task(1)
    def create_post(self):
        auth_header = {"x-access-token": token}
        self.client.post(
            "/api/prediction",
            files={
                "payload": (
                    "test_image.jpeg",
                    open("./tests/test_image.jpeg", "rb"),
                    "multipart/form-data",
                )
            },
            data={
                "first_name": "john",
                "last_name": "doe",
                "age": 65,
                "email": "test@test.com",
                "state": "la",
                "zip_code": "90024",
                "symptom_days": 2,
                "trouble_breathing": 1,
                "chest_pain": 1,
                "tiredness": 0,
                "bluish_color": 1,
                "runny_nose": 1,
                "cough": 1,
                "fever": 0,
            },
            headers=auth_header,
        )


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(5.0, 9.0)
