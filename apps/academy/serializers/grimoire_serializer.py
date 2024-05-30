# serializers/grimoire_serializer.py
from rest_framework import serializers

from ..models.grimoire import Grimoire


class GrimoireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grimoire
        fields = [
            'id',
            'name',
            'clover_type',
            'clover_leaves',
            'rarity',
            'description'
        ]
