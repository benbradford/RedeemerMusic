import json
import base64
import os
from flask import request, jsonify, send_file

from api_common import app, extract_required_param, extract_optional_param, extract_body_from_request
from client.client_factory import get_client_factory
from helper.helper_factory import get_helper_factory
from view.service_view import ServiceView
from view.email_template import EmailTemplate
from view.services_view import ServicesView
from view.service_view import ServiceView
from view.add_service_view import AddServiceView
from view.edit_service_view import EditServiceView
from data.data_factory import get_data_factory

data_retriever = get_data_factory().get_data_retriever()
slides_helper = get_helper_factory().get_slides_helper()
gmail_client = get_client_factory().get_gmail_client()
remote_data_manager = get_data_factory().get_remote_data_manager()

def _get_service_from_id_param():
    service_id = extract_required_param('id')
    service = data_retriever.get_service(service_id)
    if service is None:
        return {}
    return service

optional_service_params=['lead', 'date', 'message', 'band1', 'band2', 'band3', 'band4', 'band5', 'song1', 'song2', 'song3', 'song4', 'song5', 'song6']

def _get_updated_service_from_params(requires_id):
    service = {}
    if requires_id:
        service['id'] = extract_required_param('id')
    for opt in optional_service_params:
        service[opt] = extract_optional_param(opt, '').replace("%20", ' ')
    return service

@app.route('/slides', methods=['GET'])
def slides_api():
    service = _get_service_from_id_param()
    slides_helper.create_powerpoint(service, '../bin/powerpoint.pptx')
    return "ok"

@app.route('/services', methods=['GET'])
def services_api():
    res = data_retriever.get_services()
    return ServicesView().render(res)

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
    recipients = extract_optional_param('recipients', "ben.bradford80@gmail.com, jonny@redeemerfolkestone.org, mark.davey9@live.co.uk, emmasarahsutton@gmail.com, elaughton7@gmail.com, ben1ayers1@gmail.com, g.yorke20@gmail.com, david.3longley@btinternet.com, chriswatkins123@gmail.com")
    return ServiceView(data_retriever).render(service, recipients)

@app.route('/edit_service', methods=['GET'])
def service_edit_api():
    service = data_retriever.get_service(extract_required_param('id'))
    return EditServiceView(data_retriever).render(service)

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
    gmail_client.send(subject, body, recipients)
    return "ok"
