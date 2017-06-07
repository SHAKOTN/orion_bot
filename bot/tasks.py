from bot.celery import app

@app.task
def hello():
    print(1+1)