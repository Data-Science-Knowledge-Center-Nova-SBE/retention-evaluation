from src.modeling import model_manager
from src.modeling.reporting.percentage_at_k import calc_percentage_at_k
from matplotlib import pyplot as plt
import statistics

def get_schools(model_id):
    schools_test = model_manager.get_extra_features_test(model_id)["agrupamento"]
    schools = {}
    for school in schools_test:
        if not school in schools:
            schools[school] = ([], [])

    return schools, schools_test


def visualize(model_id, k):
    schools, schools_test = get_schools(model_id)

    # get y_test and y_pred
    y_test = model_manager.get_y_test(model_id)
    y_pred = model_manager.get_y_pred(model_id)

    # group by school
    for i, row in enumerate(y_test):
        school = schools_test[i]
        schools[school][0].append(y_test[i])
        schools[school][1].append(y_pred[i])

    # calc percentage at k
    schools_data = []
    for school in schools:
        positive_target_percentage = round((sum(schools[school][0]) / len(schools[school][0]))*100,2)
        school_value = (school, calc_percentage_at_k(schools[school][0], schools[school][1], k), len(schools[school][1]),positive_target_percentage)
        schools_data.append(school_value)

    # sort by value
    schools_data.sort(key=lambda x:x[1])

    # plot distribution
    schools_distribution(schools_data)

    # print mean and std
    numbers = [x[1] for x in schools_data]
    mean = round(sum(numbers)/len(numbers),2)
    std = round(statistics.stdev(numbers),2)

    print(f"Mean: {mean}")
    print(f"Standard Deviation: {std}")

    # list schools
    print("\n{:6s} | {:6s} | {:17s} | {}".format("School", "% at k","% Target Positive", "Observations"))
    print("-"*50)
    for x,y,w,z in schools_data:
        print("{:6s} | {:6s} | {:17s} | {}".format(x, str(y), str(z), w))


def schools_distribution(schools_data):
    fig, ax = plt.subplots(figsize=(12, 7))
    x = [t[0] for t in schools_data]
    y = [t[1] for t in schools_data]
    ax.bar(x, y)
    plt.show()
