#import important libraries
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
import datetime
import pytz
from Prediction import predict_category




app = Flask(__name__)
#configure database file
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///file.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(session_options={"autoflush": False})
db.init_app(app)
app.app_context().push()






#create class for database table
class Data(db.Model):
    __tablename__ = 'Data'
    ID = db.Column(db.Integer, primary_key = True, autoincrement=True)
    URL = db.Column(db.String)
    Category = db.Column(db.String)
    Access = db.Column(db.DateTime, default=datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata')))
    
    





#route the request according to URL and method
@app.route("/", methods=["GET","POST"])
def home_page():
    if request.method == "GET":
        #renders home page
        return render_template("HomePage.html")

    if request.method == "POST" :
        #get the URL from form
        input_url = request.form['URL']
        try:
            #scrap and predict category based on received URL
            category = predict_category(input_url)
            if category:
                #set time zone
                time_zone = pytz.timezone('Asia/Kolkata')
                #create current date time object
                time_object = datetime.datetime.now(time_zone)
                #convert date time object into string for formating
                time_string = time_object.strftime("%d-%m-%Y %H:%M:%S")
                #create Data object for injecting in database
                data_add = Data(Category = category ,URL = str(input_url),Access=datetime.datetime.strptime(time_string, '%d-%m-%Y %H:%M:%S').replace(microsecond=0))
                #add data object to database
                db.session.add(data_add)
                #commit Changes
                db.session.commit()

            #renders prediction page along with variable category
            return render_template("Prediction.html",category=category)
        except:
            #renders invalidUrl page if url entered cannot be entertained
            return render_template("InvalidURL.html")
        
#route to history
@app.route("/history", methods=["GET"])
def history():
        #extract all data from database
        query_string = "select * from Data"
        datas = db.engine.execute(query_string)
        History_List= []
        for data in datas:
            History_List.append(data)
        #renders history age with data provided from database in form of list
        return render_template("History.html", datas = History_List)



#route to delete having id (integer) of data which is to be deleted 
@app.route("/delete/<int:id>", methods=["GET"])
def delete(id):
        #query particular data ehich is to be deleted by filtering with ID
        data = Data.query.filter_by(ID = id).first()
        #check wether data is available
        if data != None:
            #delete data
            db.session.delete(data)
            #commit changes
            db.session.commit()
            #redirect to history
            return redirect("/history")
        else:
            #if data is not found than render badrequest page, it can happen is user manually enter wrong id
            return render_template("BadRequest.html")




if __name__ == '__main__':
  app.run(debug=False,host='0.0.0.0',port='5000')
