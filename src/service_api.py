import json
import base64
import os
from flask import request, jsonify, send_file

from api_common import app, extract_required_param, extract_optional_param, extract_body_from_request
from service.service_factory import get_service_factory
from helper.helper_factory import get_helper_factory
from view.email_view import EmailView
from view.services_view import ServicesView

slides_helper = get_helper_factory().get_slides_helper()
service_retriever = get_helper_factory().get_songs_retriever()
sheets_service = get_service_factory().get_sheets_service()
gmail_service = get_service_factory().get_gmail_service()

def _get_service_from_param():
    service_id = extract_required_param('id')
    service = sheets_service.get_service(service_id)
    if service is None:
        return {}
    return service

@app.route('/slides', methods=['GET'])
def slides_api():
    service = _get_service_from_param()
    slides_helper.create_powerpoint(service, '../bin/powerpoint.pptx')
    return "ok"

@app.route('/services', methods=['GET'])
def services_api():
    res = sheets_service.get_services()
    return ServicesView().render(res)

@app.route('/service', methods=['GET'])
def service_api():
    service = _get_service_from_param()
    recipients = extract_optional_param('recipients', "ben.bradford80@gmail.com")
    #'ben.bradford80@gmail.com, jonny@redeemerfolkestone.org, mark.davey9@live.co.uk, emmasarahsutton@gmail.com, elaughton7@gmail.com, ben1ayers1@gmail.com, g.yorke20@gmail.com, david.3longley@btinternet.com, chriswatkins123@gmail.com'
    return EmailView(service_retriever).render_with_prompt(service, recipients)

@app.route('/send_music_email', methods=['GET'])
def send_music_email_api():
    service = _get_service_from_param()
    recipients = extract_required_param('recipients')
    body = EmailView(service_retriever).render(service)
    subject = "Redeemer Music for " + service['date']
    gmail_service.send(subject, body, recipients)
    return "ok"

# curl -X POST -d'{"band1": "BenB_Guitar","band2": "Emma_Vox","band3": "","band4": "","band5": "","date": "Sunday 1st November","id": "2","lead": "Ben B","message": "","song1": "Amazing Grace","song2": "","song3": "","song4": "","song5": ""}' localhost:5000/service
@app.route('/service', methods=['POST'])
def add_service_api():
    new_service = extract_body_from_request()
    sheets_service.add_service(new_service)
    return "ok"
