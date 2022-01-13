from django.contrib.auth.models import User
from django.db import models
import datetime

from django.utils import timezone


class ProjectState(models.Model):
    is_data_uploaded = models.BooleanField(default=False)
    data_file = models.FileField(null=True, upload_to='data/raw')
    data_submission_timestamp = models.DateTimeField(null=True)

    training = models.BooleanField(default=False)
    trained = models.BooleanField(default=True)
    last_train = models.DateTimeField(default=datetime.date(2020, 5, 14), null=True)

    training_status = models.CharField(max_length=120, default="complete")


class LogActivity(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)

    LOG_SUBMISSION = "S"
    LOG_TRAINING = "T"
    LOG_PROBLEM = "P"
    LOG_RESET = "R"

    LOG_CHOICES = [
        (LOG_SUBMISSION, "Submision"),
        (LOG_TRAINING, "Training"),
        (LOG_PROBLEM, 'Problem'),
        (LOG_RESET, 'Reset'),
    ]

    type = models.CharField(
        max_length=2,
        choices=LOG_CHOICES,
    )

    description = models.CharField(max_length=10000)

