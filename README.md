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
cp sample.config.yaml config.yaml
```

And change the API Token and Chat Id. To get your API Token create a new Telegram Bot. A Guide how to do that can be found [here](https://core.telegram.org/bots).
To find out your Chat Id you can use the [userinfobot](https://telegram.me/userinfobot).

Now start the chat with the bot once so the chat is created and the bot can find it via the id.

After that all that's left is to start the bot:

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

### Systemd

Create a `breachify.service` file in `/etc/systemd/system` that looks something like this:

```ini
[Unit]
Description=Breachify Notification Bot
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=root
WorkingDirectory=/path/to/Breachify/dir
ExecStart=/usr/bin/env python3 src/bot.py

[Install]
WantedBy=multi-user.target
```

And make sure to enable it if you want to start on boot:  
`systemctl enable breachify`

## Configure Modules

To configure the different modules of the bot simple add them to the `modules` array in the configuration file.

You can find examples for each module in the `sample.config.yaml`

### Schedules

For scheduling breachify uses the [schedule](https://pypi.org/project/schedule/) python library.
To schedule a module run all you have to do is add the property or method name as key and the method value as the keys value. If you want to use a properties like `monday` simply set the value to `null`.
So if you want to run a module every Monday at `10:12 am` you would create it like this:

```yaml
schedule:
  monday: null
  at: '10:12'
```

or if you want to run a module every 10 minutes you would do it like this:

```yaml
schedule:
  minutes: null
  every: 10
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Feature request

To create a feature request head over here and create a new issue as follows:

- Label it with feature-request pray
- Explain the feature

## License

[GNU General Public License v3.0](https://choosealicense.com/licenses/lgpl-3.0/)
