from view_base import ViewBase

class EmailView:
    def __init__(self, songs_retriever):
        self._template = open('../res/email_template.html', "r").read()
        self._confirmation_template = open('../res/email_send_confirmation_template.html' ,"r").read()
        self._songsRetriever = songs_retriever
        self._components = ['lyrics', 'chords', 'lead']

    def render(self, service):
        return ViewBase().render(self._main_section(service)\
            .replace("_PUBLISH_BUTTON_", ""))

    def render_with_prompt(self, service, recipients):
        return self._main_section(service)\
            .replace("_PUBLISH_BUTTON_", self._confirmation_template)\
            .replace("_SERVICE_", service['id'])\
            .replace("_RECIPIENTS_", recipients)

    def _main_section(self, service):
        return self._template\
            .replace("_DATE_", service['date'])\
            .replace("_EXTRA_", self._get_message(service))\
            .replace("_SONGS_", self._get_songs(service))\
            .replace("_MEMBERS_", self._get_members(service))\

    def _get_message(self, service):
        if 'message' in service:
            return service['message']
        return ""

    def _get_songs(self, service):
        output = " "
        for index in [1,2,3,4,5, 6]:
            song_key = "song" + str(index)
            if song_key in service and service[song_key] != "":
                output = output + self._get_song(service, song_key)
        return output

    def _get_song(self, service, song_key):
        output = '<li>{} -'.format(service[song_key])
        file_ids = self._songsRetriever.get_song(service[song_key], self._components)['file_ids']
        for component in self._components:
            href = "https://drive.google.com/file/d/" + file_ids[component] + "/view?usp=sharing"
            output = output + ' <a href="{}">[{}]</a>' .format(href, component)
        output += '</li>'
        return output

    def _get_members(self, service):
        output = ""
        for index in [1,2,3,4,5]:
            member_key = "band" + str(index)
            if member_key in service and service[member_key] != "":
                output = output + '<li>{}</li>'.format(service[member_key])
        return output
