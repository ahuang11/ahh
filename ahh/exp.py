from ahh import pre
import numpy as np
import xarray as xr
import pandas as pd

__author__ = 'huang.andrew12@gmail.com'
__copyright__ = 'Andrew Huang'


def arr_1d(periods=15, freq=1, y=False,
           xy=False, dt=False, start=0, neg=False,
           seed=None, no_zeros=True):
    """
    Create a 1 dimensional array

    :param periods: (int) - length of array
    :param freq: (scalar) - frequency of step
    :param y: (boolean) - whether to randomize
    :param xy: (boolean) - whether to return both x and y
    :param start: (scalar) - number to start
    :param neg: (boolean) - include negative values
    :param seed: (int) - repeat random value
    :param no_zeros: (boolean) - no zero values
    :return arr: (arr) - array
    """
    if xy:
        if seed is not None:
            np.random.seed(seed=seed)
        if dt:
            x = arr_dt(periods=periods)
        else:
            x = np.arange(start, periods, freq)
        if neg:
            arr_1d = np.arange(start,
                               periods,
                               freq) * np.random.rand(periods) * -1
        else:
            arr_1d = (np.arange(start, periods, freq) *
                      np.random.rand(periods))
        return x, arr_1d
    elif y:
        if seed is not None:
            np.random.seed(seed=seed)
        if neg:
            arr_1d = np.arange(start,
                               periods,
                               freq) * np.random.rand(periods) * -1
        else:
            arr_1d = (np.arange(start, periods, freq) *
                      np.random.rand(periods))
    else:
        arr_1d = np.arange(start, periods, freq)
    if no_zeros:
        return arr_1d + 1
    else:
        return arr_1d


def arr_dt(periods=15, freq='D', start='2016-02-28 00:00'):
    """
    Create a datetime array

    :param periods: (int) - length of array
    :param freq: (scalar) - frequency of step
    :param start: (scalar) - date to start
    :return date_range: (pd.DatetimeIndex) - range of dates
    """
    return pd.date_range(start, periods=periods, freq=freq)


def arr_ds(time=True, var='tmp'):
    """
    Read in a saved dataset containing lat, lon, and values

    :param time: (boolean) - whether to return dataset with time
    :param var: (str) - variable type (only tmp/rh currently)
    :return ds: (xr.dataset) - dataset
    """
    if time:
        if var is 'tmp':
            path = pre.join_cwd('data/air.sig995.1948.nc')
        if var is 'rh':
            path = pre.join_cwd('data/rhum.sig995.1948.nc')
    else:
        path = pre.join_cwd('data/slp.nc')
    return xr.open_dataset(path)


def arr_df():
    """
    Read in a saved dataframe containing datetime values and weather data

    :return df: (pd.DataFrame) - dataframe
    """
    path = pre.join_cwd('data/cmi.csv')
    return pre.read_csv(path, date='valid', skiprows=5,
                        spawn_dates=True, spawn_times=True)
