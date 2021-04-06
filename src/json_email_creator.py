import json
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_service import EmailService

def _hyperlink(value, song):
    if value in song:
        return ' <a href="{}">[{}]</a> '.format(song[value], value)
    return ''

def _expand_song_html(song):
    print song
    return '<li>{} - {}{}{}</li>'.format(song['name'], \
    _hyperlink('lyrics', song), \
    _hyperlink('chords', song), \
    _hyperlink('lead', song))

def _find_song(song_id, songs):
    for song in songs:
        if song['id'] == song_id:
            return song
    return None

def _make_html_song_list(service):
    songs = open('../res/songs.json', "r").read()
    songs = json.loads(songs)
    songs = songs['songList']
    output = ''
    for song_id in service['songs']:
        output = output + _expand_song_html(_find_song(song_id, songs)) + '\n'
    return output

def _expand_member_html(service, member):
    lead_str = ''
    if service['lead'] == member['name']:
        lead_str = ' (Lead)'
    return '<li>{} - {}{}</li>'.format(member['instrument'], member['name'], lead_str)

def _find_member(member_id, members):
    for member in members:
        if member['id'] == member_id:
            return member
    return None

def _make_html_members_list(service):
    members = open('../res/members.json', "r").read()
    members = json.loads(members)
    members = members['members']
    output = ''
    for member_id in service['band']:
        member = _find_member(member_id, members)
        output += _expand_member_html(service, member) + '\n'
    return output

def _get_extra_message(service):
    if 'extra' in service:
        return service['extra']
    return ""

def _create_html_message(service):
    html_template = open('../res/email_template.html', "r").read()
    html_song_list = _make_html_song_list(service)
    html_member_list = _make_html_members_list(service)
    return html_template\
        .replace('_SONGS_', html_song_list) \
        .replace('_DATE_', service['date'])\
        .replace('_MEMBERS_', html_member_list)\
        .replace('_EXTRA_', _get_extra_message(service))

def get_email_preview(service):
    email_output = _create_html_message(service)
    print email_output
    return email_output

def send_group_email(service, recipients):
    email_output = _create_html_message(service)
    email_from_file = '../res/email_from.txt'
    email_from = base64.urlsafe_b64encode(open(email_from_file, "r").read())
    message = MIMEMultipart()
    message.attach(MIMEText(email_output, "html"))
    message['to'] = recipients
    message['from'] = email_from
    message['subject'] = 'Redeemer Music for {}'.format(service['date'])
    raw_message = {'raw': base64.urlsafe_b64encode(message.as_string())}
    print message
    return EmailService().send(raw_message)
