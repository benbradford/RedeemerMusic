import getopt
import sys

from api import app
from data.data_factory import get_data_factory


class ArgsFactory:
    def __init__(self):
        self._run_service = True
        self._sync_source = 'remote'
        self._sync_components = []
        self._should_show_help = False

    def with_no_run(self):
        self._run_service = False

    def with_use_local_data(self):
        self._sync_source = 'local'

    def with_sync_component(self, component):
        self._sync_components.append(component)

    def with_help(self):
        self._should_show_help = True

    def boot(self):
        if self._should_show_help:
            print("Usage: python app.py (-s | --sync (services | songs)) (-l | --local-data) (-n | --no-run))")
            print("--sync: Will sync up local data with what is stored in drive. Choose the component to sync or none "
                  "to sync all components")
            print("--local-data: Will use the currently cached local data instead (will not sync with drive)")
            print("--no-run: Will not run the service, useful if you want to sync with remote only")
            print("<no-options>: Normal launch by syncing local data with remote then launch the service")
            return
        if len(self._sync_components) > 0:
            if 'songs' in self._sync_components:
                get_data_factory().get_songs_dao().sync(force=True)
            if 'services' in self._sync_components:
                get_data_factory().get_service_dao().sync(force=True)
        elif self._sync_source == 'remote':
            get_data_factory().get_service_dao().sync(force=True)
            get_data_factory().get_songs_dao().sync(force=True)
        if self._run_service:
            app.run()


if __name__ == "__main__":
    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv, "s:lnh", ["sync=", "local-data", "no-run", "help"])
    args_factory = ArgsFactory()

    for opt, arg in opts:
        if opt in ['-s', '--sync']:
            args_factory.with_sync_component(arg)
        elif opt in ['-n', '--no-run']:
            args_factory.with_no_run()
        elif opt in ['-l', '--local-data']:
            args_factory.with_use_local_data()
        elif opt in ['-h', '--help']:
            args_factory.with_help()
        else:
            raise Exception("Unknown command option " + opt)

    args_factory.boot()
