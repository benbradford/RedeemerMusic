from api_common import app
from data.data_factory import get_data_factory

class ArgsFactory:

    def __init__(self):
        self._run_service = True
        self._sync_source = 'remote'
        self._sync_components = []
        self._should_show_help = False

    def withNoRun(self):
        self._run_service = False

    def withUseLocalData(self):
        self._sync_source = 'local'

    def withSyncComponent(self, component):
        self._sync_components.append(component)

    def withHelp(self):
        self._should_show_help = True

    def boot(self):
        if self._should_show_help:
            self._show_help()
            return

        self._sync()

        if self._run_service:
            app.run()

    def _sync(self):
        if len(self._sync_components) > 0:
            if 'songs' in self._sync_components:
                get_data_factory().get_songs_dao().sync(force=True)
            if 'services' in self._sync_components:
                get_data_factory().get_service_dao().sync(force=True)
        elif self._sync_source == 'remote':
            get_data_factory().get_service_dao().sync(force=True)
            get_data_factory().get_songs_dao().sync(force=True)
        else:
            get_data_factory().get_service_dao().sync(force=False)
            get_data_factory().get_songs_dao().sync(force=False)


    def _show_help(self):
        print ("Usage: python app.py (-s | --sync-only (services | songs)) | (-l | --local-data)")
        print ("--sync: Will sync up local data with what is stored in drive. Choose the component to sync or none for all components")
        print ("--local-data: Will use the currently cached local data instead (will not sync with drive)")
        print ("--no-run: Will not run the servuce")
        print ("<no-options>: Normal launch by syncing local data with remote then launch the service")
