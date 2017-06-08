<h2>This is a simple Slack Bot I made for me and my friends as we have a gaming slack chat</h2>

This bot is ready to be deployed to Heroku (Procfile and requirements.txt are created and filled).
If you want to use celery and write your own tasks for it add to Procfile:
```bash
worker: celery worker --app=bot.celery.app
```

Available plugins right now:
- Overwatch: Statistics, hero stats etc
- Notes: Create, edit and share notes with your slackmates in channels
- Weather: Ask bot to print the weather of the city
- File storage(files): Store your files in dropbox
- SoundCloud: *coming soon*

**NOTE**: You can remove plugins from *plugins/* directory if you don't want to use them.

All you need to do is to specify 5 ENV_VARIABLES:
- BOT_ID : Your slackbot ID
- REGION : EU/US (for overwatch plugin: if you don't use it - just skip this)
- APIXU_API_KEY: Weather service token(Apixu). This is very friendly and free to use service.
Just skip this if you don't want to use weather plugin
- SLACK_BOT_TOKEN : You can obtain it on web.slack.com
- DROPBOX_TOKEN: Dropbox app token for *files* plugin
- ENV : set to *development* if you don't have redis and want to use local memory.
Set to *production* if you want to use your redis to store data from plugins
- REDIS_URL: Redis URL if you set ENV to *production*
- CELERY_ENABLED: Set value to 1 if you want to use celery and also-
- AMQP_URL: for celery too

If you want to run it locally - just clone repo, specify ENV variables and make:
```bash
python bot/core.py
```

<h1>Examples of plugins</h1>

<h2> Overwatch Plugin</h2>

![Alt text](http://i.imgur.com/IgMcsWM.png "Overwatch stats")

![Alt text](http://i.imgur.com/ZgiwDYY.png "Overwatch hero stats")

<h2> Notes plugin </h2>

![Alt text](http://i.imgur.com/jrYDjiG.png "Notes ")

![Alt text](http://i.imgur.com/jo3VpZH.png "Show note")

<h2> Storage plugin </h2>

<h3> Works good with .webm, .jpeg, .png </h3>

![Alt text](http://i.imgur.com/8IMW49n.png "Show file")


