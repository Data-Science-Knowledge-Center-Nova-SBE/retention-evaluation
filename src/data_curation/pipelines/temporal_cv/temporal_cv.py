import more_itertools


def temporal_cv(dataset_beginning=1998, dataset_end=2019, prediction_window=1, train_history=6, test_history=1):
    """
    Returns lists of tuples, one list for each of training, training labels, testing, and testing labels,
    and one tuple for each fold. All possible folds within the user requirements are created.

        Parameters:
                dataset_beginning (int): The start of the data to be considered, in years
                dataset_end (int): The end of the data to be considered, in years
                prediction_window (int): The lenght of the prediction the user intends
                train_history (int): The number of years to be considered for training
                test_history (int): The number of years to be considered for testing

        Returns:
                train_folds (list): The list of tuples with the years contained in each of the folds for training
                train_label_folds (list): The list of tuples with the years contained in each of the folds for training
                labels
                test_folds (list): The list of tuples with the years contained in each of the folds for testing
                test_label_folds (list): The list of tuples with the years contained in each of the folds for testing
                labels
    """

    if prediction_window not in (4, 2, 1):
        print('The prediction window is not valid. Please select 4, 2, or 1 years.')
        return

    # calculated
    gap = prediction_window - 1

    # Train folds - years
    tr_range = range(dataset_beginning, dataset_end - test_history - gap - test_history - prediction_window + 1)
    train_folds = list(more_itertools.windowed(list(tr_range), n=train_history, step=1))

    # # Train label folds - years
    # tr_label_range = range(dataset_beginning + prediction_window, dataset_end - test_history - gap - test_history + 1)
    # train_label_folds = list(more_itertools.windowed(list(tr_label_range), n=train_history, step=1))

    # Test folds - years
    te_range = range(dataset_beginning + train_history + prediction_window, dataset_end - test_history - gap + 1)
    test_folds = list(more_itertools.windowed(list(te_range), n=test_history, step=1))

    # # Test label folds - years
    # te_label_range = range(dataset_beginning + train_history + prediction_window + prediction_window, dataset_end + 1)
    # test_label_folds = list(more_itertools.windowed(list(te_label_range), n=test_history, step=1))

    return train_folds, test_folds
