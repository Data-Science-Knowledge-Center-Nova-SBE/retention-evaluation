from src.modeling.feature_selection.extra_features import get_extra_features


def run(dataframe):
    df = dataframe.copy()
    return df, get_extra_features(dataframe)
