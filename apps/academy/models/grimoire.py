from django.db import models

from apps.default.models.base_model import BaseModel
from ..utils.choices_util import(
    CLOVER_TYPES,
    CLOVER_LEAVES,
    RARITY_LEVELS
)


class Grimoire(BaseModel):

    name = models.CharField(max_length=50)
    clover_type = models.CharField(max_length=10, choices=CLOVER_TYPES)
    clover_leaves = models.IntegerField(choices=CLOVER_LEAVES)
    rarity = models.CharField(max_length=20, choices=RARITY_LEVELS)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Grimoire'
