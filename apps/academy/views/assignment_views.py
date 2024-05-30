from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from drf_yasg.utils import swagger_auto_schema

from ..models import Assignment
from ..serializers.assignment_serializer import AssignmentSerializer


class AssignmentViewSet(GenericViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    @swagger_auto_schema(tags=['Assignments'])
    @action(detail=False, methods=['get'])
    def list_assignments(self, request):
        """
        List all grimoire assignments.

        ---
        Returns:
            The response containing the serialized data of all grimoire assignments.
        Response: [
            {
                "id": "c1d2e3f4-5g6h-7i8j-9k0l-1m2n3o4p5q6r",
                "application": {
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
                "grimoire": {
                    "id": "s1t2u3v4-5w6x-7y8z-9a0b-1c2d3e4f5g6h",
                    "name": "Grimoire of the Mystic Flame",
                    "clover_type": "fire",
                    "clover_leaves": 4,
                    "rarity": "unusual",
                    "description": "A powerful grimoire imbued with the essence of fire."
                },
                "assignment_date": "2023-06-11"
            },
            ...
        ]
        """
        assignments = self.get_queryset()
        serializer = self.get_serializer(assignments, many=True)
        return Response(serializer.data)
