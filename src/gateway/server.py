import os, gridfs, pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId

server = Flask(__name__)

# Set up the mongodb servers for the video database
mongo_video = PyMongo(server, uri="mongodb://mongo:27017/videos")

# Set up the mongodb servers for the mp3 database
mongo_mp3 = PyMongo(server, uri="mongodb://mongo:27017/mp3s")

# Set up the gridfs for the video and mp3 dbs
fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

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
            err = util.upload(f, fs_videos, channel, access)
            
            if err:
                return err
        
        return "success!", 200
    else:
        return "not authorized", 401
    
@server.route("/download", methods=["GET"])
def download():
    access, err = validate.token(request)

    # Return an error if unable to validate the token
    if err:
        return err

    
    access = json.loads(access)

    if access["admin"]:
        # Attempt to get the fid
        fid_string = request.args.get("fid")

        # Handle errors with the fid not being found
        if not fid_string:
            return "fid is required", 400

        try:
            # Return the file to the client
            out = fs_mp3s.get(ObjectId(fid_string))
            return send_file(out, download_name=f"{fid_string}.mp3")
        except Exception as err:
            print(err)
            return "internal server error", 500

    # Return an error if the user is not authorized
    return "not authorized", 401

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)