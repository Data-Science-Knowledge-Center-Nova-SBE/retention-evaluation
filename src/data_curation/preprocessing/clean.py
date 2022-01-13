
import pandas as pd
from aggregations import anoLetivo_transformer

def group_assiduidade(df):
    #Function to group missings from the date level to the period level (same level as Avaliacao)
    pass

def lowercase_removespaces(dataframe):
    
    columns = list(dataframe.columns)
    
    for i in columns: #Itera coluna a coluna
        try:
            #Coloca todos os caracteres em lowercase e retira leading ou trailing spaces
            dataframe[i] = dataframe[i].str.lower().str.strip()
    
        except:
            continue
            
    return dataframe
    
def unique_id(dataframe):

    #Creates a unique id
    dataframe['nProcesso_agrupamento'] = dataframe['nProcesso'] + '_' + dataframe['agrupamento']

    #Drops "duplicate" columns 
    dataframe.drop(columns = ['nProcesso', 'agrupamento'], inplace = True)

    return dataframe

def rFinal_10_adjustment(dataframe):
    #This function checks whether there are any records of students in the 10th grade, whose rFinal in the 9th grade, in the previous school year, is 0

    cur = mydb.cursor()
    cur.execute("SELECT * FROM alunos_avaliados_10ano")
    alunos_avaliados_10ano = pd.DataFrame(cur.fetchall())
    alunos_avaliados_10ano.columns = cur.column_names

    #Applies all the necessary transformations to the newly imported table
    alunos_avaliados_10ano = lowercase_removespaces(alunos_avaliados_10ano)
    alunos_avaliados_10ano = unique_id(alunos_avaliados_10ano)
    alunos_avaliados_10ano.sort_values(by=['anoLetivo'], inplace=True) #Para garntir que, caso o aluno apareça duas vezes na tabela, o ano letivo mais antigo apareça primeiro
    alunos_avaliados_10ano = anoLetivo_transformer(alunos_avaliados_10ano)
    
    #List to store ids of rows that need to be changed
    ids = []
    
    #Possible rows that migth be changed (we are only interested in rows of 9th grade, rFinal of 0 and students with information regarding the 10th year)
    sample = dataframe[dataframe['nProcesso_agrupamento'].isin(alunos_avaliados_10ano['nProcesso_agrupamento'].unique())]
    sample = sample[sample['ano'] == '9']
    sample = sample[sample['rFinal']=='0']
    
    #Checks which students, in the school year prior to being in the 10th grade, were in the 9th grade
    for i in alunos_avaliados_10ano['nProcesso_agrupamento'].unique():

        study_year = str(int(alunos_avaliados_10ano['anoLetivo'][alunos_avaliados_10ano['nProcesso_agrupamento']==i].values[0][0:4])-1
                            ) + '/' + str(int(alunos_avaliados_10ano['anoLetivo'][alunos_avaliados_10ano['nProcesso_agrupamento']==i].values[0][5:])-1)

        if len(sample[(sample['nProcesso_agrupamento'] == i) &
                    (sample['anoLetivo'] == study_year) &
                    (sample['ano'] == '9') &
                    (sample['rFinal'] == '0')]) != 0:

            ids.append(list(sample[(sample['nProcesso_agrupamento'] == i) &
                      (sample['anoLetivo'] == study_year) &
                      (sample['ano'] == '9') &
                      (sample['rFinal'] == '0')].index)[0])
    
    #Updates the rFinal of the respective rows to a "Pass" (2)
    dataframe['rFinal'].loc[ids] = '2'
    
    return dataframe

