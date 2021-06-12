from __future__ import print_function
import pickle
import os.path
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build

from credentials import get_credentials

class GmailClient:

    def __init__(self, creds):
        self._service = build('gmail', 'v1', credentials=creds)

    def send(self, subject, body, recipients):
        email_output = body
        message = MIMEMultipart()
        message.attach(MIMEText(email_output, "html"))
        message['to'] = recipients
        message['from'] = base64.urlsafe_b64encode("ben.bradford80@gmail.com")
        message['subject'] = subject
        raw_message = {'raw': base64.urlsafe_b64encode(message.as_string())}
        return self._service.users().messages().send(userId='me', body=raw_message).execute()
