# URLTopic Prediction Web Application
Predict Topic based on URL entered

# APP Structure
App is divided into 4 parts
*  app.py
*  Sqlite database file
*  Templates
*  prediction.py
*  BBC_News_Train.csv

# Details
*Sqlite database file* is used for storing data. <br> 
*prediction.py* helps in scraping URL content and predicting category through ML Classifiction algorithm. <br>
*Templates* is used for storing html pages. <br>
*BBC_News_Train.csv* is open source data used to train ML classification Model.<br>
*app.py* is where application logic resides, it is used for querying data, handling request & rendering html templates.

# Run Application
First of all install all packages with particular version mentioned in *requirment.txt* file <br>
To do that go to cmd prompt, move to directory where files are saved then run *pip install -r requirements.txt* command <br>
After successfully excecuting, run *python app.py* command and wait for server to start. <br>
Copy URL provided by server and run in chrome browser. <br>
__Explore the webapp now!__
