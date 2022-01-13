from xgboost import XGBClassifier
from src.util.timer import Timer


def train(x_train, y_train, max_depth=None, n_estimators=100, learning_rate=0.1):
    # model
    model = XGBClassifier(max_depth=max_depth, n_estimators=n_estimators, learning_rate=learning_rate)

    # train
    timer = Timer()
    model.fit(x_train, y_train)
    timer.stop()

    return model
