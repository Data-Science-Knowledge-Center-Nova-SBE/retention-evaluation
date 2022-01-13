def split_train_test(df, docs, ano_letivo_split):
    """
    :param df: consolidataed database dataframe
    :param ano_lectivo_split: inclusive lective year to perform split
    :return: df_train, df_test
    """
    for doc in docs:
        doc.start(f"s01 Split by ano_letivo {ano_letivo_split}", df)


    df_train = df[df["anoLetivo"] <= ano_letivo_split]
    df_test = df[df["anoLetivo"] > ano_letivo_split]


    for doc in docs:
        if doc.is_train:
            doc.end(df_train)
        else:
            doc.end(df_test)

    return df_train, df_test
