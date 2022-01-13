import pandas as pd
import matplotlib.pyplot as plt


def feature_importance(model, feature_names):

    # extract feature importance given model type
    class_type = model.__class__.__name__

    if class_type=="LogisticRegression":
        importances = model.coef_[0]
    else:
        importances = model.feature_importances_

    # convert values into series
    importances_series = pd.Series(importances, index=feature_names)

    # sort by importance
    importances_series = importances_series.sort_values(ascending=True)

    # return list of tuples
    importances_series = list(zip(importances_series, importances_series.index))

    return importances_series


def display_importances(importances_series):
    # list of tuples into series
    values, idx = zip(*importances_series)
    importances_series = pd.Series(values, idx)

    # plot chart
    fig, ax = plt.subplots()
    fig.set_figheight(15)
    importances_series.plot.barh(ax=ax)

    ax.set_title("Feature importances using MDI")
    ax.set_ylabel("Mean decrease in impurity")
    fig.tight_layout()
