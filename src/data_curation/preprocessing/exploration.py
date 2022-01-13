import pandas as pd


def summary_pandas(df):
    """
    :param df: dataframe
    :return: dataframe of:
        column name
        type of object
        number of distinct values
        unique values (showsa a maximum of 10 unique values)
        missing values
    """
    # Series
    data_types = pd.DataFrame(df.dtypes, columns=["Type"])
    applied = df.apply(lambda x: [x.unique()[:10]])
    applied = pd.DataFrame(applied.T).rename(columns={0: 'Values'})
    missing = pd.DataFrame(round(df.isnull().sum() / len(df) * 100, 2)).rename(columns={0: '% Missing'})
    applied_counts = df.apply(lambda x: len(x.unique()))
    applied_counts = pd.DataFrame(applied_counts, columns=["Distinct values"])
    dd_df = pd.concat([pd.concat([pd.concat([data_types, applied_counts], axis=1), applied], axis=1), missing], axis=1)
    print("Database has {:,} rows and {:,} columns".format(df.shape[0], df.shape[1]))

    return dd_df