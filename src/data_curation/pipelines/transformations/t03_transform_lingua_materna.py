import db
from src.data_curation.pipelines.transformations import t10_columns_to_lowercase
import pandas as pd
import pathlib
import os

file_path = pathlib.Path(__file__).parent.resolve()
LINGUA_MATERNA = pd.read_csv(os.path.join(file_path, "support_data", "correspondencia_linguaMaterna.csv"))


def run(dataframe, docs):
    for doc in docs:
        doc.start("t03 - Transform linguaMaterna to binary", dataframe)

    agg_linguaMaterna = LINGUA_MATERNA.copy()
    agg_linguaMaterna = t10_columns_to_lowercase.run(agg_linguaMaterna,[])

    for i in range(len(agg_linguaMaterna)):  # Itera linha a linha da tabela de aggr e retorna o valor referente
        dataframe['linguaMaterna'][dataframe['linguaMaterna'] == agg_linguaMaterna['linguaMaterna_raw'][i]] = \
        agg_linguaMaterna['linguaMaterna_pt_flag'][i]

    # Se o valor não estiver na tabela, passa a portuguese (default)
    dataframe['linguaMaterna'][(dataframe['linguaMaterna'] != 0) &
                               (dataframe['linguaMaterna'] != 1)] = 1

    for doc in docs:
        doc.end(dataframe)

    return dataframe
