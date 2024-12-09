import smtplib ,ssl
import imghdr
from email.message import EmailMessage

host="smtp.gmail.com"
port=465
context=ssl.create_default_context()

#Enter your own email , recommend using gmail's app password
username=""
password=""

#Enter the receiver email you want to send
receiver=""
context=ssl.create_default_context()

def send_email(image_path):
    email_message=EmailMessage()
    email_message["Subject"]="Alert"
    email_message.set_content("Hey, something had shown up on screen!!!")

    with open(image_path, "rb" ) as file:
        content=file.read()

    email_message.add_attachment(content,maintype="image", subtype=imghdr.what(None,content))

    gmail=smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)

    gmail.ehlo()
    gmail.starttls
    gmail.login(user=username, password=password)
    gmail.sendmail(username,username, email_message.as_string())
    gmail.quit()