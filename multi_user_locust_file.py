import time
from locust import HttpUser, task, between
import json
import logging, sys

# Can be here in this file, a seperate file or read from CSV.
USER_CRED_DATA = [
    ("user1@email.com","upasswordvalue"),
    ("user2@email.com","upasswordvalue")
]

# Loop that ensures each simulated user we spin up has a unique token value when sending requests.
def do_login(self):
    for x in USER_CRED_DATA:
        self.email, self.password = USER_CRED_DATA.pop()

        response = self.client.post("/api/v1/login", json={
            "email":self.email,
            "password":self.password,
        })

        jsonResponse = response.json()
        token_value = jsonResponse['key_for_token_value']

        logging.info('Login with %s email and %s password', self.email, self.password)

        return token_value

class GenericUser(HttpUser):
    wait_time = between(1, 5)

    token_value = ""
    email = ""
    password = ""

    # For each user we simulate, login and store the token value from the response. We can then pass this into our header to make authenticated requests.
    def on_start(self):
        self.token_value = do_login(self)

    # In our example scenario these endpoints require a token otherwise 401 will be thrown.
    @task(2)
    def some_get_request(self):
        self.client.get("/api/v1/getrequestexample", headers={'Content-Type': 'application/json','Token': self.token_value})

        logging.info('Request sent as %s email for /api/v1/getrequestexample', self.email)

    @task(5)
    def some_post_request(self):
        payload = json.dumps({ "name":"My first post","body":"Lorem ipsum dolar."})

        self.client.post("/api/v1/postrequestexample", headers={'Content-Type': 'application/json','Token': self.token_value}, data=payload)
        
        logging.info('Request sent as %s email for /api/v1/postrequestexample', self.email)
