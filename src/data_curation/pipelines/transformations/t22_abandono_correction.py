def run(df, docs):

    for doc in docs:
        doc.start("t22 - Abandono", df)

    df['rFinal'][df['abandono']=='1'] = '1'


    for doc in docs:
        doc.end(df)

    return df