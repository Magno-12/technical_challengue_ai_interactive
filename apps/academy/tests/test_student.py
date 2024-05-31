from django.test import Client, TransactionTestCase

from rest_framework import status

from apps.academy.models.student import Student


class StudentViewSetTest(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.student_data = {
            "first_name": "Yuno",
            "last_name": "Grinberryall",
            "age": 15,
            "magical_affinity": "Wind"
        }
        self.student = Student.objects.create(**self.student_data)

    def test_create_student(self):
        url = '/student/create_student/'
        data = {
            "first_name": "Asta",
            "last_name": "Staria",
            "age": 16,
            "magical_affinity": "Darkness"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Student.objects.filter(first_name="Asta", last_name="Staria").exists())

    def test_list_students(self):
        url = '/student/list_students/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_student_with_existing_name(self):
        url = '/student/create_student/'
        data = {
            "first_name": "Yuno",
            "last_name": "Grinberryall",
            "age": 15,
            "magical_affinity": "Wind"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_student_with_invalid_age(self):
        url = '/student/create_student/'
        data = {
            "first_name": "Noelle",
            "last_name": "Silva",
            "age": 100,
            "magical_affinity": "Water"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
