import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor


def start(message, fs_videos, fs_mp3s, channel):
    # Load the JSON of the message
    message = json.loads(message)

    # Create an empty temp file
    tf = tempfile.NamedTemporaryFile()
    # Retrieve the video contents
    out = fs_videos.get(ObjectId(message["video_fid"]))
    # Add the video contents to the empty file
    tf.write(out.read())
    # Create audio from temp video file
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    # Close and automatically delete the temp file
    tf.close()

    # Write audio to the file
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)

    # Save file to mongo
    f = open(tf_path, "rb")
    data = f.read()
    fid = fs_mp3s.put(data)
    f.close()
    os.remove(tf_path)

    # Update the message with the new mp3 file
    message["mp3_fid"] = str(fid)

    # Attempt to create the MP3 queue
    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    # Unable to put the message on the queue
    except Exception as err:
        # Delete the mp3 from mongodb as well
        fs_mp3s.delete(fid)
        return "failed to publish message"