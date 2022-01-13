import db
from src.modeling.model_manager.files import download_file
from src.modeling.reporting.feature_importance import display_importances

def get_column(column, id):
    query = f"SELECT {column} FROM model_manager WHERE id = {id}"
    data = db.execute(query).fetchone()[0]
    return data


def get_y_test(id):
    column = get_column("y_test_filename", id)
    return download_file(column)

def get_extra_features_test(id):
    column = get_column("extra_features_test_filename", id)
    return download_file(column)

def get_y_pred(id):
    column = get_column("y_pred_filename", id)
    return download_file(column)


def get_model(id):
    column = get_column("model_filename", id)
    return download_file(column)


def show_feature_importance(id):
    feature_importance = get_column("feature_importance", id)
    tuples = []
    for x in feature_importance.replace(" ","")[2:-2].split("),("):
        x = x.split(",")
        x[0]=float(x[0])
        tuples.append(tuple(x))
    display_importances(tuples)
