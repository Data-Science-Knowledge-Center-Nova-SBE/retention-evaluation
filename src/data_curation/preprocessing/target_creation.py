import pandas as pd
import numpy as np

def target_creation_1year(dataframe, prediction_year):
    #This function generates the target variable, based on the variable rFinal, for one prediction year
    #It takes as input:
    #dataframe: dataframe to be used
    #prediction_year: school year of prediction (ex: 9, 8, 6)
    
    #Gets the indexes of the rows corresponding to the prediction year
    work_index = list(dataframe[(dataframe['ano'] == str(prediction_year - 1)) &
                               (dataframe['rFinal'] == '2')].index)
    work_index.extend(list(dataframe[(dataframe['ano'] == str(prediction_year)) &
                               (dataframe['rFinal'] == '1')].index))
    
    year_diff = (9 - prediction_year) + 1

    for i in work_index:

        #Calculates the school year corresponding to the 9th grade
        study_year = str(int(dataframe['anoLetivo'][i][0:4])+year_diff
                        ) + '/' + str(int(dataframe['anoLetivo'][i][5:])+year_diff)

        #Saves the student id
        student = dataframe['nProcesso_agrupamento'][i]

        #If there is no record of the student
        if len(dataframe['ano'][(dataframe['nProcesso_agrupamento'] == student) &
                                             (dataframe['anoLetivo'] == study_year)]) == 0:
            #The target remains -1
            continue

        #If there is a record, but not of the 9th grade
        elif (dataframe['ano'][(dataframe['nProcesso_agrupamento'] == student) &
                                             (dataframe['anoLetivo'] == study_year)] != '9').array[0]:

            dataframe['target'][i] = 1

        #If it is in the 9th grade and the student passed
        elif (dataframe['rFinal'][(dataframe['nProcesso_agrupamento'] == student) &
                                             (dataframe['anoLetivo'] == study_year) &
                                              (dataframe['ano'] == '9')] == '2').array[0]:

            dataframe['target'][i] = 0

        #If it is in the 9th grade, but the student failed
        elif (dataframe['rFinal'][(dataframe['nProcesso_agrupamento'] == student) &
                                             (dataframe['anoLetivo'] == study_year) &
                                              (dataframe['ano'] == '9')] == '1').array[0]:

            dataframe['target'][i] = 1

        #If it is in the 9th grade, but we don't know whether he passed or failed
        elif (dataframe['rFinal'][(dataframe['nProcesso_agrupamento'] == student) &
                                             (dataframe['anoLetivo'] == study_year) &
                                              (dataframe['ano'] == '9')] == '0').array[0]:

            dataframe['target'][i] = np.nan
        #else we "lost" the student in the database, therefore the target value is -1  

    return dataframe

def target_creation_3years(dataframe):
    #This function generates the target variable, based on the variable rFinal, for all three prediction years 

    #Sets the target of all rows as -1
    dataframe['target'] = -1 
    
    #Generates the target variable for all prediction years
    dataframe = target_creation_1year(dataframe,9)
    dataframe = target_creation_1year(dataframe,8)
    dataframe = target_creation_1year(dataframe,6)
    
    return dataframe