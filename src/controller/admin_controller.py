from flask import render_template
from util import redirect_url, UNAUTHORISED
from controller import Controller


class AdminController(Controller):

    def __init__(self, user, log_helper, data):
        Controller.__init__(self, user, log_helper, 'AdminController')
        self._user_dao = data

    def show_users_edit_page(self):
        if not self._user.is_authenticated or not self._user.is_admin():
            return UNAUTHORISED
        users = self._user_dao.get_all()
        return render_template('users_edit.html', user=self._user, users=users)

    def update_user(self, id, scope):
        if not self._user.is_authenticated or not self._user.is_admin():
            self._log_warn("User unauthorised to update users for " + self._user.email)
            return UNAUTHORISED

        if scope == 'field-marshal':
            scope = 'rdm/admin'
        elif scope == 'captain':
            scope = 'rdm/captain'
        elif scope == 'sergeant':
            scope = 'rdm/sergeant'
        elif scope == 'private':
            scope = 'rdm/private'
        self._user_dao.update_scope(id, scope)
        self._log_info("User " + str(id) + " updated to scope " + scope)
        return redirect_url('users_edit_page_api')
