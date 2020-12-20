import logging
from util import storage, scheduler

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from modules.module_interface import ModuleInterface

"""
The Core Class of this project. It contains the Bot logic.
"""
class NotifyBot:

  def __init__(self):
    """
    Initialize the Bot
    """
    self._configure_logger()
        
    self.storage = storage.Storage()
    self._load_config()

    self._configure_bot()
    self._load_modules()
    self._configure_scheduler()

  def start(self):
    """
    Starts the Bot and sends out the start message
    """
    self.logger.info('Starting Notifier')
    self._send_system_message('Bip Bup. I am now running! :)')
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    self.updater.idle()

  def _load_config(self):
    """
    Loads the Bot configuration file

    On fail it will call `self._shutdown`
    """
    try:
      self.config = self.storage.load_config()
    except Exception as e:
      self.logger.error('Could not load config file: %s' % str(e))
      self._shutdown()

  def _configure_scheduler(self):
    """
    Configures the scheduler and start it.

    On fail it will call `self._shutdown`
    """
    
    try:
      self.scheduler = scheduler.Scheduler(self)
      # Start Jobs
      self.scheduler.run_continuously()
    except Exception as e:
      self.logger.error('Could not configure scheduler: %s' % str(e))
      self._shutdown()

  def _load_modules(self):
    """
    Loads the different modules and initializes them
    """

    self.modules = []

    for module_config in self.config.get('modules', []):
      try:
        names = module_config['name'].split('.')
        mod = __import__('modules.' + names[0], fromlist=names[1])
        module_class = getattr(mod, names[1])
        self.modules.append(module_class(notifier=self, config=module_config))
      except:
        self.logger.error('Could not load module: ' + module_config.get('name', 'No name provided.'))

  def _configure_bot(self):
    """
    Configure the Bot and connect to the Telegram API
    """
    
    try:
      self.updater = Updater(self.config['api_token'], use_context=True)
    except:
      self.logger.error('Could not connect to the Telegram API')
      self._shutdown()

  def _configure_logger(self):
    """
    Configure the Logger
    """
    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    self.logger = logging.getLogger(__name__)

  def _shutdown(self, _=None, __=None):
    """
    Shutdown the Bot. Will cancel all running schelduled jobs
    and sends out a shutdown message.
    """

    self.scheduler.shutdown()
    self._send_system_message('Bip Bup. Shutting down... :(')

  def _send_system_message(self, message, parse_mode=telegram.ParseMode.MARKDOWN_V2):
    """
    Sends a system message

    Keyword arguments:
    message -- the message that should be send
    parse_mode -- the mode how the message should be parsed (Default: ParseMode.MARKDOWN_V2)
    """
    self.send_message(ModuleInterface('System', self, {}), message, parse_mode=parse_mode)

  def send_message(self, module, message, part=None, of=None, parse_mode=telegram.ParseMode.MARKDOWN_V2):
    """
    Sends out a message. If the message is longer then 4000 characters
    it automatically cuts it into multiple parts.

    Keyword arguments:
    module -- the module that sends the message
    message -- the message that should be send
    part -- the part number (Default: None)
    of -- the total amount of parts. Needs to be set if part is not None (Default: None)
    parse_mode -- the mode how the message should be parsed (Default: ParseMode.MARKDOWN_V2)
    """
    
    try:
      text = None

      if (part is not None and of is None):
        raise Exception("'part' was set but 'of' wasn't.")

      # If the message doesn't need to be partitioned and isn't a part
      # we can just send it
      if len(message) <= 4000 and part is None:
        text = "*\\[{name}\\]* on *{server}*:\n```\n{message}\n```".format(
          name=module.name,
          message=message,
          server=self.config['server']
        )

      # Message is to long and wasn't partitioned beforehand
      # so we need to do it
      elif len(message) > 4000 and part is None:
        # calculate the parts
        parts = [message[i : i + 4000] for i in range(0, len(message), 4000)]

        i = 1
        for part in parts:
          # Send all the parts
          self.send_message(module, part, i, len(parts), parse_mode)
          i += 1

      elif part is not None:
        text = "*\\[{name}\\]* on *{server}* \\({part} / {of}\\):\n```\n{message}\n```".format(
          name=module.name,
          message=message,
          server=self.config['server'],
          part=part,
          of=of
        )

      if text is not None:
        # Send the message to the chat
        self.updater.bot.send_message(
          chat_id=self.config['chat_id'],
          text=text,
          parse_mode=parse_mode
        )
    except Exception as e:
      self.logger.error('Could not send message: %s' % str(e))

bot = NotifyBot()

try:
  bot.start()
except:
  bot._shutdown()

bot._shutdown()
