# Breachify
A Telegram Bot that notifies you about your server security and breaches.

The bot can send you notifications, when somebody login into your server, a mail report and much more.

## Installation
```bash
# SSH
git clone git@github.com:Tandashi/Breachify.git

# HTTPS
git clone https://github.com/Tandashi/Breachify.git
```

```bash
cd Breachify
pip3 install -r requirements.txt
```

Now you can create the configuration as follows:
```bash
cp sample.config.json config.json
```
And change the API Token and Chat Id. To get your API Token create a new Telegram. A Guide how to do that can be found [here](https://core.telegram.org/bots).
To find out your Chat Id you can use the [userinfobot](https://telegram.me/userinfobot).


After that you start the bot as followes:
```bash
python3 src/bot.py
```
### Cron
You might want to run the bot when your server starts. To do so you can simply create a crontab entry. This could look something likes this but might very depending on your sever setup:
```bash
crontab -e
```

And add the following:
```bash
@reboot cd /path/to/breachify; python3 src/bot.py
```

## Configure Modules

### Schedules

## Create new Modules

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Feature request
To create a feature request head over here and create a new issue as follows:
- Label it with feature-request pray
- Explain the feature

## License
[GNU General Public License v3.0](https://choosealicense.com/licenses/lgpl-3.0/)
