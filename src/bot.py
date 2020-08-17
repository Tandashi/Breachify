import logging
from util import storage, scheduler

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

class NotifyBot:

  def __init__(self):
    self._configure_logger()
        
    self.storage = storage.Storage()
    self.config = self.storage.load_config()

    self._configure_bot()
    self._load_modules()
    self._configure_scheduler()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    self.updater.idle()

  def _configure_scheduler(self):
    self.scheduler = scheduler.Scheduler(self.modules)
    # Start Jobs
    self.scheduler.run_continuously()

  def _load_modules(self):
    self.modules = []

    for module_config in self.config['modules']:
      names = module_config['name'].split('.')
      mod = __import__('modules.' + names[0], fromlist=names[1])
      module_class = getattr(mod, names[1])
      self.modules.append(module_class(notifier=self, config=module_config))

  def _configure_bot(self):
    self.updater = Updater(self.config['api_token'], use_context=True, user_sig_handler=self._shutdown)

  def _configure_logger(self):
    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    self.logger = logging.getLogger(__name__)

  def _shutdown(self, _, __):
    self.scheduler.shutdown()

  def send_message(self, module, message, part=None, of=None):
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


bot = NotifyBot()
