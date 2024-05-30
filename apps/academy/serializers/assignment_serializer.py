from rest_framework import serializers

from ..models.assignment import Assignment
from .application_serializer import ApplicationSerializer
from .grimoire_serializer import GrimoireSerializer


class AssignmentSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer()
    grimoire = GrimoireSerializer()

    class Meta:
        model = Assignment
        fields = [
            'id',
            'application',
            'grimoire',
            'assignment_date'
        ]
