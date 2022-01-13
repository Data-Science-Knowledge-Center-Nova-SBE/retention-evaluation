import numpy as np


def run(df, docs):
    for doc in docs:
        doc.start("t13 - Genero", df)

    df['genero'].replace(['m', 'masculino'], 1, inplace=True)
    df['genero'].replace(['f', 'feminino'], 0, inplace=True)
    df['genero'][(df['genero'] != 1) & (df['genero'] != 0)] = np.nan

    for doc in docs:
        doc.end(df)

    return df
