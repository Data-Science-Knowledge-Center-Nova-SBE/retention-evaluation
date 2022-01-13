from sklearn.metrics import recall_score, f1_score, precision_score, accuracy_score
from . import feature_importance
from src.modeling import model_manager
from .percentage_at_k import calc_percentage_at_k


class EvaluationReport():

    def __init__(self,
                 y_test,
                 y_pred,
                 y_pred_scores,
                 extra_features_test,
                 model,
                 feature_names,
                 database_id,
                 heuristic=False,
                 algorithm=""):
        # set descriptive vars
        self.algorithm = algorithm
        self.database_id = database_id

        # set y true and predicted values
        self.y_test = y_test
        self.y_pred = y_pred
        self.y_pred_scores = y_pred_scores

        self.model = model
        self.feature_names = feature_names
        self.heuristic = heuristic
        self.extra_features_test = extra_features_test

        # set metrics values
        self._set_classification_metrics()
        self._set_precision_at_k()

        if self.heuristic:
            self.feature_importance = []
        else:
            self._set_feature_importance()

    def _set_classification_metrics(self):
        self.accuracy = round(accuracy_score(self.y_test, self.y_pred) * 100, 2)
        self.precision = round(precision_score(self.y_test, self.y_pred) * 100, 2)
        self.recall = round(recall_score(self.y_test, self.y_pred) * 100, 2)
        self.f1 = round(f1_score(self.y_test, self.y_pred) * 100, 2)

    def _set_precision_at_k(self):
        self.precision_at_k_10 = calc_percentage_at_k(self.y_test, self.y_pred_scores, 10)
        self.precision_at_k_15 = calc_percentage_at_k(self.y_test, self.y_pred_scores, 15)
        self.precision_at_k_20 = calc_percentage_at_k(self.y_test, self.y_pred_scores, 20)

    def _set_feature_importance(self):
        self.feature_importance = feature_importance.feature_importance(self.model, self.feature_names)

    def display(self):
        print("\n{:17s} {}".format("Accuracy:", self.accuracy))
        print("{:17s} {}".format("Precision:", self.precision))
        print("{:17s} {}".format("Recall:", self.recall))
        print("{:17s} {}".format("F1:", self.f1))
        print("{:17s} {}".format("Precision at 10%:", self.precision_at_k_10))
        print("{:17s} {}".format("Precision at 15%:", self.precision_at_k_15))
        print("{:17s} {}".format("Precision at 20%:", self.precision_at_k_20))

        if not self.heuristic:
            feature_importance.display_importances(self.feature_importance)

    def save(self, model_group='N/A'):
        model_manager.save(self,model_group)
