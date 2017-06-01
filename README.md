<h4>This is a simple Slack Bot I made for me and my friends as we have a gaming slack chat.</h4>

This thing is ready to be deployed to Heroku (Procfile and requirements.txt are created and filled).

Available plugins right now:
- Overwatch: Statistics, hero stats etc
- Notes: Create, edit and share notes with your slackmates in channels
- SoundCloud: *coming soon*
- File storage: *coming soon*

All you need to do is to specify 3 ENV_VARIABLES: 
- BOT_ID : Your slackbot ID
- REGION : EU/US (for overwatch plugin: if you don't use it - just skip this)
- SLACK_BOT_TOKEN : You can obtain it on web.slack.com
- ENV : set to *development* if you don't have redis and want to use local memory.
Set to *production* if you want to use your redis to store data from plugins
- REDIS_URL: Redis URL if you set ENV to *production*

If you want to run it locally - just clone repo, specify ENV variables and make:
```bash
python bot/core.py
```