import json

def get_minimize_data(jsonData):
  return json.dumps(jsonData, separators=(',', ':'))
