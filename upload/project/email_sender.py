import sys
import smtplib
import imghdr
from email.message import EmailMessage
from image_handle import IMAGE_FILE_NAME

EMAIL_ADDRESS = 'pi.sm.drawing@gmail.com'
EMAIL_PASSWORD = 'PiRaSpBeRrY'


if __name__ == "__main__":
    destination = sys.argv[1]
    msg = EmailMessage()
    msg['Subject'] = 'Pi drawing'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = destination
    msg.set_content('This is a drawing made with pi!')
    
    with open(IMAGE_FILE_NAME, 'rb') as img:
        img_data = img.read()
        img_type = imghdr.what(img.name)
        img_name = img.name

    msg.add_attachment(img_data, maintype='image', subtype=img_type, filename=img_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
