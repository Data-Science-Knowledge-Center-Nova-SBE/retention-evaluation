import db
from src.data_curation.pipelines.transformations import t10_columns_to_lowercase, t11_unique_id, t15_ano_letivo


def run(df, docs):
    for doc in docs:
        doc.start("t20 - r final 10 adjustments", df)

    # This function checks whether there are any records of students in the 10th grade, whose rFinal in the 9th grade, in the previous school year, is 0
    alunos_avaliados_10ano = db.get_dataframe("alunos_avaliados_10ano")
    alunos_avaliados_10ano = t10_columns_to_lowercase.run(alunos_avaliados_10ano, [])

    # Applies all the necessary transformations to the newly imported table
    alunos_avaliados_10ano = t11_unique_id.run(alunos_avaliados_10ano, [])
    alunos_avaliados_10ano.sort_values(by=['anoLetivo'],
                                       inplace=True)  # Para garntir que, caso o aluno apareça duas vezes na tabela, o ano letivo mais antigo apareça primeiro
    alunos_avaliados_10ano = t15_ano_letivo.run(alunos_avaliados_10ano, [])

    # List to store ids of rows that need to be changed
    ids = []

    # Possible rows that migth be changed (we are only interested in rows of 9th grade, rFinal of 0 and students with information regarding the 10th year)
    sample = df[
        df['nProcesso_agrupamento'].isin(alunos_avaliados_10ano['nProcesso_agrupamento'].unique())]
    sample = sample[sample['ano'] == '9']
    sample = sample[sample['rFinal'] == '0']

    # Checks which students, in the school year prior to being in the 10th grade, were in the 9th grade
    for i in alunos_avaliados_10ano['nProcesso_agrupamento'].unique():
        years = alunos_avaliados_10ano['anoLetivo'][alunos_avaliados_10ano['nProcesso_agrupamento'] == i]
        if not years.values.any():
            continue

        year_1 =years.values[0][0:4]
        year_2 = years.values[0][5:]

        study_year = str(int(year_1)-1) + '/' + str(int(year_2)-1)

        if len(sample[(sample['nProcesso_agrupamento'] == i) &
                      (sample['anoLetivo'] == study_year) &
                      (sample['ano'] == '9') &
                      (sample['rFinal'] == '0')]) != 0:
            ids.append(list(sample[(sample['nProcesso_agrupamento'] == i) &
                                   (sample['anoLetivo'] == study_year) &
                                   (sample['ano'] == '9') &
                                   (sample['rFinal'] == '0')].index)[0])

    # Updates the rFinal of the respective rows to a "Pass" (2)
    df['rFinal'].loc[ids] = '2'

    for doc in docs:
        doc.end(df)

    return df
