def run(df,docs):
    for doc in docs:
        doc.start("t15 - Ano letivo", df)

    # Remove commas
    df['anoLetivo'] = df['anoLetivo'].str.replace(',', '')

    # Save indexes of bad rows
    bad_values_index = list(df['anoLetivo'][df['anoLetivo'].str.len() == 7].index)

    # for each bad value, updates the value
    for i in bad_values_index:
        df['anoLetivo'][i] = df['anoLetivo'][i][0:4] + '/' + str(
            int(df['anoLetivo'][i][0:4]) + 1)

    for doc in docs:
        doc.end(df)

    return df
