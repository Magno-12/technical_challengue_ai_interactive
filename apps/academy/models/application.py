from django.db import models

from apps.default.models.base_model import BaseModel
from ..utils.choices_utils import APPLICATION_STATUSES
from .student import Student


class Application(BaseModel):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=APPLICATION_STATUSES,
        default='pending'
    )
    rejection_reason = models.TextField(blank=True)

    def __str__(self):
        return f"Application #{self.id} - {self.student}"
    class Meta:
        db_table = 'Application'
