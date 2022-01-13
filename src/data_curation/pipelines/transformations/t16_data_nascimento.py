import numpy as np
import pandas as pd


def run(df, docs):
    for doc in docs:
        doc.start("t16 - Data de nascimento", df)

    month_dict = {
        'jan': '1', 'feb': '2', 'mar': '3', 'apr': '4',
        'may': '5', 'jun': '6', 'jul': '7', 'aug': '8',
        'sep': '9', 'oct': '10', 'nov': '11', 'dec': '12'
    }

    df['dataNascimento'] = df['dataNascimento'].astype(str)

    # Replaces characters of months with their number
    for i in month_dict:
        df['dataNascimento'] = df['dataNascimento'].str.replace(i, month_dict[i])

    # Removes all characters that are not numbers
    df['dataNascimento'] = df['dataNascimento'].str.replace(' ', '').str.replace('/', '').str.replace(
        '\\', '').str.replace('-', '')
    df[df['dataNascimento'] == ''] = np.nan

    # Turns every string into the rigth format to be converted into a date
    df['dataNascimento'][df['dataNascimento'].str.len() > 4] = '1/' + \
                                                                   df['dataNascimento'][
                                                                       df[
                                                                           'dataNascimento'].str.len() > 4].str.slice(
                                                                       0, -4) + \
                                                                   '/' + \
                                                                   df['dataNascimento'][
                                                                       df[
                                                                           'dataNascimento'].str.len() > 4].str.slice(
                                                                       -4)

    df['dataNascimento'][df['dataNascimento'].str.len() <= 4] = '1/' + \
                                                                    df['dataNascimento'][
                                                                        df[
                                                                            'dataNascimento'].str.len() <= 4].str.slice(
                                                                        0, -2) + \
                                                                    '/' + \
                                                                    df['dataNascimento'][
                                                                        df[
                                                                            'dataNascimento'].str.len() <= 4].str.slice(
                                                                        -2)

    bad_index = list(df['dataNascimento'][df['dataNascimento'].str.len() <= 7].index)

    for i in bad_index:
        if int(df['dataNascimento'][i][-2:]) < 20:
            df['dataNascimento'][i] = df['dataNascimento'][i][:-2] + '20' + \
                                        df['dataNascimento'][i][-2:]
        else:
            df['dataNascimento'][i] = df['dataNascimento'][i][:-2] + '19' + \
                                        df['dataNascimento'][i][-2:]

    # Turns the column into datetime
    df['dataNascimento'] = pd.to_datetime(df['dataNascimento'], dayfirst=True, errors='coerce')

    # Creates the age column
    df['age'] = np.round(
        (pd.to_datetime('1/8/' + df['anoLetivo'].str.slice(-4)) - df['dataNascimento']).astype(
            'timedelta64[D]') / 365)

    # Cleans the age column
    df['age'][(df['age'] > 65) | (df['age'] < 9)] = np.nan

    # Creates the expected_age column
    df['expected_age'] = df['age'] - (df['ano'].astype(float) + 6)


    for doc in docs:
        doc.end(df)

    return df
