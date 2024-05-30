from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from drf_yasg.utils import swagger_auto_schema

from ..models import Application
from ..serializers.application_serializer import(
    ApplicationSerializer,
    ApplicationCreateSerializer
)
from ..utils.assign_grimoire_util import assign_grimoire_to_application


class ApplicationViewSet(GenericViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    @swagger_auto_schema(tags=['Applications'])
    @action(detail=False, methods=['post'])
    def submit_application(self, request):
        """
        Submit a new application.

        ---
        Body:
            {
                "student": "a8f9c6d0-1b3a-4c5e-8f7g-6h5i4j3k2l1m",
                "application_date": "2023-06-10"
            }
        ---
        Returns:
            The response containing the serialized data of the created application.
        Response: {
            "id": "b9g8h7i6-5d4c-3b2a-1z0y-9x8w7v6u5t4s",
            "student": {
                "id": "a8f9c6d0-1b3a-4c5e-8f7g-6h5i4j3k2l1m",
                "first_name": "John",
                "last_name": "Doe",
                "age": 20,
                "magical_affinity": "Fire",
                "identification": "ABC1234567"
            },
            "application_date": "2023-06-10",
            "status": "pending",
            "rejection_reason": null
        }
        """
        serializer = ApplicationCreateSerializer(data=request.data)
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
                "first_name": "John",
                "last_name": "Doe",
                "age": 20,
                "magical_affinity": "Fire",
                "identification": "ABC1234567"
            },
            "application_date": "2023-06-10",
            "status": "approved",
            "rejection_reason": null
        }
        """
        application = self.get_object()
        serializer = ApplicationSerializer(application, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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
                "first_name": "John",
                "last_name": "Doe",
                "age": 20,
                "magical_affinity": "Fire",
                "identification": "ABC1234567"
            },
            "application_date": "2023-06-10",
            "status": "approved",
            "rejection_reason": null
        }
        """
        application = self.get_object()
        status_data = request.data.get('status')

        if status_data == 'approved':
            assign_grimoire_to_application(application)

        serializer = ApplicationSerializer(application, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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
                    "first_name": "John",
                    "last_name": "Doe",
                    "age": 20,
                    "magical_affinity": "Fire",
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
