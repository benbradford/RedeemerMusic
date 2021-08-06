import os
from flask import send_file, render_template, redirect, url_for
from jinja2 import Template

powerpoint_location = os.path.join(os.path.dirname(__file__), '../../bin/')

# TODO: sync with sheets_client to get these headings
optional_service_params = ['lead', 'date', 'message', 'band1', 'band2', 'band3', 'band4', 'band5', 'song1', 'song2',
                           'song3', 'song4', 'song5', 'song6', 'email_status', 'slides_email_status']

FROM_ADDRESS = 'ben.bradford80@gmail.com'


class ServiceController:
    def __init__(self, gmail_client, service_dao, songs_dao, slides_helper, recipients_dao, band_dao):
        self._gmail_client = gmail_client
        self._service_dao = service_dao
        self._songs_dao = songs_dao
        self._slides_helper = slides_helper
        self._recipients_dao = recipients_dao
        self._band_dao = band_dao

    def show_services_page(self):
        services = self._service_dao.get_all_services()
        return render_template('services.html', services=services)

    def show_add_service_page(self):
        return render_template('service_add.html',
                               service={},
                               songs=self._songs_dao.get_all(),
                               song_names=self._songs_dao.get_song_names(),
                               members=self._band_dao.get_member_list())

    def add_service(self, optional_params):
        service = ServiceController._get_updated_service_from_params(None, optional_params)
        self._service_dao.set(service)
        return redirect(url_for('services_api'))

    def show_service(self, service_id):
        service = self._service_dao.get(service_id)
        service_email_details = self._get_email_details(service, 'Service', 'email_status',
                                                        self._recipients_dao.get_service_email_addresses())
        ppt_email_details = self._get_email_details(service, 'Powerpoint', 'slides_email_status',
                                                    self._recipients_dao.get_ppt_email_addresses())
        return render_template('service.html', service=service, service_email_params=service_email_details,
                               ppt_email_params=ppt_email_details, songs=self._songs_dao.get_all())

    def show_edit_service_page(self, service_id):
        service = self._service_dao.get(service_id)
        return render_template('service_edit.html',
                               service=service,
                               songs=self._songs_dao.get_all(),
                               song_names=self._songs_dao.get_song_names(),
                               members=self._band_dao.get_member_list())

    def update_service(self, service_id, optional_params):
        service = self._get_updated_service_from_params(service_id, optional_params)
        self._service_dao.update(service)
        return redirect(url_for('services_api'))

    def send_music_email(self, service_id, recipients):
        service = self._service_dao.get(service_id)
        template_filename = os.path.join(os.path.dirname(__file__), '../../templates/service_email_template.html')
        template_file = open(template_filename, 'r').read()
        template = Template(template_file)
        body = template.render(service=service, songs=self._songs_dao.get_all())

        subject = "Redeemer Music for " + service['date']
        self._gmail_client.send(subject, body, recipients, FROM_ADDRESS)
        ServiceController._update_email_status(service, 'email_status')
        self._service_dao.update(service)
        return redirect(url_for('services_api'))

    def send_slides_email(self, service_id, recipients):
        service = self._get_service_from_id(service_id)
        ppt_filename = powerpoint_location + service['date'] + ' powerpoint.pptx'
        self._slides_helper.create_powerpoint(service, ppt_filename)

        template_filename = os.path.join(os.path.dirname(__file__), '../../templates/powerpoint_email_template.html')
        template_file = open(template_filename, 'r').read()
        template = Template(template_file)
        body = template.render(date=service['date'])
        subject = "Powerpoint slides for " + service['date']
        self._gmail_client.send_attachment(subject, body, recipients, FROM_ADDRESS,
                                           ppt_filename,
                                           service['date'] + ' powerpoint.pptx')
        ServiceController._update_email_status(service, 'slides_email_status')
        self._service_dao.update(service)
        return redirect(url_for('services_api'))

    def preview_slides(self, service_id):
        service = self._get_service_from_id(service_id)
        ppt_filename = powerpoint_location + service['date'] + ' powerpoint.pptx'
        self._slides_helper.create_powerpoint(service, ppt_filename)
        return send_file(ppt_filename, as_attachment=True)

    def _get_service_from_id(self, service_id):
        service = self._service_dao.get(service_id)
        if service is None:
            print("ERROR cannot find service from id " + str(service_id))
            raise Exception("This is why this is here")
            return {}
        return service

    def _get_email_details(self, service, label_name, email_component, all_recipients):
        email_details = {'recipients': all_recipients, 'font_size': "24px",
                         'email_label': 'Send {} Email'.format(label_name)}
        if service[email_component] == 'sent':
            email_details['email_label'] = "Resend {} Email".format(label_name)
            email_details['font_size'] = "12px"
        elif service[email_component] == 'not sent test':
            email_details['email_label'] = "Send Test {} Email".format(label_name)
            email_details['recipients'] = self._recipients_dao.get_test_email_addresses()

        return email_details

    @staticmethod
    def _get_updated_service_from_params(service_id, optional_params):
        service = {}
        if service_id:
            service['id'] = int(service_id)
        for opt in optional_service_params:
            service[opt] = ServiceController._extract_optional_param(opt, optional_params, '').replace("%20", ' ')
        return service

    @staticmethod
    def _extract_optional_param(name, optional_params, default):
        if name in optional_params:
            return optional_params[name]
        else:
            return default

    @staticmethod
    def _update_email_status(service, email_status):
        if email_status not in service:
            service[email_status] = 'not sent test'

        if service[email_status] == 'not sent test':
            service[email_status] = 'not sent'
        else:
            service[email_status] = 'sent'
