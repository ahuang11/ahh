from ahh.ext import MISC
from calendar import isleap
from netCDF4 import num2date
from dateutil.relativedelta import relativedelta
import matplotlib.dates as mdates
import xarray as xr
import pandas as pd
import numpy as np
import datetime
import os

__author__ = 'huang.andrew12@gmail.com'
__copyright__ = 'Andrew Huang'


class OutOfRange(Exception):
    pass


def dt2jul(dt):
    """
    Return julian day out of a datetime.

    :param dt: (datetime.datetime/int) - datetime
    :return jday: (int) - julian day
    """
    return dt.timetuple().tm_yday


def jul2dt(jday, year=2010):
    """
    Find the datetime from a julian date.

    :param jday: (int) - julian day
    :param year: (int) - year to determine if leap
    :return dt: (datetime.datetime) - respective datetime
    """
    this_dir = os.path.dirname(os.path.realpath(__file__))

    if isleap(year):
        if jday < 1 or jday > 366:
            print('\nInput Julian day is out of 1-366 range!\n')
            raise(OutOfRange)
        cal_str = 'jd_cal_leap'
    else:
        if jday < 1 or jday > 365:
            print('\nInput Julian day is out of 1-365 range!\n')
            raise(OutOfRange)
        cal_str = 'jd_cal'

    cal_path = os.path.join(this_dir, 'data', '{}.pkl'.format(cal_str))

    cal = pd.read_pickle(cal_path)
    jday_idc = np.where(cal == jday)

    mth = jday_idc[1][0] + 1
    day = jday_idc[0][0] + 1
    return datetime.datetime(year, mth, day)


def dtnow():
    """
    Get current UTC in datetime.

    :return utcnow: (datetime.datetime) - UTC now in datetime
    """
    return datetime.datetime.utcnow()


def td2dict(td):
    """
    Get a breakdown of the timedelta

    :param td: (datetime.timedelta) - datetime timedelta
    :return td_breakdown: (dict) - dictionary containing breakdown
    """
    d = td.days
    h = td.seconds // 3600
    m = (td.seconds // 60) % 60
    s = td.seconds % 60
    return dict(days=d, hours=h, minutes=m, seconds=s)


def clockit(start, n='', save=None, show=True, return_td=False):
    """
    Get elapsed time since start.

    :param start: (datetime.datetime) - start datetime
    :param n: (str) - label/description
    :param save: (str) - name of file to export error message to
    :param show: (boolean): whether to print time taken
    :param return_dt: (boolean): whether to return datetime timedelta taken
    :return time_taken: (datetime.timedelta) - time taken
    """
    td_taken = datetime.datetime.utcnow() - start
    td_dict = td2dict(td_taken)

    days_taken = td_dict['days']
    hours_taken = td_dict['hours']
    minutes_taken = td_dict['minutes']
    seconds_taken = td_dict['seconds']

    clockit_fmt = '{0} Days, {1} Hours, {2} Minutes, {3} Seconds Elapsed'
    clockit_fmtd = clockit_fmt.format(days_taken,
                                      hours_taken,
                                      minutes_taken,
                                      seconds_taken)

    if show:
        print(n)
        print(clockit_fmtd)
        print('')

    if save is not None:
        if '.txt' not in save:
            save += '.txt'
        with open(save, 'a') as f:
            f.write(clockit_fmtd)
            f.write('\n')

    if return_td:
        return td_taken


def time2dt(time=None, strf='infer', calendar='standard',
            year=None, month=None, day=None,
            hour=None, minute=None, second=None):
    """
    Creates a datetime array based on an unopened time variable or arrays of
    time strings.

    :param time: (netCDF4.Variable/str) - unopened time var/string type array
    :param strf: (str) - time format of string, option of 'infer'
    :param calendar: (str) - type of calendar
    :param year: (arr) - array of years
    :param month: (arr) - array of months
    :param day: (arr) - array of days
    :param hour: (arr) - array of hours
    :param minute: (arr) - array of minutes
    :param second: (arr) - array of seconds
    :return dt_arr: (np.array) - array of datetimes
    """
    if strf is not None:
        if strf is 'infer':
            dt_arr = pd.to_datetime(time, infer_datetime_format=True)
        else:
            dt_arr = pd.to_datetime(time, format=strf)
    elif year is not None:
        dt_dict = {'year': year, 'month': month, 'day': day}
        if hour is not None:
            dt_dict['hour'] = hour
        if minute is not None:
            dt_dict['minute'] = minute
        if second is not None:
            dt_dict['second'] = second
        dt_arr = pd.to_datetime(dt_dict)
    else:
        try:
            dt_arr = num2date(
                time[:], units=time.units, calendar=time.calendar)
        except:
            dt_arr = num2date(
                time[:], units=time.units, calendar=calendar)
    try:
        return pd.DatetimeIndex(dt_arr)
    except:
        print('Unable to return pd.DatetimeIndex, returning dt_arr')
        return dt_arr


def dt2seas(dts, four=True, target=None):
    """
    From a datetime array create an array of seasons.

    :param dts: (arr) - array of datetimes
    :param four: (boolean) - limit to four seasons
    :param target: (str) - whether the season "begin" or "end" at month
    :return dt_arr: (xr.DataArray) - array of seasons
    """
    dts = pd.DatetimeIndex(dts)

    if target is 'begin':
        dts = dts.shift(3, freq='1M')

    if four and not target:
        ds = xr.Dataset({'dts': dts})
        return ds.dts.dt.season.values
    else:
        month_in = MISC['months_initial']
        months = dts.month
        try:
            return np.array([(month_in[month - 3] +
                             month_in[month - 2] +
                             month_in[month - 1]) for
                             month in months])
        except:
            return (month_in[months - 3] +
                    month_in[months - 2] +
                    month_in[months - 1])


def dt2spec(dt, spec):
    """
    Convert datetimes to specified time value.

    :param dt: (datetime.datetime) - array of datetimes
    :param spec: (str) - name of time value
    :return spec_arr: (list) - list of specified time values
    """
    if isinstance(dt[0], datetime.timedelta):
        if spec is 'day':
            return [x.days for x in dt]
        elif spec is 'month':
            return [x.months for x in dt]
        elif spec is 'year':
            return [x.years for x in dt]
        elif spec is 'minute':
            return [x.minutes for x in dt]
        elif spec is 'second':
            return [x.seconds for x in dt]
    else:
        if spec is 'day':
            return [x.day for x in dt]
        elif spec is 'month':
            return [x.month for x in dt]
        elif spec is 'year':
            return [x.year for x in dt]
        elif spec is 'minute':
            return [x.minute for x in dt]
        elif spec is 'second':
            return [x.second for x in dt]


def str2spec(str_arr, spec):
    """
    Convert strings to specified time value assuming
    '%Y-%m-%d %H:%M:%S' format.

    :param str: (str) - array of strings
    :param spec: (str) - name of time value
    :return spec_arr: (np.array) - list of specified time values
    """
    if spec is 'day':
        return np.array([x[8:10] for x in str_arr], dtype='int')
    elif spec is 'month':
        return np.array([x[5:7] for x in str_arr], dtype='int')
    elif spec is 'year':
        return np.array([x[0:4] for x in str_arr], dtype='int')
    elif spec is 'hour':
        return np.array([x[11:13] for x in str_arr], dtype='int')
    elif spec is 'minute':
        return np.array([x[14:16] for x in str_arr], dtype='int')
    elif spec is 'second':
        return np.array([x[17:19] for x in str_arr], dtype='int')


def dt2num(dt, reverse=False):
    """
    Convert datetime to a number to indicate location on matplotlib plot.

    :param dt: (datetime.datetime) - a datetime object
    :param reverse: (boolean) - whether to reverse the operation
    :return mdate: (scalar) - value of datetime as a number
    """
    if reverse:
        return mdates.num2date(dt)
    else:
        return mdates.date2num(dt)


def spawn_dates_times(df, spawn_dates=True, spawn_times=False):
    """
    Build date/times column from a timeseries dataframe

    :param df: (pd.DataFrame) - dataframe with datetime index
    :param spawn_dates: (boolean) - whether to spawn year, month, day cols
    :param spawn_times: (boolean) - whether to spawn hour, minute, second cols
    :return df: (pd.DataFrame) - dataframe with datetime index
    """
    if spawn_dates:
        ind = df.index
        df = df.assign(year=ind.year, month=ind.month, day=ind.day)

    if spawn_times:
        ind = df.index
        df = df.assign(hour=ind.hour, minute=ind.minute, second=ind.second)

    return df


def shift_months(dts, nmonths):
    """
    Shift datetime(s) by number of months

    :param dts: (datetime.datetime/arr) - datetime objects
    :param nmonths: (int) - number of months to shift the datetime
    :return dts: (datetime.datetime) - datetime shifted by nmonths
    """
    try:
        return pd.DatetimeIndex([dt + relativedelta(months=nmonths)
                                 for dt in dts])
    except:
        return dts + relativedelta(months=nmonths)
