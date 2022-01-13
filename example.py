import time
from datetime import datetime, timedelta
format_time_start_work = datetime.strptime('10:00:00', '%H:%M:%S')
time_delta = timedelta(minutes=60)
list_of_time = [(format_time_start_work + (time_delta * i)).time() for i in range(0, 11)]

t = '12:00:00'
format_time_start_work_1 = datetime.strptime(t, '%H:%M:%S').time()
list_of_time.remove(format_time_start_work_1)

print(list_of_time)


# a = datetime.now()
# c = a +b
