from sklearn.model_selection import RandomizedSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz

import pydotplus
import collections
import multiprocessing

from src.util.timer import Timer


def _save_tree_graph(model, feature_names):
    dot_data = export_graphviz(model,
                               feature_names=feature_names,
                               out_file=None,
                               filled=True,
                               rounded=True)

    graph = pydotplus.graph_from_dot_data(dot_data)

    colors = ('turquoise', 'orange')
    edges = collections.defaultdict(list)

    for edge in graph.get_edge_list():
        edges[edge.get_source()].append(int(edge.get_destination()))

    for edge in edges:
        edges[edge].sort()
        for i in range(2):
            dest = graph.get_node(str(edges[edge][i]))[0]
            dest.set_fillcolor(colors[i])

    # save
    graph.write_png('model_decision_tree.png')


def find_best_model():
    # set number of jobs goven the n cpus
    n_cpus = multiprocessing.cpu_count()
    n_jobs = max(1, int(n_cpus / 3))

    # set model
    model = DecisionTreeRegressor(random_state=0)

    # set hyper parameters
    param_dist = {
        'max_depth': [x for x in range(30)],
        'max_leaf_nodes': [x for x in range(200)]
    }

    # set ramdomized search
    n_iter = 1000
    model = RandomizedSearchCV(model,
                               n_jobs=n_jobs,
                               param_distributions=param_dist,
                               n_iter=n_iter,
                               verbose=1)

    return model


def train(x_train,
          y_train,
          max_depth=None,
          max_leaf_nodes=None,
          search=False):
    """
    :param max_depth:
    :param max_leaf_nodes:
    :return:
    """

    # set model
    if search:
        model = find_best_model()
    else:
        model = DecisionTreeClassifier(random_state=0, max_depth=max_depth, max_leaf_nodes=max_leaf_nodes)

    # train
    timer = Timer()
    model.fit(x_train, y_train)
    timer.stop()

    if search:
        print("\nBest parameters:\n")
        for param in model.best_params_:
            print("{}: {}".format(param, model.best_params_[param]))
        print()

    return model
