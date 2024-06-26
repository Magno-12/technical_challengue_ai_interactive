from django.db import models
from django.core.validators import MaxValueValidator

from apps.default.models.base_model import BaseModel
from ..utils.choices_util import MAGICAL_AFFINITIES


class Student(BaseModel):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    identification = models.CharField(max_length=10, unique=True)
    age = models.IntegerField(validators=[MaxValueValidator(99)])
    magical_affinity = models.CharField(
        max_length=10,
        choices=MAGICAL_AFFINITIES
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'Student'
        unique_together = ('first_name', 'last_name')
