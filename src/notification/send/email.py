import smtplib, os, json
from email.message import EmailMessage


def notification(message):
    # try:
    message = json.loads(message)
    mp3_fid = message["mp3_fid"]
    # Create dummy gmail account to send the emails from
    sender_address = os.environ.get("GMAIL_ADDRESS")
    sender_password = os.environ.get("GMAIL_PASSWORD")
    # Send the message to the original user asociated with the JWT
    receiver_address = message["username"]

    # Create the message for the email
    msg = EmailMessage()
    msg.set_content(f"mp3 file_id: {mp3_fid} is now ready!")
    msg["Subject"] = "MP3 Download"
    msg["From"] = sender_address
    msg["To"] = receiver_address

    # Connect the email to a secure server to send the message
    session = smtplib.SMTP("smtp.gmail.com", 587)
    session.starttls()
    # Login to the email account to send the message
    session.login(sender_address, sender_password)
    # Send the message
    session.send_message(msg, sender_address, receiver_address)
    session.quit()
    print("Mail Sent")
    
    # except Exception as err:
    # print(err)
    # return err