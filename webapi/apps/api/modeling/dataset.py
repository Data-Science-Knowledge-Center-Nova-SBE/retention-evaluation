
import requests
import numpy as np
import environment


def get_data():
  session = requests.Session()
  session.trust_env = False
  endpoint = "/history"
  response = session.get(environment.API_URL + endpoint)
  return response.json()

