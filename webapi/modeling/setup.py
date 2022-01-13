import pickle
import pathlib
import os
import shap

file_path = pathlib.Path(__file__).parent.resolve()

MODELS = []
EXPLAINERS = []


def get_moodels_path():
  models_path = os.path.join(file_path, "..", "models")
  models_dir = os.listdir(models_path)

  if not len(models_dir) >= 3:
    models_path = os.path.join(file_path, "..", "default_models")
  return models_path

def set_models():

  global MODELS
  global EXPLAINERS

  MODELS = []
  EXPLAINERS = []


  models_path = get_moodels_path()

  for file in ["model_6_grade.pkl", "model_8_grade.pkl", "model_9_grade.pkl"]:
    # get model
    with open(f"{models_path}/{file}", "rb") as f:
      model = pickle.load(f)


    MODELS.append(model)
    EXPLAINERS.append(shap.TreeExplainer(model))


