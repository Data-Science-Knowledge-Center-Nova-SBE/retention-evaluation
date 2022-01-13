import pandas as pd
from src.modeling.shap_manager.meta import get_meta


def view_all():
    return get_meta()


def get_docs(id):
    df = get_meta()
    docs = df[df["id"] == id]["docs"].iloc[0]
    df = pd.read_json(docs)
    return df
