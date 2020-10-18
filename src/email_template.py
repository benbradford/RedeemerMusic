from song_item import SongItem
from member import Member
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

class EmailTemplate:
    def __init__(self, date, song_items, members, lead):
        self._template = open("../res/email_template.txt", "r").read()
        self._html = open('../res/email_template.html', "r").read()
        song_list = self._make_song_list(song_items)
        member_list  = self._make_members_list(members, lead)
        html_song_list = self._make_html_song_list(song_items)
        html_member_list = self._make_html_members_list(members, lead)
        self._template = self._template.replace('_SONGS_', song_list).replace('_DATE_', date).replace('_MEMBERS_', member_list)
        self._html = self._html.replace('_SONGS_', html_song_list).replace('_DATE_', date).replace('_MEMBERS_', html_member_list)

    def create_message(self, date):
        message = MIMEMultipart()
        message['to'] = open('../res/email_recipients.txt', "r").read()
        message['from'] = open('../res/email_from.txt', "r").read()
        message['subject'] = 'Redeemer Music for ' + date
        message.attach(MIMEText(self._template, "plain"))
        message.attach(MIMEText(self._html, "html"))
        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def _make_song_list(self, song_items):
        n = 1
        song_list = ''
        for item in song_items:
            song_list = song_list + str(n) + '. ' + item.expand() + '\n'
            n = n + 1
        return song_list

    def _make_members_list(self, members, lead):
        member_list = ''
        for member in members:
            member_list = member_list + member.expand(lead) + '\n'
        return member_list

    def _make_html_song_list(self, song_items):
        song_list = ''
        for item in song_items:
            song_list = song_list + item.expand_html() + '\n'
        return song_list

    def _make_html_members_list(self, members, lead):
        member_list = ''
        for member in members:
            member_list = member_list + member.expand_html(lead) + '\n'
        return member_list
