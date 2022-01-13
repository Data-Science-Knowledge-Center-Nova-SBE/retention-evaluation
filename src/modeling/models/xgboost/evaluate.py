from .train import train
from .test import predict
from src.modeling import model_manager
import numpy as np
from ...reporting.evaluation_report import EvaluationReport

ALGORITHM_NAME = "XGBoost"


def evaluate(database_id,
             x_train,
             y_train,
             x_test,
             y_test,
             feature_names,
             extra_features_test,
             search=False,
             max_depth=None,
             max_leaf_nodes=None,
             n_estimators=100,
             learning_rate=0.1,
             save_results=False,
             model_group='N/A'):
    model = train(x_train, y_train, max_depth=max_depth, n_estimators=n_estimators, learning_rate=learning_rate)
    y_pred, y_pred_scores = predict(x_test, model)

    y_pred_scores_target = []

    for i in y_pred_scores:
        y_pred_scores_target.append(i[np.where(model.classes_ == 1)[0][0]])

    y_pred_scores_target = np.array(y_pred_scores_target)

    # evaluate
    report = EvaluationReport(y_test, y_pred, y_pred_scores_target, extra_features_test, model, feature_names, database_id,
                              algorithm=ALGORITHM_NAME)

    if save_results:
        report.save(model_group=model_group)

    return report
