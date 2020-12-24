import yaml

class ConfigLoader:
  def load_config():
    with open('config.yaml', 'r') as f:
      return yaml.load(f, Loader=yaml.FullLoader)