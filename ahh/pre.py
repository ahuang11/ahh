from netCDF4 import MFDataset, Dataset
from ahh import era, ext
import xarray as xr
import pandas as pd
import glob
import os

__author__ = 'huang.andrew12@gmail.com'
__copyright__ = 'Andrew Huang'


class FileExists(Exception):
    pass


def wget_fi(fi_url, out_dir=None, user=None, pwd=None, quiet=False):
    """
    Wrapper of wget; downloads files that matches the given glob_str. Can
    input username and password if authentication is required.

    :param fi_url: (str) - the file url
    :param out_dir: (str) - name of directory for files to be saved
    :param user: (str) - username
    :param pwd: (str) - password
    :param quiet: (boolean) - whether to download silently
    :return out_list: (list) - list of downloaded files' paths
    """
    wget_base = "wget -r -np -nd -nc --glob=on"

    if quiet:
        add_on_cmd = " -q"
        wget_base += add_on_cmd
    if user is not None and pwd is not None:
        add_on_cmd = " --user={user} \
                  --password={pwd} '{fi_url}'" \
                  .format(user=user, pwd=pwd,
                          fi_url=fi_url)
        wget_base += add_on_cmd
    wget_cmd = "{base} '{fi_url}'" \
        .format(base=wget_base, fi_url=fi_url)

    if out_dir is not None:
        mkdir(out_dir)
        add_on_cmd = " -P {}".format(out_dir)
        wget_cmd += add_on_cmd

    os.system(wget_cmd)

    if out_dir is not None:
        fp = os.path.join(out_dir, os.path.basename(fi_url))
        out_list = sorted(glob.glob('{}'.format(fp)))
    else:
        out_list = sorted(glob.glob('{}'.format(os.path.basename(fi_url)
                                                )
                                    )
                          )

    if len(out_list) == 1:
        return out_list[0]
    else:
        return out_list


def wget_list(fi_list, nthreads=1, out_dir=None, user=None, pwd=None):
    """
    Wrapper of wget_fi; allows downloading multiple files simulataneously
    User/pwd doesn't work with more than 1 thread.

    :param fi_list: (list) - list of file urls
    :param nthreads: (int) - number of files to download simulataneously
    :param out_dir: (str) - name of directory for files to be saved
    :param user: (str) - username
    :param pwd: (str) - password
    :return fi_list: (list) - list of downloaded files' paths
    """
    out_list = []
    if nthreads > 1:
        if out_dir is not None:
            current_dir = os.getcwd()
            os.chdir(out_dir)
        out_list = ext.parallelize(wget_fi, fi_list,
                                   nthreads=nthreads)
        if out_dir is not None:
            os.chdir(current_dir)
    else:
        for fi in fi_list:
            out_list.append(wget_fi(fi,
                            out_dir=out_dir,
                            user=user, pwd=pwd))
    return out_list


def gen_fi_list(fmt, start, end, freq='1D', **kwargs):
    """
    Generate a file list for individual files that
    contain monotonically increasing dates

    :param fmt: (str): string format of files in {dt:%Y%m%d_%H%M} fmt
    :param start: (str): start time in 'YYYY-MM-DD HH:MM:SS' fmt or similar
    :param end: (str): end time in 'YYYY-MM-DD HH:MM:SS' fmt or similar
    :param freq: (int): interval between each time step
    :return fi_list: (list) - list of file names
    """
    dts = pd.date_range(start, end, freq=freq, **kwargs)
    fi_list = []
    for dt in dts:
        fi_list.append(fmt.format(dt=dt))
    return fi_list


def peek_nc(file_path, dump=True):
    """
    Prints the variables inside the netCDF dataset.

    :param file_path: (str) - path to file
    :param dump: (boolean) - ncdump file
    """
    if dump:
        ncdump_cmd = 'ncdump -h {}'.format(file_path)
        print(os.popen(ncdump_cmd))
    else:
        fi_in = Dataset(file_path, mode='r')
        print(fi_in)


def concat_nc(glob_str, out_fi=None, in_dir='./', out_dir='./', rec_dim=None):
    """
    Wrapper of NCO's ncrcat and optional ncks; concatenates a list of netCDF
    files given a glob_str (i.e. 'THETA.1440x720x50.2010*.nc') and outputs
    concatenated file as the given out_fi. If there's an error complaining
    that there's no record dimension, can give the dimension name to
    concatenate across under rec_dim.

    :param glob_str: (str) - the naming pattern of the files
    :param out_fi: (str) - name of concatenated file
    :param in_dir: (str) - directory of input files
    :param out_dir: (str) - directory of output file
    :param rec_dim: (str) - name of dimension to act as record dimension
    :return out_path: (str) - path to final concatenated file
    """
    fi_url = os.path.join(in_dir, glob_str)
    url_names = sorted(glob.glob('{}'.format(fi_url)))

    fi_name = url_names[0]
    if out_fi is None:
        out_fi = '{}_concat.nc'.format(fi_name.replace('nc', ''))
    out_path = os.path.join(out_dir, out_fi)

    if rec_dim is not None:
        if os.path.isfile('{}_rd'.format(fi_name)):
            print('{fi_name}_rd already exists! Not remaking {fi_name}_rd.'
                  .format(fi_name=fi_name))
        else:
            rec_append_cmd = \
                'ncks -O --mk_rec_dmn {rec_dim} {fi_name} {fi_name}_rd' \
                .format(rec_dim=rec_dim, fi_name=fi_name)
            os.system(rec_append_cmd)
        rec_str = '{}_rd'.format(fi_name)
        url_list = [rec_str] + url_names[1:]
    else:
        url_list = url_names

    url_list_str = ' '.join(url_list)
    os.system('ncrcat {input_list} {out_path}'.format(
        input_list=url_list_str, out_path=out_path))
    return out_path


def grb2nc(glob_str, in_dir='./', out_dir='./'):
    """
    Creates netCDF files from grib files.

    :param glob_str: (str) - the naming pattern of the files
    :param in_dir: (str) - directory of input files
    :param out_dir: (str) - directory of output files
    :return fo_names: (list) - list of netCDF files' names
    """
    fi_url = os.path.join(in_dir, glob_str)
    fi_names = sorted(glob.glob('{}'.format(fi_url)))
    fo_names = []
    for fi_name in fi_names:
        fo_name_dir = fi_name.replace(in_dir, out_dir)
        if fi_name.endswith('.grb'):
            fo_name = fo_name_dir.replace('.grb', '.nc')
        elif fi_name.endswith('.grb2'):
            fo_name = fo_name_dir.replace('.grb2', '.nc')
        elif fi_name.endswith('.grib'):
            fo_name = fo_name_dir.replace('.grib', '.nc')
        elif fi_name.endswith('.grib2'):
            fo_name = fo_name_dir.replace('.grib2', '.nc')
        os.system("wgrib2 {fi_name} -netcdf {fo_name}".format(
                                                              fi_name=fi_name,
                                                              fo_name=fo_name))
        fo_names.append(fo_name)
    if len(fo_names) == 1:
        return fo_names[0]
    else:
        return fo_names


def read_nc(file_path,
            lat='lat',
            lon='lon',
            time='time',
            num2date=True,
            peek=False,
            dump=False,
            extra=None,
            extra2=None,
            extra3=None,
            original=False,
            already=False,
            glob=False):
    """
    Reads the netCDF4 file's lats, lons, and time and returns those
    parameters in addition to an opened netCDF4 dataset.

    :param file_path: (str) - path to file
    :param peek: (boolean) - print out description of netCDF4 dataset
    :param dump: (boolean) - run peek_nc(dump=True)
    :param extra: (str) - return an extra variable given name of variable
    :param num2date: (boolean) - converts time to datetime
    :param extra2: (str) - return a second variable given name of variable
    :param extra3: (str) - return a third variable given name of variable
    :param already: (boolean) - whether lat, lon, time is already imported
                                if so, only return the extras
    :param glob: (boolean) - indicate whether file_path is "glob"able
    :return fi_in, time, lats, lons: \
            (netCDF4.Dataset, np.array, np.array, np.array) \
            netCDF4 dataset, time array, latitude array, longitude array
    """
    if '.nc' not in file_path:
        file_path += '.nc'
        print('Suffix .nc was appended to filepath!')
    if glob:
        fi_in = MFDataset(file_path)
    else:
        fi_in = Dataset(file_path, mode='r')
    if peek:
        print(fi_in)
    if dump:
        peek_nc(file_path)
    if already:
        if extra is not None:
            extra_var = fi_in.variables[extra][:]
            if extra2 is not None:
                extra_var2 = fi_in.variables[extra2][:]
                if extra3 is not None:
                    extra_var3 = fi_in.variables[extra3][:]
                    return extra_var, extra_var2, extra_var3
                return extra_var, extra_var2
            return extra_var
    else:
        try:
            lats = fi_in.variables[lat][:]
            lons = fi_in.variables[lon][:]
        except:
            print('Unable to find the given lat, lon variable name!')
            print('Will try the variable names: "latitude" and "longitude"')
            try:
                lats = fi_in.variables['latitude'][:]
                lons = fi_in.variables['longitude'][:]
            except:
                print('Unable to find any lat, lon variable; returning None')
                lats = None
                lons = None
        try:
            if num2date:
                try:
                    time_var = fi_in.variables[time]
                    time = era.time2dt(time_var)
                except:
                    print('Unable to convert time to dt; returning time')
                    time = fi_in.variables[time][:]
            else:
                time = fi_in.variables[time][:]
        except:
            print('Unable to create time variable; returning None')
            time = None
        if extra is not None:
            extra_var = fi_in.variables[extra][:]
            if extra2 is not None:
                extra_var2 = fi_in.variables[extra2][:]
                if extra3 is not None:
                    extra_var3 = fi_in.variables[extra3][:]
                    return time, lats, lons, extra_var, extra_var2, extra_var3
                return time, lats, lons, extra_var, extra_var2
            return time, lats, lons, extra_var
        if original:
            return fi_in, time, lats, lons
        else:
            fi_in.close()
            return time, lats, lons


def export_nc(var_list, name_list, units_list, lat=None, lon=None,
              out='untitled', time=None, z=None, description=None,
              fmt='NETCDF3_64BIT', lat_name='lat', lon_name='lon',
              time_name='time', z_name='z', lat_units='degrees_north',
              lon_units='degrees_east', time_units='unknown',
              z_units='unknown', time_calendar='unknown', replace=False):
    """
    Exports a netCDF3 file.

    :param var_list: (list) - list of variables in np.array
    :param name_list: (list) - list of variable names in string
    :param units_list: (list) - list of units names in string
    :param lat: (np.array) - array of latitudes
    :param lon: (np.array) - array of longitudes
    :param out: (str) - name of output file
    :param time: (np.array) - time/date variable
    :param z: (np.array) - z/level/depth variable
    :param description: (str) - description of data
    :param fmt: (str) - output format
    :param time_name: (str) - what to name the time variable
    :param z_name: (str) - what to name the z variable
    :param lat_units: (str) - units of latitude
    :param lon_units: (str) - units of longitude
    :param time_units: (str) - units of time
    :param z_units: (str) - units of z
    :param time_calendar: (str) - type of calendar
    """
    suffix = '.nc'

    if suffix in out:
        output_fi_name = out
    else:
        output_fi_name = out + suffix

    if replace:
        pass
    else:
        if os.path.isfile(output_fi_name):
            print('\nOutput file already exists; appending _1!\n')
            if suffix in output_fi_name:
                output_fi_name = output_fi_name[:-3] + '_1' + suffix

    fi_out = Dataset(output_fi_name, 'w', format=fmt)

    if description is not None:
        fi_out.description = description

    if time is not None:
        fi_out.createDimension(time_name, len(time))
        fi_out_time = fi_out.createVariable(time_name, 'f4', (time_name,))
        fi_out_time.units = time_units
        if time_units is 'unknown':
            print('\nPlease set time_units; defaulting to unknown\n')
        if time_calendar is not 'unknown':
            fi_out_time.calendar = time_calendar
        fi_out_time[:] = time

    if z is not None:
        fi_out.createDimension(z_name, len(z))
        fi_out_z = fi_out.createVariable(z_name, 'f4', (z_name,))
        fi_out_z.units = z_units
        if z_units == 'unknown':
            print('\nPlease set z_units; defaulting to unknown\n')
        fi_out_z[:] = z

    if lat is not None:
        fi_out.createDimension(lat_name, len(lat))
        fi_out_lat = fi_out.createVariable(lat_name, 'f4', (lat_name,))
        fi_out_lat.units = lat_units
        fi_out_lat[:] = lat

    if lon is not None:
        fi_out.createDimension(lon_name, len(lon))
        fi_out_lon = fi_out.createVariable(lon_name, 'f4', (lon_name,))
        fi_out_lon.units = lon_units
        fi_out_lon[:] = lon

    for var, name, units in zip(var_list, name_list, units_list):
        if time is not None and z is not None:
            if lat is None and lon is None:
                fi_out_var = fi_out.createVariable(name, 'f4',
                                                   (
                                                    time_name,
                                                    z_name,
                                                    )
                                                   )
                fi_out_var.units = units
                fi_out_var[:, :] = var
            else:
                fi_out_var = fi_out.createVariable(name, 'f4',
                                                   (
                                                    time_name,
                                                    z_name,
                                                    lat_name,
                                                    lon_name
                                                    )
                                                   )
                fi_out_var.units = units
                fi_out_var[:, :, :, :] = var
        elif z is not None:
            if lat is None and lon is None:
                fi_out_var = fi_out.createVariable(name, 'f4',
                                                   (z_name))
                fi_out_var.units = units
                fi_out_var[:] = var
            else:
                fi_out_var = fi_out.createVariable(name, 'f4',
                                                   (z_name,
                                                    lat_name,
                                                    lon_name
                                                    )
                                                   )
                fi_out_var.units = units
                fi_out_var[:, :, :] = var
        elif time is not None:
            if lat is None and lon is None:
                fi_out_var = fi_out.createVariable(name, 'f4',
                                                   (time_name))
                fi_out_var.units = units
                fi_out_var[:] = var
            else:
                fi_out_var = fi_out.createVariable(name, 'f4',
                                                   (time_name,
                                                    lat_name,
                                                    lon_name
                                                    )
                                                   )
                fi_out_var.units = units
                fi_out_var[:, :, :] = var
        else:
            fi_out_var = fi_out.createVariable(name, 'f4',
                                               (lat_name,
                                                lon_name
                                                )
                                               )
            fi_out_var.units = units
            fi_out_var[:, :] = var

    fi_out.close()


def join_cwd(path='', up=0, fp=True):
    """
    Join a path to current working directory. If path isn't provided,
    returns current working directory.

    :param path: (str) - path to be joined to current working directory
    :param up: (int) - number of times to go up one directory
    :param fp: (boolean) - whether to use originating file path
    :return full_path: (str) - full designated path
    """
    if path[0] is '/':
        path = path[1:]
    if fp:
        this_dir = os.path.dirname(os.path.realpath(__file__))
    else:
        this_dir = os.getcwd()
    for i in range(0, up):
        this_dir = os.path.dirname(this_dir)
    full_path = os.path.join(this_dir, path)
    return full_path


def mkdir(dir_path):
    """
    Creates a directory if it doesn't exist.

    :param dir_path: (str) - directory path
    :return dir_path: (str) - directory path
    """
    if not os.path.exists(dir_path):
        os.makedirs('{0}'.format(dir_path))
    return dir_path


def read_csv(path='', date=None, time=None, skiprows=None,
             spawn_dates=False, spawn_times=False,
             year=None, month=None, day=None,
             hour=None, minute=None, second=None,
             clear=False, dropna=False, strip=True, lower=True,
             **kwargs):
    """
    Read a time series csv and tries to create a datetime index.

    :param path: (str) - path to csv
    :param date: (str) - name of time column to be converted
    :param time: (arr) - column name of time; will merge with time
    :param skiprows: (list) - list of row numbers to skip
    :param spawn_dates: (boolean) - whether to spawn year, month, day cols
    :param spawn_times: (boolean) - whether to spawn hour, minute, second cols
    :param year: (arr) - column name of years
    :param month: (arr) - column name of months
    :param day: (arr) - column name of days
    :param hour: (arr) - column name of hours
    :param minute: (arr) - column name of minutes
    :param second: (arr) - column name of seconds
    :param dropna: (boolean) - whether to drop rows with NaNs
    :param strip: (boolean) - whether to remove whitespace in column names
    :param lower: (boolean) - whether to convert column names to lower came
    :return df: (pd.DataFrame) - dataframe with datetime index
    """
    if year is not None:
        df = pd.read_csv(path, skiprows=skiprows, **kwargs)
        if dropna:
            df = df.dropna()
        dt_dict = {'year': df[year], 'month': df[month], 'day': df[day]}
        if hour is not None:
            dt_dict['hour'] = df[hour]
        if minute is not None:
            dt_dict['minute'] = df[minute]
        if second is not None:
            dt_dict['second'] = df[second]
        df.set_index(era.time2dt(**dt_dict), inplace=True)
    elif date is not None and time is not None:
        df = pd.read_csv(path, skiprows=skiprows, **kwargs)
        if dropna:
            df = df.dropna()
        dates = df[date]
        times = df[time]
        dts = era.time2dt(dates + ' ' + times, strf='infer')
        df.set_index(dts, inplace=True)
    elif date is not None:
        df = pd.read_csv(path, index_col=date,
                         parse_dates=True, skiprows=skiprows, **kwargs)
        if dropna:
            df = df.dropna()
    else:
        df = pd.read_csv(path, skiprows=skiprows, **kwargs)
        if dropna:
            df = df.dropna()

    if clear:
        if date is not None:
            df.drop(date, 1, inplace=True)
        if time is not None:
            df.drop(time, 1, inplace=True)
        if year is not None:
            df.drop(year, 1, inplace=True)
        if month is not None:
            df.drop(month, 1, inplace=True)
        if day is not None:
            df.drop(day, 1, inplace=True)
        try:
            df.drop(hour, 1, inplace=True)
            df.drop(minute, 1, inplace=True)
            df.drop(second, 1, inplace=True)
        except:
            pass

    df = era.spawn_dates_times(df,
                               spawn_dates=spawn_dates,
                               spawn_times=spawn_times)

    if strip:
        df.columns = [col.strip() for col in df.columns]

    if lower:
        df.columns = [col.lower() for col in df.columns]

    return df


def merge(df1, df2, monthly=False):
    """
    Merge two dataframes

    :param df1: (pd.DataFrame) - dataframe to merge
    :param df2: (pd.DataFrame) - another dataframe to merge
    :param monthly: (boolean) - whether to groupby month first
    :return merged_df: (pd.DataFrame) - combined df1 and df2
    """
    if monthly:
        df1 = df1.groupby('1M').mean()
        df2 = df2.groupby('1M').mean()
    return df1.merge(df2,
                     how='outer',
                     left_index=True,
                     right_index=True)


def make_xr(data, lat=None, lon=None, time=None, z=None):
    """
    Create an on the go xarray.

    :param data: (np.array) - array of data
    :param lat: (np.array) - array of latitudes
    :param lon: (np.array) - array of longitudes
    :param z: (np.array) - z/level/depth variable
    """
    if time is not None and z is not None:
        if lat is None and lon is None:
            ds = xr.DataArray(data, coords={'time': time, 'level': z},
                              dims=('time', 'level'))
        else:
            ds = xr.DataArray(data, coords={'time': time, 'level': z,
                                            'lat': lat, 'lon': lon},
                              dims=('time', 'level', 'lat', 'lon'))
    elif z is not None:
        if lat is None and lon is None:
            ds = xr.DataArray(data, coords={'level': z}, dims=('level'))
        else:
            ds = xr.DataArray(data, coords={'level': z,
                                            'lat': lat, 'lon': lon},
                              dims=('level', 'lat', 'lon'))
    elif time is not None:
        if lat is None and lon is None:
            ds = xr.DataArray(data, coords={'time': time},
                              dims=('time'))
        else:
            ds = xr.DataArray(data, coords={'time': time,
                                            'lat': lat, 'lon': lon},
                              dims=('time', 'lat', 'lon'))
    else:
        ds = xr.DataArray(data, coords={'lat': lat, 'lon': lon},
                          dims=('lat', 'lon'))
    return ds


def save(df, name):
    """
    Save a dataframe as a csv and pickle file

    :param df: (pd.DataFrame) - dataframe to save
    :param name: (str) - output name
    :return name: (str) - output name
    """
    df.to_csv('{0}.csv'.format(name))
    df.to_pickle('{0}.pkl'.format(name))
    return name
