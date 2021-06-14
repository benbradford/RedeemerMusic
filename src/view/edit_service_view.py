from view.view_base import ViewBase

class EditServiceView:
    def __init__(self, data_retriever):
        self._template = open('../res/edit_service_view.html', "r").read()
        self._leaders = ["Ben B", "Chris W"]
        self._players = ["Ben B - Vocals and Guitar", "Chris W - Guitar", "Ellie - Vocals", "Emma - Vocals"]
        self._data_retriever = data_retriever

    def render(self, service):
        return ViewBase().render(\
            self._template.replace("_SERVICE_ID_", service['id'])\
                          .replace("_LEAD_", self._display_lead_options())\
                          .replace("_DATE_", service['date'])\
                          .replace("_MESSAGE_", service['message'])\
                          .replace("_BAND_", self._display_band(service))\
                          .replace("_SONGS_", self._display_songs(service)))

    def _display_lead_options(self):
        for leader in self._leaders:
            output = '<option value="' + leader + '">' + leader + '</option>'

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
