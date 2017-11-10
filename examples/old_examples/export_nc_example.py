from ahh import pre, sci

fi_name = './example_data/theta_salt_lat_lon_avg.nc'
time, _, _, depth, theta, salt = pre.read_nc(
                                             fi_name,
                                             extra='depth',
                                             extra2='theta',
                                             extra3='salt')

theta_time_avg = sci.get_avg(theta, axis=(0))
salt_time_avg = sci.get_avg(salt, axis=(0))

out = './example_data/theta_salt_lat_lon_time_avg'
name_list = ['theta', 'salt']
var_list = [theta_time_avg, salt_time_avg]
units_list = ['deg F', 'PSU']
description = 'Average of theta and salinity over time, lat, and lon.'

pre.export_nc(var_list, name_list, units_list, lat=None, lon=None,
              out=out, time=None, z=depth, description=description,
              fmt='NETCDF3_64BIT', lat_name=None, lon_name=None,
              time_name='time', z_name='depth', lat_units='degrees_north',
              lon_units='degrees_east', z_units='meters',
              time_units='days since 1992-01-01 00:00:00',
              time_calendar='standard', replace=True)
