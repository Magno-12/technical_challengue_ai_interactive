from django.utils import timezone

from rest_framework import serializers

from ..models import Application
from .student_serializer import StudentSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'student',
            'application_date',
            'status',
            'rejection_reason'
        ]
        read_only_fields = ['student']


class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status']


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['student']

    def create(self, validated_data):
        student = validated_data['student']
        application_date = timezone.now().date()

        if student.age >= 14 and student.magical_affinity in [
            'Fire',
            'Water',
            'Wind',
            'Darkness',
            'Light',
            'Earth'
        ]:
            status = 'approved'
        else:
            status = 'pending'

        application = Application.objects.create(
            student=student,
            application_date=application_date,
            status=status
        )
        return application
