def predict(x_test, model):
    y_pred = model.predict(x_test)
    y_pred_scores = model.predict_proba(x_test)
    return y_pred, y_pred_scores
