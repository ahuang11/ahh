from ahh import vis, pre

_, slp_lat, slp_lon, slp_arr = pre.read_nc(
                                           './example_data/slp.nc',
                                           extra='slp_pos_nao', peek=True)
_, tmp_lat, tmp_lon, tmp_arr = pre.read_nc('./example_data/tmp.nc',
                                           extra='tmp_pos_nao')

title = 'Temp [K] and Contoured SLP [Pa] Anomalies'

ax = vis.plot_map(tmp_arr, tmp_lat, tmp_lon,
                       data2=slp_arr, lats2=slp_lat, lons2=slp_lon,
                       contour=[2, 4], contour2=[-4, -2], vmin=-3, vmax=3,
                       wrap=True, figsize=(9, 6), interval=1, title=title, close=False,
                       save='./example_images/plot_map_example.png')

# plot blue filled region
lat_i, lat_e, lon_i, lon_e = 30, 76, 248, 278
vis.plot_bounds(ax, lat_i, lat_e, lon_i, lon_e, color='b', fill=True,
                alpha=0.15)

# plot green dashed outlined region
lat_i, lat_e, lon_i, lon_e = 76, 52, 230, 240
vis.plot_bounds(ax, lat_i, lat_e, lon_i, lon_e, color='g', linestyle='dashed')

# plot red solid outlined region
lat_i, lat_e, lon_i, lon_e = 60, 48, 240, 260
vis.plot_bounds(ax, lat_i, lat_e, lon_i, lon_e, color='red')
vis.savefig('./example_images/plot_map_example_with_bound.png')