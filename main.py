from calendar import calendar
from datetime import datetime, timedelta
from flask import Flask, render_template, request
from init_db import show_table,add_to_cliets

app = Flask(__name__)
app.config['SECRET_KEY'] = 'докторская колбаса'

list_of_time = []


def list_of_dates_for_year():
    now = datetime.now()
    months = [i for i in range(1, 13)]
    days = calendar.monthrange(now.year, now.month)[1]
    dict_days = {}
    dict_months = {}
    list_of_time_work = create_list_of_time('10:00:00.00')
    for i in range(1, days + 1):
        dict_days[i] = list_of_time_work
        for j in months:
            dict_months[j] = dict_days

    return dict_months

def reserve_time(dates,times):
    format_time_start_work = datetime.strptime(times, '%H:%M:%S.%f').time()
    d = datetime.strptime(dates,'%Y-%m-%d').date()
    month_record = d.month
    day_record = d.day
    month = list_of_dates_for_year()
    time_index = month[month_record][day_record].index(format_time_start_work)
    del month[month_record][day_record][time_index]
    return month



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



@app.route('/haircut/<int:user_id>', methods=['get', 'post'])
def main_web(user_id):
    data_about_time_workers = create_dict_of_params()
    list_of_time = create_list_of_time('10:00:00.00')
    if request.method == 'GET':
        return render_template('haircutuser.html', data_about_time_workers=data_about_time_workers,
                           list_of_time=list_of_time)


@app.route('/haircut', methods=['get', 'post'])
def main_web_1():
    if request.method=='POST':
        select_master = request.form.get('select_master')
        select_time = request.form.get('select_time')
        select_date = request.form.get('datep')
        name_client = request.form.get('nameclients')
        number_client = request.form.get('number')
        date_record = ' '.join([select_date,select_time])
        add_to_cliets(name_client,number_client,date_record,select_master)
        return render_template('record.html', select_time=select_time, select_master=select_master,
                               select_date=select_date, name_client=name_client)



if __name__ == '__main__':
    app.run(debug=True)
