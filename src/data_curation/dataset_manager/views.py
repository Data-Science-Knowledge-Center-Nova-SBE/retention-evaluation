from src.data_curation.dataset_manager import get_meta
import pandas as pd


def view_all():
    return get_meta()


def get_docs(id):
    df = get_meta()
    docs = df[df["id"] == id]["docs"].iloc[0]
    df = pd.read_json(docs)
    return df
