from flask import *
import requests
import datetime

app = Flask(__name__)


@app.route('/')
def index():
    dates = requests.get(url="https://olimp.miet.ru/ppo_it_final/date", headers={'X-Auth-Token': 'ppo_10_10096'})
    dates = dates.json()
    date = dates['message'][0].split('-')
    day, month, year = date[0], date[1], date[2]

    new_req = requests.get(f"https://olimp.miet.ru/ppo_it_final?day={day}&month={month}&year={year}",
                           headers={'X-Auth-Token': 'ppo_10_10096'}).json()
    windows_for_flat = new_req["message"]['windows_for_flat']['data']
    windows_numbers = []
    floors_count = len(new_req["message"]['windows']['data'].keys())

    k = 1
    for i in range(floors_count):
        floor = []
        o = 0
        for j in windows_for_flat:
            floor.append([(k)] * j)
            k += 1
        for l in range(len(floor)):
            state = new_req["message"]['windows']['data'][f'floor_{i + 1}']
            for p in range(len(floor[l])):
                floor[l][p] = (floor[l][p], state[o])
                o += 1
        windows_numbers.append(floor)


    return render_template('index.html', request=new_req, windows=windows_numbers)


if __name__ == '__main__':
    app.run()
