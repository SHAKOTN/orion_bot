This is a simple Slack Bot I made for me and my friends as we have a gaming slack chat.

This thing is ready to be deployed to Heroku (Procfile and requirements.txt are created and filled).

All you need to do is to specify 3 ENV_VARIABLES: 
- BOT_ID : Your slackbot ID
- REGION: EU/US
- SLACK_BOT_TOKEN : You can obtain it on web.slack.com

If you want to run it locally - just clone repo, specify ENV variables and make:
python bot/core.py
