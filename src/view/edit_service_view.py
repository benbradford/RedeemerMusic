class EditServiceView:
    def __init__(self):
        self._template = open('../res/view_service.html', "r").read()

    def render(self, service, optional_service_params):
        return ViewBase().render(\
        self._template.replace("_SERVICE_ID_", service['id'])\
        .replace("_LEAD_", self._display_bullet(service, 'lead'))\
        .replace("_EXTRA_", self._display_bullet(service, 'extra'))
        .replace("_BAND_", self._band(service))\
        .replace("_SONGS_", self._songs(service))

    def _display_bullet(self, service, component):
        if component in service[component]:
            return '<li><b>{}</b> - {}</li>'.format(component, service[component])
        return ""

    def _param_value(self, component, display):
        return '<input type="hidden" name="{}" value="{}" />'.format(component, display)

    def _band(self, service): # todo duplicate
        output = ""
        for index in [1,2,3,4,5]:
            member_key = "band" + str(index)
            if member_key in service and service[member_key] != "":
                output = output + '<li>{}</li>'.format(service[member_key])
        return output

    def _songs(self, service):
        output = " "
        for index in [1,2,3,4,5, 6]:
            song_key = "song" + str(index)
            if song_key in service and service[song_key] != "":
                output = output + '<li>{}</li>'.format(service[song_key])
        return output

    def _edit_params(self, service, optional_service_params): # todo duplicate
        output = ""
        for opt in optional_service_params:
            if opt in service:
                output = output + '<input type="hidden" name="{}" value="{}" />'.format(opt, service[opt])
        return output
