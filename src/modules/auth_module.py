import subprocess
from modules.module_interface import ModuleInterface

class AuthModule(ModuleInterface):

  def __init__(self, notifier, config, data):
    super().__init__('Auth Module', notifier, config, data)

  def execute(self):
    last_log_entry = self.data.get('last_log_entry', None)

    info = subprocess.run(
      "cat /var/log/auth.log | " + " | ".join(self.config.get("filter", ['echo'])),
      shell=True,
      stdout=subprocess.PIPE
    )
    lines = info.stdout.decode('utf-8').split("\n")
    lines = list(filter(lambda x: x != "", lines))

    message = ""

    found_last_entry = False
    for line in lines:
      if last_log_entry is None:
        found_last_entry = True
        last_log_entry = line

      if last_log_entry == line and found_last_entry is False:
        found_last_entry = True
        last_log_entry = line
        continue

      if found_last_entry:
        last_log_entry = line
        message += line + "\n"

    if not found_last_entry and len(lines) > 0:
      message = '\n'.join(lines)
      last_log_entry = lines[-1]

    if message:
      self.notifier.send_message(self, message)

    self.data['last_log_entry'] = last_log_entry
    self.notifier.update_module_data(self.data)