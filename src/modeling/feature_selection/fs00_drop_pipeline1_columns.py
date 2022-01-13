from src.modeling.feature_selection.extra_features import get_extra_features


def run(dataframe):
    df = dataframe.copy()

    # drop
    drop_columns = [
        "anoLetivo",
        'age',
        'ciclo',
        'nProcesso',
        'agrupamento'
    ]
    try:
        df.drop(drop_columns, axis=1, inplace=True)

    except:
        for i in drop_columns:
            try:
                df.drop([i], axis=1, inplace=True)
            except:
                pass

    return df, get_extra_features(dataframe)
