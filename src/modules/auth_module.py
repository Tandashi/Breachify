import subprocess
from modules.module_interface import ModuleInterface

class AuthModule(ModuleInterface):

  def __init__(self, notifier, config, data):
    super().__init__('Auth Module', notifier, config, data)

  def execute(self):
    # Get the last log entry that was stored
    last_log_entry = self.data.get('last_log_entry', None)

    # Get the auth log
    info = subprocess.run(
      "cat /var/log/auth.log | " + " | ".join(self.config.get("filter", ['echo'])),
      shell=True,
      stdout=subprocess.PIPE
    )
    # Get lines from stdout and filter all empty once
    lines = info.stdout.decode('utf-8').split("\n")
    lines = list(filter(lambda x: x != "", lines))

    # Holds the message that should be sent
    message = ""
    # Holds if the last logentry was found
    found_last_entry = False
    # Go through all lines
    for line in lines:
      # If the last log entry is None we found the
      # last entry and set it acordingly
      if last_log_entry is None:
        found_last_entry = True
        last_log_entry = line
      # If the last_logentry wasn't found and it matches the
      # current line. Set the last entry acordingly and continue
      if last_log_entry == line and found_last_entry is False:
        found_last_entry = True
        last_log_entry = line
        continue
      # if we have found the last entry append to the
      # message and set the line to the last log entry
      if found_last_entry:
        last_log_entry = line
        message += line + "\n"

    # if we haven't found the last log entry in the output
    # we just use the last line as new last log entry and send out all the
    # log. This is because we might have generated more new entries
    # then we output
    if not found_last_entry and len(lines) > 0:
      message = '\n'.join(lines)
      last_log_entry = lines[-1]

    # If there is a message to send. Send it!
    if message:
      self.notifier.send_message(self, message)

    # Store the last log entry in the data and 
    # then store the data
    self.data['last_log_entry'] = last_log_entry
    self.notifier.update_module_data(self.data)