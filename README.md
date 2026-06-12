test
# Discord Bot

## Setup
Install Python 3.11+, create `.env`, add DISCORD_TOKEN.

```
pip install -r requirements.txt
python bot.py
```

## Render
Create a worker service, add DISCORD_TOKEN environment variable, deploy with render.yaml.

## Dashboard
Run:
```
python dashboard/app.py
```
Open localhost.

## Reload / Restart
- Use `?reload` to reload all cogs.
- Use `?reload general` to reload only one cog.
- Use `?restart` to restart the bot process.

The bot also watches `cogs/*.py` and automatically reloads a cog when its file changes.

## Troubleshooting
Check logs/bot.log, verify token permissions and intents.
