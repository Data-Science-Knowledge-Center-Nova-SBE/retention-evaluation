from .splits import s01_by_ano_letivo
from src.data_curation.pipelines import transformations
from .. import dataset_manager
from ...documentation.transformations_doc import TransformationsDoc


def run_train(df, docs, drop_first_ohe=False):
    df = transformations.t03_transform_lingua_materna.run(df, docs)
    df = transformations.t04_one_hot_encode.run(df, docs, "anoEscMae", drop_first_ohe)
    #df = transformations.t09_calc_average_nuclear.run(df, [docs])
    df = transformations.t04_one_hot_encode.run(df, docs, "nacionalidade")
    #df = transformations.t06_drop_periods.run(df, docs, [1, 2])

    drop_columns = [
        "negative_class_ratio_nuclear_externa",
        "nProcesso_agrupamento",
        "distrito",
        "concelho",
        "anoLetivo",
        "turma",
        "rFinal",
        "estado",
        "dataNascimento",
        "abandono",
        "nProcesso",
        "transferencia"
    ]
    df = transformations.t01_drop_columns.run(df, docs, drop_columns)
    df = transformations.t05_drop_null.run(df, docs)

    columns_to_int = [
        "escalao",
        "nee",
    ]
    df = transformations.t07_data_type_to_int.run(df, docs, columns_to_int)

    return df


def run_test(df, docs, drop_first_ohe=False):
    return run_train(df, docs, drop_first_ohe)


def run_for_all_rows(df, docs):

    df = transformations.t10_columns_to_lowercase.run(df, docs)
    df = transformations.t11_unique_id.run(df, docs)
    df = transformations.t12_nee.run(df, docs)
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

    return df


def run(dataframe, ano_letivo_split="2017/2018", save=True, drop_first_ohe=False):
    # clone dataframe to preserve the old one
    df = dataframe.copy()

    # init documentation
    description = f"Split until (inclusive) ano letivo {ano_letivo_split}"
    docs_train = TransformationsDoc(description)
    docs_test = TransformationsDoc(description, display=False, is_train=False)
    docs = [docs_train, docs_test]

    # run transformations for all dataset
    df = run_for_all_rows(df, docs)

    # split into train and test
    df_train, df_test = s01_by_ano_letivo.split_train_test(df, docs, ano_letivo_split)

    # apply pipeline
    # to train
    print("Train")
    df_train = run_train(df_train, [docs_train], drop_first_ohe)

    # to test
    print("\nTest")
    df_test = run_test(df_test, [docs_test], drop_first_ohe)

    # save to the database
    if save:
        dataset_manager.save("pipeline 1 - train", df_train, docs_train, train='1')
        dataset_manager.save("pipeline 1 - test", df_test, docs_test, train = '0')

    return df_train, docs_train.save(), df_test, docs_test.save()
