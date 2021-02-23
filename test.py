import ipo_calendar
from datetime import datetime, timedelta

exan = ipo_calendar.Calendars()

#
# 
# 
# 
print(exan.ipo_calendar(from_date='2021-02-21', to_date='2021-03-01'))


#print(datetime.now().strftime("%Y-%m-%d"))
#print((datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"))