import pandas as pd
import os
print(os.getcwd())
from src.data_curation.preprocessing.primary_keys import *



def duplicates(df,table='ALUNOS'):
    """
    :param df:
    :param table: 'ALUNOS', 'ASSIDUIDADE' 'AULAS_DADAS', 'AVALIACAO', 'CURRICULO', 'INSCRICOES' ou 'TURMAS'
    :return: df
    """
    if table == 'ALUNOS':
        keys = PRIMARY_KEYS_ALUNOS
    elif table == 'ASSIDUIDADE':
        keys = PRIMARY_KEYS_ASSIDUIDADE
    elif table == 'AULAS_DADAS':
        keys = PRIMARY_KEYS_AULAS_DADAS
    elif table == 'AVALIACAO':
        keys = PRIMARY_KEYS_AVALIACAO
    elif table == 'CURRICULO':
        keys = PRIMARY_KEYS_CURRICULO
    elif table == 'INSCRICOES':
        keys = PRIMARY_KEYS_INSCRICOES
    elif table == 'TURMAS':
        keys = PRIMARY_KEYS_TURMAS
    else:
        return "Invalid selection of table param"
    df = df.drop_duplicates().drop_duplicates(subset=keys, keep='last').copy()
    return df


