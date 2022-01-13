from src.modeling.feature_selection.extra_features import get_extra_features


def run(dataframe):
    df = dataframe.copy()

    # drop
    drop_columns = [
        "agrupamento",
    ]
    df.drop(drop_columns, axis=1, inplace=True)

    return df, get_extra_features(dataframe)
