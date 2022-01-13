def run(df, docs):
    for doc in docs:
        doc.start("t10 - Columns to lowercase", df)

    columns = list(df.columns)

    # for each column
    for i in columns:
        try:
            # all charts to lowercase and no leading or trailing spaces
            df[i] = df[i].str.lower().str.strip()
        except:
            continue

    for doc in docs:
        doc.end(df)

    return df
