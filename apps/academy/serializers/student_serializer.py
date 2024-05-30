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

    def validate_age(self, value):
        if value > 99:
            raise serializers.ValidationError('Age must be a maximum of 2 digits.')
        return value

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')

        if Student.objects.filter(first_name=first_name, last_name=last_name).exists():
            raise serializers.ValidationError('A student with the same name already exists.')

        return attrs

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
