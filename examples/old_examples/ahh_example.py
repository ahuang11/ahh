from ahh import ext, pre


# Read in data
fi_1d_dir = './example_data/theta_salt_lat_lon_time_avg.nc'
fi_2d_dir = './example_data/tmp.nc'
_, lats, lons, theta, salt = pre.read_nc(fi_1d_dir,
                                         extra='theta',
                                         extra2='salt')  # 1D data
_, lats, lons, tmp = pre.read_nc(fi_2d_dir, extra='tmp_pos_nao')  # 2D data

# 1D Data ext.ahh() Example
print('Without name')
ext.ahh(theta)

print('With name')
ext.ahh(theta, 'Theta')

print('Another method with name')
ext.ahh(Theta=theta)

print('Multiple variables with name')
ext.ahh(theta=theta, salt=salt)

print('More decimal points and more items')
ext.ahh(pot_tmp=theta, precision=4, edgeitems=7)

print('To hide snippet and center')
stop = ext.ahh(pot_temp=theta, quiet=True)

print('To stop displaying after first loop')
stop = False
for i in range(0, 3):
    stop = ext.ahh(theta=theta, salt=salt, stop=stop)

# 2D Data ext.ahh() Example
print('2D Example')
ext.ahh(tmp_2d=tmp)

# Can also use the settings from 1D
print('Can use settings just as 1D')
ext.ahh(temp_2d=tmp, quiet=True)
