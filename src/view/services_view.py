from view_base import ViewBase

class ServicesView:
    def __init__(self):
        self._template = open('../res/services_view.html', "r").read()

    def render(self, services):
        return ViewBase().render(self._template.replace("_SERVICES_", self._display_options(services)))

    def _display_options(self, services):
        output = ""
        for service in services:
            output += self._display_option(service['date'], service['id'])
        return output

    def _display_option(self, name, id):
        return '<option value="' + id + '">' + name + '</option>'
