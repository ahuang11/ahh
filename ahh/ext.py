from operator import itemgetter
from multiprocessing import Pool
import xarray as xr
import numpy as np
import glob as g
import linecache
import itertools
import datetime
import time
import sys
import re

__author__ = 'huang.andrew12@gmail.com'
__copyright__ = 'Andrew Huang'


class EmptyGlob(Exception):
    pass


class MismatchGlob(Exception):
    pass


MISC = {'months_initial': ['J', 'F', 'M', 'A', 'M', 'J',
                           'J', 'A', 'S', 'O', 'N', 'D'],
        'months_short': ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                         'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'months_long': ['January', 'February', 'March', 'April',
                        'May', 'June', 'July', 'August', 'September',
                        'October', 'November', 'Dececember'],
        'weekdays_initial': ['M', 'T', 'W', 'Th',
                             'F', 'Sa', 'Su'],
        'weekdays_short': ['Mon', 'Tue', 'Wed', 'Thu',
                           'Fri', 'Sat', 'Sun'],
        'weekdays_long': ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                          'Friday', 'Saturday', 'Sunday'],
        'alphabet': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                     'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                     'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                     'y', 'z'],
        'alphabet_cap': ['A', 'B', 'C', 'D', 'E', 'F', 'G',
                         'H', 'I', 'J', 'K', 'L', 'M',
                         'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                         'U', 'V', 'W', 'X', 'Y', 'Z'],
        'days_per_month': [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
        'days_per_month_leap': [31, 29, 31, 30, 31, 30, 31,
                                31, 30, 31, 30, 31],
        }


def ahh(variable=None,
        n='ahh',
        ignore=None,
        col=None,
        time=0,
        level=0,
        center=0,
        offset=0,
        threshold=15,
        precision=2,
        edgeitems=5,
        suppress=True,
        snippet=True,
        fillval_high=99999.,
        fillval_low=-99999.,
        quiet=False,
        stop=False,
        **named_vars):
    """
    Wrapper of one_ahh(); explores a variable.

    :param variable: (array) - variable to be evaluated
    :param n: (str) - name of variable
    :param ignore: (scalar/str) - a value/str to ignore
    :param col: (str) - if dataframe, name of column
    :param time: (integer) - index of time to print in snippet
    :param level: (integer) - index of time to print in snippet
    :param center: (int) - if not 0, the number*2 to print around the center
    :param offset: (int) - count of indices offset from the center
    :param threshold: (int) - count before abbrieviating the print
    :param precision: (int) - number of decimal places
    :param edgeitems: (int) - how many numbers to print on the edge
    :param suppress: (boolean) - whether to suppress scientific notation
    :param snippet: (boolean) - whether to exclude snippet of values
    :param fillval_high: (float) - anything equal/greater than fill value will
                              not be included in the max
    :param fillval_low: (float) - anything equal/less than fill value will
                          not be included in the min
    :param named_vars: (args) - named variables to be evaluated (fills in n)
    :param quiet: (boolean) - whether to show snippet/center values
    :param stop: (boolean) - whether to stop the ahh-ing in a loop
    :return stop: (boolean) - stop the ahh-ing in a loop
    """
    kwargs = {'ignore': ignore, 'col': col, 'time': time, 'level': level,
              'center': center, 'offset': offset, 'threshold': threshold,
              'precision': precision, 'edgeitems': edgeitems,
              'suppress': suppress, 'snippet': snippet,
              'fillval_high': fillval_high, 'fillval_low': fillval_low,
              'quiet': quiet, 'stop': stop}
    if stop:
        return True
    else:
        if variable is not None:
            xr_variables = ahh_xr_check(variable)
            if len(xr_variables) == 0:
                one_ahh(variable=variable, n=n, **kwargs)
            elif len(xr_variables) == 1:
                variable = xr_variables[0][1]
                if n is 'ahh':
                    n = xr_variables[0][0]
                one_ahh(variable=variable, n=n, **kwargs)
            elif len(xr_variables) > 1:
                for i, xr_variable in enumerate(xr_variables):
                    if n is 'ahh':
                        n = xr_variable[0]
                    one_ahh(variable=xr_variable[1], n=n, **kwargs)
        for name, item in named_vars.items():
            n = name
            xr_variables = ahh_xr_check(item)
            if len(xr_variables) == 0:
                one_ahh(variable=item, n=n, **kwargs)
            elif len(xr_variables) == 1:
                variable = xr_variables[0][1]
                if n is 'ahh':
                    n = xr_variables[0][0]
                one_ahh(variable=variable, n=n, **kwargs)
            elif len(xr_variables) > 1:
                for i, xr_variable in enumerate(xr_variables):
                    if n is 'ahh':
                        n = xr_variable[0]
                    one_ahh(variable=xr_variable[1], n=n, **kwargs)
        return True


def ahhh(*variables, **named_vars):
    """
    The lite version of ahh; pass as many variables to this,
    but no settings to change

    :param named_vars: (args) - variables to be evaluated
    :return stop: (boolean) - stop the ahh-ing in a loop
    """
    n = 'ahh'
    for item in variables:
        xr_variables = ahh_xr_check(item)
        if len(xr_variables) == 0:
            one_ahh(variable=item)
        elif len(xr_variables) == 1:
            variable = xr_variables[0][1]
            if n is 'ahh':
                n = xr_variables[0][0]
            one_ahh(variable=variable, n=n)
        elif len(xr_variables) > 1:
            for i, xr_variable in enumerate(xr_variables):
                if n is 'ahh':
                    n = xr_variable[0]
                one_ahh(variable=xr_variable[1], n=n)

    for name, item in named_vars.items():
        n = name
        xr_variables = ahh_xr_check(item)
        if len(xr_variables) == 0:
            one_ahh(variable=item, n=n)
        elif len(xr_variables) == 1:
            variable = xr_variables[0][1]
            if n is 'ahh':
                n = xr_variables[0][0]
            one_ahh(variable=variable, n=n)
        elif len(xr_variables) > 1:
            for i, xr_variable in enumerate(xr_variables):
                if n is 'ahh':
                    n = xr_variable[0]
                one_ahh(variable=xr_variable[1], n=n)


def one_ahh(variable,
            n='ahh',
            ignore=None,
            col=None,
            time=0,
            level=0,
            center=0,
            offset=0,
            threshold=15,
            precision=2,
            edgeitems=5,
            suppress=True,
            snippet=True,
            fillval_high=99999.,
            fillval_low=-99999.,
            quiet=False,
            stop=False
            ):
    """
    Explores type, unnested type, length, and shape of a variable.
    Can optionally include a name to differentiate from other 'ahh's.

    :param variable: (array) - variable to be evaluated
    :param n: (str) - name of variable
    :param ignore: (scalar/str) - a value/str to ignore
    :param col: (str) - if dataframe, name of column
    :param time: (integer) - index of time to print in snippet
    :param level: (integer) - index of time to print in snippet
    :param center: (int) - if not 0, the number*2 to print around the center
    :param offset: (int) - count of indices offset from the center
    :param threshold: (int) - count before abbrieviating the print
    :param precision: (int) - number of decimal places
    :param edgeitems: (int) - how many numbers to print on the edge
    :param suppress: (boolean) - whether to suppress scientific notation
    :param snippet: (boolean) - whether to exclude snippet of values
    :param fillval_high: (float) - anything equal/greater than fill value will
                              not be included in the max
    :param fillval_low: (float) - anything equal/less than fill value will
                          not be included in the min
    :param quiet: (boolean) - whether to show snippet/center values
    :param stop: (boolean) - whether to stop the ahh-ing in a loop
    """
    if stop:
        pass
    else:
        try:
            if isinstance(variable, np.ma.MaskedArray):
                variable = variable.filled(np.nan)

            if col is not None:
                variable = variable[col]
            type_of_var2 = None
            shape_of_var = None
            len_shape_of_var = 1
            max_of_var = None
            min_of_var = None
            col_names = None
            type_of_var = type(variable)

            if ignore is not None:
                variable = np.where(variable == ignore,
                                    np.nan, variable).astype('float')

            try:
                len_of_var = len(variable)
                center_of_var = len(variable)/2
            except:
                len_of_var = 0
                center_of_var = None
            try:
                shape_of_var = np.ma.array(variable).shape
                len_shape_of_var = len(shape_of_var)
                try:
                    if len_shape_of_var == 1:
                        type_of_var2 = type(variable[0])
                    elif len_shape_of_var == 2:
                        type_of_var2 = type(variable[0][0])
                    elif len_shape_of_var == 3:
                        type_of_var2 = type(variable[0][0][0])
                    elif len_shape_of_var == 4:
                        type_of_var2 = type(variable[0][0][0][0])
                except:
                    type_of_var2 = type(np.ma.array(variable).flatten()[0])
                if len_shape_of_var == 2:
                    center_lat_of_var = shape_of_var[0] / 2
                    center_lon_of_var = shape_of_var[1] / 2
                elif len_shape_of_var == 3:
                    center_lat_of_var = shape_of_var[1] / 2
                    center_lon_of_var = shape_of_var[2] / 2
                elif len_shape_of_var == 4:
                    center_lat_of_var = shape_of_var[2] / 2
                    center_lon_of_var = shape_of_var[3] / 2
                else:
                    center_lat_of_var = None
                    center_lon_of_var = None
            except:
                pass

            try:
                nanmask = np.logical_not(np.isnan(variable))
                variable_ravel = np.ravel(variable[nanmask])
                fillval_idc = np.where(
                                      (variable_ravel < fillval_high) &
                                      (variable_ravel > fillval_low)
                                      )
                variable_clean = variable_ravel[fillval_idc]
                max_of_var = np.nanmax(variable_clean)
                min_of_var = np.nanmin(variable_clean)
                avg_of_var = np.nanmean(variable_clean)
                med_of_var = np.nanmedian(variable_clean)
            except:
                report_err()
                print('Unable to get the max/min values!')

            try:
                col_names = variable.columns
            except:
                pass

            np.set_printoptions(
                               suppress=suppress,
                               threshold=threshold,
                               precision=precision,
                               edgeitems=edgeitems
                               )

            print('')
            print('            Name: {}'.format(n))
            print('          Length: {}'.format(len_of_var))
            print('      Dimensions: {}'.format(shape_of_var))
            print('   Unnested Type: {}'.format(type_of_var2))
            print('Overarching Type: {}'.format(type_of_var))
            print('Minimum, Maximum: {0:.3f}, {1:.3f}'.format(min_of_var,
                                                              max_of_var))
            print(' Average, Median: {0:.3f}, {1:.3f}'.format(avg_of_var,
                                                              med_of_var))
            print('')

            if quiet:
                pass
            else:
                if col_names is not None:
                    print('Column names:')
                    print('{}'.format(col_names.values))
                    print('')
                if snippet:
                    print('Snippet of values:')
                    if col_names is not None:
                        try:
                            print(variable.head(edgeitems))
                        except Exception as e:
                            print(e)
                            pass
                    elif len_shape_of_var == 2:
                        try:
                            print(variable[:, :][0])
                        except:
                            print(variable)
                    elif len_shape_of_var == 3:
                        try:
                            print(variable[time, :, :][0])
                        except:
                            print(variable[0])
                    elif len_shape_of_var == 4:
                        try:
                            print(variable[time, level, :, :][0])
                        except:
                            print(variable[0][0])
                    else:
                        if len_of_var > 30:
                            print(np.array(variable))
                        else:
                            print(variable)
                else:
                    pass

                if center != 0:
                    try:
                        if len_shape_of_var == 2:
                            print('Center lat indice {lat}, lon indice {lon}:'
                                  .format(lat=center_lat_of_var + offset,
                                          lon=center_lon_of_var + offset
                                          )
                                  )
                            print(variable[
                                           int(center_lat_of_var -
                                               center + offset):
                                           int(center_lat_of_var +
                                               center + offset),
                                           int(center_lon_of_var -
                                               center + offset):
                                           int(center_lon_of_var +
                                               center + offset),
                                           ][0]
                                  )
                        elif len_shape_of_var == 3:
                            print('Center lat indice {lat}, lon indice {lon}:'
                                  .format(lat=center_lat_of_var + offset,
                                          lon=center_lon_of_var + offset
                                          )
                                  )
                            print(variable[
                                           time,
                                           int(center_lat_of_var -
                                               center + offset):
                                           int(center_lat_of_var +
                                               center + offset),
                                           int(center_lon_of_var -
                                               center + offset):
                                           int(center_lon_of_var +
                                               center + offset),
                                           ][0]
                                  )
                        elif len_shape_of_var == 4:
                            print('Center lat indice {lat}, lon indice {lon}:'
                                  .format(lat=center_lat_of_var + offset,
                                          lon=center_lon_of_var + offset
                                          )
                                  )
                            print(variable[
                                           time,
                                           level,
                                           int(center_lat_of_var -
                                               center + offset):
                                           int(center_lat_of_var +
                                               center + offset),
                                           int(center_lon_of_var -
                                               center + offset):
                                           int(center_lon_of_var +
                                               center + offset),
                                           ][0]
                                  )
                        else:
                            print('Center indice {}:'
                                  .format(center_of_var + offset))
                            start_slice = int(center_of_var - center + offset)
                            end_slice = int(center_of_var + center + offset)
                            center_slice = slice(start_slice, end_slice)
                            print(variable[center_slice]
                                  )
                    except Exception as e:
                        print(e)
                        print('Unable to get center of variable!')

                print('')
        except Exception as e:
            print('\nUnable to ahh due to this:')
            print(e)
            print('')


def ahh_xr_check(variable):
    """
    Checks if variable is xarray; if so, return list of names and items

    :param variable: (array) - variable to be evaluated
    :return varlist: (list) - list of tuples of variable name and values
    """
    if isinstance(variable, xr.Dataset):
        variable_list = []
        var_names = list(variable.data_vars)
        for var_name in var_names:
            variable_list.append(variable[var_name].values)
        return list(zip(var_names, variable_list))
    elif isinstance(variable, xr.DataArray):
        return [(variable.name, variable.values)]
    else:
        return []


def p(num=1):
    """
    Prints a noticeable mark in the terminal to help debug.

    :param num: (int) - number to differentiate your markers
    """
    print('\n######## MARK {} ########\n'.format(num))


def lonw2e(lon, reverse=False):
    """
    Converts a west longitude to east longitude, can also do in reverse.

    :param lon: (int) - a west longitude
    :param reverse: (boolean) - indicator whether input is an array
    :param array: (boolean) - indicator whether to go the other direction
    :return translated_lon: (int) - translated longitude
    """
    if not reverse:
        try:
            translated_lon = np.array(lon)
            west_lon_idc = np.where(translated_lon < 0)
            translated_lon[west_lon_idc] += 360
        except:
            if lon < 0:
                translated_lon = 360 + lon
            else:
                print('Input lon, {}, is already in east coordinates!'
                      .format(lon))
    else:
        try:
            translated_lon = np.array(lon)
            west_lon_idc = np.where(translated_lon > 180)
            translated_lon[west_lon_idc] -= 360
        except:
            if lon > 180:
                translated_lon = lon - 360
            else:
                print('Input lon, {}, is already in east coordinates!'
                      .format(lon))

    return translated_lon


def get_idc(lats,
            lons,
            lower_lat,
            upper_lat,
            left_lon,
            right_lon,
            maxmin=False,
            w2e=False,
            e2w=False):
    """
    Finds the indices for given latitudes and longitudes boundary.

    :param lats: (np.array) - array of latitudes
    :param lons: (np.array) - array of longitudes
    :param lower_lat: (float) - southern latitude boundary
    :param upper_lat: (float) - northern latitude boundary
    :param left_lon: (float) - western longitude boundary
    :param right_lon: (float) - eastern longitude boundary
    :param maxmin: (boolean) - return only the max and min of lat/lon idc
    :param w2e: (boolean) - convert input west longitudes to east longitudes
    :param e2w: (boolean) - convert input east longitudes to west longitudes
    :return lats_idc, lons_idc: (np.array, np.array) - indices of lats/lons
    :return lat_start_idc, lat_end_idc, lon_start_idc, lon_end_idc: \
             (np.int64, np.int64, np.int64, np.int64) \
             the lowest and highest lat/lon indices
    """
    lats = np.array(lats)
    lons = np.array(lons)

    if w2e:
        left_lon = lonw2e(left_lon)
        right_lon = lonw2e(right_lon)

    if e2w:
        left_lon = lonw2e(left_lon, reverse=True)
        right_lon = lonw2e(right_lon, reverse=True)

    lats_idc = np.where(
                         (lats >= lower_lat)
                         &
                         (lats <= upper_lat)
                         )

    if right_lon < left_lon:
        lons_idc = np.where(
                             (lons >= right_lon)
                             &
                             (lons <= left_lon)
                             )
    else:
        lons_idc = np.where(
                             (lons >= left_lon)
                             &
                             (lons <= right_lon)
                             )
        print('Input right_lon < left_lon! Their positions are auto swapped!')

    if len(lats_idc) == 0:
        print('Unable to find any lat indices within the range!')
    if len(lons_idc) == 0:
        print('Unable to find any lon indices within the range!')
        print('Perhaps convert west longitudes to east, or vice versa?')

    if maxmin:
        lats_idc = lats_idc[0].min(), lats_idc[0].max()
        lons_idc = lons_idc[0].min(), lons_idc[0].max()
        lat_start_idc = lats_idc[0]
        lat_end_idc = lats_idc[1]
        lon_start_idc = lons_idc[0]
        lon_end_idc = lons_idc[1]
        return lat_start_idc, lat_end_idc, lon_start_idc, lon_end_idc

    return lats_idc[0], lons_idc[0]


def get_lvls_idc(lvls, lower_lvl, upper_lvl, maxmin=False):
    """
    Finds the levels indices for given lower and upper boundary.

    :param lvls: (np.array) - array of levels
    :param lower_lvl: (float) - lower level boundary
    :param upper_lvl: (float) - upper level boundary
    :param maxmin: (boolean) - return only the max and min of level idc
    :return lvls_idc: (np.array) - indices of levels
    :return lvl_start_idc, lvl_end_idc: - (np.int64, np.int64) \
             the lowest and highest level indices
    """
    lvls = np.array(lvls)

    lvls_idc = np.where(
                         (lvls >= lower_lvl)
                         &
                         (lvls <= upper_lvl)
                         )

    if len(lvls_idc) == 0:
        print('Unable to find any lat indices within the range!')

    if maxmin:
        lvls_idc = lvls_idc[0].min(), lvls_idc[0].max()
        lvl_start_idc = lvls_idc[0]
        lvl_end_idc = lvls_idc[1]
        return lvl_start_idc, lvl_end_idc

    return lvls_idc[0]


def get_times_idc(times, start_yr, end_yr,
                  start_mth=1, end_mth=12,
                  start_day=1, end_day=31,
                  maxmin=False):
    """
    Finds the times indices for given start time and end time.

    :param times: (np.array) - array of datetimes
    :param start_yr: (int) - lower year boundary
    :param end_yr: (int) - upper year boundary
    :param start_mth: (int) - lower month boundary
    :param end_mth: (int) - upper month boundary
    :param start_day: (int) - lower day boundary
    :param end_day: (int) - upper day boundary
    :param maxmin: (boolean) - return only the max and min of time idc
    :return times_idc: (np.array) - indices of times
    :return time_start_idc, time_end_idc: (np.int64, np.int64) - \
            the lowest and highest time indices
    """
    start_dt = datetime.datetime(start_yr, start_mth, start_day)
    while True:
        try:
            end_dt = datetime.datetime(end_yr, end_mth, end_day)
            break
        except Exception as e:
            end_day -= 1
            print('Unable to create end datetime due to this error\n{}'
                  .format(e))
            print('Changing end day to {}!'
                  .format(end_day))

    times_idc = np.where(
                         (times >= start_dt)
                         &
                         (times <= end_dt)
                         )

    if len(times_idc) == 0:
        print('Unable to find any times indices within the range!')

    if maxmin:
        times_idc = times_idc[0].min(), times_idc[0].max()
        time_start_idc = times_idc[0]
        time_end_idc = times_idc[1]
        return time_start_idc, time_end_idc

    return times_idc[0]


def get_closest(data, target_val, type_var='typical'):
    """
    Get the closest value and index to target value.

    :param data: (np.array) - data
    :param target_val: (float/datetime.datetime) - target value
    :param type_var: (str) - typical (float) or datetime (datetime.datetime)
    :return closest_val, closest_val_idc: (datetime.datetime/float, int) -
             the closest value to target value and the index of that
    """
    if type_var == 'typical':
        diff = np.abs(np.array(data) - target_val)
        closest_val_idc = min(enumerate(diff), key=itemgetter(1))[0]
        return data[closest_val_idc], closest_val_idc
    if type_var == 'datetime':
        closest_val = min(data, key=lambda d: abs(d - target_val))
        closest_val_idc = np.where(data == closest_val)[0]
        if len(closest_val_idc) == 0:
            data = np.ma.array(data)
            closest_val_idc = np.where(data == closest_val)[0]
        return closest_val, closest_val_idc


def flatten(nested_list):
    """
    Flatten a nested list.

    :param nested_list: (list) - list of lists
    :return flattened_list: (list) - flattened list
    """
    return list(itertools.chain(*nested_list))


def formalize_str(input_str, suffix=None):
    """
    Capitalize string by word and remove underscores.

    :param input_str: (str) - string to replace underscores and title
    :param suffix: (str) - suffix in string to be removed
    :return output_str: (str) - formalized string
    """
    if suffix:
        input_str = input_str.replace(suffix, '')
    output_str = input_str.replace('_', ' ').title()
    return output_str


def round_to(x, base=1, prec=2):
    """
    Round to nearest base with precision.

    :param x: (scalar) - value to be rounded from
    :param base: (scalar) - value to be rounded to
    :param prec: (int) - number of decimal points
    :return rounded_val: (scalar) - rounded value
    """
    try:
        return round(base * round(float(x) / base), prec)
    except:
        print('Unable to round to')
        return x


def get_order_mag(x):
    """
    Get order of magnitude of value.

    :param x: (scalar) - value to extract order of magnitude from
    :return order_mag: (scalar) - order of magnitude
    """
    try:
        return int(np.log10(x))
    except:
        # print('Cannot get order of magnitude.')
        return 0


def round_to_nearest_mag(x):
    """
    Round to nearest order of magnitude.

    :param x: (scalar) - value to round to the nearest order of magnitude
    :return rounded_val: (scalar) - rounded value
    """
    try:
        order_mag = get_order_mag(x)
        return 5. * np.power(10, round_to(order_mag))
    except:
        print('Unable to round to nearest magnitude')
        return x


def split_consec(data):
    """
    Split into lists where values are no longer the same.
    For example, x = [1, 1, 3, 2]
    split_consec(x) == [array([1, 1]), array([3]), array([2])]

    :param data: (arr) - array of data
    :return: (list) - list of lists of consecutive same values
    """
    return np.split(data, np.where(np.diff(data) != 0)[0] + 1)


def sleep(seconds):
    """
    Wrapper of time.sleep; awaits number of seconds input.

    :param seconds: (int) - number of seconds to wait
    """
    time.sleep(seconds)


def glob(glob_str, nfiles=None, mismatch='warn'):
    """
    Return sorted glob list.

    :param glob_str: (str) - filename wildcard
    :param nfiles: (int) - number of expected files
    :param mismatch: (str) - warn or raise error
    :return glob_list: (list) - sorted list of filenames
    """
    glob_list = sorted(g.glob(glob_str))
    glob_len = len(glob_list)
    if glob_len == 0:
        raise EmptyGlob('No files match {0}!'.format(glob_str))

    mismatch_fmt = 'Expected {0} files from {1}, but got {2} files!'
    if nfiles is not None:
        nfiles = int(nfiles)
        if glob_len != nfiles:
            if mismatch is 'raise':
                raise MismatchGlob(mismatch_fmt.format(nfiles,
                                                       glob_str,
                                                       glob_len)
                                   )
            else:
                print(mismatch_fmt.format(nfiles,
                                          glob_str,
                                          glob_len)
                      )
    return glob_list


def parallelize(function, alist, nthreads=2, arg2=None, arg3=None, arg4=None):
    """
    Parallelize a function over a list of items.

    :param function: (function) - tasks to apply to list
    :param alist: (list) - a list of items to parallelize
    :param nthreads: (int) - number of threads to use
    :param arg2: (any) - constant; repeated argument
    :param arg3: (any) - constant; repeated argument
    :param arg4: (any) - constant; repeated argument
    """
    if arg4 is not None:
        args = zip(alist, itertools.repeat(arg2), itertools.repeat(arg3),
                   itertools.repeat(arg4))
    elif arg3 is not None:
        args = zip(alist, itertools.repeat(arg2), itertools.repeat(arg3))
    elif arg2 is not None:
        args = zip(alist, itertools.repeat(arg2))
    else:
        args = alist

    pool = Pool(nthreads)
    output = pool.map(function, args)
    pool.close()
    pool.join()

    return output


def report_err(save=None, comment=None, show=True):
    """
    :param save: (str) - name of file to export error message to
    :param comment: (str) - additional comments to append to error report
    :param show: (boolean): whether to print report
    :return tb: (str) - get a formatted traceback message
    """
    dtnow_str = datetime.datetime.utcnow().strftime('%b %d %H:%MZ')
    exception_type, value, traceback = sys.exc_info()

    while 1:
        if not traceback.tb_next:
            break
        traceback = traceback.tb_next

    frame = traceback.tb_frame
    lineno = traceback.tb_lineno
    filename = frame.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, frame.f_globals)

    error_fmt = '{0} {1} - {2} on line {3} in {4}: "{5}"'
    error_report = error_fmt.format(dtnow_str,
                                    exception_type.__name__,
                                    value,
                                    lineno,
                                    filename,
                                    line.strip(' ').strip('\n')
                                    )

    if comment is not None:
        error_report += ' - {0}'.format(comment)

    if show:
        print(error_report)

    if save is not None:
        if '.txt' not in save:
            save += '.txt'
        with open(save, 'a') as f:
            f.write(error_report)
            f.write('\n')


def append_to_fn(fn, append_str):
    """
    Append string before the file ending

    :param fn: (str) - filename
    :param append_str: (str) - string to add to filename
    :return new_fn: (str) - append string combined with filename
    """
    fn_list = fn.split('.')
    fn_list = '.'.join(fn_list[:-1]) + append_str + '.' + fn_list[-1]
    return ''.join(fn_list)


def strip_2ws(astr, strip=True):
    """
    Strips double white spaces

    :param astr: (str) - a string
    :param strip: (boolean) - whether to strip whitespace on edges
    """
    if strip:
        return re.sub(' +', ' ', astr).strip()
    else:
        return re.sub(' +', ' ', astr)


def get_ocean_mask(data, lats, lons,
                   reverse=False,
                   apply_mask=False,
                   **kwargs):
    """
    CURRENTLY BROKEN IN NEWER VERSIONS!
    Wrapper of basemap.maskoceans to mask either ocean or land

    :param data: (array) - data to be masked
    :param lats: (array) - array of latitudes
    :param lons: (array) - array of longitudes
    :param reverse: (boolean) - whether to mask land instead
    :param apply_mask: (boolean) - whether to apply mask
    :return mask: (arr) - array of booleans
    :return data, lons: - return data, lons
    """
    from mpl_toolkits.basemap import shiftgrid, maskoceans

    if len(np.where(lons > 180)[0]) > 0:
        data, lons = shiftgrid(180, data, lons, start=False)

    lons_mesh, lats_mesh = np.meshgrid(lons, lats)
    mask = maskoceans(lons_mesh, lats_mesh, data, **kwargs).mask

    if reverse:
        mask = np.logical_not(mask)

    if apply_mask:
        return np.ma.masked_array(data, mask), lons
    else:
        return mask
