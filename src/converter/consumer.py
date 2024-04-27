import pika, sys, os, time
from pymongo import MongoClient
import gridfs
from convert import to_mp3


def main():
    # Get access to the MongoDB to access the dbs for videos and mp3s
    client = MongoClient("mongo", 27017)
    db_videos = client.videos
    db_mp3s = client.mp3s
    # Access the videos and mp3s using gridfs
    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)

    # Configure rabbitmq connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()


    def callback(ch, method, properties, body):
        """Executed whenever a message is consumed from the queue. Convert the video to mp3."""
        err = to_mp3.start(body, fs_videos, fs_mp3s, ch)
        # Return an error if there is a failure to process a video, do not remove video from queue
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        # Acknowledge if a video was successfully processed
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    # Consume videos from the queue
    channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"), on_message_callback=callback
    )

    print("Waiting for messages. To exit press CTRL+C")

    channel.start_consuming()

if __name__ == "__main__":
    # Allow the program to be interrupted by a keyboard interrupt
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)