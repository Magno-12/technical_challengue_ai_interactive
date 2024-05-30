from django.db import models

from apps.default.models.base_model import BaseModel
from .application import Application
from .grimoire import Grimoire


class Assignment(BaseModel):

    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    grimoire = models.ForeignKey(Grimoire, on_delete=models.CASCADE)
    assignment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assignment #{self.id} - {self.application}"

    class Meta:
        db_table = 'Assignment'
