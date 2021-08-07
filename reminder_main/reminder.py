from flask import Flask
import calendar

app = Flask(__name__)
@app.route('/')
def calendar_month():
    calendars = calendar.month()
    return calendars

    if __name__ == "__main__":
        app.run()


