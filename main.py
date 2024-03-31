from flask import *
import requests
import datetime

app = Flask(__name__)


@app.route('/<int:date_id>')
@app.route('/')
def index(date_id=0):
    dates = requests.get(url="https://olimp.miet.ru/ppo_it_final/date", headers={'X-Auth-Token': 'ppo_10_10096'})
    dates = dates.json()
    date = dates['message'][date_id].split('-')
    day, month, year = date[0], date[1], date[2]

    new_req = requests.get(f"https://olimp.miet.ru/ppo_it_final?day={day}&month={month}&year={year}",
                           headers={'X-Auth-Token': 'ppo_10_10096'}).json()
    windows_for_flat = new_req["message"]['windows_for_flat']['data']
    windows_numbers = []
    floors_count = len(new_req["message"]['windows']['data'].keys())
    rooms_count = new_req['message']['flats_count']['data']

    k = 1
    counter = 0
    rooms_number = []
    for i in range(floors_count):
        floor = []
        o = 0
        for j in windows_for_flat:
            floor.append([(k)] * j)
            k += 1
        for l in range(len(floor)):
            state = new_req["message"]['windows']['data'][f'floor_{i + 1}']
            flag = 0
            for p in range(len(floor[l])):
                floor[l][p] = (floor[l][p], state[o])
                if state[o] and not flag:
                    flag = 1
                    rooms_number.append(floor[l][p][0])
                    counter += 1
                o += 1
        windows_numbers.append(floor)

    return render_template('index.html', request=new_req, windows=windows_numbers, windows_for_room=" ".join(list(map(str, windows_for_flat))),
                           rooms_count=rooms_count, active_rooms_counter=counter, active_rooms=", ".join(list(map(str, rooms_number))),
                           all_dates=dates['message'], today=dates['message'][date_id])


if __name__ == '__main__':
    app.run()
