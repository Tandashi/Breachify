import subprocess
import re
from modules.module_interface import ModuleInterface

def create_message_count_regex(type: str):
  """
  Creates a regeular expression for a type in the message section of the
  pflogsumm output
  """
  return re.compile(r'(\d+)\s*' + type)

# All message types we want to allow thresholds for
threshold_messages = [
  "received", "delivered", "forwarded", "deferred", "bounced",
  "rejected", "reject warnings", "held", "discarded",
  "bytes received", "bytes delivered", "senders", "sending hosts/domains",
  "recipients", "recipient hosts/domains"
]
# Generate a dict with all available types and their regular expresions
# Key = type with / and space replaced with underscore
# Value = the regular expression for the type
threshold_message_regex = { re.sub(r'[\s*\/]', "_", key): create_message_count_regex(key) for key in threshold_messages }

class MailModule(ModuleInterface):
  def __init__(self, notifier, config, data):
    super().__init__('Mail Module', notifier, config, data)

  def execute(self):
    should_send_message = False

    # Run pflogsumm command
    info = subprocess.run(
      "cat /var/log/mail.log | " + self.config.get('pflogsumm_command', 'echo'),
      shell=True,
      stdout=subprocess.PIPE
    )

    # Get command output
    info_stdout_text = info.stdout.decode('utf-8')
    thresholds: dict = self.config.get('thresholds', {})

    # Go through the threshold keys
    for threshold_key in thresholds.keys():
      # Check if the key exists in the regexes
      if threshold_key in threshold_message_regex:
        # Get the regex
        threshold_regex = threshold_message_regex[threshold_key]
        # Run it and get the result
        result = threshold_regex.findall(info_stdout_text)

        # Check if the regex matched anything in the pflogsumm output
        if (len(result) != 1):
          self.notifier.logger.error("Could not find threshold value for %s" % threshold_key)
          continue
        
        # We found something so get it
        result = int(result[0])
        # Check if the captured result is higher than the configured threshold
        # If so we want to send a message if not just ignore it a d move on
        if (result >= int(thresholds[threshold_key])):
          should_send_message = True
          self.notifier.logger.info("Message will be send because '%s' threshold was met." % threshold_key)
          break
    
    # Check if we found a threshold that was met or if we didn't configure any
    # In either case we want to send a message
    if (should_send_message or len(thresholds) == 0):
      self.notifier.send_message(self, info_stdout_text)
    # No threshold was met
    else:
      self.notifier.logger.info("Message was not send since no threshold was met.")