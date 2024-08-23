'''from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from datetime import datetime, timedelta
import threading
import flask
import json
import time

app = Flask(__name__)

#connection_string = "mongodb+srv://test:test@cluster0.bdt4998.mongodb.net/<database-name>?retryWrites=true&w=majority&appName=Cluster0"
connection_string = "mongodb+srv://aarushibawejaji:test@cluster0.imgm1l7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client=MongoClient(connection_string);
db = client["tractor"]
collection = db["6065"]

def watch_changes():
    global selected_tractor, selected_duration
    pipeline = [{'$match': {'fullDocument.tractor': int(selected_tractor)}}]
    
    try:
        with collection.watch(pipeline) as stream:
            if selected_duration =='0':
                print(selected_duration)
                for change in stream:
                    if selected_duration == '1':
                        break
                    curr_data = {
                        'latitude': change["fullDocument"]["latitude"],
                        'longitude': change["fullDocument"]["longitude"],
                        'speed': change["fullDocument"]["speed"],
                        'heading': change["fullDocument"]["heading"],
                        'timestamp': str(change["fullDocument"]["timestamp"])
                    }
                    
                    print(curr_data)
                    yield f"data:{json.dumps(curr_data)}\n\n"
                    time.sleep(1)
    except Exception as e:
        print(f"Error in change stream: {e}")
        
upload_thread = threading.Thread(target=watch_changes)
upload_thread.daemon = True
upload_thread.start()
@app.route('/')
def index():
    return render_template('home_page.html')

@app.route('/submit-data', methods=['POST'])
def submit_data():
    global selected_date, selected_duration, selected_tractor
    data = request.json

    
    selected_date = data.get('date')
    selected_tractor = data.get('tractor')
    selected_duration = data.get('duration')
    print(data)
    return jsonify(data)

@app.route('/process-data', methods=['GET'])
def process():
    global selected_tractor, selected_date, selected_duration
    selected_date = datetime.strptime(selected_date, '%Y-%m-%d')
    end_date = selected_date + timedelta(days=1)
    
         
    
    if selected_duration == '1':
        cursor = collection.find({
            'tractor': int(selected_tractor),
            'timestamp': {
                '$gte': selected_date,
                '$lt': end_date
            }
        })

        retrieved_data = []
        print("here")
        print("cur", cursor)
        for document in cursor:
            print(document)
            retrieved_data.append({
                'latitude': document["latitude"],
                'longitude': document["longitude"],
                'speed': document["speed"],
                'heading': document["heading"],
                'timestamp': document["timestamp"]
            })
            
        return jsonify(retrieved_data)
    
@app.route('/process', methods=['GET'])
def curr_val():
    global selected_duration
    try:
    
        return flask.Response(watch_changes(),mimetype="text/event-stream")
    except:
        pass'''



from flask import Flask, render_template, request, jsonify, session, Response 
from pymongo import MongoClient  
from bson.json_util import dumps 
from datetime import datetime, timedelta  
import threading  
import json 
import time  
import certifi  
import flask 
import os  
# Initialize the Flask application
app = Flask(__name__)
# Set a secret key for session management
app.secret_key = os.urandom(24) 
# Connect to MongoDB using MongoClient
client = MongoClient("mongodb+srv://aarushibawejaji:test@cluster0.imgm1l7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",tlsCAFile=certifi.where())
# Select the database and collection
db = client["tractor"]
collection = db["6055"]
# Create a threading event to stop the thread if needed
stop_event = threading.Event()  
# Function to watch changes in MongoDB collection
def watch_changes():
    global selected_duration
    global selected_tractor
    # Define the change stream pipeline
    pipeline = [{'$match': {'fullDocument.tractor': int(selected_tractor)}}]  
    try:
        with collection.watch(pipeline) as stream:
            for change in stream:
                # If duration is 1, fetch data for the whole day and stop streaming
                if selected_duration == '1':  
                    break
                curr_data = {
                    'latitude': change["fullDocument"]["latitude"],
                    'longitude': change["fullDocument"]["longitude"],
                    'speed': change["fullDocument"]["speed"],
                    'heading': change["fullDocument"]["heading"],
                    'timestamp': str(change["fullDocument"]["timestamp"])
                } 
                yield f"data:{json.dumps(curr_data)}\n\n"  
                time.sleep(1)  
    except Exception as e: 
        print(f"Error in change stream: {e}")
@app.route('/') 
def index():
    return render_template('home_page.html') 
@app.route('/submit-data', methods=['POST'])  
def submit_data():
    data = request.json
    global selected_tractor
    global selected_duration
    selected_tractor = data.get('tractor')  
    selected_duration = data.get('duration')  
    # Save the data in session
    session['selected_date'] = data.get('date')
    session['selected_tractor'] = data.get('tractor')
    session['selected_duration'] = data.get('duration')
    print(f"Data submitted: {data}") 
    return jsonify(data) 

global selected_tractor
global selected_duration

upload_thread = threading.Thread(target=watch_changes)
upload_thread.daemon = True
upload_thread.start()

@app.route('/process-data', methods=['GET'])  
def process():
    # Get the data from session
    global selected_duration
    global selected_tractor
    
    selected_date = session.get('selected_date')
    selected_tractor = session.get('selected_tractor')
    selected_duration = session.get('selected_duration')

    if not selected_date or not selected_tractor or not selected_duration:
        return jsonify({'error': 'Missing data in session'}), 400  
    # Calculate the end date for the query
    end_date = datetime.strptime(selected_date, '%Y-%m-%d') + timedelta(days=1)
    if selected_duration == '1':
        # Query the collection for the selected tractor and date range
        cursor = collection.find({
            'tractor': int(selected_tractor),
            'timestamp': {
                '$gte': datetime.strptime(selected_date, '%Y-%m-%d'),
                '$lt': end_date
            }
        })
        # Initialize an empty list to store the retrieved data
        retrieved_data = []  
        for document in cursor:  
            retrieved_data.append({
                'latitude': document["latitude"],
                'longitude': document["longitude"],
                'speed': document["speed"],
                'heading': document["heading"],
                'timestamp': document["timestamp"]
            })
        # Return the retrieved data as JSON
        return jsonify(retrieved_data)  
@app.route('/process', methods=['GET'])  
def curr_val():
    global selected_duration
    global selected_tractor
    selected_tractor = session.get('selected_tractor')  
    selected_duration = session.get('selected_duration') 
    if not selected_tractor or not selected_duration:
        return jsonify({'error': 'Missing data in session'}), 400
    print(f"Processing data with duration {selected_duration}") 
    # Stream the current data
    if selected_duration == '0':
        print("Fetching current data")
        return Response(watch_changes(), mimetype="text/event-stream")  
    # Fetch data for the whole day
    else:
        if selected_duration == '1':
            print("Fetching whole day data")
            return process()  
# Run the Flask application
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, threaded=True)  
        
        

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host="0.0.0.0", port =3000, threaded = True)
