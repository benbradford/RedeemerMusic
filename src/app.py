import sys, getopt
from api_common import app

from view.view_base import ViewBase
import songs_api
import service_api
from data.data_factory import get_data_factory

from client.client_factory import get_client_factory
from helper.helper_factory import get_helper_factory

slides_helper = get_helper_factory().get_slides_helper()
drive_client = get_client_factory().get_drive_client()
sheets_client = get_client_factory().get_sheets_client()

@app.route('/health', methods=['GET'])
def home():
    return "okidoki"

@app.route('/', methods=['GET'])
def index():
    return ViewBase().render(open('../res/index.html', "r").read())

if __name__ == "__main__":
    argv = sys.argv[1:]
    cache_source = get_data_factory().get_remote_data_manager()
    opts, args = getopt.getopt(argv,"s:lnh",["sync=", "local-data", "no-run", "help"])
    no_run = False
    for opt, arg in opts:
        if opt in ['-s', '--sync']:
            if arg == 'services':
                cache_source.sync_services()
            elif arg == 'songs':
                cache_source.sync_songs()
            elif arg == 'slides':
                cache_source.sync_slides()
            elif arg == 'all':
                cache_source.sync()
            else:
                print "Error - Unknown sync component " + arg
                raise Exception("Unkown sync component")
            cache_source = get_data_factory().get_local_cache_manager()
        elif opt in ['n', '--no-run']:
            no_run = True
        elif opt in ['-l', '--local-data']:
            cache_source = get_data_factory().get_local_cache_manager()
        elif opt in ['-h', '--help']:
            print "Usage: python app.py (-s | --sync-only (services | songs | slides | all)) | (-l | --local-data)"
            print "--sync: Will sync up local data with what is stored in drive. Choose the component to sync or 'all' for all components"
            print "--local-data: Will use the currently cached local data instead (will not sync with drive)"
            print "--no-run: Will not run the servuce"
            print "<no-options>: Normal launch by syncing local data with remote then launch the service"
            exit()
        else:
            raise Exception("Unknown command option")
    cache_source.sync()
    if no_run:
        exit()
    app.run()
