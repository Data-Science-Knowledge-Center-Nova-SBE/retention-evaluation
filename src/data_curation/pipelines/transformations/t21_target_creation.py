import numpy as np


def target_creation_1year(df, prediction_year):
    # This function generates the target variable, based on the variable rFinal, for one prediction year
    # It takes as input:
    # df: df to be used
    # prediction_year: school year of prediction (ex: 9, 8, 6)

    # Gets the indexes of the rows corresponding to the prediction year
    work_index = list(df[(df['ano'] == str(prediction_year - 1)) &
                         (df['rFinal'] == '2')].index)
    work_index.extend(list(df[(df['ano'] == str(prediction_year)) &
                              (df['rFinal'] == '1')].index))

    year_diff = (9 - prediction_year) + 1

    for i in work_index:

        # Calculates the school year corresponding to the 9th grade
        study_year = str(int(df['anoLetivo'][i][0:4]) + year_diff
                         ) + '/' + str(int(df['anoLetivo'][i][5:]) + year_diff)

        # Saves the student id
        student = df['nProcesso_agrupamento'][i]

        # If there is no record of the student
        if len(df['ano'][(df['nProcesso_agrupamento'] == student) &
                         (df['anoLetivo'] == study_year)]) == 0:
            # The target remains -1
            continue

        # If there is a record, but not of the 9th grade
        elif (df['ano'][(df['nProcesso_agrupamento'] == student) &
                        (df['anoLetivo'] == study_year)] != '9').array[0]:

            df['target'][i] = 1

        # If it is in the 9th grade and the student passed
        elif (df['rFinal'][(df['nProcesso_agrupamento'] == student) &
                           (df['anoLetivo'] == study_year) &
                           (df['ano'] == '9')] == '2').array[0]:

            df['target'][i] = 0

        # If it is in the 9th grade, but the student failed
        elif (df['rFinal'][(df['nProcesso_agrupamento'] == student) &
                           (df['anoLetivo'] == study_year) &
                           (df['ano'] == '9')] == '1').array[0]:

            df['target'][i] = 1

        # If it is in the 9th grade, but we don't know whether he passed or failed
        elif (df['rFinal'][(df['nProcesso_agrupamento'] == student) &
                           (df['anoLetivo'] == study_year) &
                           (df['ano'] == '9')] == '0').array[0]:

            df['target'][i] = np.nan
        # else we "lost" the student in the database, therefore the target value is -1

    return df


def run(df, docs):
    for doc in docs:
        doc.start("t21 - target creation", df)

    # This function generates the target variable, based on the variable rFinal,
    # for all three prediction years

    # Sets the target of all rows as -1
    df['target'] = -1

    # Generates the target variable for all prediction years
    df = target_creation_1year(df, 9)
    df = target_creation_1year(df, 8)
    df = target_creation_1year(df, 6)

    for doc in docs:
        doc.end(df)

    return df
