from flask import *
import requests

app = Flask(__name__)


@app.route('/')
def index():
    request = requests.request("https://olimp.miet.ru/ppo_it_final?X-Auth-Token=ppo_10_10096", method='GET')
    return render_template('index.html', request=request)




if __name__ == '__main__':
    app.run()