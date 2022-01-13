import numpy as np
import pandas as pd
from src.util.pandas import df_to_list_w_column_idx


def get_future_student(df_list, i, col_idx, next_ano_letivo, nProcesso, year):
    # for each student year
    for i in range(i, len(df_list)):
        row = df_list[i]

        # return if ano letivo is bigger than the one we are looking for
        if row[col_idx["nProcesso_agrupamento"]] != nProcesso:
            break

        if row[col_idx["anoLetivo"]] == next_ano_letivo and \
                row[col_idx["nProcesso_agrupamento"]] == nProcesso and \
                row[col_idx["ano"]] == year:
            return row

    return None


def calc_future_ano_letivo(ano_letivo, number_years):
    next_ano_letivo = ano_letivo.split("/")
    next_ano_letivo[0] = str(int(next_ano_letivo[0]) + number_years)
    next_ano_letivo[1] = str(int(next_ano_letivo[1]) + number_years)
    next_ano_letivo = "/".join(next_ano_letivo)
    return next_ano_letivo


def set_target_8grade(df):

    # get dataframe to lists
    df_list, col_idx, columns = df_to_list_w_column_idx(df)

    # sort dataframe list by nProcesso_agrupamento and anoLetivo
    df_list.sort(key=lambda row: (row[col_idx["nProcesso_agrupamento"]], row[col_idx["anoLetivo"]]))

    target_value = np.nan
    
    for i, row in enumerate(df_list):

        # get student id and ano letivo
        nProcesso = row[col_idx["nProcesso_agrupamento"]]
        ano_letivo = row[col_idx["anoLetivo"]]

        # calculate the next anoLetivo and two anoLetivo forward
        next_ano_letivo = calc_future_ano_letivo(ano_letivo, 1)
        two_ano_letivo = calc_future_ano_letivo(ano_letivo, 2)
        
        # is student in the 9 grade two years forward? 
        student_in_9grade = get_future_student(df_list, i, col_idx, two_ano_letivo, nProcesso, "9")
        
        # if student not found, value remains null
        if not student_in_9grade:
            pass
        # if yes, check if student passed and set target value
        else:
            if student_in_9grade[col_idx["rFinal"]] == "2":
                target_value=0
            elif student_in_9grade[col_idx["rFinal"]] == "1":
                target_value=1
            else:
                target_value=np.nan
            
        
        # is student in the 8 grade two years forward?
        student_in_8grade_2 = get_future_student(df_list, i, col_idx, two_ano_letivo, nProcesso, "8")
        
        # if student not found, value remains null
        if not student_in_8grade_2:
            pass
        # if yes, set target value to 1 (if not set before)
        else:
            if (student_in_8grade_2) and np.isnan(target_value):
                target_value=1 
            
            
        # is student in the 8 grade one year forward?
        student_in_8grade_1 = get_future_student(df_list, i, col_idx, next_ano_letivo, nProcesso, "8")

        # if student not found, value remains null
        if not student_in_8grade_1:
            pass
        # if yes and student retained set target value to 1 (if not set before)
        else:
            if (student_in_8grade_1[col_idx["rFinal"]] == "1") and np.isnan(target_value):
                target_value=1
            
        df_list[i][col_idx["target"]] = target_value
        
        
        # safety check that the student is not found somewhere in the future still in 7th grade
        # is student in 7 grade two years forward?
        student_in_7grade_2 = get_future_student(df_list, i, col_idx, two_ano_letivo, nProcesso, "7")

        # if student not found, value remains null
        if not student_in_7grade_2:
            pass
        # if yes and student retained set target value to 1 (if not set before)
        else:
            if (student_in_7grade_2) and np.isnan(target_value):
                target_value=1

        # is student in 5 grade one year forward?
        student_in_7grade_1 = get_future_student(df_list, i, col_idx, next_ano_letivo, nProcesso, "7")

        # if student not found, value remains null
        if not student_in_7grade_1:
            pass
        # if yes and student retained set target value to 1 (if not set before)
        else:
            if (student_in_7grade_1) and np.isnan(target_value):
                target_value=1


    df = pd.DataFrame(df_list, columns=columns)
    return df



def run(df, docs):
    """
    calculates target for students that will be in the 8th grade in the following year
    :param df:
    :return df:
    """
    # set documentation
    for doc in docs:
        doc.start("t0801 - 8th grade target creation", df)

    # filter - only students on 7th and 8th or 9th grade
    df = df[df["ano"].isin(["7", "8", "9"])]
    
    # remove - students who failed on 7th grade
    df = df[~((df["ano"] == "7") & (df["rFinal"] == "1"))]
    
    # set default target - to nan
    df["target"] = np.nan
    
    # set target for 8th graders
    df = set_target_8grade(df)
    
    # remove - students who passed on 8th grade
    df = df[~((df["ano"] == "8") & (df["rFinal"] == "2"))]
    
    # remove - students from 9th grade
    df = df[~((df["ano"] == "9"))]

    # regist differences for documentation
    for doc in docs:
        doc.end(df)

    return df
