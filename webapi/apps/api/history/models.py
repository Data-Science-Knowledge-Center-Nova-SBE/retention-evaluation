from django.db import models
from django.utils import timezone


class HistoryLog(models.Model):
    grade = models.CharField(default="9", max_length=1)
    created_at = models.DateTimeField(default=timezone.now)
    input_data = models.CharField(max_length=100000, default="[]")
    output_data = models.CharField(max_length=100000, default="[]")

    def __str__(self):
        return str(self.created_at)
