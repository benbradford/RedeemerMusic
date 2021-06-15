from view_common import read_template_file

class ViewBase:
    def __init__(self):
        self._template = read_template_file('view_base.html')

    def render(self, body):
        return self._template.replace("_MAIN_BODY_", body)
