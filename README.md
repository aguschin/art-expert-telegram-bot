# art-expert-telegram-bot

Deploy something like https://t.me/AIArtExpertBot

Read more about tools used:
- Python Telegram Bot https://python-telegram-bot.org

To deploy:

1. set telegram token

```sh
$ flyctl secrets set TELEGRAM_TOKEN=tokenvalue
```

2. change appname in fly.toml to your app name (will be created automatically)

3. deploy

```sh
$ flyctl deploy
```
