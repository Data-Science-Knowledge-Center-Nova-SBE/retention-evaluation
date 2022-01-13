import json
from src.modeling.models import random_forest, xgboost
from modeling import setup
from modeling import shap

import random
from modeling.transform import transform_data_9_grade, transform_data_8_grade, transform_data_6_grade
import numpy as np

from modeling.shap import add_shap


def pred_based_on_k(y_pred, k):
    values = list(y_pred.copy())

    values.sort()
    values.reverse()

    n_percentage = round(len(values) * k / 100)
    threshold = values[n_percentage]
    c1 = 0  # todo remove
    c2 = 0
    for i in range(len(y_pred)):
        if y_pred[i] > threshold:
            y_pred[i] = 1
            c1 += 1
        else:
            y_pred[i] = 0
            c2 += 1

    return y_pred


def add_predictions_to_data(data, y_pred, shap_values, grade="9"):
    # get columns
    columns = list(data.columns)

    input_data = data.to_numpy()
    data = data[["ano"]]

    # select columns
    data["nProcesso"] = [i for i in range(1, len(data) + 1)]

    # delete ano
    data.drop(["ano"], axis=1, inplace=True)

    # add predictions
    data["score"] = [round(random.uniform(0, 1), 2) for i in range(len(data))]

    # convert to json
    data = data.to_json(orient="records")
    data = json.loads(data)

    # add shap
    data = add_shap(columns, data, shap_values, input_data, grade)

    return data


def get_predictions_9_grade(data):
    # get model
    model = setup.MODELS[2]

    # transform data
    data = transform_data_9_grade(data)
    array = data.to_numpy()

    # predict
    y_pred, y_pred_scores = random_forest.test.predict(array, model)
    scores = y_pred_scores[:, 1]

    # get shap
    shap_values = shap.run(setup.EXPLAINERS[2], array)

    # build response
    response = add_predictions_to_data(data, scores, shap_values, grade="9")

    return response


def get_predictions_8_grade(data):
    # get model
    model = setup.MODELS[1]

    # transform data
    data = transform_data_8_grade(data)
    array = data.to_numpy()

    # predict
    print(type(model))
    print("\n\n\n")
    y_pred, y_pred_scores = xgboost.test.predict(array, model)
    scores = y_pred_scores[:, 1]

    # get shap
    shap_values = shap.run(setup.EXPLAINERS[1], array)

    # build response
    response = add_predictions_to_data(data, scores, shap_values, grade="8")

    return response


def get_predictions_6_grade(data):
    # get model
    model = setup.MODELS[0]

    # transform data
    data = transform_data_6_grade(data)
    array = data.to_numpy()

    print(type(model))
    y_pred, y_pred_scores = random_forest.test.predict(array, model)
    scores = y_pred_scores[:, 1]

    # get shap
    shap_values = shap.run(setup.EXPLAINERS[0], array)

    # build response
    response = add_predictions_to_data(data, scores, shap_values, grade="6")

    return response


setup.set_models()
