import subprocess
from modules.module_interface import ModuleInterface

class MailModule(ModuleInterface):

  def __init__(self, notifier, config):
    super().__init__('Mail Module', notifier, config)

  def execute(self):
    info = subprocess.run(
      "cat /var/log/mail.log | " + self.config['pflogsumm_command'],
      shell=True,
      stdout=subprocess.PIPE
    )

    self.notifier.send_message(self, info.stdout.decode('utf-8'))