from song_items import SongItems
from email_template import EmailTemplate
from members import Members
from email_service import EmailService
import base64
import json
import sys, getopt

all_song_items = SongItems('res/songs.json')
all_members = Members('res/members.json')

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

def main(param_filename, email_from_file, email_to_file):

    params = json.loads(open(param_filename, "r").read())

    songs = get_songs(params)
    band = get_band(params)
    date = params['date']
    lead = params['lead']
    extra = params['extra']

    template = EmailTemplate(date, songs, band, lead, extra)
    email_from = base64.urlsafe_b64encode(open(email_from_file, "r").read())
    email_to = open(email_to_file, "r").readline()[:-1]
    print('Will send to {}'.format(email_to))
    print('email body can be checked in bin/email_output.html')
    f = open("bin/email_output.html", "w")
    f.write(template._html)
    f.close()
    proceed_input = raw_input("Ok to proceed? (y/n): ")

    if proceed_input is 'y':
        message = template.create_message(date, email_from, email_to)
        raw_message = {'raw': base64.urlsafe_b64encode(message.as_string())}
        EmailService().send(raw_message)

if __name__ == '__main__':
    argv = sys.argv[1:]
    service_file = 'services/test_service.json'
    email_from_file = 'res/email_from.txt'
    email_to_file = 'res/email_recipients.txt'
    try:
        opts, args = getopt.getopt(argv, "s:f:t:",["service=","from=","to="])
    except getopt.GetoptError:
        print 'create_group_email.py -s <service_file> -f <email_from_file> -t <email_to_file>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-s', '--service'):
            service_file = arg
        elif opt in ('-f', '--from'):
            email_from_file = arg
        elif opt in ('-t', '--to'):
            email_to_file = arg
    main(service_file, email_from_file, email_to_file)
