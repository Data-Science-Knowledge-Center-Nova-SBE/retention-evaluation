from sklearn.linear_model import LogisticRegression

from src.util.timer import Timer


def train(x_train, y_train):
    # model
    model = LogisticRegression()

    # train
    timer = Timer()
    model.fit(x_train, y_train)
    timer.stop()

    return model
