import random
from datetime import datetime, timedelta

from flask import Flask, render_template, request, flash, redirect, url_for

from init_db import show_table, add_to_cliets, check_time_records, show_records_to_masters

from root import create_app



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


def check_time(time_record, date_record, select_master):
    time_and_date_record = datetime.strptime(' '.join([date_record, time_record]), '%Y-%m-%d %H:%M:%S')
    all_time_record = check_time_records(select_master)
    if time_and_date_record in all_time_record:
        return True
    else:
        return False


def dict_records_for_masters():
    rec = show_records_to_masters()
    dict_masters = {}
    for i in rec:
        if i[-1] in dict_masters.keys():
            dict_masters[i[-1]].append(i[0:-1])
        else:
            dict_masters[i[-1]] = [i[0:-1]]
    return dict_masters


@app.route('/haitcut', methods=['get', 'post'])
def main_web_1():
    if request.method == 'GET':
        data_about_time_workers = create_dict_of_params()
        list_of_time = create_list_of_time('10:00:00.00')
        return render_template('haircutuser.html', data_about_time_workers=data_about_time_workers,
                               list_of_time=list_of_time)
    if request.method == 'POST':
        select_master = request.form.get('select_master')
        select_time = request.form.get('select_time')
        select_date = request.form.get('datep')
        name_client = request.form.get('nameclients')
        number_client = request.form.get('number')
        date_record = datetime.strptime(' '.join([select_date, select_time]), '%Y-%m-%d %H:%M:%S')
        check_times = check_time(select_time, select_date, select_master)
        if check_times:
            flash('This time is busy. Select, please, other time or date or master')
            return redirect('/haircut')
        else:
            add_to_cliets(name_client, number_client, date_record, select_master)
            return render_template('record.html', select_time=select_time, select_master=select_master,
                                   select_date=select_date, name_client=name_client)


@app.route('/formasters')
def for_masters():
    records_masters = dict_records_for_masters()

    return render_template('hairdresser.html',
                           records_masters=records_masters
                           )


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
