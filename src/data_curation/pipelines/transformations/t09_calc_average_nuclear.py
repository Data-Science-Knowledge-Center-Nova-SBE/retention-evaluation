import numpy as np


def calc_row_columns_average(row, columns):
    values = []

    # filter to not consider nan values
    for column in columns:
        value = row[column]
        if value != np.nan:
            values.append(value)

    if len(values) == 0:
        return np.nan

    return sum(values) / len(values)


def calc_period_nuclear_non_nuclear(df, period):
    nuclear_columns = []
    non_nuclear_columns = []

    # get period class columns
    for column in list(df.columns):

        # continue if is not period column
        if not column.startswith(f"class{period}P"):
            continue

        # check if is nuclear
        if column.endswith(("matematica", "portuges")):
            nuclear_columns.append(column)
        else:
            non_nuclear_columns.append(column)

    df[f"average_nuclear_{period}P"] = df.apply(lambda row: calc_row_columns_average(row, nuclear_columns), axis=1)
    df[f"average_not_nuclear_{period}P"] = df.apply(lambda row: calc_row_columns_average(row, non_nuclear_columns),
                                                    axis=1)

    return df


def run(df, docs, periods=[1, 2, 3]):
    for doc in docs:
        doc.start("t09 - Calc average nuclear/non nuclear", df)

    # for each period
    for period in periods:
        df = calc_period_nuclear_non_nuclear(df, period)

    for doc in docs:
        doc.end(df)

    return df
