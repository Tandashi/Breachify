import logging
from util import storage, scheduler

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

class NotifyBot:

  def __init__(self):
    self._configure_logger()
        
    self.storage = storage.Storage()
    self._load_config()

    self._configure_bot()
    self._load_modules()
    self._configure_scheduler()

  def start(self):
    self.logger.info('Starting Notifier')
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    self.updater.idle()

  def _load_config(self):
    try:
      self.config = self.storage.load_config()
    except Exception as e:
      self.logger.error('Could not load config file: %s' % str(e))
      exit(1)

  def _configure_scheduler(self):
    try:
      self.scheduler = scheduler.Scheduler(self)
      # Start Jobs
      self.scheduler.run_continuously()
    except Exception as e:
      self.logger.error('Could not configure scheduler: %s' % str(e))
      exit(1)

  def _load_modules(self):
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
    try:
      self.updater = Updater(self.config['api_token'], use_context=True, user_sig_handler=self._shutdown)
    except:
      self.logger.error('Could not connect to the Telegram API')
      exit(1)

  def _configure_logger(self):
    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    self.logger = logging.getLogger(__name__)

  def _shutdown(self, _, __):
    self.scheduler.shutdown()

  def send_message(self, module, message, part=None, of=None):
    try:
      if len(message) <= 4000 and part is None:
        text = "*\\[{name}\\]* on *{server}*:\n```{message}```".format(
          name=module.name,
          message=message,
          server=self.config['server']
        )

        self.updater.bot.send_message(
          chat_id=self.config['chat_id'],
          text=text,
          parse_mode=telegram.ParseMode.MARKDOWN_V2
        )

      elif len(message) > 4000 and part is None:
        parts = [message[i : i + 4000] for i in range(0, len(message), 4000)]

        i = 1
        for part in parts:
          self.send_message(module, part, i, len(parts))
          i += 1

      elif part is not None:
        text = "*\\[{name}\\]* on *{server}* \\({part} / {of}\\):\n```{message}```".format(
          name=module.name,
          message=message,
          server=self.config['server'],
          part=part,
          of=of
        )
        self.updater.bot.send_message(
          chat_id=self.config['chat_id'],
          text=text,
          parse_mode=telegram.ParseMode.MARKDOWN_V2
        )
    except Exception as e:
      self.logger.error('Could not send message: %s' % str(e))

bot = NotifyBot()
bot.start()
