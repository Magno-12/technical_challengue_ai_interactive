from django.test import Client, TransactionTestCase

from rest_framework import status

from apps.academy.models.application import Application
from apps.academy.models.student import Student


class ApplicationViewSetTest(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.student_data = {
            "first_name": "Yuno",
            "last_name": "Grinberryall",
            "age": 15,
            "magical_affinity": "Wind"
        }
        self.student = Student.objects.create(**self.student_data)
        self.application_data = {
            "student": self.student
        }
        self.application = Application.objects.create(**self.application_data)

    def test_submit_application(self):
        url = '/application/submit_application/'
        data = {
            "student": self.student.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_applications(self):
        url = '/application/list_applications/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_application(self):
        url = f'/application/{self.application.id}/update_application/'
        data = {
            "status": "approved"
        }
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_application(self):
        url = f'/application/{self.application.id}/delete_application/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
