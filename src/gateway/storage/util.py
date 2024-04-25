import pika, json

def upload(f, fs, channel, access):
    """Upload the file to mongodb, then add the file to the queue to be converted in RabbitMQ"""
    # Determine if the file wa uploaded correctly 
    try:
        fid = fs.put(f)
    except Exception as err:
        print(err)
        return "internal server error", 500

    # Create information on the file that was added
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    # Put the video on the queue for rabbitMQ
    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        print(err)
        fs.delete(fid)
        return "internal server error", 500