from flask import render_template, redirect, url_for


class RecipientsController:
    def __init__(self, recipients_dao):
        self._recipients_dao = recipients_dao

    def show_recipients_page(self):
        recipients = self._recipients_dao.get_recipients()
        return render_template('recipients_edit.html', recipients=recipients)

    def show_add_new_page(self):
        return render_template('recipients_add.html')

    def add_new(self, request):
        name = request['name']
        email = request['email']
        self._recipients_dao.set_recipient(email,
                                           name,
                                           'test' in request,
                                           'ppt' in request,
                                           'service' in request)
        return redirect(url_for('recipients_api'))

    def add_recipient_register(self, email, register_index):
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
        return redirect(url_for('recipients_api'))

    def remove_recipient_register(self, email, register_index):
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
        return redirect(url_for('recipients_api'))
