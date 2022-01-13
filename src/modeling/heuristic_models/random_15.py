from src.modeling.reporting.evaluation_report import EvaluationReport
from random import choices

import numpy as np

ALGORITHM_NAME = "HEURISTIC - Random Insuccess (15%)"


def predict(x_test, feature_names):
    """
    Prediction is positive if the student has negative
    to math and portuguese in the 3rd period

    :param x_test:
    :param feature_names:
    :return: list of predictions correspondent to the x_test
    """
    predictions = []

    for i in x_test:
        my_random = choices([0, 1], [0.85, 0.15])[0]
        predictions.append(my_random)

    return predictions


def evaluate(database_id,
             x_train,
             y_train,
             x_test,
             y_test,
             feature_names,
             extra_features_test):
    y_pred = predict(x_test, feature_names)

    # report
    report = EvaluationReport(y_test, y_pred, extra_features_test, predict, feature_names, database_id,
                              heuristic=True,
                              algorithm=ALGORITHM_NAME)
    report.save()

    return report
