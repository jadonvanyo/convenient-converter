import os, gridfs, pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://mongo:27017/videos"

mongo = PyMongo(server)

fs = gridfs.GridFS(mongo.db)

# Communicate with RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()
# Open the rabbitmq channel if it is closed
if not channel.is_open:
    channel.open()


@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    # Return the token if no error is found
    if not err:
        return token
    # Return the error if an error is found
    else:
        return err
    
@server.route("/upload", methods=["POST"])
def upload():
    # Validate the token to get the access or errors
    access, err = validate.token(request)
    
    # Convert the JSON string to a python object
    access = json.loads(access)
    
    # Determine if the token has admin permissions
    if access["admin"]:
        # Determine if there is one file being uploaded for conversion
        if len(request.files) > 1 or len(request.files) < 1:
            return "exactly 1 file required", 400
        
        # Loop through the key values in the request files
        for _, f in request.files.items():
            # Check if there were any errors in any of the values
            err = util.upload(f, fs, channel, access)
            
            if err:
                return err
        
        return "success!", 200
    else:
        return "not authorized", 401
    
@server.route("/download", methods=["GET"])
def download():
    pass

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)