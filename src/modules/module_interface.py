class ModuleInterface:

  def __init__(self, name, notifier, config, data={}):
    self.name = name
    self.notifier = notifier
    self.config = config
    self.data = data

    self.data['name'] = self.config['name']

  def execute(self):
    pass