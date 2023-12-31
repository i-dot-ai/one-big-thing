import random
import string

from locust import FastHttpUser, between, task
from pyquery import PyQuery


def make_code(length=6):
    return "".join(random.choices(string.ascii_lowercase, k=length))


class OneBigThingUser(FastHttpUser):
    wait_time = between(1, 5)

    @task
    def view_home(self):
        response = self.client.get("/home/")
        assert response.status_code == 200

    @task
    def view_index(self):
        response = self.client.get("/")
        assert response.status_code == 200

    def login(self):
        self.client.get("/")
        response = self.client.get("/accounts/signup/")
        content = response.content
        content = content.decode("utf-8")
        csrf_token = PyQuery(content)("form input[name='csrfmiddlewaretoken']").attr("value")
        email = f"firstname.lastname+{make_code()}@example.com"

        data = {
            "email": email,
            "password1": "Fl1bbl3-Fl1bbl3",
            "password2": "Fl1bbl3-Fl1bbl3",
            "grade": "GRADE6",
            "department": "visitengland",
            "profession": "LEGAL",
            "csrfmiddlewaretoken": csrf_token,
        }
        self.client.post("/accounts/signup/", data=data)
        response = self.client.get("/home/")
        content = response.content.decode("utf-8")
        assert email in content

    def on_start(self):
        self.login()
