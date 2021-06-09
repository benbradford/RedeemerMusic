
class ViewBase:
    def __init__(self):
        self._template = open('../res/view_base.html', "r").read()

    def render(self, body):
        return self._template.replace("_MAIN_BODY_", body)
