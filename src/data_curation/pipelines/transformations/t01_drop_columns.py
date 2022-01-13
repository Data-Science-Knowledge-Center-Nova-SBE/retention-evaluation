def run(df, docs, columns):
    """
    drops a list of columns

    :param df:
    :param columns:
    :return:
    """
    for doc in docs:
        doc.start("t01 - Drop columns", df)

    try:
        df.drop(columns, axis=1, inplace=True)

    except:
        for i in columns:
            try:
                df.drop([i], axis=1, inplace=True)
            except:
                pass

    for doc in docs:
        doc.end(df)

    return df
