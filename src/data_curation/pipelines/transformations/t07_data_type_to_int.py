def run(df, docs, columns):
    """
    converts each column to type int

    :param df:
    :param columns:
    :return:
    """
    for doc in docs:
        doc.start("t07 - Change type of {} to int".format(str(columns).replace("'", "")), df)


    for column in columns:
        df[column] = df[column].astype(int)

    for doc in docs:
        doc.end(df)

    return df
