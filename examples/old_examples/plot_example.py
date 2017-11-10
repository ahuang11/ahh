from ahh import pre, vis

fi_name = './example_data/theta_salt_lat_lon_time_avg'
_, _, _, depth, theta, salt = pre.read_nc(fi_name,
                                          extra='depth',
                                          extra2='theta',
                                          extra3='salt')

ax = vis.plot_line(depth, theta,
                   title='Global Week Avg of Temperature and Salinity vs Depth',
                   xlabel='Depth (m)',
                   ylabel='Temperature (F)',
                   label='Temperature',
                   legend=True,
                   xlim=(0, 2000),
                   ylim=(0, 15),
                   figsize=(15, 10))


vis.plot_line(depth, salt,
              ylim=(34, 35),
              twinx=ax,
              ylabel='Salinity (PSU)',
              label='Salinity',
              legend=True,
              color=vis.COLORS['blue'],
              figsize='null',
              save='./example_images/example_plot_same_axes_scale.png')
