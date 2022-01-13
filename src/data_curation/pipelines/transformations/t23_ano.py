import numpy as np


def run(df, docs):
    for doc in docs:
        doc.start("t23 - Ano", df)

    df['failed_last_year'] = 0

    max_grade = df['ano'].max()
    df['failed_last_year'][df['ano'] == max_grade] = 1

    for doc in docs:
        doc.end(df)

    return df
