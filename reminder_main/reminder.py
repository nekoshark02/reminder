from flask import Flask,render_template
import datetime

time_n = datetime.datetime.now()

remind = Flask(__name__)

@remind.route("/")
def reminder_():
    return render_template('reminder_html')
    
if __name__ == "__main__":
    remind.run()


