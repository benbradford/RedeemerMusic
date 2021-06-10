import io
from operator import itemgetter

from service.service_factory import get_service_factory
sheets_service = get_service_factory().get_sheets_service()

old_services = [
        {
            "band": [
                "BenB_Guitar_Vox",
                "Emma_Vox"
            ],
            "date": "Sunday 6th February",
            "extra": "",
            "id": 17,
            "lead": "Ben B",
            "songs": [
                57,
                30,
                52,
                55,
                9,
                56
            ]
        }
    ]

songList = [

    ]

def get_song_name(id):
    for song in songList:
        if song['id'] == id:
            return song['name']
    print id
    raise Exception("cannot find song")

services = []
for old in old_services:
    service = {}
    service['id'] = old['id'] + 10
    if 'extra' in old:
        service['message'] = old['extra']
    else:
        service['message'] = ''
    service['lead'] = old['lead']
    service['date'] = old['date']
    for index in [1,2,3,4,5]:
        if index <= len(old['band']):
            service['band' + str(index)] = old['band'][index-1]
        else:
            service['band' + str(index)] = ""

    for index in [1,2,3,4,5,6]:
        if index <= len(old['songs']):
            service['song' + str(index)] = get_song_name(old['songs'][index-1])
        else:
            service['song' + str(index)] = ""

    services.append(service)

services.sort(key=itemgetter("id"))

for service in services:
    print service
    sheets_service.add_service(service)
