from flask import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/https://olimp.miet.ru/ppo_it_final")




if __name__ == '__main__':
    app.run()