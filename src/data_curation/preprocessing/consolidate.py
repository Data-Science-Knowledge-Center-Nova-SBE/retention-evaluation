import pandas as pd

from src.data_curation.preprocessing.primary_keys import *

def consolidate(df_alunos,df_avaliacao):
    # Avaliacao and Assiduidade

    #Alunos and Avaliacao
    df = pd.merge(df_alunos, df_avaliacao, on=PRIMARY_KEYS_ALUNOS,
                                how='left', suffixes=('_alunos', '_avaliacao'), validate='1:m')
    pass


def pivot_avaliacao():

    query = "select * from atb2.avaliacao_singlerow_per_discipline_group where periodo <> ''"

    df_raw = pd.read_sql(query, mydb)

    df_raw = df_raw.rename(columns={"average_grade": 'class'})
    periodo_dict = {'1P':'1P_','2P':'2P_','3P':'3P_','externa':'3P_','1P2S':'2P_','1S':'1S_','2S':'3P_'}
    df_raw['periodo_c'] = df_raw['periodo'].replace(periodo_dict)

    pivot_df = pd.pivot_table(df_raw, values = ['class', 'adapted_curric_flag', 'negative_class_ratio', 'disciplines_in_group'],
                                  index = ['nProcesso', 'agrupamento', 'anoLetivo_c', 'ano_c'], 
                                  columns=['periodo_c', 'disciplina_agg'],
                                  aggfunc={'class': np.mean,
                                          'adapted_curric_flag': np.max, 
                                          'negative_class_ratio': np.mean, 
                                          'disciplines_in_group': np.max}
                         ).reset_index()

    pivot_df.columns = pivot_df.columns.map(''.join)
    pivot_df = pivot_df.fillna(0)

    return pivot_df
