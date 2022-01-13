from . import train, test
from ...reporting.evaluation_report import EvaluationReport

ALGORITHM_NAME = "Decision Tree"


def evaluate(database_id,
             x_train,
             y_train,
             x_test,
             y_test,
             feature_names,
             extra_features_test,
             search=False,
             save_results=False):
    model = train.train(x_train, y_train, search=search)
    y_pred = test.predict(x_test, model)

    # report
    report = EvaluationReport(y_test, y_pred,extra_features_test, model, feature_names, database_id, algorithm=ALGORITHM_NAME)

    if save_results:
        report.save()

    return report
