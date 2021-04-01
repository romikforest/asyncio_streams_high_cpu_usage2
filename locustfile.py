from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def hello_world(self):
        self.client.get('/')
        # http://127.0.0.1:8000

    def on_start(self):
        pass