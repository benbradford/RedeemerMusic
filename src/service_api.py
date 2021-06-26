import json
import base64
import os
from flask import request, jsonify, send_file, render_template

from api_common import app, extract_required_param, extract_optional_param, extract_body_from_request
from client.client_factory import get_client_factory
from view.view_common import read_template_file
from view.service_view import ServiceView
from view.email_template import EmailTemplate
from view.services_view import ServicesView
from view.service_view import ServiceView
from view.add_service_view import AddServiceView
from view.edit_service_view import EditServiceView
from data.data_factory import get_data_factory
from helper.slides_helper import SlidesHelper
from helper.recipients_helper import RecipientsHelper

powerpoint_location = os.path.join(os.path.dirname(__file__), '../bin/')

data_retriever = get_data_factory().get_data_retriever()
gmail_client = get_client_factory().get_gmail_client()
remote_data_manager = get_data_factory().get_remote_data_manager()

def _get_service_from_id_param():
    service_id = extract_required_param('id')
    service = data_retriever.get_service(service_id)
    if service is None:
        return {}
    return service

optional_service_params=['lead', 'date', 'message', 'band1', 'band2', 'band3', 'band4', 'band5', 'song1', 'song2', 'song3', 'song4', 'song5', 'song6', 'email_status']

def _get_updated_service_from_params(requires_id):
    service = {}
    if requires_id:
        service['id'] = extract_required_param('id')
    for opt in optional_service_params:
        service[opt] = extract_optional_param(opt, '').replace("%20", ' ')
    return service

@app.route('/services', methods=['GET'])
def services_api():
    res = data_retriever.get_services()
    return render_template('services.html', services=res)

@app.route("/add_service_page", methods=['GET'])
def add_service_page_api():
    service = {}
    return AddServiceView(data_retriever).render(service)

@app.route("/add_service", methods=['GET'])
def add_service_api():
    service =  _get_updated_service_from_params(False)
    remote_data_manager.add_service(service)
    return ServicesView().render(data_retriever.get_services())

@app.route('/service', methods=['GET'])
def service_api():
    service = data_retriever.get_service(extract_required_param('id'))
    return ServiceView(data_retriever, RecipientsHelper()).render(service)

@app.route('/edit_service', methods=['GET'])
def service_edit_api():
    service = data_retriever.get_service(extract_required_param('id'))
    return EditServiceView(data_retriever).render(service, RecipientsHelper())

@app.route('/update_service', methods=['GET'])
def update_service_api():
    service = _get_updated_service_from_params(True)
    remote_data_manager.update_service(service)
    return ServicesView().render(data_retriever.get_services())

@app.route('/send_music_email', methods=['GET'])
def send_music_email_api():
    service = _get_service_from_id_param() # todo this could be passed in
    recipients = extract_required_param('recipients')
    body = EmailTemplate(data_retriever).get_template(service)\
                .replace("_PUBLISH_BUTTON_", "")
    subject = "Redeemer Music for " + service['date']
    gmail_client.send(subject, body, recipients, RecipientsHelper().get_from_address())
    if service['email_status'] == 'not sent test':
        service['email_status'] = 'not sent'
    else:
        service['email_status'] = 'sent'
    remote_data_manager.update_service(service)
    return ServiceView(data_retriever, RecipientsHelper()).render(service)

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
    remote_data_manager.update_service(service)
    return ServiceView(data_retriever, RecipientsHelper()).render(service)

@app.route('/preview_slides', methods=['GET'])
def preview_slides_api():
    service = _get_service_from_id_param()
    ppt_filename = powerpoint_location + service['date'] + ' powerpoint.pptx'
    SlidesHelper(data_retriever).create_powerpoint(service, ppt_filename)
    return send_file(ppt_filename, as_attachment=True)
