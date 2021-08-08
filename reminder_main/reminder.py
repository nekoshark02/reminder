from flask import Flask
import datetime,calendar

time_n = datetime.datetime.now()

time = Flask(__name__)
@time.route("/")
def today_time_now():
    n = time_n.strftime('%Y/%m/%d')
    return n

@time.route("/calendar/")
def calendar_today():
    year_t = int(time_n.year)
    month_t = int(time_n.month)
    calendar_t = calendar(year_t,month_t)
    return calendar_t

if __name__ == "__main__":
    time.run()


