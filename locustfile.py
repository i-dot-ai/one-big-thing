from locust import HttpUser, between, task
from pyquery import PyQuery


class OneBigThingUser(HttpUser):
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
        csrf_token = PyQuery(content)("form input[name='csrfmiddlewaretoken']").attr("value")

        data = {
            "email": "email@example.com",
            "password1": "Fl1bbl3",
            "password2": "Fl1bbl3",
            "grade": "GRADE6",
            "department": "visitengland",
            "profession": "LEGAL",
            "csrfmiddlewaretoken": csrf_token,
        }
        self.client.post("/accounts/signup/", data=data)

    def on_start(self):
        self.login()
