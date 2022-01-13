import glob

from modeling.setup import set_models


def change_models_to_default():
  # delete all inside /modeling/train
  import os
  files = glob.glob('./models/*')
  for f in files:
    os.remove(f)

  set_models()

  return
