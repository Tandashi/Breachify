import json

class Storage:
  def write_data(config):
    json_dump = json.dumps(config, sort_keys=True, indent=4)
  
    with open('data.json', 'w') as f:
      f.write(json_dump)

  def load_data():
    try:
      with open('data.json', 'r') as f:
        content = f.read()
        return json.loads(content)
    except:
      return {}

  def update_module_data(module_data, data):
    replaced_data = False

    new_data = []
    for module in data:
      if module['name'] == module_data['name']:
        new_data.append(module_data)
        replaced_data = True
      else:
        new_data.append(module)

    # If we haven't replaced the data then we need to
    # create the entry because it didn't exist yet
    if (replaced_data == False):
      new_data.append(module_data)

    data = new_data
    Storage.write_data(new_data)