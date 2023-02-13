import json

def get_minimize_data(jsonData):
  sorted_by_key = get_sorted(jsonData)
  print(sorted_by_key)
  return json.dumps(sorted_by_key, separators=(',', ':'))


def sort_dict_by_key(dictionary):
  sorted_keys = sorted(dictionary.keys())
  return {key:dictionary[key] for key in sorted_keys}

def get_sorted(dictionaryOrList):
  for key in dictionaryOrList:
    if(isinstance(dictionaryOrList[key], list) and dictionaryOrList[key].__len__() != 0 and isinstance(dictionaryOrList[key][0], dict)):
      collector = []
      for element in dictionaryOrList[key]:
        collector.append(get_sorted(element))
    
      dictionaryOrList[key] = collector

    elif(isinstance(dictionaryOrList[key], list) and dictionaryOrList[key].__len__() != 0 and isinstance(dictionaryOrList[key][0], str)):
      dictionaryOrList[key].sort()

    elif(isinstance(dictionaryOrList[key], list) and dictionaryOrList[key].__len__() != 0 and isinstance(dictionaryOrList[key][0], int)):
      dictionaryOrList[key].sort()

    elif(isinstance(dictionaryOrList[key], dict)):
      dictionaryOrList[key] = get_sorted(dictionaryOrList[key])
    
  return sort_dict_by_key(dictionaryOrList)

    
