from __future__ import print_function
import pickle
import os.path
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build

from credentials import get_credentials

class GmailService:

    def __init__(self):
        self._service = build('gmail', 'v1', credentials=get_credentials())

    def send(self):
        email_output = "<html> <body>Here is the message <B> in html </B> </body></html>"
        message = MIMEMultipart()
        message.attach(MIMEText(email_output, "html"))
        message['to'] = "ben.bradford80@gmail.com"
        message['from'] = base64.urlsafe_b64encode("ben.bradford80@gmail.com")
        message['subject'] = 'Test Email'
        raw_message = {'raw': base64.urlsafe_b64encode(message.as_string())}
        return self._service.users().messages().send(userId='me', body=raw_message).execute()
