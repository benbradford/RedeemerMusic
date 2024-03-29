from googleapiclient.discovery import build

sheet_ids = {
    'services': '1J7iIDUqKHqj5FyCaRZIAUnaRLN3uiffc50GwHpCKZJY',
    'songs': '1tkKaiOsae9eNxUOSawa_e_OfAfnzNPhwZBmcXTp_-qU'
}


class SheetsClient:

    def __init__(self, credentials):
        self._service = build('sheets', 'v4', credentials=credentials)
        self._sheets = self._service.spreadsheets()
        self._last_column = 'Q'
        self._service_headings = self._get_service_headings()

    def list_song_names(self):
        songs = []
        result = self._sheets.values().get(spreadsheetId=sheet_ids['songs'],
                                           range='A2:' + self._last_column).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
        else:
            for row in values:
                songs.append(row[0])
        return songs

    def get_service(self, service_id):
        services = self._get_services
        for service in services:
            if service['id'] == service_id:
                return service
        return None

    def _get_services(self):
        print("Getting Services")
        result = self._sheets.values().get(spreadsheetId=sheet_ids['services'],
                                           range='A2:' + self._last_column).execute()
        values = result.get('values', [])

        services = []
        if not values:
            print('No data found.')
        else:
            for row in values:
                service = {}
                for j in range(0, len(self._service_headings)):
                    service[self._service_headings[j]] = row[j] # recently removed an except here
                services.append(service)
        return services

    def add_song(self, name, ccli):
        res = self._sheets.values().get(spreadsheetId=sheet_ids['songs'], range='A2:A').execute()
        row_number = str(len(res) + 1)
        add_range = 'A' + row_number + ':' + row_number
        self._sheets.values().append(
            spreadsheetId=sheet_ids['songs'],
            range=add_range,
            body={
                "majorDimension": "ROWS",
                "values": [[name, ccli]]
            },
            valueInputOption='USER_ENTERED'
        ).execute()

    def update_song(self, old_song_name, song_name, ccli):
        row_number = self._find_row_with_song_matching_name(old_song_name)
        update_range = 'A' + row_number + ':' + row_number

        self._sheets.values().update(
            spreadsheetId=sheet_ids['songs'],
            range=update_range,
            body={
                "majorDimension": "ROWS",
                "values": [[song_name, ccli]]
            },
            valueInputOption='USER_ENTERED'
        ).execute()

    def add_service(self, service):
        res = self._get_next_row_and_id()
        row_number = res[0]
        service['id'] = res[1]
        add_range = 'A' + row_number + ':B' + row_number
        row = self._create_row_for_service(service)

        self._sheets.values().append(
            spreadsheetId=sheet_ids['services'],
            range=add_range,
            body={
                "majorDimension": "ROWS",
                "values": [row]
            },
            valueInputOption='USER_ENTERED'
        ).execute()

    def update_service(self, service):
        row_number = str(service['id'] - 3)
        query_range = 'A' + row_number + ':' + row_number
        row = self._create_row_for_service(service)
        self._sheets.values().update(
            spreadsheetId=sheet_ids['services'],
            range=query_range,
            body={
                "majorDimension": "ROWS",
                "values": [row]
            },
            valueInputOption='USER_ENTERED'
        ).execute()

    def _create_row_for_service(self, service):
        row = []
        for j in range(0, len(self._service_headings)):
            row.append(self._add_to_row(service, self._service_headings[j]))
        return row

    def _get_next_row_and_id(self):
        res = self._sheets.values().get(spreadsheetId=sheet_ids['services'], range='A2:A').execute()
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

    def _find_row_with_song_matching_name(self, name):
        res = self._sheets.values().get(spreadsheetId=sheet_ids['songs'], range='A2:A').execute()
        current_ids = res.get('values', [])
        for i in range(len(current_ids)):
            if current_ids[i][0] == name:
                return str(i + 2)
        print("Error - cannot find song with name " + str(name))
        raise Exception("Cannot find existing service")

    def _get_service_headings(self):
        headings = []
        result = self._sheets.values().get(spreadsheetId=sheet_ids['services'],
                                           range='A1:' + self._last_column + '1').execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
        else:
            for heading in values[0]:
                headings.append(heading)
        return headings
