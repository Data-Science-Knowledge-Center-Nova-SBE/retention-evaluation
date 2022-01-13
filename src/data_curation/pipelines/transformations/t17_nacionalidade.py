import pandas as pd
from src.data_curation.pipelines.transformations import t10_columns_to_lowercase
import pathlib
import os

file_path = pathlib.Path(__file__).parent.resolve()
NACIONALIDADE = pd.read_csv(os.path.join(file_path,"support_data","correspondencia_nacionalidade.csv"))

def run(df, docs):
    for doc in docs:
        doc.start("t17 - Nacionalidade", df)

    agg_nacionalidade = t10_columns_to_lowercase.run(NACIONALIDADE.copy(),[])

    for i in range(len(agg_nacionalidade)):  # Itera linha a linha da tabela de aggr e retorna o valor referente
        df['nacionalidade'][df['nacionalidade'] == agg_nacionalidade['nacionalidade_raw'][i]] = \
            agg_nacionalidade['nacionalidade_agg'][i]

    # Se o valor não estiver na tabela, passa a portuguese (default)
    df['nacionalidade'][(df['nacionalidade'] != 'other') &
                        (df['nacionalidade'] != 'european') &
                        (df['nacionalidade'] != 'palop') &
                        (df['nacionalidade'] != 'portuguese') &
                        (df['nacionalidade'] != 'brazil')] = 'portuguese'
    for doc in docs:
        doc.end(df)

    return df
