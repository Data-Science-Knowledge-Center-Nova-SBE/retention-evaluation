from src.data_curation.pipelines import pipeline_2, pipeline_8grade_1, pipeline_6grade_1
from src.modeling.feature_selection import fs00_drop_pipeline1_columns, fs02_drop_agrupamento

from modeling.features import FEATURES_9_GRADE, FEATURES_8_GRADE, FEATURES_6_GRADE
import pandas as pd



def add_one_hot_encoding(df):
    ohe = [
        'anoEscMae__basic_2nd',
        'anoEscMae__basic_3rd',
        'anoEscMae__college',
        'anoEscMae__none',
        'anoEscMae__secondary',
        'anoEscMae__unknown',
        'nacionalidade__brazil',
        'nacionalidade__european',
        'nacionalidade__other',
        'nacionalidade__palop',
        'nacionalidade__portuguese',
        'distrito_agrup__aveiro',
        'distrito_agrup__braga',
        'distrito_agrup__bragança',
        'distrito_agrup__castelo branco',
        'distrito_agrup__coimbra',
        'distrito_agrup__faro',
        'distrito_agrup__leiria',
        'distrito_agrup__portalegre',
        'distrito_agrup__porto',
        'distrito_agrup__santarém',
        'distrito_agrup__viseu'
    ]

    columns = list(df.columns)
    for feature in ohe:
        if not feature in columns:
            df[feature] = 0

    return df


def get_features(df, features):
    new_df = pd.DataFrame()
    columns = list(df.columns)
    for feature in features:
        if feature in columns:
            new_df[feature] = df[feature]

    return new_df


def transform_data_9_grade(df):
    df = pipeline_2.run_production(df)
    df = add_one_hot_encoding(df)
    df, _ = fs00_drop_pipeline1_columns.run(df)
    df = get_features(df, FEATURES_9_GRADE)
    return df

def transform_data_8_grade(df):
    df = pipeline_8grade_1.run_production(df)
    df = add_one_hot_encoding(df)
    df, _ = fs00_drop_pipeline1_columns.run(df)
    df = get_features(df, FEATURES_8_GRADE)
    return df


def transform_data_6_grade(df):
    df = pipeline_6grade_1.run_production(df)
    df = add_one_hot_encoding(df)
    df, _ = fs00_drop_pipeline1_columns.run(df)
    df = get_features(df, FEATURES_6_GRADE)
    return df

