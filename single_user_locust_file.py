import time
from locust import HttpUser, task, between
import json
import logging, sys

def do_login(self):
    response = self.client.post("/api/v1/login", json={
        "email":"email1@email.com",
        "password":"passwordval",
    })

    jsonResponse = response.json()
    token_value = jsonResponse['key_for_token_value']

    return token_value

class GenericUser(HttpUser):
    wait_time = between(1, 5)

    token_value = ""

    def on_start(self):
        self.token_value = do_login(self)

    @task(1)
    def some_get_request(self):
        self.client.get("/api/v1/getrequestexample", headers={'Content-Type': 'application/json','token': self.token_value})

    @task(2)
    def some_post_request(self):
        payload = json.dumps({ "name":"My first post","body":"Lorem ipsum dolar."})

        self.client.post("/api/v1/postrequestexample", headers={'Content-Type': 'application/json','token': self.token_value}, data=payload)
        