


def calc_percentage_at_k(test, pred, k):
    # sort scores, ascending
    pred, test = zip(*sorted(zip(pred, test)))
    pred, test = list(pred), list(test)
    pred.reverse()
    test.reverse()

    # calculates number of values to consider
    n_percentage = round(len(pred) * k / 100)

    # check if predicted is equal to true value, and count it
    # set true and false positive counters
    tp, fp = 0, 0
    for i in range(n_percentage):
        # true positive
        if test[i] == 1:
            tp += 1

    precision_at_k = tp / n_percentage
    return round(precision_at_k * 100, 2)