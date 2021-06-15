from view_base import ViewBase
from email_template import EmailTemplate
from view_common import read_template_file

class ServiceView:
    def __init__(self, data_retriever):
        self._confirmation_template = read_template_file('email_send_confirmation_template.html')
        self._email_template = EmailTemplate(data_retriever)

    def render(self, service, recipients):
        return ViewBase().render(self._email_template.get_template(service)\
            .replace("_PUBLISH_BUTTON_", self._confirmation_template)\
            .replace("_SERVICE_", service['id'])\
            .replace("_RECIPIENTS_", recipients))
