from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
import datetime
import pytz
from Prediction import predict_category




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///file.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(session_options={"autoflush": False})
db.init_app(app)
app.app_context().push()







class Data(db.Model):
    __tablename__ = 'Data'
    ID = db.Column(db.Integer, primary_key = True, autoincrement=True)
    URL = db.Column(db.String)
    Category = db.Column(db.String)
    Access = db.Column(db.DateTime, default=datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata')))
    
    






@app.route("/", methods=["GET","POST"])
def home_page():
    if request.method == "GET":
        return render_template("HomePage.html")

    if request.method == "POST" :
        input_url = request.form['URL']
        try:
            category = predict_category(input_url)
            if category:
                tz = pytz.timezone('Asia/Kolkata')
                timea = datetime.datetime.now(tz)
                times = timea.strftime("%d-%m-%Y %H:%M:%S")
                data_add = Data(Category = category ,URL = str(input_url),Access=datetime.datetime.strptime(times, '%d-%m-%Y %H:%M:%S').replace(microsecond=0))
                db.session.add(data_add)
                db.session.commit()

            
            return render_template("Prediction.html",category=category)
        except:
            return render_template("InvalidURL.html")
        

@app.route("/history", methods=["GET"])
def history():
    
        query_string = "select * from Data"
        datas = db.engine.execute(query_string)
        History_List= []
        for data in datas:
            History_List.append(data)
        return render_template("History.html", datas = History_List)




@app.route("/delete/<id>", methods=["GET"])
def delete(id):
        data = Data.query.filter_by(ID = id).first()
        db.session.delete(data)
        db.session.commit()
        return redirect("/history")




if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0')