import os
import smtplib
import datetime
import pandas as pd
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


attactment = f'output_{datetime.datetime.now().strftime("%Y-%m-%d")}.xlsx'


def sendEmail():
    sender_email = '<email>' #have to match with the password, the real email
    sender_password = '<app-password>' #generated from https://myaccount.google.com/apppasswords
    recipient_email = '<sender-email>'
    subject = 'Hello from Python'
    body = 'This is an email that generated and sent by a Python script!'

    with open(attactment, 'rb') as attachment:
        # Add the attachment to the message
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename= {os.path.basename(attactment)}',
    )

    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email
    html_part = MIMEText(body)
    message.attach(html_part)
    message.attach(part)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, message.as_string())
    server.quit()

def generateExcel():
    # Create some sample data
    data = {'Name': ['Alice', 'Bob', 'Charlie', 'David'],
            'Age': [25, 32, 18, 47],
            'Gender': ['F', 'M', 'M', 'M'],
            'Salary': [50000, 75000, 40000, 90000]}

    # Convert the data into a Pandas DataFrame
    df = pd.DataFrame(data)

    # Create a new Excel file and write the DataFrame to it
    with pd.ExcelWriter(attactment) as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')


generateExcel()
sendEmail()
os.remove(attactment)
