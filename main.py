from datetime import datetime, timedelta

from flask import Flask, render_template, request

from init_db import show_table

app = Flask(__name__)
app.config['SECRET_KEY'] = 'докторская колбаса'

name_hairdressers = 0
date_and_time_record = 0

def create_dict_of_params():
    masters = show_table('masters')
    masters_names = [masters[i][1] for i in range(len(masters))]
    data_about_time_workers = {}
    data_about_time_workers['datenow'] = datetime.today().strftime('%A %d %b')
    data_about_time_workers['timenow'] = datetime.today().strftime('%H:%M')
    data_about_time_workers['names_hairdressers'] = masters_names
    data_about_time_workers['numbers_of_workers'] = len(data_about_time_workers['names_hairdressers'])
    return data_about_time_workers


def create_list_of_time(time_start_work):
    format_time_start_work = datetime.strptime(time_start_work, '%H:%M:%S.%f')
    time_delta = timedelta(minutes=60)
    list_of_time = [(format_time_start_work + (time_delta * i)).time() for i in range(0, 11)]
    return list_of_time


@app.route('/')
def main_web():
    data_about_time_workers = create_dict_of_params()
    list_of_time = create_list_of_time('10:00:00.00')
    return render_template('haircutuser.html', data_about_time_workers=data_about_time_workers,
                           list_of_time=list_of_time)


@app.route('/createrecord', methods=['get', 'post'])
def create_record():
    if request.method=='POST':
        name_hairdressers = request.values.get('select_master')
        date_and_time_record = ' '.join([request.values.get('date'), request.values.get('select_time')])
        return render_template('record.html', name_hairdressers=name_hairdressers,
                           date_and_time_record=date_and_time_record)
    elif request.method =='GET':
        name_G = request.form.get('nameclients')
        print(name_G)



if __name__ == '__main__':
    app.run(debug=True)
