from view.view_base import ViewBase
from view_common import read_template_file

class ManipulateServiceBaseView:
    def __init__(self, data_retriever):
        self._template = read_template_file('edit_service_view.html')
        self._leaders = ["Ben B", "Chris W"]
        self._players = ["Ben B - Vocals and Guitar", "Chris W - Guitar", "Ellie - Vocals", "Emma - Vocals"]
        self._data_retriever = data_retriever

    def render(self, service):
        return ViewBase().render(\
            self._template.replace("_LEAD_", self._display_lead_options(service))\
                          .replace("_DATE_", self._get_value(service, 'date'))\
                          .replace("_MESSAGE_", self._get_value(service, 'message'))\
                          .replace("_BAND_", self._display_band(service))\
                          .replace("_SONGS_", self._display_songs(service))
                          .replace("_TYPE_", self.title())\
                          .replace("_METHOD_NAME_", self.method_name())\
                          .replace("_HIDDEN_", self.hidden_value(service))
                          .replace("_CANCEL_ACTION_", self.cancel_action(service)))

    def title(self):
        pass

    def method_name(self):
        pass

    def hidden_value(self, service):
        pass

    def cancel_action(self, service):
        pass

    def _get_value(self, service, component):
        if component in service:
            return service[component]
        return ""

    def _display_lead_options(self, service):
        selected = 'Ben B'
        if 'lead' in service:
            selected = service['lead']
        output = ""
        for leader in self._leaders:
            output += '<option '
            if selected == leader:
                output += 'selected="selected" '
            output += 'value="' + leader + '">' + leader + '</option>'

        return output

    def _display_band(self, service):
        output = ""
        for index in [1,2,3,4,5]:
            member_key = "band" + str(index)

            output = output + '<label for="' + member_key + '">' + member_key + '</label>'
            output = output + '<select id="' + member_key + '" name="' + member_key + '">'
            if member_key in service and service[member_key] != "":
                output += '<option value=""> </option>'
            else:
                output += '<option selected="selected" value=""> </option>'
            for player in self._players:
                output += '<option '
                if member_key in service and service[member_key] == player:
                    output += 'selected="selected" '
                output += 'value="' + player + '">' + player + '</option>'

            output = output + '</select><br/>'
        return output

    def _display_songs(self, service):
        output = ""
        for index in [1,2,3,4,5,6]:
            member_key = "song" + str(index)
            output = output + '<label for="' + member_key + '">' + member_key + '</label>'
            output = output + '<select id="' + member_key + '" name="' + member_key + '">'
            if member_key in service and service[member_key] != "":
                output += '<option value=""> </option>'
            else:
                output += '<option selected="selected" value=""> </option>'
            for song in self._data_retriever.get_song_names():
                output += '<option '
                if member_key in service and service[member_key] == song:
                    output += 'selected="selected" '
                output += 'value="' + song + '">' + song + '</option>'

            output = output + '</select><br/>'
        return output
