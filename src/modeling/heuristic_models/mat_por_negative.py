from src.modeling.reporting.evaluation_report import EvaluationReport

ALGORITHM_NAME = "HEURISTIC - Negative to Math and Portuguese"


def predict(x_test, feature_names):
    """
    Prediction is positive if the student has negative
    to math and portuguese in the 3rd period

    :param x_test:
    :param feature_names:
    :return: list of predictions correspondent to the x_test
    """
    predictions = []

    # get index of target columns
    mat_idx = feature_names.index("class3P_matematica")
    por_idx = feature_names.index("class3P_portugues")

    for row in x_test:
        if row[mat_idx] <= 2 and row[por_idx] <= 2:
            value = 1
        else:
            value = 0

        predictions.append(value)

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
