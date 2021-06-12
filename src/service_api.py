import json
import base64
import os
from flask import request, jsonify, send_file

from api_common import app, extract_required_param, extract_optional_param, extract_body_from_request
from client.client_factory import get_client_factory
from helper.helper_factory import get_helper_factory
from view.email_view import EmailView
from view.services_view import ServicesView
from view.service_view import ServiceView
from data.data_factory import get_data_factory

data_retriever = get_data_factory().get_data_retriever()
slides_helper = get_helper_factory().get_slides_helper()
gmail_client = get_client_factory().get_gmail_client()

def _get_service_from_id_param():
    service_id = extract_required_param('id')
    service = data_retriever.get_service(service_id)
    if service is None:
        return {}
    return service

@app.route('/slides', methods=['GET'])
def slides_api():
    service = _get_service_from_id_param()
    slides_helper.create_powerpoint(service, '../bin/powerpoint.pptx')
    return "ok"

@app.route('/services', methods=['GET'])
def services_api():
    # add service using dropdowns https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/request#setdatavalidationrequest
    res = data_retriever.get_services()
    return ServicesView().render(res)

@app.route('/service', methods=['GET'])
def service_api():
    service = data_retriever.get_service(extract_required_param('id'))
    recipients = extract_optional_param('recipients', "ben.bradford80@gmail.com")#"ben.bradford80@gmail.com, jonny@redeemerfolkestone.org, mark.davey9@live.co.uk, emmasarahsutton@gmail.com, elaughton7@gmail.com, ben1ayers1@gmail.com, g.yorke20@gmail.com, david.3longley@btinternet.com, chriswatkins123@gmail.com")
    return EmailView(data_retriever).render_with_prompt(service, recipients)

@app.route('/edit_service', methods=['GET'])
def service_edit_api():
    service = data_retriever.get_service(extract_required_param('id'))
    return jsonify(service)

@app.route('/send_music_email', methods=['GET'])
def send_music_email_api():
    service = _get_service_from_id_param() # todo this could be passed in
    recipients = extract_required_param('recipients')
    body = EmailView(data_retriever).render(service)
    subject = "Redeemer Music for " + service['date']
    gmail_client.send(subject, body, recipients)
    return "ok"
