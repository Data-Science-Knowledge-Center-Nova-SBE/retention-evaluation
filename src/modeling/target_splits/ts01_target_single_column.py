from src.modeling.target_splits import util


def run(dataframe, show_visualization = True):
    # preserve old dataframe
    x_df = dataframe.copy()

    # set y
    y_df = x_df["target"].copy()
    y = y_df.to_numpy()

    # drop target
    x_df.drop(["target"], axis=1, inplace=True)

    # set x
    x = x_df.to_numpy()

    # set feature names
    feature_names = list(x_df.columns)

    # visualization
    if show_visualization:
        util.visualize_array(x, y)

    return x, x_df, y, y_df, feature_names
