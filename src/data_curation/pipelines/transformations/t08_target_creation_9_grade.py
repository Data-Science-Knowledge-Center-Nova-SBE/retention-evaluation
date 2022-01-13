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


def calc_next_ano_letivo(ano_letivo):
    next_ano_letivo = ano_letivo.split("/")
    next_ano_letivo[0] = str(int(next_ano_letivo[0]) + 1)
    next_ano_letivo[1] = str(int(next_ano_letivo[1]) + 1)
    next_ano_letivo = "/".join(next_ano_letivo)
    return next_ano_letivo


def set_target(df):

    # get dataframe to lists
    df_list, col_idx, columns = df_to_list_w_column_idx(df)

    # sort dataframe list by nProcesso_agrupamento and anoLetivo
    df_list.sort(key=lambda row: (row[col_idx["nProcesso_agrupamento"]], row[col_idx["anoLetivo"]]))

    for i, row in enumerate(df_list):

        # get student id and ano letivo
        nProcesso = row[col_idx["nProcesso_agrupamento"]]
        ano_letivo = row[col_idx["anoLetivo"]]

        # calculate the next anoLetivo, the value whe will search for
        next_ano_letivo = calc_next_ano_letivo(ano_letivo)

        # search for student in next anoLetivo by id
        student_in_future = get_future_student(df_list, i, col_idx, next_ano_letivo, nProcesso, "9")

        # if student not found, value remains null
        if not student_in_future:
            continue

        # check if student passed and set target value
        if student_in_future[col_idx["rFinal"]] == "2":
            target_value=0
        elif student_in_future[col_idx["rFinal"]] == "1":
            target_value=1
        else:
            target_value=np.nan

        df_list[i][col_idx["target"]] = target_value

    df = pd.DataFrame(df_list, columns=columns)
    return df


def run(df, docs):
    """
    drops all rows of the dataframe that contains at least one null

    :param df:
    :return:
    """
    # set documentation
    for doc in docs:
        doc.start("t08 - 9th grade target creation", df)

    # filter - only students on 8th and 9th grade
    df = df[df["ano"].isin(["8", "9"])]

    # remove - students who failed on 8th grade
    df = df[~((df["ano"] == "8") & (df["rFinal"] == "1"))]

    # set default target - to nan
    df["target"] = np.nan

    # set target for 8th graders
    df = set_target(df)

    # remove - students who passed on 9th grade
    df = df[~((df["ano"] == "9") & (df["rFinal"] == "2"))]

    # regist differences for documentation
    for doc in docs:
        doc.end(df)

    return df
