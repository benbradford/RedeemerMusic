from credentials import get_credentials

from googleapiclient.discovery import build

sheets_id = '1J7iIDUqKHqj5FyCaRZIAUnaRLN3uiffc50GwHpCKZJY'
songs_id = '1tkKaiOsae9eNxUOSawa_e_OfAfnzNPhwZBmcXTp_-qU'

class SheetsClient:

    def __init__(self, creds):
        self._service = build('sheets', 'v4', credentials=creds)
        self._sheets = self._service.spreadsheets()
        self._headings = self._get_headings()

    def list_song_names(self):
        songs = []
        result = self._sheets.values().get(spreadsheetId=songs_id,
                                        range='A2:A').execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
        else:
            for row in values:
                songs.append(row[0])
        return songs

    def get_service(self, service_id):
        services = self.get_services()
        for service in services:
            if service['id'] == service_id:
                return service
        return None

    def get_services(self):
        result = self._sheets.values().get(spreadsheetId=sheets_id,
                                range='A2:O').execute()
        values = result.get('values', [])

        services = []
        if not values:
            print('No data found.')
        else:
            for row in values:
                service = {}
                for j in range(0, len(self._headings)):
                    try:
                        service[self._headings[j]] = row[j]
                    except:
                        pass
                services.append(service)

        return services

    def add_service(self, service):
        row_number = str(len(self._sheets.values().get(
            spreadsheetId=sheets_id,
            range='A1:O')
        .execute().get('values', [])) + 1)
        r = 'A' + row_number + ':O' + row_number
        print("Adding range " + r)
        rows = []

        row = []
        for j in range(0, len(self._headings)):
            self._add_to_row(row, service,self._headings[j])
        rows.append(row)

        self._sheets.values().append(
            spreadsheetId=sheets_id,
            range=r,
            body={
                "majorDimension": "ROWS",
                "values": rows
            },
            valueInputOption = 'USER_ENTERED'
        ).execute()

    def _add_to_row(self, row, service, key):
        if key in service:
            row.append(service[key])
        else:
            row.append('')

    def _get_headings(self):
        headings = []
        result = self._sheets.values().get(spreadsheetId=sheets_id,
                                range='A1:O1').execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
        else:
            for heading in values[0]:
                headings.append(heading)
        return headings
