import numpy as np
import operator
import xarray as xr
from ahh import ext
from collections import Counter
from scipy.stats.stats import pearsonr

__author__ = 'huang.andrew12@gmail.com'
__copyright__ = 'Andrew Huang'


def get_uac(obs, fcst, clim):
    """
    Calculates the uncentered anomaly correlation.

    :param obs: (np.ma.array) - observation
    :param fcst: (np.ma.array) - forecast
    :param clim: (np.ma.array) - climatology
    :return uac: (np.array) - uncentered anomaly correlation
    """
    size_arr = obs.shape
    len_arr = size_arr[0]
    uac = np.zeros(len_arr)

    for i in range(len_arr):
        fcst_prime = np.ma.array(fcst[i, :, :] - clim)
        obs_prime = np.ma.array(obs[i, :, :] - clim)
        numerator = np.sum(fcst_prime * obs_prime)
        denominator = np.sum(
            np.square(fcst_prime)) * np.sum(np.square(obs_prime))
        uac[i] = numerator / np.sqrt(denominator)

    return uac


def get_cac(obs, fcst, clim, idc):
    """
    Calculates the centered anomaly correlation.

    :param obs: (np.ma.array) - observation
    :param fcst: (np.ma.array) - forecast
    :param clim: (np.ma.array) - climatology
    :param idc: (np.array) - indices of grid points
    :return cac: (np.ma.array) - centered anomaly correlation
    """
    size_arr = obs.shape
    len_arr = size_arr[0]
    cac = np.zeros(len_arr)

    lat_start_idc = idc[0][0]
    lat_end_idc = idc[0][-1]

    lon_start_idc = idc[1][0]
    lon_end_idc = idc[1][-1]

    for i in range(len_arr):
        fcst_prime = np.ma.array(
            fcst[i, lat_start_idc:lat_end_idc + 1,
                 lon_start_idc:lon_end_idc + 1] -
            clim[lat_start_idc:lat_end_idc + 1,
                 lon_start_idc:lon_end_idc + 1])
        obs_prime = np.ma.array(
            obs[i, lat_start_idc:lat_end_idc + 1,
                lon_start_idc:lon_end_idc + 1] -
            clim[lat_start_idc:lat_end_idc + 1,
                 lon_start_idc:lon_end_idc + 1])

        fcst_prime_avg = np.ma.average(
            np.ma.array(
                fcst[i, lat_start_idc:lat_end_idc + 1,
                     lon_start_idc:lon_end_idc + 1] -
                clim[lat_start_idc:lat_end_idc + 1,
                     lon_start_idc:lon_end_idc + 1])
            )
        obs_prime_avg = np.ma.average(
            np.ma.array(
                obs[i, lat_start_idc:lat_end_idc + 1,
                    lon_start_idc:lon_end_idc + 1] -
                clim[lat_start_idc:lat_end_idc + 1,
                     lon_start_idc:lon_end_idc + 1])
            )

        numerator = np.sum((
            fcst_prime - fcst_prime_avg) * (obs_prime - obs_prime_avg))
        denominator = np.sum(np.square(fcst_prime - fcst_prime_avg)) * \
            np.sum(np.square(obs_prime - obs_prime_avg))
        cac[i] = numerator / np.sqrt(denominator)

    return cac


def get_rmse(obs, fcst, idc):
    """
    Calculates the root mean square error.

    :param obs: (np.array) - observation
    :param fcst: (np.array) - forecast
    :param idc: (np.array) - indices of grid points
    :return rmse: (np.array) - root mean square error
    """
    size_arr = obs.shape
    len_arr = size_arr[0]
    grid_points = size_arr[1] * size_arr[2]
    rmse = np.zeros(len_arr)

    lat_start_idc = idc[0][0]
    lat_end_idc = idc[0][-1]

    lon_start_idc = idc[1][0]
    lon_end_idc = idc[1][-1]

    for i in range(len_arr):
        rmse[i] = np.sqrt(
            (1 / grid_points) *
            np.sum(
                np.square(
                    fcst[
                        i,
                        lat_start_idc:lat_end_idc + 1,
                        lon_start_idc:lon_end_idc + 1] -
                    obs[
                        i,
                        lat_start_idc:lat_end_idc + 1,
                        lon_start_idc:lon_end_idc + 1]
                       )
                   )
             )
    return rmse


def convert(variable,
            mm2in=False,
            c2f=False,
            c2k=False,
            f2k=False,
            mps2mph=False,
            km2mi=False,
            reverse=False
            ):
    """
    Converts the variable from one unit to another.

    :param variable: (np.array) - variable values
    :param mm2in: (boolean) - millimeters to inches
    :param c2f: (boolean) - Celsius to Fahrenheit
    :param c2k: (boolean) - Celsius to Kelvin
    :param f2k: (boolean) - Fahrenheit to Kelvin
    :param mps2mph: (boolean) - meters per second to miles per hour
    :param reverse: (boolean) - reverses the conversions (mm2in becomes in2mm)
    :return conv_var: (np.array) - converted variable values
    """
    np_var = np.array(variable)
    if not reverse:
        if mm2in:
            conv_var = np_var / 25.4
        elif c2f:
            conv_var = np_var * 1.8 + 32
        elif c2k:
            conv_var = np.var + 273.15
        elif f2k:
            conv_var = np_var * 1.8 + 32 + 273.15
        elif mps2mph:
            conv_var = np_var / 1609.344 * 3600
        elif km2mi:
            conv_var = np_var * 0.621371
    elif reverse:
        if mm2in:
            conv_var = np_var * 25.4
        elif c2f:
            conv_var = (np_var - 32) / 1.8
        elif c2k:
            conv_var = np.var - 273.15
        elif f2k:
            conv_var = (np_var - 32) / 1.8 - 273.15
        elif mps2mph:
            conv_var = np_var * 1609.344 / 3600
        elif km2mi:
            conv_var = np_var / 0.621371
    return conv_var


def get_norm_anom(data_avg):
    """
    Finds the normalized anomaly of some averaged data.

    :param data_avg: (np.ma.array) - average data values
    :return data_anom: (arr) - normalized anomaly
    """
    data_std = np.std(data_avg)
    data_clim = np.mean(data_avg)
    data_anom = np.zeros_like(data_avg)
    data_anom = (data_avg - data_clim) / data_std
    return data_anom


def get_anom(data):
    """
    Finds the anomaly by taking the difference
    between actual and mean.

    :param data: (np.ma.array) - data values
    :return data_anom: (arr) - anomaly
    """
    data_clim = np.mean(data)
    data_anom = data - data_clim
    return data_anom


def get_norm(data):
    """
    Normalize the data to a range of 0 to 1

    :param data: (arr) - data values
    :return data_norm: (arr) - normalized data values
    """
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def get_avg(data, axis=(0),
            times_idc=None,
            lats_idc=None,
            lons_idc=None,
            lvls_idc=None,
            change_lvl_order=False):
    """
    Finds the areal and/or time average and/or level, but first,
    data dimensions must be in these orders:
    lat, lon;
    time, lat, lon;
    time, level, lat, lon OR time, lat, lon, level (if change_lvl_order).

    :param data: (np.ma.array) - input data
    :param axis: (tuple) - axis to average over
    :param times_idc: (np.array) - time indices
    :param lats_idc: (np.array) - latitude indices
    :param lons_idc: (np.array) - longitude indices
    :param lvls_idc: (float) - level indices
    :param change_lvl_order: (boolean) - changes order of level dimension
    :return avg: (np.ma.array) - average over given parameters
    """
    data_shp = data.shape

    if len(data_shp) == 2:
        if lats_idc is None:
            lat_start_idc = 0
            lat_end_idc = data_shp[0]
        else:
            lat_start_idc = lats_idc.min()
            lat_end_idc = lats_idc.max()
        if lons_idc is None:
            lon_start_idc = 0
            lon_end_idc = data_shp[1]
        else:
            lon_start_idc = lons_idc.min()
            lon_end_idc = lons_idc.max()
        return np.ma.average(np.ma.array(data[
                               lat_start_idc:lat_end_idc + 1,
                               lon_start_idc:lon_end_idc + 1
                               ]),
                             axis=axis)

    if len(data_shp) == 3:
        if times_idc is None:
            time_start_idc = 0
            time_end_idc = data_shp[0]
        else:
            time_start_idc = times_idc.min()
            time_end_idc = times_idc.max()
        if lats_idc is None:
            lat_start_idc = 0
            lat_end_idc = data_shp[1]
        else:
            lat_start_idc = lats_idc.min()
            lat_end_idc = lats_idc.max()
        if lons_idc is None:
            lon_start_idc = 0
            lon_end_idc = data_shp[2]
        else:
            lon_start_idc = lons_idc.min()
            lon_end_idc = lons_idc.max()
        return np.ma.average(np.ma.array(data[
                               time_start_idc:time_end_idc + 1,
                               lat_start_idc:lat_end_idc + 1,
                               lon_start_idc:lon_end_idc + 1
                               ]),
                             axis=axis)

    if len(data_shp) == 4:
        if change_lvl_order:
            if times_idc is None:
                time_start_idc = 0
                time_end_idc = data_shp[0]
            else:
                time_start_idc = times_idc.min()
                time_end_idc = times_idc.max()
            if lats_idc is None:
                lat_start_idc = 0
                lat_end_idc = data_shp[1]
            else:
                lat_start_idc = lats_idc.min()
                lat_end_idc = lats_idc.max()
            if lons_idc is None:
                lon_start_idc = 0
                lon_end_idc = data_shp[2]
            else:
                lon_start_idc = lons_idc.min()
                lon_end_idc = lons_idc.max()
            if lvls_idc is None:
                lvl_start_idc = 0
                lvl_end_idc = data_shp[3]
            else:
                lvl_start_idc = lvls_idc.min()
                lvl_end_idc = lvls_idc.max()
            return np.ma.average(np.ma.array(data[
                                   time_start_idc:time_end_idc + 1,
                                   lat_start_idc:lat_end_idc + 1,
                                   lon_start_idc:lon_end_idc + 1,
                                   lvl_start_idc:lvl_end_idc + 1,
                                   ]),
                                 axis=axis)
        else:
            if times_idc is None:
                time_start_idc = 0
                time_end_idc = data_shp[0]
            else:
                time_start_idc = times_idc.min()
                time_end_idc = times_idc.max()
            if lvls_idc is None:
                lvl_start_idc = 0
                lvl_end_idc = data_shp[1]
            else:
                lvl_start_idc = lvls_idc.min()
                lvl_end_idc = lvls_idc.max()
            if lats_idc is None:
                lat_start_idc = 0
                lat_end_idc = data_shp[2]
            else:
                lat_start_idc = lats_idc.min()
                lat_end_idc = lats_idc.max()
            if lons_idc is None:
                lon_start_idc = 0
                lon_end_idc = data_shp[3]
            else:
                lon_start_idc = lons_idc.min()
                lon_end_idc = lons_idc.max()
            return np.ma.average(np.ma.array(data[
                                   time_start_idc:time_end_idc + 1,
                                   lvl_start_idc:lvl_end_idc + 1,
                                   lat_start_idc:lat_end_idc + 1,
                                   lon_start_idc:lon_end_idc + 1,
                                   ]),
                                 axis=axis)


def get_stats(data, show=True, return_str='vertical'):
    """
    Get basic stats of an array.

    :param data: (np.array) - array of data
    :param show: (boolean) - whether to print out stats
    :param return_str: (str) - indicator of to return vert, hori, or none str
    :return vert_format: (str) - vertically formatted string
    :return hori_format: (str) - horizontally formatted string
    :return leng, mini, maxi, med, avg, std: (np.float64) - \
        length, maximum, medium, average, standard deviation
    """
    if len(np.shape(data)) > 1:
        data = np.array(data).ravel()
        print('\nThe get_stats data was temporarily converted to 1D.')

    leng = len(data)
    mini = np.min(data)
    maxi = np.max(data)
    med = np.median(data)
    avg = np.average(data)
    std = np.std(data)

    len_str = 'Len: {0:6}'.format(leng)
    avg_str = 'Avg: {0:6.2f}'.format(avg)
    med_str = 'Med: {0:6.2f}'.format(med)
    max_str = 'Max: {0:6.2f}'.format(maxi)
    min_str = 'Min: {0:6.2f}'.format(mini)
    std_str = 'Std: {0:6.2f}'.format(std)

    hori_format = '\n{leng:12}, ' \
        '{mini:12}, ' \
        '{maxi:12}, ' \
        '{med:12}, ' \
        '{avg:12}, ' \
        '{std:12}\n'.format(leng=len_str,
                            mini=min_str,
                            maxi=max_str,
                            med=med_str,
                            avg=avg_str,
                            std=std_str)

    vert_format = hori_format.replace(', ', '\n')

    if show:
        print(hori_format)

    if 'horizontal' in return_str:
        return hori_format
    elif 'vertical' in return_str:
        return vert_format
    else:
        return leng, mini, maxi, med, avg, std


def get_counts(data, show=True, return_str=False):
    """
    Get count distribution of data.

    :param data: (np.array) - array of data
    :param show: (boolean) - whether to print out distribution
    :param return_str: (boolean) - whether to return formatted string
    :return count_list: (list) - list of count names and values
    :return formatted: (str) - optional formatted string of count list
    """
    count_list = sorted(Counter(data).items(), key=operator.itemgetter(0))
    count_list.append(('total', len(data)))

    formatted_str = []

    if show:
        for count in count_list:
            key = ext.formalize_str(str(count[0]))
            count_val = count[1]
            formatted = ('{key}: {count}'.format(key=key, count=count_val))
            formatted_str.append(formatted)
            print(formatted)

    formatted_str = '\n'.join(formatted_str)

    if return_str:
        return count_list, formatted_str
    else:
        return count_list


def get_corr(x, y):
    """
    Get the Pearson's correlation coefficient and two tailed p-value.

    :param x: (scalar/arr) - values
    :param y: (scalar/arr) - values
    :return corr, pval: (scalar, scalar) - correlation coefficient, p-value
    """
    return pearsonr(x, y)


def cosd(x):
    """
    Cosine function evaluating values in degrees.

    :param x: (scalar/arr) - values
    :return: (scalar/arr) - cosine of the values
    """
    return np.cos(np.radians(x))


def sind(x):
    """
    Sine function evaluating values in degrees.

    :param x: (scalar/arr) - values
    :return: (scalar/arr) - sine of the values
    """
    return np.sin(np.radians(x))


def tand(x):
    """
    Tangent function evaluating values in degrees.

    :param x: (scalar/arr) - values
    :return: (scalar/arr) - tangent of the values
    """
    return np.tan(np.radians(x))


def asind(x):
    """
    Arc sine function returning degrees.

    :param x: (scalar/arr) - values
    :return: (scalar/arr) - arc sine of the values
    """
    return np.degrees(np.arcsin(x))


def acosd(x):
    """
    Arc cosine function returning degrees.

    :param x: (scalar/arr) - values
    :return: (scalar/arr) - arc cosine of the values
    """
    return np.degrees(np.arccos(x))


def atand(x):
    """
    Arc tangent function returning degrees.

    :param x: (scalar/arr) - values
    :return: (scalar/arr) - arc tangent of the values
    """
    return np.degrees(np.arctan(x))


def get_c(a, b):
    """
    Get c in the Pythagorean theorem.

    :param a: (scalar) - value
    :param b: (scalar) - value
    :return c: (scalar) - value
    """
    return np.sqrt(a * a + b * b)


def get_terc_avg(data):
    """
    Get rolling seasonal terciles

    :param a: (scalar) - value
    :param b: (scalar) - value
    :return c: (scalar) - value
    """
    return xr.DataArray(data).rolling(dim_0=3).mean().values


def get_regression(x, y=None, deg=1, **kwargs):
    """
    Wrapper of np.polyfit to create regressions

    :param x: (arr) - x values
    :param y: (arr) - y values
    :param deg: (int) - degree of fitting polynomial
    """
    if y is None:
        y = x
        x = range(len(x))
    pfit = np.poly1d(np.polyfit(x, y, deg, **kwargs))
    return pfit(x)
