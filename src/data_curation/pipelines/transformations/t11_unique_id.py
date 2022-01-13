def run(df, docs):
    for doc in docs:
        doc.start("t11 - Transform Unique Id", df)

    # Creates a unique id
    df['nProcesso_agrupamento'] = str(df['nProcesso']) + '_' + str(df['agrupamento'])

    for doc in docs:
        doc.end(df)

    return df
