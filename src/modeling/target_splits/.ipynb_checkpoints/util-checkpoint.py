import numpy as np
import matplotlib.pyplot as plt


def visualize_array(x_array, y_array):
    print("{:14s} {}".format("Rows:", x_array.shape[0]))
    print("{:14s} {}".format("Train columns:", x_array.shape[1]))

    if len(y_array.shape) == 1:
        n_columns = 1
    else:
        n_columns = y_array.shape[1]

    print("{:14s} {}".format("Test columns:", n_columns))
    target_distribution(y_array)


def target_distribution(array):
    labels, values = np.unique(array, return_counts=True)
    total = values.sum()

    # prints
    print("Target:")
    for i, label in enumerate(labels):
        print("{} - {}%".format(label, round(values[i] / total * 100, 2)))

    # bar chart
    plt.bar(labels, values)
    plt.title("Target Distribution")
    plt.show()
