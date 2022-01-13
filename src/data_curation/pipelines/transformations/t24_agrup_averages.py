import numpy as np


def run(df, docs):
    for doc in docs:
        doc.start("t24 - Agrupamento averages", df)

    df['escalao'] = df['escalao'].astype(int)

    selection_cols = [
        'agrupamento',
        'anoLetivo',
        'escalao',
        'linguaMaterna',
        'anoEscMae_ord',
        'expected_age',
        'class3P_avg',
        'negative_class_ratio_3P'
    ]

    df["anoEscMae_ord"] = df["anoEscMae_ord"].astype(float)
    df["linguaMaterna"] = df["linguaMaterna"].astype(float)

    group_by = ['agrupamento', 'anoLetivo']
    df_agrupamento = df[selection_cols] \
        .groupby(group_by) \
        .mean() \
        .reset_index()


    df_agrupamento.columns = [
        'agrupamento',
        'anoLetivo',
        'escalao_agrup',
        'linguaMaterna_agrup',
        'escMae_agrup',
        'expected_age_agrup',
        'class_avg_agrup',
        'negative_class_ratio_agrup'
    ]
    df = df.merge(df_agrupamento,
                  how='left',
                  on=['agrupamento', 'anoLetivo'])

    for doc in docs:
        doc.end(df)

    return df
