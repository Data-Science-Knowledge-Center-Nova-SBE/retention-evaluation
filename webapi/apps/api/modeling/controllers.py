import json

from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.api import modeling
from apps.web.management.models import ProjectState, LogActivity
import requests
import logging
import os
import numpy as np

# Get an instance of a logger
from modeling.setup import set_models

from apps.api.history.models import HistoryLog
from modeling.predict import get_predictions_9_grade, get_predictions_8_grade, get_predictions_6_grade
from . import util

logger = logging.getLogger(__name__)

# set processed data folder
DATASET_PROCESSED = os.path.join(os.getcwd(), "data", "processed")

"""
Train
"""


class ResponseThen(Response):
    def __init__(self, data, then_callback, **kwargs):
        super().__init__(data, **kwargs)
        self.then_callback = then_callback

    def close(self):
        super().close()
        self.then_callback()


@api_view(['POST'])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@authentication_classes((TokenAuthentication,))
def train(request):
    """
    train train

    Creates a machine learning train capable to predict the campaign success.

    It may take 5 minutes (approximately).

    (does not require parameters)

    """
    print("train")

    state, _ = ProjectState.objects.get_or_create()

    # start training
    state.training = True
    state.training_status = "processing data"
    state.save()

    # log
    LogActivity.objects.create(type=LogActivity.LOG_TRAINING,
                               description="Training start")

    def do_after():
        try:

            # update state
            state.training_status = 'modeling'
            state.save()

            # train
            print("get dataset")
            train, test = get_dataset()

            from modeling.src.modeling.models.random_forest_regressor import train as rf_train
            for i in range(7):
                y_train = np.array(test[i])
                rf_train(train, y_train, days=i)

            # save project state
            state.training = False
            state.trained = True
            state.training_status = "complete"
            state.last_train = timezone.now()
            state.save()

            # log
            LogActivity.objects.create(type=LogActivity.LOG_TRAINING, description="Training complete")
            set_models()

        except Exception as exception:
            print("error")
            print(exception)
            state.training = False
            state.trained = False
            state.training_status = "failed"

            # log
            LogActivity.objects.create(type=LogActivity.LOG_PROBLEM, description=str(exception))

            state.save()

    return ResponseThen({}, do_after, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@authentication_classes((TokenAuthentication,))
def train_state(request):
    """
    returns the state of the training process []
    """
    state, _ = ProjectState.objects.get_or_create()

    return Response({"state": state.training_status}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@authentication_classes((TokenAuthentication,))
def predict_9_grade(request):
    # get data
    data = request.data

    # json to dataframe
    df = util.json_to_dataframe(data)

    # predict
    response = get_predictions_9_grade(df)

    # save into history logs
    HistoryLog.objects.create(grade="9",
                              input_data=json.dumps(data),
                              output_data=json.dumps(response))

    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@authentication_classes((TokenAuthentication,))
def predict_8_grade(request):
    # get data
    data = request.data

    # json to dataframe
    df = util.json_to_dataframe(data)

    # predict
    response = get_predictions_8_grade(df)

    # save into history logs
    HistoryLog.objects.create(grade="8",
                              input_data=json.dumps(data),
                              output_data=json.dumps(response))

    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.AllowAny, IsAuthenticated))
@authentication_classes((TokenAuthentication,))
def predict_6_grade(request):
    # get data
    data = request.data

    # json to dataframe
    df = util.json_to_dataframe(data)

    # predict
    response = get_predictions_6_grade(df)

    # save into history logs
    HistoryLog.objects.create(grade="6",
                              input_data=json.dumps(data),
                              output_data=json.dumps(response))

    return Response(response, status=status.HTTP_200_OK)
