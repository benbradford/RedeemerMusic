from flask import render_template, redirect, url_for

UNAUTHORISED = "The current user is not authorised to perform that operation"


class AdminController:

    def __init__(self, user, data):
        self._user = user
        self._user_dao = data

    def show_users_edit_page(self):
        if not self._user.is_authenticated or not self._user.is_admin():
            return UNAUTHORISED
        users = self._user_dao.get_all()
        return render_template('users_edit.html', user=self._user, users=users)

    def update_user(self, id, scope):
        if scope == 'field-marshal':
            scope = 'rdm/admin'
        elif scope == 'captain':
            scope = 'rdm/captain'
        elif scope == 'sergeant':
            scope = 'rdm/sergeant'
        elif scope == 'private':
            scope = 'rdm/private'
        self._user_dao.update_scope(id, scope)
        return redirect(url_for('users_edit_page_api'))