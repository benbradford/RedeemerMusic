from view_base import ViewBase
from email_template import EmailTemplate
from view_common import read_template_file

class ServiceView:
    def __init__(self, data_retriever):
        self._confirmation_template = read_template_file('email_send_confirmation_template.html')
        self._email_template = EmailTemplate(data_retriever)

    def render(self, service, recipients_helper):
        recipients = recipients_helper.get_all_recipients()
        font_size = "24px"
        email_label = 'Send Email'
        if service['email_status'] == 'sent':
            email_label = "Resend Email"
            font_size = "12px"
        elif service['email_status'] == 'not sent test':
            email_label = "Send Test Email"
            recipients = recipients_helper.get_test_recipient()
        confirmation = self._confirmation_template.replace("_SEND_EMAIL_LABEL_", email_label)\
                        .replace("_FONT_SIZE_", font_size)

        return ViewBase().render(self._email_template.get_template(service)\
            .replace("_PUBLISH_BUTTON_", confirmation)\
            .replace("_SERVICE_", service['id'])\
            .replace("_RECIPIENTS_", recipients)\
            .replace("_RECIPIENT_LIST_", self._recipient_list(recipients)))

    def _recipient_list(self, recipients):
        output = ""
        for add in recipients.split(', '):
            output += '{}<br/>'.format(add)
        return output
