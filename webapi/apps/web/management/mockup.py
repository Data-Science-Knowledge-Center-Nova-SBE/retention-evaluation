import random
import pandas as pd
import json


def get_random_name():
    names = ["Miguel", "Susana", " Pedro", "Mateus", "Ângelo", "Beatriz", "Ana", " Maria", "Carlos", "José"]
    return names[random.randint(0, len(names) - 1)]


def add_random_names(data):
    for x in data:
        x["name"] = get_random_name()

    return data


def get_mockup_data(grade='9'):
    # read file
    df = pd.read_csv("mockup_data/dummy_" + grade + "grade.csv")

    # dataframe to json
    result = df.to_json(orient="values")
    result = json.loads(result)

    # add columns
    columns = list(df.columns)
    result.insert(0, columns)

    return result
