import pymongo
from pymongo import MongoClient
import certifi
import time
import random
import datetime

#client = MongoClient("mongodb+srv://aarushibawejaji:test@cluster0.imgm1l7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",tlsCAFile=certifi.where())
client = MongoClient("mongodb+srv://aarushibawejaji:test@cluster0.imgm1l7.mongodb.net",tlsCAFile=certifi.where())

db = client["tractor"]
collection = db["6065"]

document_list = []
start_time=time.time()
while True:
    lat=28.2345+(random.randint(11, 100))/10000
    lng=77.4567+(random.randint(11, 100))/10000
    spd=(random.randint(100,999))/100
    head=random.randint(0,360)
    tract=60
    '''random.randint(50,60)'''
    data = {
            "tractor":tract,
            "timestamp": datetime.datetime.utcnow(),
            "latitude":lat,
            "longitude":lng,
            "speed":spd,
            "heading":head
            }
    print(data)

    collection.insert_one(data)
    print("uploaded")
    time.sleep(1)
    

