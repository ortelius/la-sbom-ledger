import json

def get_minimize_data(jsonData):
  sorted_by_key = get_sorted(jsonData)
  return json.dumps(sorted_by_key, separators=(',', ':'))


def get_sorted(dictionaryOrList):

  if(isinstance(dictionaryOrList, dict)):
    return get_sorted_object(dictionaryOrList)
  elif(isinstance(dictionaryOrList, list)):
    collector = []
    for element in dictionaryOrList:
      collector.append(get_sorted_object(element))
    return collector
  
  return dictionaryOrList
    
    
def get_sorted_object(dictionary):
  for key in dictionary:
    if(isinstance(dictionary[key], list) and dictionary[key].__len__() != 0 and isinstance(dictionary[key][0], dict)):
      collector = []
      for element in dictionary[key]:
        collector.append(get_sorted(element))
    
      dictionary[key] = collector

    elif(isinstance(dictionary[key], list) and dictionary[key].__len__() != 0 and isinstance(dictionary[key][0], str)):
      dictionary[key].sort()

    elif(isinstance(dictionary[key], list) and dictionary[key].__len__() != 0 and isinstance(dictionary[key][0], int)):
      dictionary[key].sort()

    elif(isinstance(dictionary[key], list) and dictionary[key].__len__() != 0 and isinstance(dictionary[key][0], float)):
      dictionary[key].sort()

    elif(isinstance(dictionary[key], dict)):
      dictionary[key] = get_sorted(dictionary[key])
    
  return sort_dict_by_key(dictionary)

def sort_dict_by_key(dictionary):
  sorted_keys = sorted(dictionary.keys())
  return {key:dictionary[key] for key in sorted_keys}
