from song_item import SongItem
from member import Member
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailTemplate:
    def __init__(self, date, song_items, members, lead, extra):
        self._html = open('res/email_template.html', "r").read()
        html_song_list = self._make_html_song_list(song_items)
        html_member_list = self._make_html_members_list(members, lead)
        self._html = self._html\
        .replace('_SONGS_', html_song_list) \
        .replace('_DATE_', date)\
        .replace('_MEMBERS_', html_member_list)\
        .replace('_EXTRA_', extra)

    def create_message(self, date, _from, to):
        message = MIMEMultipart()
        message.attach(MIMEText(self._html, "html"))
        message['to'] = to
        message['from'] = _from
        message['subject'] = 'Redeemer Music for {}'.format(date)
        return message

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
