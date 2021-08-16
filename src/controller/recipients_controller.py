from flask import render_template
from util import redirect_url, UNAUTHORISED
from controller import Controller


class RecipientsController(Controller):
    def __init__(self, user, log_helper, recipients_dao):
        Controller.__init__(self, user, log_helper, 'RecipientsController')
        self._recipients_dao = recipients_dao

    def show_recipients_page(self):
        recipients = self._recipients_dao.get_recipients()
        return render_template('recipients_edit.html', user=self._user, recipients=recipients)

    def show_add_new_page(self):
        if not self._user.is_authenticated or not self._user.can_email():
            return UNAUTHORISED
        return render_template('recipients_add.html', user=self._user)

    def add_new(self, request):
        if not self._user.is_authenticated or not self._user.can_email():
            return UNAUTHORISED
        name = request['name']
        email = request['email']
        self._recipients_dao.set_recipient(email,
                                           name,
                                           'test' in request,
                                           'ppt' in request,
                                           'service' in request)
        return redirect_url('recipients_api')

    def add_recipient_register(self, email, register_index):
        if not self._user.is_authenticated or not self._user.can_email():
            return UNAUTHORISED
        recipient = self._recipients_dao.get_recipient(email)
        name = recipient['name']
        test = None
        ppt = None
        service = None
        if str(register_index) == '0':
            test = True
        if str(register_index) == '1':
            ppt = True
        if str(register_index) == '2':
            service = True
        self._recipients_dao.update_recipient(email, name, test, ppt, service)
        return redirect_url('recipients_api')

    def remove_recipient_register(self, email, register_index):
        if not self._user.is_authenticated or not self._user.can_email():
            return UNAUTHORISED
        recipient = self._recipients_dao.get_recipient(email)
        name = recipient['name']
        test = None
        ppt = None
        service = None
        if str(register_index) == '0':
            test = False
        if str(register_index) == '1':
            ppt = False
        if str(register_index) == '2':
            service = False
        self._recipients_dao.update_recipient(email, name, test, ppt, service)
        return redirect_url('recipients_api')
