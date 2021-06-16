import sys, getopt
import app_init
from view.view_base import ViewBase
from view.view_common import read_template_file
from api_common import app

import songs_api
import service_api

from args_factory import ArgsFactory

@app.route('/health', methods=['GET'])
def home():
    return "okidoki"

@app.route('/', methods=['GET'])
def index():
    return ViewBase().render(read_template_file('index.html'))

if __name__ == "__main__":
    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv,"s:lnh",["sync=", "local-data", "no-run", "help"])
    args_factory = ArgsFactory()

    for opt, arg in opts:
        if opt in ['-s', '--sync']:
            args_factory.withSyncComponent(arg)
        elif opt in ['-n', '--no-run']:
            args_factory.withNoRun()
        elif opt in ['-l', '--local-data']:
            args_factory.withUseLocalData()
        elif opt in ['-h', '--help']:
            args_factory.withHelp()
        else:
            print "Unkown option " + opt
            raise Exception("Unknown command option")

    args_factory.boot()
