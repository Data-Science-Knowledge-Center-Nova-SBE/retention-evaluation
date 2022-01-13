import pandas as pd


def json_to_dataframe(data):
    new_data = {}

    for i, column in enumerate(data[0]):
        array = [x[i] for x in data[1:]]
        new_data[column] = array

    df = pd.DataFrame(new_data)

    return df
