import json

class Storage:
  def _write_data(data):
    """
    Writes the data to the data.json file

    Keyargs:
    data - the data to store in the data.json file
    """
    json_dump = json.dumps(data, sort_keys=True, indent=4)
  
    with open('data.json', 'w') as f:
      f.write(json_dump)

  def load_data():
    """
    Loads the data from the data.json file

    returns: The parsed content of the data.json file as dict
    """
    try:
      with open('data.json', 'r') as f:
        content = f.read()
        return json.loads(content)
    except:
      return {}

  def update_module_data(module_data, data):
    """
    Updates the module data with the given data

    Keyargs:
    module_data - the new module data
    data - the complete data to update the module_data in
    """
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
    Storage._write_data(new_data)