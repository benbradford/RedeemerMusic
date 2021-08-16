from user import User


class ControllerFactory:

    def __init__(self, controller, log_helper, data):
        self._data = data
        self._controller = controller
        self._controllers = {}
        self._log_helper = log_helper

    def get(self, user):
        if user is None:
            user = User.default
        if user.get_id() not in self._controllers:
            self._controllers[user.get_id()] = self._controller(user, self._log_helper, self._data)
        return self._controllers[user.get_id()]
