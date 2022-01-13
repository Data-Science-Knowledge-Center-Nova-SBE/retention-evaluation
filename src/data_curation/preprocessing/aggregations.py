from clean import lowercase_removespaces
import mysql.connector
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

def nee_transformer(dataframe):
    
    dataframe['nee'].replace([True, 'true', 't'], '1', inplace=True)
    dataframe['nee'][(dataframe['nee']!='0') & (dataframe['nee']!='1')] = '0'
            
    return dataframe

def genero_transformer(dataframe):
    
    dataframe['genero'].replace(['m', 'masculino'], 1, inplace=True)
    dataframe['genero'].replace(['f', 'feminino'], 0, inplace=True)
    dataframe['genero'][(dataframe['genero']!=1) & (dataframe['genero']!=0)] = np.nan
    
    return dataframe

def escalao_transformer(dataframe):
    
    cur = mydb.cursor()
    cur.execute("SELECT * FROM correspondencia_escalao")
    agg_escalao = pd.DataFrame(cur.fetchall())
    agg_escalao.columns = cur.column_names
    
    agg_escalao = lowercase_removespaces(agg_escalao)
    
    for i in range(len(agg_escalao)): #Itera linha a linha da tabela de aggr e retorna o valor referente
        dataframe['escalao'][dataframe['escalao'] == agg_escalao['escalao_raw'][i]] = agg_escalao['escalao_agg'][i]
    
    #Se o valor não estiver na tabela, passa a 3 (default)
    dataframe['escalao'][(dataframe['escalao'] != '1') &
                         (dataframe['escalao'] != '2') &
                         (dataframe['escalao'] != '3')] = 3
    
    return dataframe

def anoLetivo_transformer(dataframe):
    
    dataframe['anoLetivo'] = dataframe['anoLetivo'].str.replace(',', '') #Retira vírgulas
    
    bad_values_index = list(dataframe['anoLetivo'][dataframe['anoLetivo'].str.len() == 7].index) #Guarda os indexes dos valores que precisam de ser alterados
    
    for i in bad_values_index: #Itera cada index e uniformiza o valor
        dataframe['anoLetivo'][i] = dataframe['anoLetivo'][i][0:4] + '/' + str(int(dataframe['anoLetivo'][i][0:4]) + 1)
    
    return dataframe

def dataNascimento_transformer(dataframe):
    
    month_dict = {'jan':'1','feb':'2','mar':'3','apr':'4','may':'5','jun':'6','jul':'7','aug':'8','sep':'9','oct':'10','nov':'11','dec':'12'}
    
    #Replaces characters of months with their number
    for i in month_dict:
        dataframe['datanascimento'] = dataframe['datanascimento'].str.replace(i, month_dict[i])

    #Removes all characters that are not numbers
    dataframe['datanascimento'] = dataframe['datanascimento'].str.replace(' ','').str.replace('/','').str.replace('\\','').str.replace('-','')
    dataframe[dataframe['datanascimento'] == ''] = np.nan
    
    #Turns every string into the rigth format to be converted into a date
    dataframe['datanascimento'][dataframe['datanascimento'].str.len()>4] = '1/' + \
                                                                               dataframe['datanascimento'][dataframe['datanascimento'].str.len()>4].str.slice(0,-4) + \
                                                                               '/' + \
                                                                               dataframe['datanascimento'][dataframe['datanascimento'].str.len()>4].str.slice(-4)
    
    dataframe['datanascimento'][dataframe['datanascimento'].str.len()<=4] = '1/' + \
                                                                                dataframe['datanascimento'][dataframe['datanascimento'].str.len()<=4].str.slice(0,-2) + \
                                                                                '/' + \
                                                                                dataframe['datanascimento'][dataframe['datanascimento'].str.len()<=4].str.slice(-2)
    
    bad_index = list(dataframe['datanascimento'][dataframe['datanascimento'].str.len() <= 7].index)

    for i in bad_index:
        if int(dataframe['datanascimento'][i][-2:]) < 20:
            dataframe['datanascimento'][i] = dataframe['datanascimento'][i][:-2] + '20' + dataframe['datanascimento'][i][-2:]
        else:
            dataframe['datanascimento'][i] = dataframe['datanascimento'][i][:-2] + '19' + dataframe['datanascimento'][i][-2:]
    
    #Turns the column into datetime
    dataframe['datanascimento'] = pd.to_datetime(dataframe['datanascimento'], dayfirst=True, errors='coerce')
    
    #Creates the age column
    dataframe['age'] = np.round((pd.to_datetime('1/9/' + dataframe['anoLetivo'].str.slice(-4)) - dataframe['datanascimento']).astype('timedelta64[D]') / 365)
    
    #Cleans the age column
    dataframe['age'][(dataframe['age'] > 65) | (dataframe['age'] < 9)] = np.nan
    
    return dataframe

def nacionalidade_transformer(dataframe):
    
    cur = mydb.cursor()
    cur.execute("SELECT * FROM correspondencia_nacionalidade")
    agg_nacionalidade = pd.DataFrame(cur.fetchall())
    agg_nacionalidade.columns = cur.column_names
    
    agg_nacionalidade = lowercase_removespaces(agg_nacionalidade)
    
    for i in range(len(agg_nacionalidade)): #Itera linha a linha da tabela de aggr e retorna o valor referente
        dataframe['nacionalidade'][dataframe['nacionalidade'] == agg_nacionalidade['nacionalidade_raw'][i]] = agg_nacionalidade['nacionalidade_agg'][i]
    
    #Se o valor não estiver na tabela, passa a portuguese (default)
    dataframe['nacionalidade'][(dataframe['nacionalidade'] != 'other') &
                               (dataframe['nacionalidade'] != 'european') &
                               (dataframe['nacionalidade'] != 'palop') &
                               (dataframe['nacionalidade'] != 'portuguese') &
                               (dataframe['nacionalidade'] != 'brazil') ] = 'portuguese'
    
    return dataframe

def linguaMaterna_transformer(dataframe):
    
    cur = mydb.cursor()
    cur.execute("SELECT * FROM correspondencia_linguaMaterna")
    agg_linguaMaterna = pd.DataFrame(cur.fetchall())
    agg_linguaMaterna.columns = cur.column_names
    
    agg_linguaMaterna = lowercase_removespaces(agg_linguaMaterna)
    
    for i in range(len(agg_linguaMaterna)): #Itera linha a linha da tabela de aggr e retorna o valor referente
        dataframe['linguaMaterna'][dataframe['linguaMaterna'] == agg_linguaMaterna['linguaMaterna_raw'][i]] = agg_linguaMaterna['linguaMaterna_pt_flag'][i]
    
    #Se o valor não estiver na tabela, passa a portuguese (default)
    dataframe['linguaMaterna'][(dataframe['linguaMaterna'] != 0) &
                               (dataframe['linguaMaterna'] != 1)] = 1
    
    return dataframe

def anoEscMae_transformer(dataframe):
    
    cur = mydb.cursor()
    cur.execute("SELECT * FROM correspondencia_anoEscMae")
    agg_anoEscMae = pd.DataFrame(cur.fetchall())
    agg_anoEscMae.columns = cur.column_names
    
    agg_anoEscMae = lowercase_removespaces(agg_anoEscMae)
    
    dataframe['anoEscMae_ord'] = dataframe['anoEscMae']
    
    for i in range(len(agg_anoEscMae)): #Itera linha a linha da tabela de aggr e retorna o valor referente
        dataframe['anoEscMae_ord'][dataframe['anoEscMae_ord'] == agg_anoEscMae['anoEscMae_raw'][i]] = agg_anoEscMae['anoEscMae_agg_ord'][i]
        dataframe['anoEscMae'][dataframe['anoEscMae'] == agg_anoEscMae['anoEscMae_raw'][i]] = agg_anoEscMae['anoEscMae_agg_cat'][i]
    
    #Se o valor não estiver na tabela, passa a 0 ou unknown
    dataframe['anoEscMae_ord'][~dataframe['anoEscMae_ord'].isin(agg_anoEscMae['anoEscMae_agg_ord'].unique())] = 0
    
    dataframe['anoEscMae'][~dataframe['anoEscMae'].isin(agg_anoEscMae['anoEscMae_agg_cat'].unique())] = 'unknown'

    return dataframe