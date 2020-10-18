from email_service import EmailService
from song_item import SongItem
from song_items import SongItems
from email_template import EmailTemplate
from member import Member
from members import Members

def labels():
        service = EmailService()._service

        # Call the Gmail API
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
        else:
            print('Labels:')
            for label in labels:
                print(label['name'])

def main():

    song_items = SongItems('../res/songs.json')
    members = Members('../res/members.json')

    item1 = song_items.get_by_id('To God Be The Glory Simple')
    item2 = song_items.get_by_id('There is a redeemer C')

    member1 = members.get_by_id('BenB_Guitar_Vox')
    member2 = members.get_by_id('Emma_Vox')

    date = 'Sunday 18th October'

    template = EmailTemplate(date, [item1, item2], [member1, member2], 'Ben B')
    message = template.create_message(date)

    print(EmailService().send(message))

if __name__ == '__main__':
    main()
