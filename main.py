from datetime import datetime, timedelta

from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'докторская колбаса'

date_record = 0
def create_dict_of_params(*args):
    data_about_time_workers = {}
    data_about_time_workers['datenow'] = datetime.today().strftime('%A %d %b')
    data_about_time_workers['timenow'] = datetime.today().strftime('%H:%M')
    data_about_time_workers['names_hairdressers'] = args
    data_about_time_workers['numbers_of_workers'] = len(data_about_time_workers['names_hairdressers'])
    return data_about_time_workers

def create_list_of_time(time_start_work):
    format_time_start_work = datetime.strptime(time_start_work, '%H:%M:%S.%f')
    time_delta = timedelta(minutes=60)
    list_of_time = [(format_time_start_work + (time_delta * i)).time() for i in range(0, 11)]
    return list_of_time



@app.route('/',methods=['get','post'])
def main_web():
    data_about_time_workers = create_dict_of_params('Alisa','Bob')
    list_of_time = create_list_of_time('10:00:00.00')
    if request.method == 'POST':
        name_hairdressers = request.values.get('select_master')
        date_record = request.values.get('date')
        time_record = request.values.get('select_time')
        format_time_record = datetime.strptime(time_record, '%H:%M:%S').time()
        list_of_time.remove(format_time_record)
        print(list_of_time)


    return render_template('haircutuser.html', data_about_time_workers=data_about_time_workers,
                           list_of_time=list_of_time)

@app.route('/createrecord',methods = ['post'])
def create_record():
    datarecord = date_record
    print(datarecord)
    return render_template('record.html')

if __name__ == '__main__':
    app.run(debug=True)
