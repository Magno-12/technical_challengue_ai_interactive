from rest_framework import serializers

from ..models import Application
from .student_serializer import StudentSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = Application
        fields = [
            'id',
            'student',
            'application_date',
            'status',
            'rejection_reason'
        ]


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'student',
            'application_date',
            'status',
            'rejection_reason'
        ]