from view_base import ViewBase
from email_template import EmailTemplate
from view_common import read_template_file

class ServiceView:
    def __init__(self, data_retriever, recipients_helper):
        self._confirmation_template = read_template_file('email_send_confirmation_template.html')
        self._email_template = EmailTemplate(data_retriever)
        self._recipients_helper = recipients_helper

    def render(self, service):
        service_email_details = self._get_email_details(service, 'Service', 'email_status', self._recipients_helper.get_all_recipients())
        ppt_email_details = self._get_email_details(service, 'Powerpoint', 'slides_email_status', self._recipients_helper.get_ppt_recipients())
        confirmation = self._confirmation_template.replace("_SEND_EMAIL_LABEL_", service_email_details['email_label'])\
                        .replace("_FONT_SIZE_", service_email_details['font_size'])\
                        .replace("_SEND_POWERPOINT_EMAIL_LABEL_", ppt_email_details['email_label'])\
                        .replace("_PPT_FONT_SIZE_", ppt_email_details['font_size'])\
                        .replace("_SERVICE_RECIPIENTS_", service_email_details['recipients'])\
                        .replace("_SERVICE_RECIPIENT_LIST_", self._recipient_list(service_email_details['recipients']))\
                        .replace("_POWERPOINT_RECIPIENTS_", ppt_email_details['recipients'])\
                        .replace("_POWERPOINT_RECIPIENT_LIST_", self._recipient_list(ppt_email_details['recipients']))

        return ViewBase().render(self._email_template.get_template(service)\
            .replace("_PUBLISH_BUTTON_", confirmation)\
            .replace("_SERVICE_", service['id']))

    def _recipient_list(self, recipients):
        output = ""
        for add in recipients.split(', '):
            output += '{}<br/>'.format(add)
        return output

    def _get_email_details(self, service, label_name, email_component, all_recipients):
        email_details = {}
        email_details['recipients'] = all_recipients
        email_details['font_size'] = "24px"
        email_details['email_label'] = 'Send {} Email'.format(label_name)
        if service[email_component] == 'sent':
            email_details['email_label'] = "Resend {} Email".format(label_name)
            email_details['font_size'] = "12px"
        elif service[email_component] == 'not sent test':
            email_details['email_label'] = "Send Test {} Email".format(label_name)
            email_details['recipients'] = self._recipients_helper.get_test_recipient()
        return email_details
