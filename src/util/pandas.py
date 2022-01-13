
def df_to_list_w_column_idx(df):
    """

    :param df: pandas DataFrame
    :return: tuple with 3 items:
    - a list of lists
    - a dictionary with key column name and value column index
    - the list of columns
    """

    columns = df.columns
    c_idx = {}
    for i, col in enumerate(columns):
        c_idx[col] = i

    data = df.to_numpy().tolist()

    return data, c_idx, columns