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
    cache_source = get_data_factory().get_local_cache_manager()
    run_service = True
    opts, args = getopt.getopt(argv,"d:",["data-source="])

    for opt, arg in opts:
        if opt == '-d':
            if arg =='r' or arg == 'remote':
                cache_source = get_data_factory().get_remote_data_manager()
                run_service = False
            elif arg !='l' and arg != 'local':
                raise Exception("Invalid argument for data-source. Must be local or remote")

    cache_source.sync()
    if run_service:
        app.run()
