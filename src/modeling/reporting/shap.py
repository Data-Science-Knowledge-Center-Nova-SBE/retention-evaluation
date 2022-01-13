import pandas as pd
import numpy as np
import shap
from src import dataset_manager
from src import model_manager
from src.modeling import feature_selection
from src.modeling import target_splits
from src.modeling import shap_manager




def shap_run(model_id, save=False):
    """
    Outputs a dataframe with the top 5 variables with most impact for both possible predictions.

    Parameters:
    model_id (int): ID of the model to be used
    save (bool): Whether the output table is to be saved to the database
    """

    # get model-dataset correspondence
    df_model = model_manager.view_all()
    df_dataset = dataset_manager.view_all()

    df_dataset = df_dataset.rename(columns={'id': 'dataset_id', 'docs': 'dataset_docs', 'datetime': 'dataset_datetime'})
    df_model = df_model.rename(columns={'docs': 'model_docs'})

    df_dataset['dataset_years'] = 0

    for ds_id in df_dataset['dataset_id'].unique():
        year_start = df_dataset[df_dataset['dataset_id'] == ds_id].dataset_docs.values[0].find('(') + 1
        year_end = df_dataset[df_dataset['dataset_id'] == ds_id].dataset_docs.values[0].find(')')

        df_dataset['dataset_years'][df_dataset['dataset_id'] == ds_id] = \
        df_dataset[df_dataset['dataset_id'] == ds_id].dataset_docs.values[0][year_start:year_end].replace(',', '')

    df_test = df_dataset[df_dataset['train'] == '0']
    df_train = df_dataset[df_dataset['train'] == '1']

    df_test = df_test.rename(columns={'dataset_id': 'test_dataset_id',
                                      'n_rows': 'test_nrows',
                                      'null_percentage': 'test_nullperc',
                                      'table_name': 'test_table_name',
                                      'dataset_years': 'test_years',
                                      'dataset_docs': 'test_dataset_docs'
                                      })

    df_merged = pd.merge(df_model, df_train[
        ['dataset_id', 'table_name', 'n_rows', 'cv_group', 'fold', 'dataset_years', 'dataset_datetime',
         'dataset_docs']], how='inner', on=['dataset_id'])
    df_results = pd.merge(df_merged, df_test[
        ['test_dataset_id', 'test_nrows', 'test_nullperc', 'test_table_name', 'test_years', 'cv_group', 'fold',
         'test_dataset_docs']], how='inner', on=['cv_group', 'fold'])

    # get model
    df_model_selected = df_results[df_results['id'] == model_id]
    model = model_manager.get_model(model_id)

    # get test df corresponding to model ID
    df_test = dataset_manager.load_dataset_by_id(int(df_model_selected['test_dataset_id']))

    # feature selection
    df_test, extra_features_test = feature_selection.fs00_drop_pipeline1_columns.run(df_test)
    df_test, extra_features_test = feature_selection.fs02_drop_agrupamento.run(df_test)

    # target split
    x_test, x_test_df, y_test, y_test_df, _ = target_splits.ts01_target_single_column.run(df_test,
                                                                                          show_visualization=False)

    # get shap values for all observations
    explainer = shap.TreeExplainer(model)
    all_shap_values = explainer.shap_values(x_test_df)  # cane take some time to run, depending on dataset length

    # create df with all shap values, variables, and students for pred=0
    df0 = pd.DataFrame(data=None, columns=x_test_df.columns)
    dic0 = {}

    for student in all_shap_values[0]:

        for shap_value, variable in zip(student, x_test_df.columns):
            d = {variable: shap_value}
            dic0.update(d)

        df0 = df0.append(dic0, ignore_index=True)

    # create df with all shap values, variables, and students for pred=1
    df1 = pd.DataFrame(data=None, columns=x_test_df.columns)
    dic1 = {}

    for student in all_shap_values[1]:

        for shap_value, variable in zip(student, x_test_df.columns):
            d = {variable: shap_value}
            dic1.update(d)

        df1 = df1.append(dic1, ignore_index=True)

    # create df with top 5 variables for pred=0
    temp_df = pd.DataFrame(df0).T

    top5_df_0 = pd.DataFrame(np.zeros((0, 5)),
                             columns=['top1_non_failure', 'top2_non_failure', 'top3_non_failure', 'top4_non_failure',
                                      'top5_non_failure'])

    for i in temp_df.columns:
        df1row = pd.DataFrame(temp_df.nlargest(5, i).index.tolist(),
                              index=['top1_non_failure', 'top2_non_failure', 'top3_non_failure', 'top4_non_failure',
                                     'top5_non_failure']).T
        top5_df_0 = pd.concat([top5_df_0, df1row], axis=0)

    # create df with top 5 variables for pred=1
    temp_df = pd.DataFrame(df1).T

    top5_df_1 = pd.DataFrame(np.zeros((0, 5)),
                             columns=['top1_failure', 'top2_failure', 'top3_failure', 'top4_failure', 'top5_failure'])

    for i in temp_df.columns:
        df1row = pd.DataFrame(temp_df.nlargest(5, i).index.tolist(),
                              index=['top1_failure', 'top2_failure', 'top3_failure', 'top4_failure', 'top5_failure']).T
        top5_df_1 = pd.concat([top5_df_1, df1row], axis=0)

    # concatenating the two dataframes into one
    df = pd.concat([top5_df_0.reset_index(drop=True), top5_df_1.reset_index(drop=True)], axis=1)

    # save df to database if save=True
    if save:
        shap_manager.save(df)

    return df
