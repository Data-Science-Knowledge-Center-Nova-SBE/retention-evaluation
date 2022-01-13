def run(df, docs):
    for doc in docs:
        doc.start("t12 - Nee", df)

    df['nee'].replace([True, 'true', 't'], '1', inplace=True)
    df['nee'][(df['nee'] != '0') & (df['nee'] != '1')] = '0'

    for doc in docs:
        doc.end(df)

    return df
