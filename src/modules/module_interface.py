class ModuleInterface:

  def __init__(self, name, notifier, config):
    self.name = name
    self.notifier = notifier
    self.config = config

  def execute(self):
    pass