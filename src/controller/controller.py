class Controller:

    def __init__(self, user, log_helper, log_prefix):
        self._log_helper = log_helper
        self._user = user
        self._log_prefix = log_prefix

    def _log_debug(self, msg):
        self._log_helper.get_for(self._user).debug(self._log_prefix + " - " + msg)

    def _log_info(self, msg):
        self._log_helper.get_for(self._user).info(self._log_prefix + " - " + msg)

    def _log_warn(self, msg):
        self._log_helper.get_for(self._user).warn(self._log_prefix + " - " + msg)

    def _log_error(self, msg):
        self._log_helper.get_for(self._user).error(self._log_prefix + " - " + msg)
