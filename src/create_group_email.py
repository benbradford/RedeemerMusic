from song_item import SongItem
from song_items import SongItems
from email_template import EmailTemplate
from member import Member
from members import Members
from email_service import EmailService
import base64
import json

from email.mime.text import MIMEText

all_song_items = SongItems('../res/songs.json')
all_members = Members('../res/members.json')

def get_songs(params):
    songs = []
    for song in params['songs']:
        songs.append(all_song_items.get_by_id(song))
    return songs

def get_band(params):
    band = []
    for member in params['band']:
        band.append(all_members.get_by_id(member))
    return band

def main(param_filename):

    params = json.loads(open(param_filename, "r").read())

    songs = get_songs(params)
    band = get_band(params)
    date = params['date']
    lead = params['lead']
    extra = params['extra']

    template = EmailTemplate(date, songs, band, lead, extra)
    email_from = base64.urlsafe_b64encode(open('../res/email_from.txt', "r").read())
    email_to = open('../res/email_from.txt', "r").readline()[:-1]
    message = template.create_message(date, email_from, email_to)

    raw_message = {'raw': base64.urlsafe_b64encode(message.as_string())}
    EmailService().send(raw_message)

if __name__ == '__main__':
    main('../res/email_param_template.json')
