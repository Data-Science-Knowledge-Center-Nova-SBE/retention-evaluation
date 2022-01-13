import pandas as pd


def dataframe_summary(df):
    """
    :param df: dataframe
    :return: dataframe of:
        column name
        type of object
        number of distinct values
        unique values (showsa a maximum of 10 unique values)
        missing values
    """

    print("Database has {:,} rows and {:,} columns".format(df.shape[0], df.shape[1]))

    # return if no rows
    if df.shape[0] == 0:
        return

    # type
    data_types = pd.DataFrame(df.dtypes, columns=["Type"])

    # values
    applied = df.apply(lambda x: [x.unique()[:10]])
    applied = pd.DataFrame(applied.T).rename(columns={0: 'Values'})

    # % missing
    missing = pd.DataFrame(round(df.isnull().sum() / len(df) * 100, 2)).rename(columns={0: '% Missing'})

    # distinct values
    applied_counts = df.apply(lambda x: len(x.unique()))
    applied_counts = pd.DataFrame(applied_counts, columns=["Distinct values"])

    # concatenation
    final_df = pd.concat([data_types, applied_counts, applied, missing], axis=1)

    return final_df
