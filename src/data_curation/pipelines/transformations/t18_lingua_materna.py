from src.data_curation.pipelines.transformations import t10_columns_to_lowercase
import pandas as pd
import pathlib
import os

file_path = pathlib.Path(__file__).parent.resolve()
LINGUA_MATERNA = pd.read_csv(os.path.join(file_path,"support_data","correspondencia_lingua_materna.csv"))

def run(df, docs):
    for doc in docs:
        doc.start("t18 - Lingua materna", df)

    agg_linguaMaterna = t10_columns_to_lowercase.run(LINGUA_MATERNA.copy(),[])

    for i in range(len(agg_linguaMaterna)):  # Itera linha a linha da tabela de aggr e retorna o valor referente
        df['linguaMaterna'][df['linguaMaterna'] == agg_linguaMaterna['linguaMaterna_raw'][i]] = \
            agg_linguaMaterna['linguaMaterna_pt_flag'][i]

    # Se o valor não estiver na tabela, passa a portuguese (default)
    df['linguaMaterna'][(df['linguaMaterna'] != 0) &
                        (df['linguaMaterna'] != 1)] = 1
    for doc in docs:
        doc.end(df)

    return df
