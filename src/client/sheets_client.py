from credentials import get_credentials

from googleapiclient.discovery import build

sheets_id = '1J7iIDUqKHqj5FyCaRZIAUnaRLN3uiffc50GwHpCKZJY'
songs_id = '1tkKaiOsae9eNxUOSawa_e_OfAfnzNPhwZBmcXTp_-qU'

class SheetsClient:

    def __init__(self, creds):
        self._service = build('sheets', 'v4', credentials=creds)
        self._sheets = self._service.spreadsheets()
        self._headings = self._get_headings()
        self._last_column = 'P'

    def list_song_names(self):
        songs = []
        result = self._sheets.values().get(spreadsheetId=songs_id,
                                        range='A2:' + self._last_column).execute()
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
                                range='A2:' + self._last_column).execute()
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
        res = self._get_next_row_and_id()
        row_number = res[0]
        service['id'] = res[1]
        range = 'A' + row_number + ':' + row_number
        row = self._create_row_for_service(service)

        self._sheets.values().append(
            spreadsheetId=sheets_id,
            range=range,
            body={
                "majorDimension": "ROWS",
                "values": [row]
            },
            valueInputOption = 'USER_ENTERED'
        ).execute()

    def update_service(self, service):
        row_number = self._find_row_matching_service(service)
        range = 'A' + row_number + ':' + row_number
        row = self._create_row_for_service(service)
        self._sheets.values().update(
            spreadsheetId=sheets_id,
            range=range,
            body={
                "majorDimension": "ROWS",
                "values": [row]
            },
            valueInputOption = 'USER_ENTERED'
        ).execute()

    def _create_row_for_service(self, service):
        row = []
        for j in range(0, len(self._headings)):
            row.append(self._add_to_row(service,self._headings[j]))
        return row

    def _get_next_row_and_id(self):
        res = self._sheets.values().get(spreadsheetId=sheets_id, range='A2:A').execute()
        current_ids = res.get('values', [])
        row_number = str(len(res) + 1)
        ids = []
        for id in current_ids:
            if id[0] != 'id':
                ids.append(int(id[0]))
        return [row_number, str(max(ids) + 1)]

    def _add_to_row(self, service, key):
        if key in service:
            return service[key]
        else:
            return ''

    def _find_row_matching_service(self, service):
        res = self._sheets.values().get(spreadsheetId=sheets_id, range='A2:A').execute()
        current_ids = res.get('values', [])
        for i in range(len(current_ids)):
            if current_ids[i][0] == service['id']:
                return str(i + 2)
        print "Error - cannot find service with id " + service['id']
        raise Exception("Cannot find existing service")

    def _get_headings(self):
        headings = []
        result = self._sheets.values().get(spreadsheetId=sheets_id,
                                range='A1:P1').execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
        else:
            for heading in values[0]:
                headings.append(heading)
        return headings
