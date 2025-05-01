from locust import HttpUser, task, between

class ClinicUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def list_patients(self):
        self.client.get("/api/clinic/patients/")

    @task
    def list_staff(self):
        self.client.get("/api/clinic/staff/")
