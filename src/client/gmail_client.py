import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from googleapiclient.discovery import build

from credentials import get_credentials

class GmailClient:

    def __init__(self, creds):
        self._service = build('gmail', 'v1', credentials=creds)

    def send(self, subject, body, recipients, from_address):
        message = self._create_message(subject, body, recipients, from_address)
        raw_message = {'raw': base64.urlsafe_b64encode(message.as_string())}
        return self._service.users().messages().send(userId='me', body=raw_message).execute()

    def send_attachment(self, subject, body, recipients, from_address, filename_to_attach):
        message = self._create_message(subject, body, recipients, from_address)
        with open(filename_to_attach, "rb") as file:
            part = MIMEApplication( file.read(), Name=filename_to_attach)
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="' + filename_to_attach
            message.attach(part)
        raw_message = {'raw': base64.urlsafe_b64encode(message.as_string())}
        return self._service.users().messages().send(userId='me', body=raw_message).execute()

    def _create_message(self, subject, body, recipients, from_address):
        email_output = body
        message = MIMEMultipart()
        message.attach(MIMEText(email_output, "html"))
        message['to'] = recipients
        message['from'] = base64.urlsafe_b64encode(from_address)
        message['subject'] = subject
        return message
