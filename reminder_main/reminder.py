import calendar
from flask import Flask

app = Flask(__name__)

@app.route('/')
def calendar_month():
    calendar_month = print(calendar.month())
    return calendar_month

if __name__ == "__main__":
    app.run()


