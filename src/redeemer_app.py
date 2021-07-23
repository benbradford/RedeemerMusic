import sys, getopt
import app_init
from flask import render_template, redirect, url_for

from api_common import app
import songs_api
import service_api
import user_api
from args_factory import ArgsFactory


@app.route('/health', methods=['GET'])
def health():
    return "okidoki"


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('home_api'), code=302)


@app.route('/home', methods=['GET'])
def home_api():
    return render_template('home.html')


@app.route('/about', methods=['GET'])
def about_api():
    return render_template('about.html')


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
