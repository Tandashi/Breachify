import subprocess
import re
from modules.module_interface import ModuleInterface

def create_message_count_regex(type: str):
  return re.compile(r'(\d+)\s*' + type)

threshold_messages = [
  "received", "delivered", "forwarded", "deferred", "bounced",
  "rejected", "reject warnings", "held", "discarded",
  "bytes received", "bytes delivered", "senders", "sending hosts/domains",
  "recipients", "recipient hosts/domains"
]
threshold_message_regex = { re.sub(r'[\s*\/]', "_", key): create_message_count_regex(key) for key in threshold_messages }

class MailModule(ModuleInterface):
  def __init__(self, notifier, config):
    super().__init__('Mail Module', notifier, config)

  def execute(self):
    should_send_message = False

    info = subprocess.run(
      "cat /var/log/mail.log | " + self.config.get('pflogsumm_command', 'echo'),
      shell=True,
      stdout=subprocess.PIPE
    )

    info_stdout_text = info.stdout.decode('utf-8')
    thresholds: dict = self.config.get('thresholds', {})

    for threshold_key in thresholds.keys():
      if threshold_key in threshold_message_regex:
        threshold_regex = threshold_message_regex[threshold_key]
        result = threshold_regex.findall(info_stdout_text)

        if (len(result) != 1):
          self.notifier.logger.error("Could not find threshold value for %s" % threshold_key)
          continue

        result = int(result[0])
        if (result >= int(thresholds[threshold_key])):
          should_send_message = True
          self.notifier.logger.info("Message will be send because '%s' threshold was met." % threshold_key)
          break

    if (should_send_message or len(thresholds) == 0):
      self.notifier.send_message(self, info_stdout_text)
    else:
      self.notifier.logger.info("Message was not send since no threshold was met.")