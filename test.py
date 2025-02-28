from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta
app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://test:test@cluster0.bdt4998.mongodb.net/<database-name>?retryWrites=true&w=majority&appName=Cluster0")
db = client["jan23"]

@app.route('/')
def index():
    return render_template('home_page.html')

@app.route('/submit-data', methods=['POST'])
def submit_data():
    # Get the data from the POST request
    data = request.json
    selected_date = (data.get('date')).split("-")
    date = selected_date[2]+selected_date[1]+selected_date[0][2:4]
    print(date)    
    # Make a request to MongoDB to retrieve data for the selected date and tractor
    collection = db["test5"]

    cursor = collection.find({'date':int(date)})

    retrieved_data = []
    for document in cursor:
        try :
            if document["head"] <360.0:
                
                retrieved_data.append({
                'latitude': document["latitude"],
                'longitude': document["longitude"],
                'speed': document["speed"],
                'heading': document["head"],
                'timestamp':document["time"],
                'timestamph':document["time"]
                })
        except KeyError:
            retrieved_data.append({
                'latitude': document["latitude"],
                'longitude': document["longitude"],
                'speed': document["speed"],
                'timestamp':document["time"]
            })        
    print("done",len(retrieved_data))
    # Return the retrieved data as a JSON response
    return jsonify(retrieved_data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port =3000, threaded = True)
