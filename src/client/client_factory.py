from sheets_client import SheetsClient
from gmail_client import GmailClient
from drive_client import DriveClient
from credentials import get_credentials


class ClientFactory:
    def __init__(self):
        self._credentials = get_credentials()
        self._drive_client = None
        self._sheets_client = None
        self._gmail_client = None

    def get_drive_client(self):
        if self._drive_client is None:
            self._drive_client = DriveClient(self._credentials)
        return self._drive_client

    def get_sheets_client(self):
        if self._sheets_client is None:
            self._sheets_client = SheetsClient(self._credentials)
        return self._sheets_client

    def get_gmail_client(self):
        if self._gmail_client is None:
            self._gmail_client = GmailClient(self._credentials)
        return self._gmail_client


client_factory = ClientFactory()


def get_client_factory():
    return client_factory
