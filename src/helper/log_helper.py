class Logger:

    def __init__(self, logger, user):
        self._user = user
        self._logger = logger

    def debug(self, msg):
        self._logger.debug(self._log_message('DEBUG', msg))

    def info(self, msg):
        self._logger.info(self._log_message('INFO', msg))

    def warn(self, msg):
        self._logger.warn(self._log_message('WARN', msg))

    def error(self, msg):
        self._logger.error(self._log_message('ERROR', msg))

    def _log_message(self, level, msg):
        return '[' + level + ']' + ' <' + self._user_output() + '> ' + msg

    def _user_output(self):
        if self._user and self._user.is_authenticated:
            return self._user.name
        return 'anon'


class LogHelper:

    def __init__(self, logger):
        self._loggers = []
        self._logger = logger

    def get(self):
        for l in self._loggers:
            if l['key'] == 'anon':
                return l['value']
        new_entry = {'key': 'anon', 'value': Logger(self._logger, None)}
        self._loggers.append(new_entry)
        return new_entry['value']

    def get_for(self, user):
        if user and user.is_authenticated:
            key = user.id
        else:
            key = 'anon'
        for l in self._loggers:
            if l['key'] == key:
                return l['value']
        new_entry = {'key': key, 'value': Logger(self._logger, user)}
        self._loggers.append(new_entry)
        return new_entry['value']
