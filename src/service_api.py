import json
import base64
import os
from flask import request, jsonify, send_file, render_template
from jinja2 import Template

from api_common import app, extract_required_param, extract_optional_param, extract_body_from_request
from client.client_factory import get_client_factory
from data.data_factory import get_data_factory
from helper.slides_helper import SlidesHelper
from helper.recipients_helper import RecipientsHelper
from data.service_dao import ServiceDao

powerpoint_location = os.path.join(os.path.dirname(__file__), '../bin/')

data_retriever = get_data_factory().get_data_retriever()
gmail_client = get_client_factory().get_gmail_client()
service_dao = ServiceDao(get_client_factory().get_sheets_client())

def _get_service_from_id_param():
    service_id = extract_required_param('id')
    service = service_dao.get(service_id)
    if service is None:
        return {}
    return service

# TODO: sync with sheets_client to get these headings
optional_service_params=['lead', 'date', 'message', 'band1', 'band2', 'band3', 'band4', 'band5', 'song1', 'song2', 'song3', 'song4', 'song5', 'song6', 'email_status', 'slides_email_status']

def _get_updated_service_from_params(requires_id):
    service = {}
    if requires_id:
        service['id'] = extract_required_param('id')
    for opt in optional_service_params:
        service[opt] = extract_optional_param(opt, '').replace("%20", ' ')
    return service

def _get_email_details(service, label_name, email_component, all_recipients):
    email_details = {}
    email_details['recipients'] = all_recipients
    email_details['font_size'] = "24px"
    email_details['email_label'] = 'Send {} Email'.format(label_name)
    if service[email_component] == 'sent':
        email_details['email_label'] = "Resend {} Email".format(label_name)
        email_details['font_size'] = "12px"
    elif service[email_component] == 'not sent test':
        email_details['email_label'] = "Send Test {} Email".format(label_name)
        email_details['recipients'] = RecipientsHelper().get_test_recipient()

    return email_details

@app.route('/services', methods=['GET'])
def services_api():
    return render_template('services.html', services=service_dao.get_all())

@app.route("/add_service_page", methods=['GET'])
def add_service_page_api():
    service = {}
    return render_template('service_add.html',\
                            service=service,\
                            songs=data_retriever.get_songs(),\
                            song_names=data_retriever.get_song_names())

@app.route("/add_service", methods=['GET'])
def add_service_api():
    service =  _get_updated_service_from_params(False)
    service_dao.set(service)
    return render_template('services.html', services=service_dao.get_all())

@app.route('/service', methods=['GET'])
def service_api():
    service = service_dao.get(extract_required_param('id'))
    service_email_details = _get_email_details(service, 'Service', 'email_status', RecipientsHelper().get_all_recipients())
    ppt_email_details = _get_email_details(service, 'Powerpoint', 'slides_email_status', RecipientsHelper().get_ppt_recipients())
    return render_template( 'service.html',\
                            service=service,\
                            service_email_params=service_email_details,\
                            ppt_email_params=ppt_email_details,\
                            songs=data_retriever.get_songs())

@app.route('/edit_service', methods=['GET'])
def service_edit_api():
    service = service_dao.get(extract_required_param('id'))
    return render_template('service_edit.html',\
                            service=service,\
                            songs=data_retriever.get_songs(),\
                            song_names=data_retriever.get_song_names())

@app.route('/update_service', methods=['GET'])
def update_service_api():
    service = _get_updated_service_from_params(True)
    service_dao.update(service)
    return render_template('services.html', services=service_dao.get_all())

@app.route('/send_music_email', methods=['GET'])
def send_music_email_api():
    service = service_dao.get(extract_required_param('id'))
    template_filename = os.path.join(os.path.dirname(__file__), '../templates/service_email_template.html')
    template_file = open(template_filename, 'r').read()
    template = Template( template_file )
    body = template.render(service=service, songs=data_retriever.get_songs())
    recipients = extract_required_param('recipients')
    subject = "Redeemer Music for " + service['date']
    gmail_client.send(subject, body, recipients, RecipientsHelper().get_from_address())
    if service['email_status'] == 'not sent test':
        service['email_status'] = 'not sent'
    else:
        service['email_status'] = 'sent'
    service_dao.update(service)
    return render_template('services.html', services=service_dao.get_all())

@app.route('/email_slides', methods=['GET'])
def email_slides_api():
    service = _get_service_from_id_param()
    ppt_filename = powerpoint_location + service['date'] + ' powerpoint.pptx'
    SlidesHelper(data_retriever).create_powerpoint(service, ppt_filename)
    recipients = extract_required_param('recipients')
    body = read_template_file('powerpoint_email_template.html').replace('_DATE_', service['date'])
    subject = "Powerpoint slides for " + service['date']
    gmail_client.send_attachment(subject, body, recipients, RecipientsHelper().get_from_address(), ppt_filename)
    if service['slides_email_status'] == 'not sent test':
        service['slides_email_status'] = 'not sent'
    else:
        service['slides_email_status'] = 'sent'
    service_dao.update(service)
    service = service_dao.get(extract_required_param('id'))
    service_email_details = _get_email_details(service, 'Service', 'email_status', RecipientsHelper().get_all_recipients())
    ppt_email_details = _get_email_details(service, 'Powerpoint', 'slides_email_status', RecipientsHelper().get_ppt_recipients())
    return render_template( 'service.html',\
                            service=service,\
                            service_email_params=service_email_details,\
                            ppt_email_params=ppt_email_details,\
                            songs=data_retriever.get_songs())

@app.route('/preview_slides', methods=['GET'])
def preview_slides_api():
    service = _get_service_from_id_param()
    ppt_filename = powerpoint_location + service['date'] + ' powerpoint.pptx'
    SlidesHelper(data_retriever).create_powerpoint(service, ppt_filename)
    return send_file(ppt_filename, as_attachment=True)
