from datetime import datetime

import requests

import environment
from modeling.predict import get_date_data, encode_lota_name
from modeling.src.modeling.models import random_forest_regressor


def get_data():
    endpoint = "/history"
    response = requests.get(environment.API_URL + endpoint)
    return response.json()


def get_header():
    return [
        "kg_sum_(t-7)",
        "kg_sum_(t-6)",
        "kg_sum_(t-5)",
        "kg_sum_(t-4)",
        "kg_sum_(t-3)",
        "kg_sum_(t-2)",
        "kg_sum_(t-1)",
        "nome_lota_encode",
        "week",
        "weekday",
        "day",
        "month_sin",
        "month_cos"
    ]


def get_lota_rows(lota, data):
    x_rows = []
    y_rows = []

    keys = list(data.keys())

    # for each day
    for i, date in enumerate(data):
        # ensure t-7 and t+10
        if i < 7 or i > len(data) - 10:
            continue

        x_row = []
        y_row = []

        # add previous days
        for j in range(7, 0, -1):
            kg = data[keys[i - j]]["kg"]
            x_row.append(kg)

        # add next days
        for j in range(11):
            kg = data[keys[i + j]]["kg"]
            y_row.append(kg)

        # add lota
        x_row.append(encode_lota_name(lota))

        # add date
        date = datetime.strptime(date, "%Y-%m-%d")
        x_row.extend(get_date_data(date))

        # save rows
        x_rows.append(x_row)
        y_rows.append(y_row)

    return x_rows, y_rows


def data_to_rows(data):
    x = []
    y = []

    for lota in data:
        x_rows, y_rows = get_lota_rows(lota, data[lota])
        x.extend(x_rows)
        y.extend(y_rows)

    return x, y


def train():
    print("get data")
    data = get_data()
    print("process data")
    x, y = data_to_rows(data)
    print("train data")
    random_forest_regressor.train(x, y)
    print("end")
