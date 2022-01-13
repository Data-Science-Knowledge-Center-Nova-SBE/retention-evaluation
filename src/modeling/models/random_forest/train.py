from sklearn.ensemble import RandomForestClassifier

from src.util.timer import Timer


def train(x_train, y_train, max_depth=None, n_estimators=100):
    # model
    model = RandomForestClassifier(max_depth=max_depth, n_estimators=n_estimators)

    # train
    timer = Timer()
    model.fit(x_train, y_train)
    timer.stop()

    return model
