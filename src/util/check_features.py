
def check_features(df, features):
    print("Columns to create:\n")
    for x in features:
        if not x in list(df.columns):
            print(x)

    print("\nColumns to delete:\n")
    for x in list(df.columns):
        if not x in features:
            print(x)

