from .splits import s02_cross_validation
from src.data_curation.pipelines import transformations
from .. import dataset_manager
from ...documentation.transformations_doc import TransformationsDoc
from src.data_curation import dataset_manager


def run_train(df, docs, drop_first_ohe=False):
    df = transformations.t03_transform_lingua_materna.run(df, docs)
    df = transformations.t04_one_hot_encode.run(df, docs, "anoEscMae", drop_first_ohe)
    #df = transformations.t09_calc_average_nuclear.run(df, [docs])
    df = transformations.t04_one_hot_encode.run(df, docs, "nacionalidade")
    try:
        df = transformations.t04_one_hot_encode.run(df, docs, "distrito_agrup")
    except:
        df = df
    #df = transformations.t06_drop_periods.run(df, docs, [1, 2])

    drop_columns = [
        "negative_class_ratio_nuclear_externa",
        "nProcesso_agrupamento",
        "distrito",
        "concelho",
        #"anoLetivo",
        "turma",
        "rFinal",
        "estado",
        "dataNascimento",
        "abandono",
        #"nProcesso",
        "transferencia",
        'adapted_curric_flag',
        "nee",
        'class1P_outros',
        'class2P_outros',
        'class3P_outros',
        'class1P_ingles_ling_estr',
        'class2P_ingles_ling_estr',
        'class3P_ingles_ling_estr'
    ]
    df = transformations.t01_drop_columns.run(df, docs, drop_columns)
    df = transformations.t05_drop_null.run(df, docs)

    columns_to_int = [
        "escalao",

    ]
    df = transformations.t07_data_type_to_int.run(df, docs, columns_to_int)

    return df


def run_test(df, docs, drop_first_ohe=False):
    return run_train(df, docs, drop_first_ohe)


def run_for_all_rows(df, docs):

    df = transformations.t10_columns_to_lowercase.run(df, docs)
    df = transformations.t11_unique_id.run(df, docs)
    df = transformations.t13_genero.run(df, docs)
    df = transformations.t14_escalao.run(df, docs)
    df = transformations.t15_ano_letivo.run(df, docs)
    df = transformations.t16_data_nascimento.run(df, docs)
    df = transformations.t17_nacionalidade.run(df, docs)
    df = transformations.t18_lingua_materna.run(df, docs)
    df = transformations.t19_ano_esc_mae.run(df, docs)
    df = transformations.t20_r_final_10_adjustments.run(df, docs)
    df = transformations.t22_abandono_correction.run(df, docs)
    df = transformations.t08_target_creation_9_grade.run(df, docs)
    df = transformations.t23_ano.run(df, docs)
    df = transformations.t24_agrup_averages.run(df, docs)

    return df


def run(dataframe, dataset_beginning=1998, dataset_end=2019, prediction_window=1, train_history=5, test_history=1,
        save=True, drop_first_ohe=False, selected_cols = False):
    # clone dataframe to preserve the old one
    df = dataframe.copy()

    if selected_cols:
        df = df[selected_cols]

    # init documentation
    description = f"Temporal cross-validation for beginning in {dataset_beginning} and ending in {dataset_end}"

    docs_train = TransformationsDoc(description)
    docs_test = TransformationsDoc(description, display=False, is_train=False)
    docs = [docs_train, docs_test]

    # run transformations for all dataset
    df = run_for_all_rows(df, docs)
    df = run_train(df, docs, drop_first_ohe)

    # split into cv train and test folds
    df_full = s02_cross_validation.apply_temporal_cv(df, docs_train, dataset_beginning, dataset_end, prediction_window,
                                                     train_history, test_history)

    # save to the database
    if save:
        #Counter to "calculate" the folds
        counter = 0

        #Calculating the group
        df_prov = dataset_manager.view_all().sort_values(by='datetime', ascending=False)

        try:
            group = str(int(list(df_prov['cv_group'][df_prov['fold'].notnull()].head(1))[0]) + 1)

        except:
            group = '1'

        dataset_manager.save("pipeline 2", df, docs_train, group=group, save_duplicate=False)

        for i in df_full:
            counter += 1

            dataset_manager.save("pipeline 2", i['df_train_folds'], i['docs_train'], train="1", fold=str(counter),group=group, save_duplicate=False)
            dataset_manager.save("pipeline 2", i['df_test_folds'], i['docs_test'], train="0", fold=str(counter),group=group, save_duplicate=False)

    return df_full, df, df_full[0]['docs_train'].save(), df_full[0]['docs_test'].save()

def run_production(df):

    # transfrom all
    df = transformations.t10_columns_to_lowercase.run(df, [])
    df = transformations.t11_unique_id.run(df, [])
    df = transformations.t13_genero.run(df, [])
    df = transformations.t14_escalao.run(df, [])
    df = transformations.t15_ano_letivo.run(df, [])
    df = transformations.t16_data_nascimento.run(df, [])
    df = transformations.t17_nacionalidade.run(df, [])
    df = transformations.t18_lingua_materna.run(df, [])
    df = transformations.t19_ano_esc_mae.run(df, [])
    #df = transformations.t20_r_final_10_adjustments.run(df, [])
    #df = transformations.t22_abandono_correction.run(df, [])
    #df = transformations.t08_target_creation_9_grade.run(df, [])
    df = transformations.t23_ano.run(df, [])
    df = transformations.t24_agrup_averages.run(df, [])
    df = transformations.t03_transform_lingua_materna.run(df, [])
    df = transformations.t04_one_hot_encode.run(df, [], "anoEscMae")
    # df = transformations.t09_calc_average_nuclear.run(df, [[]])
    df = transformations.t04_one_hot_encode.run(df, [], "nacionalidade")

    try:
        df = transformations.t04_one_hot_encode.run(df, [], "distrito_agrup")
    except:
        df = df
    # df = transformations.t06_drop_periods.run(df, [], [1, 2])

    drop_columns = [
        "negative_class_ratio_nuclear_externa",
        "nProcesso_agrupamento",
        "distrito",
        "concelho",
        # "anoLetivo",
        "turma",
        "rFinal",
        "estado",
        "dataNascimento",
        "abandono",
        "nProcesso",
        "transferencia",
        'adapted_curric_flag',
        "nee",
        'class1P_outros',
        'class2P_outros',
        'class3P_outros',
        'class1P_ingles_ling_estr',
        'class2P_ingles_ling_estr',
        'class3P_ingles_ling_estr'
    ]
    df = transformations.t01_drop_columns.run(df, [], drop_columns)
    df = transformations.t05_drop_null.run(df, [])


    columns_to_int = [
        "escalao",

    ]
    #df = transformations.t07_data_type_to_int.run(df, [], columns_to_int)

    return df