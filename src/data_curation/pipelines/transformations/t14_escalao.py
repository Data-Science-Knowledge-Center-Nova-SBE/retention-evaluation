import pandas as pd
from src.data_curation.pipelines.transformations import t10_columns_to_lowercase
import pathlib
import os

file_path = pathlib.Path(__file__).parent.resolve()
ESCALAO = pd.read_csv(os.path.join(file_path, "support_data", "correspondencia_escalao.csv"))


def run(df, docs):
    for doc in docs:
        doc.start("t14 - Escalao", df)

    agg_escalao = t10_columns_to_lowercase.run(ESCALAO.copy(), [])

    for i in range(len(agg_escalao)):  # Itera linha a linha da tabela de aggr e retorna o valor referente
        df['escalao'][df['escalao'] == agg_escalao['escalao_raw'][i]] = agg_escalao['escalao_agg'][i]

    # Se o valor não estiver na tabela, passa a 3 (default)
    df['escalao'][(df['escalao'] != '1') &
                  (df['escalao'] != '2') &
                  (df['escalao'] != '3')] = 3

    for doc in docs:
        doc.end(df)

    return df
