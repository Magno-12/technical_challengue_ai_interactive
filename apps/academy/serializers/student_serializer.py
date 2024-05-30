import random
import string

from rest_framework import serializers

from ..models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'first_name',
            'last_name',
            'identification',
            'age',
            'magical_affinity'
        ]


class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'first_name',
            'last_name',
            'age',
            'magical_affinity'
        ]

    def create(self, validated_data):
        identification = self.generate_unique_identification()

        validated_data['identification'] = identification

        student = Student.objects.create(**validated_data)

        return student

    def generate_unique_identification(self):
        characters = string.ascii_letters + string.digits
        identification = ''.join(
            random.choice(characters) for _ in range(10)
        )

        while Student.objects.filter(
            identification=identification
        ).exists():
            identification = ''.join(
                random.choice(characters) for _ in range(10)
            )

        return identification
