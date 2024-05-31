from django.test import Client, TransactionTestCase

from rest_framework import status

from apps.academy.models.application import Application
from apps.academy.models.student import Student
from apps.academy.models.grimoire import Grimoire
from apps.academy.models.assignment import Assignment


class AssignmentViewSetTest(TransactionTestCase):
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
        self.grimoire_data = {
            "name": "Grimoire of the Wind",
            "clover_type": "wind",
            "clover_leaves": 4,
            "rarity": "unusual",
            "description": "A powerful grimoire of the wind element."
        }
        self.grimoire = Grimoire.objects.create(**self.grimoire_data)
        self.assignment_data = {
            "application": self.application,
            "grimoire": self.grimoire
        }
        self.assignment = Assignment.objects.create(**self.assignment_data)

    def test_list_assignments(self):
        url = '/assignment/list_assignments/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_assignment(self):
        url = '/application/submit_application/'
        data = {
            "student": self.student.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assignment.objects.count(), 2)  # Cambia esta línea
        self.assertTrue(Assignment.objects.filter(application__student=self.student).exists())

    def test_delete_assignment(self):
        url = f'/application/{self.application.id}/update_application_status/'
        data = {
            "status": "rejected"
        }
        response = self.client.patch(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Assignment.objects.count(), 0)  # Cambia esta línea
        # Verifica que la asignación se haya eliminado correctamente
        self.assertFalse(Assignment.objects.filter(application=self.application).exists())

    def test_reassign_grimoire(self):
        url = f'/application/{self.application.id}/update_application/'
        data = {
            "status": "approved"
        }
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Assignment.objects.count(), 1)
