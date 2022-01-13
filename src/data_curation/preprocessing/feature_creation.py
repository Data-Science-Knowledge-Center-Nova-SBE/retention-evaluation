import pandas as pd
from clean import lowercase_removespaces

def distrito_concelho_flag_creator(dataframe):
    #This function creates two flag variables, that indicate whether a student goes to a school (1) in the same district that he lives, or not (0)

    cur = mydb.cursor()
    cur.execute("SELECT * FROM correspondencia_agrupamento_distrito_concelho")
    cadc = pd.DataFrame(cur.fetchall())
    cadc.columns = cur.column_names

    cadc = lowercase_removespaces(cadc)

    #Creates flag variables
    dataframe['concelho_flag'] = 0
    dataframe['distrito_flag'] = 0
    
    #Imputs "weird" values as the most common value (1)
    dataframe['concelho_flag'][dataframe['concelho a'].isin(['nd'])] = 1
    dataframe['distrito_flag'][dataframe['distrito'].isin(['', 'NULL'])] = 1

    #Checks whether the student goes to a school in the same district where he lives and changes the flag value accordingly
    for i in cadc['agrupamento']:
        dataframe['concelho_flag'][(dataframe['agrupamento']==i)&
                                   (dataframe['concelho a']==cadc['concelho a'][cadc['agrupamento']==i].values[0])
                                      ] = 1

        dataframe['distrito_flag'][(dataframe['agrupamento']==i)&
                                   (dataframe['distrito']==cadc['distrito'][cadc['agrupamento']==i].values[0])
                                      ] = 1
        
    return dataframe