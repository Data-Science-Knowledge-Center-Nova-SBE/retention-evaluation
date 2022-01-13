import pandas as pd
from src.data_curation.pipelines.transformations import t10_columns_to_lowercase
import pathlib
import os

file_path = pathlib.Path(__file__).parent.resolve()
ANO_ESC_MAE = pd.read_csv(os.path.join(file_path,"support_data","correspondencia_anoEscMae.csv"))

def run(df, docs):
    for doc in docs:
        doc.start("t19 - Ano esc mae", df)

    agg_anoEscMae = t10_columns_to_lowercase.run(ANO_ESC_MAE.copy(),[])

    df['anoEscMae_ord'] = df['anoEscMae']

    for i in range(len(agg_anoEscMae)):  # Itera linha a linha da tabela de aggr e retorna o valor referente
        df['anoEscMae_ord'][df['anoEscMae_ord'] == agg_anoEscMae['anoEscMae_raw'][i]] = \
            agg_anoEscMae['anoEscMae_agg_ord'][i]
        df['anoEscMae'][df['anoEscMae'] == agg_anoEscMae['anoEscMae_raw'][i]] = \
            agg_anoEscMae['anoEscMae_agg_cat'][i]

    # Se o valor não estiver na tabela, passa a 0 ou unknown
    df['anoEscMae_ord'][~df['anoEscMae_ord'].isin(agg_anoEscMae['anoEscMae_agg_ord'].unique())] = 0

    df['anoEscMae'][~df['anoEscMae'].isin(agg_anoEscMae['anoEscMae_agg_cat'].unique())] = 'unknown'

    for doc in docs:
        doc.end(df)

    return df
