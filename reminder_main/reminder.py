from flask import Flask, render_template,request
import datetime


time_n = datetime.datetime.now()

remind = Flask(__name__)

@remind.route("/")
def reminder_mainpage():
    return render_template('reminder.html')
@remind.route("/ivent",methods=['GET','POST'])
def reminder_ivent():
    try:
        if request.method == 'GET':
            return request.args.get('query','')
        elif request.method == 'POST':
            return request.form['query']
        else:
            return 400
    except Exception as e:
        return str(e)
    
if __name__ == "__main__":
    remind.run()


