from api_common import app

from view.view_base import ViewBase
import songs_api
import service_api

@app.route('/health', methods=['GET'])
def home():
    return "okidoki"

@app.route('/', methods=['GET'])
def index():
    return ViewBase().render(open('../res/index.html', "r").read())

app.run()
