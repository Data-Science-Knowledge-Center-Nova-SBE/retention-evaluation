from .conversion import convert_var_name


def mean_shap_features(shap_features, array):
    total = 0

    for x in array:

        # ignore features that may not exist
        if not x in shap_features:
            continue

        total += shap_features[x]

    return round(total / len(array),2)


def add_mean_features(shap_features):
    names_1p_2p = [
        "Rácio de Negativas em Classificação Intermédia",
        "Rácio de Negativas em Classificação Intermédia - Disciplinas Nucleares",
        "Rácio de Negativas em Classificação Intermédia - Disciplinas Não Nucleares",
        "Classificação Intermédia - Inglês ou Língua Estrangeira",
        "Classificação Intermédia - Arte e Tecnologia",
        "Classificação Intermédia - Ciências Físicas e Naturais",
        "Classificação Intermédia - Ciências Sociais e Humanas",
        "Classificação Intermédia - Educação Física",
        "Classificação Intermédia - Inglês",
        "Classificação Intermédia - Língua Estrangeira II",
        "Classificação Intermédia - Matemática",
        "Classificação Intermédia - Português",
        "Classificação Intermédia - Outras Disciplinas"
    ]

    for name in names_1p_2p:
        name_1p = name + " 1P"
        name_2p = name + " 2P"

        # add mean of features
        shap_features[name] = mean_shap_features(shap_features, [name_1p, name_2p])

        # delete features used for calculation
        if name_1p in shap_features:
            del shap_features[name_1p]
            del shap_features[name_2p]

    return shap_features


def add_shap(columns, data, shap_values, input_data, grade="9"):

    if grade == "9":
        shap_values = shap_values[0]
    elif grade == "8":
        shap_values = shap_values
    else:
        shap_values = shap_values[0]

    for i, item in enumerate(data):
        shap_features = {}
        for j, feature in enumerate(columns):
            create, feature = convert_var_name(feature, input_data[i, j])

            if create:
                shap_features[feature] = round(shap_values[i][j] * 100, 2)

        shap_features = add_mean_features(shap_features)
        item["importance"] = shap_features

    return data


def run(explainer, data):
    shap_values = explainer.shap_values(data)
    return shap_values
