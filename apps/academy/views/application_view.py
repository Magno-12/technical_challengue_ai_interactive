from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from drf_yasg.utils import swagger_auto_schema

from ..models.application import Application
from ..models.assignment import Assignment
from ..models.student import Student
from ..serializers.application_serializer import(
    ApplicationSerializer,
    ApplicationCreateSerializer,
    ApplicationStatusSerializer
)
from ..utils.assign_grimoire_util import assign_grimoire_to_application


class ApplicationViewSet(GenericViewSet):
    queryset = Application.objects.all()
    def get_serializer_class(self):
        if self.action == 'update_application_status':
            return ApplicationStatusSerializer
        elif self.action in ['update_application', 'list_applications']:
            return ApplicationSerializer
        return ApplicationCreateSerializer

    @swagger_auto_schema(tags=['Applications'])
    @action(detail=False, methods=['post'])
    def submit_application(self, request):
        """
        Submit a new application.

        ---
        Body:
            {
                "student": "a8f9c6d0-1b3a-4c5e-8f7g-6h5i4j3k2l1m",
            }
        ---
        Returns:
            The response containing the serialized data of the created application.
        Response: {
            "id": "b9g8h7i6-5d4c-3b2a-1z0y-9x8w7v6u5t4s",
            "student": {
                "id": "a8f9c6d0-1b3a-4c5e-8f7g-6h5i4j3k2l1m",
                "first_name": "Yuno",
                "last_name": "Grinberryall",
                "age": 15,
                "magical_affinity": "Wind"
                "identification": "ABC1234567"
            },
            "application_date": "2023-06-10",
            "status": "pending",
            "rejection_reason": null
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save()

        if application.status == 'approved':
            assign_grimoire_to_application(application)

        return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(tags=['Applications'])
    @action(detail=True, methods=['put'])
    def update_application(self, request, pk=None):
        """
        Update an existing application.

        ---
        Args:
            pk (str): The unique identifier of the application to update.
        ---
        Body:
            {
                "student": "a8f9c6d0-1b3a-4c5e-8f7g-6h5i4j3k2l1m",
                "application_date": "2023-06-10",
                "status": "approved",
                "rejection_reason": null
            }
        ---
        Returns:
            The response containing the serialized data of the updated application.
        Response: {
            "id": "b9g8h7i6-5d4c-3b2a-1z0y-9x8w7v6u5t4s",
            "student": {
                "id": "a8f9c6d0-1b3a-4c5e-8f7g-6h5i4j3k2l1m",
                "first_name": "Yuno",
                "last_name": "Grinberryall",
                "age": 15,
                "magical_affinity": "Wind"
                "identification": "ABC1234567"
            },
            "application_date": "2023-06-10",
            "status": "approved",
            "rejection_reason": null
        }
        """
        application = self.get_object()
        previous_status = application.status
        previous_student_data = {
            'first_name': application.student.first_name,
            'last_name': application.student.last_name,
            'identification': application.student.identification,
            'age': application.student.age,
            'magical_affinity': application.student.magical_affinity
        }

        serializer = self.get_serializer(application, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_application = serializer.save()

        updated_student_data = {
            'first_name': updated_application.student.first_name,
            'last_name': updated_application.student.last_name,
            'identification': updated_application.student.identification,
            'age': updated_application.student.age,
            'magical_affinity': updated_application.student.magical_affinity
        }

        if previous_student_data != updated_student_data:
            # Si los datos del estudiante han cambiado, actualizar todas las instancias relacionadas
            Student.objects.filter(id=updated_application.student.id).update(**updated_student_data)

        if previous_status == 'approved' and updated_application.status != 'approved':
            # Si la solicitud estaba aprobada y se cambió a otro estado, eliminar la asignación de grimorio
            Assignment.objects.filter(application=updated_application).delete()
        elif previous_status != 'approved' and updated_application.status == 'approved':
            # Si la solicitud no estaba aprobada y se cambió a aprobada, asignar un grimorio
            assign_grimoire_to_application(updated_application)
        elif updated_application.status == 'approved':
            # Si la solicitud sigue estando aprobada después de la actualización, reasignar un grimorio
            Assignment.objects.filter(application=updated_application).delete()
            assign_grimoire_to_application(updated_application)

        return Response(serializer.data)

    @swagger_auto_schema(tags=['Applications'])
    @action(detail=True, methods=['patch'])
    def update_application_status(self, request, pk=None):
        """
        Update the status of an application.

        ---
        Args:
            pk (str): The unique identifier of the application to update.
        ---
        Body:
            {
                "status": "approved"
            }
        ---
        Returns:
            The response containing the serialized data of the updated application.
        Response: {
            "id": "b9g8h7i6-5d4c-3b2a-1z0y-9x8w7v6u5t4s",
            "student": {
                "id": "a8f9c6d0-1b3a-4c5e-8f7g-6h5i4j3k2l1m",
                "first_name": "Yuno",
                "last_name": "Grinberryall",
                "age": 15,
                "magical_affinity": "Wind"
                "identification": "ABC1234567"
            },
            "application_date": "2023-06-10",
            "status": "approved",
            "rejection_reason": null
        }
        """
        application = self.get_object()
        previous_status = application.status
        serializer = ApplicationStatusSerializer(application, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if previous_status == 'approved' and application.status != 'approved':
            # Si la solicitud estaba aprobada y se cambia a otro estado, eliminar la asignación de grimorio
            Assignment.objects.filter(application=application).delete()
        elif previous_status != 'approved' and application.status == 'approved':
            # Si la solicitud no estaba aprobada y se cambia a aprobada, asignar un grimorio
            assign_grimoire_to_application(application)

        return Response(ApplicationSerializer(application).data)

    @swagger_auto_schema(tags=['Applications'])
    @action(detail=False, methods=['get'])
    def list_applications(self, request):
        """
        List all applications.

        ---
        Returns:
            The response containing the serialized data of all applications.
        Response: [
            {
                "id": "b9g8h7i6-5d4c-3b2a-1z0y-9x8w7v6u5t4s",
                "student": {
                    "id": "a8f9c6d0-1b3a-4c5e-8f7g-6h5i4j3k2l1m",
                    "first_name": "Yuno",
                    "last_name": "Grinberryall",
                    "age": 15,
                    "magical_affinity": "Wind"
                    "identification": "ABC1234567"
                },
                "application_date": "2023-06-10",
                "status": "approved",
                "rejection_reason": null
            },
            ...
        ]
        """
        applications = self.get_queryset()
        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['Applications'])
    @action(detail=True, methods=['delete'])
    def delete_application(self, request, pk=None):
        """
        Delete an application.

        ---
        Args:
            pk (str): The unique identifier of the application to delete.
        ---
        Returns:
            The response indicating the successful deletion of the application.
        Response: {}
        """
        application = self.get_object()
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
