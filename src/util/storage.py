import json

class Storage:
  def write_config(self, config):
    json_dump = json.dumps(config, sort_keys=True, indent=4)
  
    with open('config.json', 'w') as f:
      f.write(json_dump)

  def load_config(self):
    with open('config.json', 'r') as f:
      content = f.read()
      return json.loads(content)

  def update_module_config(self, module_config, config):
    new_modules_config = []
    for module in config['modules']:
      if module['name'] == module_config['name']:
        new_modules_config.append(module_config)
      else:
        new_modules_config.append(module)

    config['modules'] = new_modules_config
    self.write_config(config)