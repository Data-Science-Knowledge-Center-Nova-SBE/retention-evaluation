def transform_predictions(data, k):
    students = sorted(data, key=lambda x: x["score"], reverse=True)

    for i, student in enumerate(students):
        # get retention_risk
        retention_risk = i < k
        student["retention_risk"] = retention_risk

        # indicators
        indicators = student["importance"]
        indicators = [(k,v) for k, v in indicators.items()]
        indicators = sorted(indicators, key=lambda x: x[1])

        if retention_risk:
            student["indicators"] = indicators[-5:]
        else:
            student["indicators"] = indicators[:5]

    return students
