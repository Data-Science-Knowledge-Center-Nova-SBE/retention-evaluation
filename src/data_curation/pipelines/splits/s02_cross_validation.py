import pandas as pd
from src.data_curation.pipelines.temporal_cv.temporal_cv import temporal_cv
from src.data_curation.pipelines.pipeline_1 import TransformationsDoc
from copy import copy, deepcopy


def apply_temporal_cv(dataframe, docs, dataset_beginning=1998, dataset_end=2019, prediction_window=2, train_history=4,
                      test_history=1):
    """
    Uses the temporal_cv function to return a list of one dictionaries with training and testing folds,
    returning one dictionary per fold, therefore allowing the integration of the temporal cross validation.

        Parameters:
                ...
                ...
                dataframe: student data with the indication of the corresponding year. The year column is
                required to be called "anoLetivo" and records for that collumn to start with the format yyyy.
                prediction_window (int): The lenght of the prediction the user intends
                train_history (int): The number of years to be considered for training
                test_history (int): The number of years to be considered for testing

        Returns:
                folds (list): list of folds (dictionaries), each containing the following times: training dataframe,
                testing dataframe, list of years used for training, and list of years used for testing.
    """

    df = dataframe.copy()

    # Calling the temporal_cv function and storing the results
    train_years, test_years = temporal_cv(dataset_beginning=dataset_beginning, dataset_end=dataset_end,
                                          prediction_window=prediction_window, train_history=train_history,
                                          test_history=test_history)

    # Preparing the anoLetivo column for the operations
    df['anoLetivo'] = df['anoLetivo'].str.slice(stop=4)
    df['anoLetivo'] = pd.to_numeric(df['anoLetivo'])

    # Appending one dictionary per fold to the list of folds
    folds = []

    for train_fold, test_fold in zip(train_years, test_years):
        dict_of_df = {}

        # Adding each fold's dataframes to the dictionary
        dict_of_df['df_train_folds'] = df[df['anoLetivo'].isin(train_fold)]
        dict_of_df['df_test_folds'] = df[df['anoLetivo'].isin(test_fold)]
        # dict_of_df['df_train_label_folds'] = df[df['anoLetivo'].isin(train_label_fold)]
        # dict_of_df['df_test_label_folds'] = df[df['anoLetivo'].isin(test_label_fold)]

        # Adding the transformations to docs for train and test
        docs_train = TransformationsDoc(f'Cross-validation train {train_fold}')
        #docs_train = deepcopy(docs)
        docs_train.start('Cross-validation', dataframe)
        docs_train.end(dict_of_df['df_train_folds'])

        docs_test = TransformationsDoc(f'Cross-validation test {test_fold}')
        #docs_test = deepcopy(docs)
        docs_test.start('Cross-validation', dataframe)
        docs_test.end(dict_of_df['df_test_folds'])

        # Adding the transformations log to the dictionary
        dict_of_df['docs_train'] = docs_train
        dict_of_df['docs_test'] = docs_test

        # Adding each fold's years to the dictionary
        dict_of_df['train_years'] = train_fold
        dict_of_df['test_years'] = test_fold
        # dict_of_df['train_label_years'] = train_label_fold
        # dict_of_df['test_label_years'] = test_label_fold

        folds.append(dict_of_df)

    return folds
