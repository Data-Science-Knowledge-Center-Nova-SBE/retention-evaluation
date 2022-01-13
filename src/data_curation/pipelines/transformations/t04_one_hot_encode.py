import pandas as pd

def run(df, docs, column, drop_first_ohe=False):
    """
    one hot encodes any column, adds to the column name a prefix with the column name

    :param df:
    :param column:
    :return:
    """
    for doc in docs:
        doc.start(f"t04 - one hot encode {column}", df)

    dummies = pd.get_dummies(df[column], prefix=column+"_", drop_first=drop_first_ohe)
    df = pd.concat([df, dummies], axis=1)
    df.drop([column], axis=1, inplace=True)

    for doc in docs:
        doc.end(df)

    return df
