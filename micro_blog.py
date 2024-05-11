import datetime
import os
from flask import Flask,render_template,request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app=Flask(__name__)
    client = MongoClient(os.getenv("mongoDB_URI"))
    app.db=client.microBlog
        # entries=[]  #creating a list to temp store the entries(local storage pupose)

    @app.route('/',methods=("GET", "POST"))
    def home_page():
            # print([e for e in app.db.entries.find({})])
            if request.method == "POST":
                entry_content=request.form.get("content")  # 'name=' in the input tag same as the inside the get("name")get the input content
                format_date=datetime.datetime.today().strftime("%Y-%m-%d")  # set the date formating in(year-month-day)
                # entries.append((entry_content,format_date))        #append or add the value in entries list (local storage variable)
                app.db.entries.insert_one({"content":entry_content,"date":format_date})
                
            entries_with_date = [       #create a list variable to print date as required format
                    (
                        entry["content"],
                        entry["date"],
                        datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b-%d")   #get the present date and print format %b-mon in char format
                    )
                    for entry in app.db.entries.find({})
            ]
            return render_template("index.html",entries=entries_with_date)  #print the value as entries_with_date inside value
     
    return app
