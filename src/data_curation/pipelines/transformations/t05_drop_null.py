def run(df, docs):
    """
    drops all rows of the dataframe that contains at least one null

    :param df:
    :return:
    """
    for doc in docs:
        doc.start("t05 - Drop null", df)

    df.dropna(inplace=True)

    for doc in docs:
        doc.end(df)

    return df
