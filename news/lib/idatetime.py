from datetime import timedelta, date, datetime
import re


def datetime_strptime_for_AMPM(dt):
    m = re.search('\d+\.\d+\.\d+', string=dt)
    _date = dt[m.start():m.end()]
    m = re.search('오전|오후|AM|PM', string=dt)
    apm = dt[m.start():m.end()]
    if apm == '오전': apm = 'AM'
    if apm == '오후': apm = 'PM'
    m = re.search('\d+:\d+', string=dt)
    _time = dt[m.start():m.end()]
    return datetime.strptime(f"{_date} {apm} {_time}", '%Y.%m.%d %p %I:%M')
