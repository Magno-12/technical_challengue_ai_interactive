from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from drf_yasg.utils import swagger_auto_schema

from ..models import Student
from ..serializers.student_serializer import(
    StudentSerializer,
    StudentCreateSerializer
)


class StudentViewSet(GenericViewSet):
    queryset = Student.objects.all()

    def get_serializer_class(self):
        if self.action == "list_students":
            return StudentSerializer
        return StudentCreateSerializer

    @swagger_auto_schema(tags=['Students'])
    @action(detail=False, methods=['post'])
    def create_student(self, request):
        """
        Creates a new student.

        ---
        Body:
            {
                "first_name": "Yuno",
                "last_name": "Grinberryall",
                "age": 15,
                "magical_affinity": "Wind"
            }
        ---
        Returns:
            The response containing the serialized data of the created student.
        Response: {
            "id": "str",
            "first_name": "Yuno",
            "last_name": "Grinberryall",
            "age": 15,
            "magical_affinity": "Wind"
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(tags=['Students'])
    @action(detail=False, methods=['get'])
    def list_students(self, request):
        """
        Retrieves a list of all students.

        ---
        Returns:
            The response containing the serialized data of all students.
        Response: [
            {
                "id": "str",
                "first_name": "Yuno",
                "last_name": "Grinberryall",
                "identification": "FcQZm0LNlk",
                "age": 15,
                "magical_affinity": "Wind"
            },
            ...
        ]
        """
        students = self.get_queryset()
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)
