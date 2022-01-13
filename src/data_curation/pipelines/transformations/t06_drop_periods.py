def run(df, docs, periods_to_delete):
    """
    deletes the grades from the periods selected to delete
    the columns will be deleted if they start by "class{period_to_delete}P"
    or ends with "_{period_to_delete}P"

    :param df:
    :param periods_to_delete: list of integers with the periods, example: [1, 2]
    :return:
    """
    for doc in docs:
        doc.start(f"t06 - Drop periods {periods_to_delete}", df)

    columns_to_delete = []

    prefixes = [f"class{x}P" for x in periods_to_delete]
    sufixes = [f"_{x}P" for x in periods_to_delete]

    # check for all columns
    for column in list(df.columns):

        # if matches prefix or sufix
        if column.startswith(tuple(prefixes)) or column.endswith(tuple(sufixes)):
            columns_to_delete.append(column)

    # drop
    df.drop(columns_to_delete, axis=1, inplace=True)

    for doc in docs:
        doc.end(df)

    return df
