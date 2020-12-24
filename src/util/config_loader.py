import yaml

class ConfigLoader:
  def load_config():
    """
    Load the configuration from the config.yaml

    returns: The parsed content of the config.yaml as dict
    """
    with open('config.yaml', 'r') as f:
      return yaml.load(f, Loader=yaml.FullLoader)