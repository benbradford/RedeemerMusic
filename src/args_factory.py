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
        remote_cache_manager = get_data_factory().get_remote_data_manager()
        if len(self._sync_components) > 0:
            if 'songs' in self._sync_components:
                remote_cache_manager.sync_songs()
            if 'services' in self._sync_components:
                remote_cache_manager.sync_services()
            if 'slides' in self._sync_components:
                remote_cache_manager.sync_slides_based_on_local()
            get_data_factory().get_local_cache_manager().sync()
        else:
            self._get_cache_manager().sync()

    def _get_cache_manager(self):
        if self._sync_source == 'remote':
            return get_data_factory().get_remote_data_manager()
        else:
            return get_data_factory().get_local_cache_manager()

    def _show_help(self):
        print "Usage: python app.py (-s | --sync-only (services | songs | slides | all)) | (-l | --local-data)"
        print "--sync: Will sync up local data with what is stored in drive. Choose the component to sync or 'all' for all components"
        print "--local-data: Will use the currently cached local data instead (will not sync with drive)"
        print "--no-run: Will not run the servuce"
        print "<no-options>: Normal launch by syncing local data with remote then launch the service"
