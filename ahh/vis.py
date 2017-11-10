import os
import copy
import datetime
import numpy as np
import xarray as xr
import pandas as pd
from collections import Counter
from ahh.ext import (round_to, get_order_mag, report_err, lonw2e)
from ahh.sci import get_stats, get_norm_anom, get_anom, get_norm
from ahh.era import td2dict
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.dates import YearLocator, MonthLocator, DayLocator,\
                             HourLocator, MinuteLocator, AutoDateLocator, \
                             DateFormatter, AutoDateFormatter
from matplotlib.ticker import MultipleLocator, \
                              FormatStrFormatter
import matplotlib.dates as mdates


__author__ = 'huang.andrew12@gmail.com'
__copyright__ = 'Andrew Huang'


class MissingInput(Exception):
    pass


class Unsupported(Exception):
    pass


THIS_DIR = os.path.dirname(os.path.realpath(__file__))

DEFAULT = {
          'scale': 1,
          'projection': None,
          'dpi': 105,
          'sizes': {
                    'figure': {'smallest': 6,
                               'smaller': 9,
                               'small': 12,
                               'medium': 14,
                               'large': 16,
                               'larger': 20,
                               'largest': 24
                               },
                    'text': {'smallest': 5.5,
                             'smaller': 7.5,
                             'small': 12,
                             'medium': 14,
                             'large': 16,
                             'larger': 20,
                             'largest': 24
                             },
                    'line': {'smallest': 0.4,
                             'smaller': 0.65,
                             'small': 1,
                             'medium': 1.15,
                             'large': 1.3,
                             'larger': 1.5,
                             'largest': 2
                             },
                    'tick': {'smallest': 0.05,
                             'smaller': 0.15,
                             'small': 0.2,
                             'medium': 0.55,
                             'large': 1.0,
                             'larger': 1.25,
                             'largest': 1.5
                             },
                    'bar': {'smallest': 6,
                            'smaller': 9,
                            'small': 12,
                            'medium': 14,
                            'large': 16,
                            'larger': 20,
                            'largest': 24
                            },
                    'marker': {'smallest': 6,
                               'smaller': 9,
                               'small': 12,
                               'medium': 14,
                               'large': 16,
                               'larger': 20,
                               'largest': 24
                               },
                    'title pad': {'smallest': 0.985,
                                  'smaller': 0.995,
                                  'small': 1.0,
                                  'medium': 1.01,
                                  'large': 1.03,
                                  'larger': 1.05,
                                  'largest': 1.07
                                  },
                    'pad': {'smallest': 0.15,
                            'smaller': 0.2,
                            'small': 0.3,
                            'medium': 0.45,
                            'large': 0.6,
                            'larger': 0.85,
                            'largest': 1.0
                            }
                    },
          'styles': {
                     'color': {'green': '#145222',
                               'red': '#DF0909',
                               'orange': '#E68D00',
                               'pink': '#CE5F5F',
                               'magenta': '#9E005D',
                               'teal': '#66A7C5',
                               'yellow': '#E0D962',
                               'stone': '#6462E0',
                               'blue': '#2147B1',
                               'purple': '#630460',
                               'black': '#202020',
                               'light gray': '#DADADA',
                               'gray': '#5B5B5B',
                               'white': '#FFFFFF',
                               },
                     'tc_color': {'dep': '#7EC6FF',
                                  'storm': '#00F9F3',
                                  'one': '#FFFFC6',
                                  'two': '#FFFF5A',
                                  'three': '#FFD97E',
                                  'four': '#FF9C00',
                                  'five': '#FF5454'
                                  },
                     'alpha': {'transparent': 0.2,
                               'translucid': 0.3,
                               'translucent': 0.5,
                               'semi opaque': 0.75,
                               'opaque': 0.95,
                               }
                    },
          'figtext': {'loc': 'bottom right',
                      'center bottom': {
                                       'xy_loc': (0.5, 0.05),
                                       'ha': 'center',
                                       'va': 'center',
                                       'lef_marg': 0.05,
                                       'rig_marg': 0.95,
                                       'bot_marg': 0.15,
                                       'top_marg': 0.95
                                        },
                      'center left': {'xy_loc': (0.1, 0.5),
                                      'ha': 'right',
                                      'va': 'center',
                                      'lef_marg': 0.175,
                                      'rig_marg': 0.95,
                                      'bot_marg': 0.15,
                                      'top_marg': 0.95
                                      },
                      'center right': {'xy_loc': (0.9, 0.5),
                                       'ha': 'left',
                                       'va': 'center',
                                       'lef_marg': 0.05,
                                       'rig_marg': 0.85,
                                       'bot_marg': 0.05,
                                       'top_marg': 0.95
                                       },
                      'bottom left': {'xy_loc': (0.1, 0.075),
                                      'ha': 'right',
                                      'va': 'bottom',
                                      'lef_marg': 0.175,
                                      'rig_marg': 0.95,
                                      'bot_marg': 0.05,
                                      'top_marg': 0.95
                                      },
                      'bottom right': {'xy_loc': (0.9, 0.075),
                                       'ha': 'left',
                                       'va': 'bottom',
                                       'lef_marg': 0.05,
                                       'rig_marg': 0.85,
                                       'bot_marg': 0.05,
                                       'top_marg': 0.95
                                       },
                      'upper left': {'xy_loc': (0.1, 0.925),
                                     'ha': 'right',
                                     'va': 'top',
                                     'lef_marg': 0.175,
                                     'rig_marg': 0.95,
                                     'bot_marg': 0.05,
                                     'top_marg': 0.95
                                     },
                      'upper right': {'xy_loc': (0.9, 0.925),
                                      'ha': 'left',
                                      'va': 'top',
                                      'lef_marg': 0.05,
                                      'rig_marg': 0.85,
                                      'bot_marg': 0.05,
                                      'top_marg': 0.95
                                      },
                      }
    }

SIZES = DEFAULT['sizes']
STYLES = DEFAULT['styles']
COLORS = STYLES['color']
ALPHAS = STYLES['alpha']

COLOR_LIST = [COLORS['red'], COLORS['teal'], COLORS['magenta'],
              COLORS['stone'], COLORS['green'], COLORS['purple'],
              COLORS['blue'], COLORS['light gray'], COLORS['pink'],
              COLORS['orange'], COLORS['gray'], COLORS['yellow'],
              COLORS['black']]

MISC_COLOR_LIST = [
                   '#fb2424',
                   '#24d324',
                   '#2139d5',
                   '#21bdbd',
                   '#cf0974',
                   '#f96710',
                   '#ccc506',
                   '#780e96',
                   '#32a26e',
                   '#f89356'
                   ]

WARM_COLOR_LIST = [
                   '#82050b',
                   '#d50303',
                   '#f33f00',
                   '#f38f00',
                   '#f0d073'
                   ]

COOL_COLOR_LIST = [
                   '#b9ddb4',
                   '#65c2a5',
                   '#3287bd',
                   '#4f32bd',
                   '#84038c'
                   ]

HOT_COLOR_LIST = [
                  '#641502',
                  '#ab0b0b',
                  '#c03210',
                  '#e27123',
                  '#ffbb3e',
                  '#f6cb7b'
                  ]

WET_COLOR_LIST = [
                  '#badbee',
                  '#6cb8d0',
                  '#59ba85',
                  '#3d9e3a',
                  '#008000',
                  '#003333'
                  ]

DRY_COLOR_LIST = [
                  '#480505',
                  '#7d3e14',
                  '#ac6434',
                  '#cf9053',
                  '#c9c85b',
                  '#ebe696'
                  ]

NEON_COLOR_LIST = [
                   '#7bfc73',
                   '#b0cd42',
                   '#cd7842',
                   '#9a3d5a',
                   '#46224b'
                   ]

DIV_COLOR_LIST = (WARM_COLOR_LIST + COOL_COLOR_LIST)[::-1]

# https://www.ncl.ucar.edu/Document/Graphics/color_tables.shtml
NCL_CMAPS = pd.read_pickle(os.path.join(THIS_DIR, 'data', 'ncl_cmaps.pkl'))
NCL_CMAP_NAMES = NCL_CMAPS.columns.tolist()


def prettify_ax(ax,
                alpha=0.75,
                xlabel=None,
                ylabel=None,
                title=None,
                suptitle=False,
                matchcolor=True,
                legend='best',
                title_pad=1.025,
                length_scale=False,
                ticks=True):
    """
    Beautify a plot axis.

    :param ax: (matplotlib.axes) - original axis
    :param alpha: (float) - how transparent it is
    :param xlabel: (str) - label of x axis
    :param ylabel: (str) - label of y axis
    :param title: (str) - title of subplot
    :param suptitle: (boolean) - whether to make a figure title
    :param matchcolor: (boolean) - whether to match edgecolor with facecolor
    :param legend: (str) - location of legend
    :param title_pad: (scalar) - distance between box and title
    :param length_scale: (scalar) - whether to scale the labels based on length
    :param ticks: (boolean) - whether to modify ticks
    :return ax: (matplotlib.axes) - prettified axis
    """
    if xlabel is None:
        xlabel = plt.getp(ax, 'xlabel')

    if ylabel is None:
        ylabel = plt.getp(ax, 'ylabel')

    if title is None:
        title = plt.getp(ax, 'title')

    set_labels(ax, xlabel=xlabel, ylabel=ylabel, suptitle=suptitle,
               title=title, title_pad=title_pad, length_scale=length_scale)

    plots = plt.getp(ax, 'children')
    for plot in plots:
        if plot.axes is not None:
            try:
                if matchcolor:
                    edgecolor = plt.getp(plot, 'facecolor')
                    plt.setp(plot,
                             edgecolor=edgecolor,
                             alpha=alpha)
            except:
                plt.setp(plot, alpha=alpha)

    set_legend(ax, loc=legend)
    set_borders(ax)

    if ticks:
        set_major_grid(ax)
        set_major_ticks(ax)
        set_major_tick_labels(ax)

        set_minor_grid(ax)
        set_minor_ticks(ax)
        set_minor_tick_labels(ax)

    return ax


def prettify_bokeh(p,
                   title_size=15,
                   xlabel_size=15,
                   ylabel_size=15,
                   ytick_label_size=10,
                   xtick_label_size=10,
                   legend_size=10,
                   font='century gothic'):
    """
    Scales bokeh plot's label sizes based on figure size

    :param p: (bokeh.figure) - bokeh figure
    :param title_size: (scalar) - title size
    :param xlabel_size: (scalar) - x label size
    :param ylabel_size: (scalar) - y label size
    :param xtick_label_size: (scalar) - x tick label size
    :param ytick_label_size: (scalar) - y tick label size
    :param legend: (scalar) - size of legend labels
    :param font: (str) - font of labels
    :return p: (bokeh.figure) - bokeh figure
    """

    title_size = str(scale_it_bokeh(p, title_size, 1)) + 'pt'

    xlabel_size = str(scale_it_bokeh(p, xlabel_size, 1)) + 'pt'
    ylabel_size = str(scale_it_bokeh(p, ylabel_size, 1)) + 'pt'

    xtick_label_size = str(scale_it_bokeh(p, xtick_label_size, 1)) + 'pt'
    ytick_label_size = str(scale_it_bokeh(p, ytick_label_size, 1)) + 'pt'

    legend_size = str(scale_it_bokeh(p, legend_size, 1)) + 'pt'

    p.title.text_font_size = title_size
    p.title.text_font_style = 'normal'
    p.title.text_font = font
    p.title.align = 'left'
    p.title.offset = 5

    p.xaxis.axis_label_text_font_style = 'normal'
    p.xaxis.axis_label_text_font = font
    p.xaxis.axis_label_text_font_size = xlabel_size
    p.xaxis.major_tick_line_color = 'white'
    p.xaxis.major_label_text_font_size = xtick_label_size
    p.xaxis.axis_line_width = 0.01
    p.xaxis.minor_tick_line_color = 'white'

    p.yaxis.axis_label_standoff = 16
    p.yaxis.axis_label_text_font_style = 'normal'
    p.yaxis.axis_label_text_font = font
    p.yaxis.axis_label_text_font_size = ylabel_size
    p.yaxis.major_tick_line_color = 'white'
    p.yaxis.major_label_text_font_size = ytick_label_size
    p.yaxis.minor_tick_line_color = 'white'
    p.yaxis.axis_line_width = 0.01

    p.grid.grid_line_dash = 'solid'

    p.legend.location = 'top_left'
    p.legend.background_fill_alpha = 0
    p.legend.border_line_alpha = 0
    p.legend.label_text_font_size = legend_size

    return p


def plot_map(data, lats=None, lons=None, figsize=None, ax=None, stipple=None,
             cmap='BlueWhiteOrangeRed', orientation='horizontal', wrap=True,
             data_lim=None, vmin=None, vmax=None, balance=True,
             lat1=-90, lat2=90, lon1=-180, lon2=180,
             latlim=None, lonlim=None, region=None,
             title='', title_pad=1.025, suptitle=False,
             lat_labels='auto', lon_labels='auto', length_scale=True,
             rows=1, cols=1, pos=1, fmt=None,
             cbar=True, cbar_label='', shrink=0.25,
             contourf=True, interval=None, tick_locs=None,
             data2=None, lats2=None, lons2=None,
             contour=None, contour2=None,
             clabel=True, clabel2=True,
             mask_land=False, mask_ocean=False,
             land=False, ocean=False, coastlines=True, rivers=False,
             countries=False, states=False, lakes=False,
             projection=None, central_longitude=0, tight_layout='auto',
             dpi=DEFAULT['dpi'], save='', close=True, returnplot=False,
             **kwargs
             ):
    """
    Makes a map on a subplot.

    :param data: (array) - data to be mapped
    :param lats: (array) - array of latitudes
    :param lons: (array) - array of longitudes
    :param figsize: (str/tup) - wide/tall/auto or tuple width x height of fig
    :param ax: (mpl.axes) - plot axis
    :param stipple: (array) - array of values to be stippled
    :param cmap: (str) - color map
    :param orientation: (str) - orientation of color bar
    :param wrap: (boolean) - fill missing data at prime meridian
    :param data_lim: (tup) - shortcut for vmin and vmax
    :param vmin: (scalar) - lower limit of color bar
    :param vmax: (scalar) - upper limit of color bar
    :param lat1: (scalar) lower limit of latitude
    :param lat2: (scalar) upper limit of latitude
    :param lon1: (scalar) left limit of longitude
    :param lon2: (scalar) right limit of longitude
    :param latlim: (tuple) shortcut for lat1 and lat2
    :param lonlim: (tuple) shortcut for lon1 and lon2
    :param region: (str) region to quickly subset lat and lon extent (na or us)
    :param title: (str) - title of subplot
    :param title_pad: (scalar) - distance between box and title
    :param suptitle: (boolean) - whether to make a figure title
    :param lat_labels: (array) - list of latitudes to show on map
    :param lon_labels: (array) - list of longitudes to show on map
    :param length_scale: (scalar) - whether to scale the labels based on length
    :param rows: (int) - number of rows for subplots
    :param cols: (int) - number of columns for subplots
    :param pos: (int) - position of current subplot
    :param fmt: (str) - format of color bar labels
    :param cbar: (boolean) - whether to show color bar
    :param cbar_label: (str) - label of color bar
    :param shrink: (scalar) - how much to shrink the color bar
    :param contourf: (boolean) - whether to cartoonize colormap
    :param interval: (scalar) - interval of tick marks on color bar
    :param tick_locs: (array) - input own tick marks on color bar
    :param data2: (array) - contours to be mapped
    :param lats2: (array) - array of contour latitudes
    :param lons2: (array) - array of contour longitudes
    :param contour: (array) - list of values to contour with solid line
    :param contour2: (array) - list of values to contour with dashed line
    :param clabel: (boolean) - whether to show value on solid contours
    :param clabel2: (boolean) - whether to show value on dashed contours
    :param mask_land: (boolean) - whether to mask land
    :param mask_ocean: (boolean) - whether to mask ocean
    :param land: (boolean) - whether to color fill land
    :param ocean: (boolean) - whether to color fill land
    :param coastlines: (boolean) - whether to draw coastline
    :param rivers: (boolean) - whether to draw rivers
    :param countries: (boolean) - whether to draw country borders
    :param states: (boolean) - whether to draw state borders
    :param lakes: (boolean) - whether to color fill lakes
    :param projection: (cartopy.crs) - projection of map
    :param central_longitude: (scalar) - longitude to center the map on
    :param tight_layout: (str) - on or auto adjust layout of subplots
    :param dpi: (int) - dots per inch to save the figure
    :param save: (str) - if filename is input, will save an image file
    :param close: (boolean) - whether to close figure after saving
    :param returnplot: (boolean) - whether to return plotted line
    :param kwargs: (kwargs) - additional keyword arguments
    :return ax: (mpl.axes) - plot axis
    :return plot: (mpl.axes) - optional image plot
    """
    from ahh.ext import get_ocean_mask
    import cartopy.util

    if isinstance(data, xr.Dataset):
        raise Exception('Please subselect a variable from xr.Dataset!')

    if isinstance(data, xr.DataArray):
        if lats is None:
            lats = data.lat.values
        if lons is None:
            lons = data.lon.values
        data = data.to_masked_array()

    if isinstance(lons, xr.DataArray):
        lons = lons.values

    if isinstance(lons, xr.DataArray):
        lats = lats.values

    if lons is None or lats is None:
        raise Exception('Missing lats and lons!')

    if data2 is None:
        data2 = data

    ndim = data.ndim
    if ndim > 2:
        raise Exception('Data must be 2D, {0}D data was input!'.format(ndim))

    if mask_ocean:
        data, lons = get_ocean_mask(data, lats, lons, apply_mask=True)
    elif mask_land:
        data, lons = get_ocean_mask(data, lats, lons,
                                    reverse=True, apply_mask=True)

    projection = _get_projection_logic(projection, lons, central_longitude)

    if lons2 is None and lats2 is None:
        lats2, lons2 = lats, lons
    else:
        lons2 -= central_longitude

    lat1, lat2, lon1, lon2 = _get_lat_lon_lim_logic(latlim, lonlim,
                                                    lat1, lat2, lon1, lon2,
                                                    region=region,
                                                    central_longitude=
                                                    central_longitude)

    _set_figsize_logic(figsize=figsize, rows=rows,
                       cols=cols, pos=pos, dpi=dpi)

    if ax is None:
        ax = plt.subplot(rows, cols, pos, projection=projection)

    if wrap:
        try:
            data, lons = cartopy.util.add_cyclic_point(data, coord=lons)
        except:
            print('Unable to wrap!')

    ax.set_extent([lon1, lon2, lat1, lat2], projection)

    _add_features(ax, land, ocean, coastlines,
                  states, countries, lakes, rivers)

    set_latlons(ax, central_longitude=central_longitude,
                lat_labels=lat_labels, lon_labels=lon_labels)

    if contourf:
        try:
            contourf[0]
            base, base2 = _get_bases_logic(contourf)
            vmin, vmax = _get_vmin_vmax_logic(data=contourf,
                                              base=base2,
                                              vmin=vmin,
                                              vmax=vmax,
                                              data_lim=data_lim)
            if tick_locs is None:
                tick_locs = contourf
        except:
            base, base2 = _get_bases_logic(data)
            vmin, vmax = _get_vmin_vmax_logic(data=data,
                                              base=base2,
                                              vmin=vmin,
                                              vmax=vmax,
                                              data_lim=data_lim)
            vmin, vmax = _balance_logic(balance, vmin, vmax)

        if interval is None:
            interval = base

        oom = get_order_mag(np.abs(vmax) - np.abs(vmin))
        interval = _get_interval_logic(interval=interval,
                                       vmin=vmin, vmax=vmax,
                                       base=base, oom=oom)

        try:
            contourf[0]
        except:
            contourf = np.arange(vmin, vmax + interval, interval)
            vmin, vmax = _fix_vmin_vmax_logic(vmin=vmin,
                                              vmax=vmax,
                                              data=contourf,
                                              interval=interval)
            contourf, interval = _fix_contourf_logic(contourf=contourf,
                                                     interval=interval,
                                                     vmin=vmin,
                                                     vmax=vmax)

        fmt = _get_fmt_logic(fmt=fmt, interval=interval)

        cmap = get_cmap(cmap, n=len(contourf))
        (tick_locs,
            cbar_count) = _get_tick_locs_cbar_count_logic(tick_locs=tick_locs,
                                                          vmin=vmin,
                                                          vmax=vmax,
                                                          interval=interval)

        im = ax.contourf(lons, lats, data, levels=contourf, extend='both',
                         transform=projection, cmap=cmap,
                         vmin=vmin, vmax=vmax, **kwargs)
        drawedges = True
    else:
        base, base2 = _get_bases_logic(data)
        vmin, vmax = _get_vmin_vmax_logic(data=data,
                                          base=base2,
                                          vmin=vmin,
                                          vmax=vmax,
                                          data_lim=data_lim)

        vmin, vmax = _balance_logic(balance, vmin, vmax)

        cmap = get_cmap(cmap, n=100)
        im = ax.pcolormesh(lons, lats, data, transform=projection,
                           cmap=cmap, vmin=vmin, vmax=vmax, **kwargs)
        drawedges = False

    if cbar:
        set_cbar(ax, im, label=cbar_label, drawedges=drawedges,
                 shrink=shrink, orientation=orientation,
                 fmt=fmt, tick_locs=tick_locs)

    if stipple:
        ax.contourf(lons2, lats2, data2, stipple, colors='none',
                    hatches=['.', '.', ' '],
                    transform=projection, **kwargs)

    _set_contour_logic(ax, lons2, lats2, data2, contour,
                       projection, fmt, clabel)
    _set_contour_logic(ax, lons2, lats2, data2, contour2,
                       projection, fmt, clabel2)

    set_labels(ax, title=title, title_pad=title_pad,
               length_scale=length_scale, suptitle=suptitle)
    set_borders(ax)

    _save_logic(save=save, tight_layout=tight_layout, close=close,
                dpi=dpi, pos=pos, rows=rows, cols=cols)

    if returnplot:
        return ax, im
    else:
        return ax


def plot_bounds(ax, lat1=-90, lat2=90, lon1=-180, lon2=180,
                latlim=None, lonlim=None,
                color='k', linestyle='solid', linewidth=1.25,
                fill=False, alpha=0.75, projection=None,
                tight_layout='on', dpi=DEFAULT['dpi'], save='',
                close=True, **kwargs):
    """
    Plot a bounded region on a map. Default is a rectangle with black outlines.

    :param ax: (matplotlib.axes) - original axis
    :param lat1: (float) - a latitudinal bound (can be any order)
    :param lat2: (float) - another latitudinal bound (can be any order)
    :param lon1: (float) - a longitudinal bound (can be any order)
    :param lon2: (float) - another longitudinal bound (can be any order)
    :param latlim: (tuple) shortcut for lat1 and lat2
    :param lonlim: (tuple) shortcut for lon1 and lon2
    :param color: (str) - matplotlib abbrieviation of color
    :param linestyle: (str) - solid, dashed, dashdot, or dotted linestyle
    :param linewidth: (scalar) - how thick line is
    :param fill: (boolean) - whether to color in the region
    :param alpha: (float) - how transparent it is
    :param projection: (cartopy.crs) - map projection
    :param tight_layout: (str) - on or auto adjust layout of subplots
    :param dpi: (int) - dots per inch to save the figure
    :param save: (str) - save figure if string is specified
    :param kwargs: (kwargs) - additional keyword arguments
    :param close: (boolean) - whether to close figure after saving
    """
    projection = _get_projection_logic(projection)

    lat1, lat2, lon1, lon2 = _get_lat_lon_lim_logic(latlim, lonlim,
                                                    lat1, lat2, lon1, lon2)

    width = lon2 - lon1
    height = lat2 - lat1

    ax.add_patch(mpatches.Rectangle(xy=[lon1, lat1],
                                    width=width,
                                    height=height,
                                    facecolor=color,
                                    edgecolor=color,
                                    linestyle=linestyle,
                                    linewidth=linewidth,
                                    alpha=alpha,
                                    transform=projection,
                                    fill=fill, **kwargs
                                    )
                 )

    _save_logic(save=save, tight_layout=tight_layout, close=close,
                dpi=dpi, pos=1, rows=1, cols=1)


def plot_line(x, y=None, figsize=None,
              ax=None, xlim=None, ylim=None,
              stats=False,
              norm=False, anom=False, norm_anom=False, cumsum=False,
              color=COLORS['red'], alpha=ALPHAS['translucent'],
              inherit=True, label='', xlabel='', ylabel='', title='',
              suptitle=False,
              title_pad=0.965, length_scale=True, linewidth=1, linestyle='-',
              xscale='linear', yscale='linear', minor_date_ticks=True,
              rows=1, cols=1, pos=1, label_inline=False,
              sharex=None, sharey=None,
              twinx=None, twiny=None, aligned=True,
              xinvert=False, yinvert=False, legend=None,
              projection=DEFAULT['projection'],
              tight_layout='auto', dpi=DEFAULT['dpi'],
              save='', close=True, returnplot=False, **kwargs):
    """
    Draw a line on a subplot. Use other functions for full customizability.

    :param x: (arr) - input x array
    :param y: (arr) - input y array
    :param figsize: (str/tup) - wide/tall/auto or tuple width x height of fig
    :param ax: (mpl.axes) - plot axis
    :param xlim: (tup) - left and right x axis limit in a tuple, respectively
    :param ylim: (tup) - left and right y axis limit in a tuple, respectively
    :param stats: (boolean/str) - whether to show stats and if str, the loc
    :param norm: (boolean) - whether to normalize the y
    :param anom: (boolean) - whether to subtract the average of y from y
    :param norm_anom: (boolean) - whether to get the normalized anomaly of y
    :param cumsum: (boolean) - whether to take the cumulative sum of y
    :param color: (str) - color of the plotted line
    :param alpha: (scalar/str) - transparency of the plotted line
    :param inherit: (boolean) - whether to inherit previous labels
    :param label: (str) - label of line to be used in legend
    :param xlabel: (str) - label of x axis
    :param ylabel: (str) - label of y axis
    :param title: (str) - title of subplot
    :param title_pad: (scalar) - distance between box and title
    :param suptitle: (boolean) - whether to make a figure title
    :param length_scale: (scalar) - whether to scale the labels based on length
    :param linewidth: (scalar) - width of the plotted line
    :param linestyle: (str) - style of the plotted line
    :param xscale: (str) - linear or log scale of x axis
    :param yscale: (str) - linear or log scale of y axis
    :param minor_date_ticks: (str) - whether to have date ticks on top axis
    :param rows: (int) - number of rows for subplots
    :param cols: (int) - number of columns for subplots
    :param pos: (int) - position of current subplot
    :param label_inline: (scalar) - whether to label in line; x-value of label
    :param sharex: (mpl.axes) - share x axis ticks with another subplot
    :param sharey: (mpl.axes) - share y axis ticks with another subplot
    :param twinx: (mpl.axes) - share x axis and have another y axis
    :param twiny: (mpl.axes) - share x axis and have another x axis
    :param aligned: (boolean) - whether to keep left and right ticks aligned
    :param xinvert: (boolean) - whether to flip x axis
    :param yinvert: (boolean) - whether to flip y axis
    :param legend: (str) - location of legend
    :param projection: (cartopy.crs) - projection of plotted line
    :param tight_layout: (str) - on or auto adjust layout of subplots
    :param dpi: (int) - dots per inch to save the figure
    :param save: (str) - if filename is input, will save an image file
    :param close: (boolean) - whether to close figure after saving
    :param returnplot: (boolean) - whether to return plotted line
    :param kwargs: (kwargs) - additional keyword arguments
    :return ax: (mpl.axes) - plot axis
    :return plot: (mpl.axes) - optional line plot
    """
    _set_figsize_logic(figsize=figsize, rows=rows,
                       cols=cols, pos=pos, dpi=dpi)

    x = _get_dt_from_pd_logic(x)
    x, xtext, xticklabels = _get_xtext_logic(x=x)
    x, y = _get_x_to_y_logic(x=x, y=y)
    y = _get_stats_logic(ax, y, norm=norm, anom=anom,
                         norm_anom=norm_anom, cumsum=cumsum)

    origin_xlim, xlim = _get_xlim_logic(x, xlim)
    origin_ylim, ylim = _get_ylim_logic(y, ylim)

    ax, rows, cols = _get_ax_logic(ax=ax, twinx=twinx, twiny=twiny,
                                   rows=rows, cols=cols, pos=pos,
                                   projection=projection)

    plot = ax.plot(x, y, **kwargs)

    if inherit:
        ax, xlabel, ylabel, title, xlim, ylim = \
            set_inherited(ax, xlabel, ylabel, title,
                          xlim, ylim, origin_xlim, origin_ylim)

    linewidth = scale_it(ax, linewidth, 0.2)

    plt.setp(plot, color=color, alpha=alpha, label=label,
             linewidth=linewidth, linestyle=linestyle,
             solid_capstyle='round', solid_joinstyle='round',
             dash_capstyle='round', dash_joinstyle='round')

    # must be after label
    if label is not None and label_inline:
        if not isinstance(label_inline, bool):
            set_inline_label(ax, plot, xval=label_inline)
        else:
            set_inline_label(ax, plot)

    if projection is not None:
        plt.setp(plot, transform=projection)

    set_axes(ax, xlim=xlim, ylim=ylim,
             xscale=xscale, yscale=yscale,
             xinvert=xinvert, yinvert=yinvert)

    #  need ax and ylim set
    _show_stats_logic(ax, y, stats)

    _settings_logic(ax=ax,
                    x=x,
                    twinx=twinx,
                    twiny=twiny,
                    xticks=None,
                    xlabel=xlabel,
                    ylabel=ylabel,
                    title=title,
                    title_pad=title_pad,
                    suptitle=suptitle,
                    aligned=aligned,
                    length_scale=length_scale,
                    xtext=xtext,
                    xticklabels=xticklabels,
                    minor_date_ticks=minor_date_ticks)

    set_legend(ax, loc=legend)

    rows, cols = _set_share_logic(ax=ax, rows=rows, cols=cols,
                                  sharex=sharex, sharey=sharey,
                                  xlabel=xlabel, ylabel=ylabel)

    _save_logic(save=save, tight_layout=tight_layout, close=close,
                dpi=dpi, pos=pos, rows=rows, cols=cols)

    if returnplot:
        return ax, plot
    else:
        return ax


def plot_bar(x, y=None, figsize=None, ax=None, xlim=None, ylim=None,
             stats=False,
             norm=False, anom=False, norm_anom=False, cumsum=False,
             matchcolor=True, color=None, facecolor=COLORS['red'],
             edgecolor=COLORS['red'], alpha=ALPHAS['semi opaque'],
             linewidth=0.25, linestyle='-', title_pad=0.965, length_scale=True,
             inherit=True, label='', xlabel='', ylabel='', title='',
             suptitle=False,
             width='auto', height=None, align='edge',
             xscale='linear', yscale='linear', minor_date_ticks=True,
             rows=1, cols=1, pos=1, orientation='vertical',
             sidebar_count=0, sidebar_pos=1, bar_vals=None,
             sharex=None, sharey=None,
             twinx=None, twiny=None, aligned=True,
             xinvert=False, yinvert=False, legend=None,
             tight_layout='auto', dpi=DEFAULT['dpi'],
             save='', close=True, returnplot=False, **kwargs):
    """
    Draw bars on a subplot. Use other functions for full customizability.
    :param x: (arr) - input x array
    :param y: (arr) - input y array
    :param xlim: (tup) - left and right x axis limit in a tuple, respectively
    :param ylim: (tup) - left and right y axis limit in a tuple, respectively
    :param figsize: (str/tup) - wide/tall/auto or tuple width x height of fig
    :param ax: (mpl.axes) - plot axis
    :param stats: (boolean/str) - whether to show stats and if str, the loc
    :param norm: (boolean) - whether to normalize the y
    :param anom: (boolean) - whether to subtract the average of y from y
    :param norm_anom: (boolean) - whether to get the normalized anomaly of y
    :param cumsum: (boolean) - whether to take the cumulative sum of y
    :param matchcolor: (boolean) - whether to match edgecolor with facecolor
    :param color: (str) - facecolor and edgecolor of plotted bar
    :param facecolor: (str) - facecolor of plotted bar
    :param edgecolor: (str) - edgecolor of plotted bar
    :param alpha: (scalar/str) - transparency of the plotted bar
    :param linewidth: (scalar) - width of plotted bar edges
    :param linestyle: (str) - style of the plotted bar edges
    :param title_pad: (scalar) - distance between box and title
    :param suptitle: (boolean) - whether to make a figure title
    :param inherit: (boolean) - whether to inherit previous labels
    :param length_scale: (scalar) - whether to scale the labels based on length
    :param label: (str) - label of line to be used in legend
    :param xlabel: (str) - label of x axis
    :param ylabel: (str) - label of y axis
    :param title: (str) - title of subplot
    :param width: (str/scalar) - width of plotted bars when vertical
    :param height: (str/scalar) - height of plotted bars when horizontal
    :param align: (str) - whether to align plotted bar on center or edge
    :param xscale: (str) - linear or log scale of x axis
    :param yscale: (str) - linear or log scale of y axis
    :param minor_date_ticks: (str) - whether to have date ticks on top axis
    :param rows: (int) - number of rows for subplots
    :param cols: (int) - number of columns for subplots
    :param pos: (int) - position of current subplot
    :param orientation: (str) - whether to have horizontal or vertical bars
    :param sidebar_count: (int) - how many bars per x
    :param sidebar_pos: (int) - the location of the side bar
    :param bar_vals: (str) - format of bar vals
    :param sharex: (mpl.axes) - share x axis ticks with another subplot
    :param sharey: (mpl.axes) - share y axis ticks with another subplot
    :param twinx: (mpl.axes) - share x axis and have another y axis
    :param twiny: (mpl.axes) - share x axis and have another x axis
    :param aligned: (boolean) - whether to keep left and right ticks aligned
    :param xinvert: (boolean) - whether to flip x axis
    :param yinvert: (boolean) - whether to flip y axis
    :param legend: (str) - location of legend
    :param tight_layout: (str) - on or auto adjust layout of subplots
    :param dpi: (int) - dots per inch to save the figure
    :param save: (str) - if filename is input, will save an image file
    :param close: (boolean) - whether to close figure after saving
    :param returnplot: (boolean) - whether to return plotted bar
    :return ax: (mpl.axes) - plot axis
    :return plot: (mpl.axes) - optional bar plot
    """
    _set_figsize_logic(figsize=figsize, rows=rows,
                       cols=cols, pos=pos, dpi=dpi,
                       sidebar_pos=sidebar_pos)

    x = _get_dt_from_pd_logic(x)
    x, xtext, xticklabels = _get_xtext_logic(x=x)
    x, y = _get_x_to_y_logic(x=x, y=y)
    y = _get_stats_logic(ax, y, norm=norm, anom=anom,
                         norm_anom=norm_anom, cumsum=cumsum)
    origin_ylim, ylim = _get_ylim_logic(y, ylim)

    facecolor, edgecolor = _get_color_logic(color,
                                            facecolor,
                                            edgecolor,
                                            matchcolor)

    if width == 'auto':
        width = _get_width_logic(x)

    if sidebar_count > 1:
        if facecolor is not COLORS['red']:
            (width, align, x_list) = get_side_bars_recs(x,
                                                        sidebar_count,
                                                        colors=False)
        else:
            (width, align,
                x_list, colors) = get_side_bars_recs(x,
                                                     sidebar_count,
                                                     colors=True)
            if facecolor is COLORS['red']:
                color = colors[sidebar_pos - 1]
        x = x_list[sidebar_pos - 1]

    ax, rows, cols = _get_ax_logic(ax=ax, twinx=twinx, twiny=twiny,
                                   rows=rows, cols=cols, pos=pos)

    # set width first
    if xtext:
        align = 'center'

    origin_xlim, xlim = _get_xlim_logic(x, xlim, pad=width, align=align)

    if sidebar_count > 1 and sidebar_count % 2 == 0:
        xlim = (xlim[0] - width * sidebar_count,
                xlim[1] + width * (sidebar_count - 1))
    elif sidebar_count > 1 and sidebar_count % 2 != 0:
        xlim = (xlim[0] - width * sidebar_count,
                xlim[1])

    if 'vertical' in orientation:
        plot = ax.bar(x, y, align=align, label=label, **kwargs)
    elif 'horizontal' in orientation:
        plot = ax.barh(x, y, height=height, align=align,
                       label=label, **kwargs)

    if inherit:
        ax, xlabel, ylabel, title, xlim, ylim = \
            set_inherited(ax, xlabel, ylabel, title,
                          xlim, ylim, origin_xlim, origin_ylim)

    linewidth = scale_it(ax, linewidth, 0.2)

    plt.setp(plot, facecolor=facecolor, edgecolor=edgecolor, alpha=alpha,
             linestyle=linestyle, width=width, linewidth=linewidth)

    set_axes(ax,
             xlim=xlim,
             ylim=ylim,
             xscale=xscale,
             yscale=yscale,
             xinvert=xinvert,
             yinvert=yinvert)

    if bar_vals != False:
        if sidebar_count == 0:
            sidebar_count = 1
        if (len(x) < (50 / sidebar_count * 1.7) and
                sidebar_pos == sidebar_count):
            if bar_vals is None:
                interval = np.median(y)
                bar_vals = _get_fmt_logic(fmt=bar_vals, interval=interval)
            set_bar_vals(ax, fmt=bar_vals, orientation='auto',
                         yinvert=yinvert)

    _settings_logic(ax=ax,
                    x=x,
                    twinx=twinx,
                    twiny=twiny,
                    xticks=None,
                    xlabel=xlabel,
                    ylabel=ylabel,
                    title=title,
                    title_pad=title_pad,
                    suptitle=suptitle,
                    aligned=aligned,
                    length_scale=length_scale,
                    xtext=xtext,
                    xticklabels=xticklabels,
                    minor_date_ticks=minor_date_ticks)

    rows, cols = _set_share_logic(ax=ax, rows=rows, cols=cols,
                                  sharex=sharex, sharey=sharey,
                                  xlabel=xlabel, ylabel=ylabel)
    set_legend(ax, loc=legend)

    #  need ax and ylim set and bar vals shifted
    _show_stats_logic(ax, y, stats)

    _save_logic(save=save, tight_layout=tight_layout, close=close,
                dpi=dpi, pos=pos, rows=rows, cols=cols)

    if returnplot:
        return ax, plot
    else:
        return ax


def plot_scatter(x, y=None, figsize=None, ax=None,
                 xlim=None, ylim=None,
                 stats=False,
                 norm=False, anom=False, norm_anom=False, cumsum=False,
                 matchcolor=True,
                 data_lim=None, vmin=None, vmax=None,
                 color=None, facecolor=COLORS['red'], edgecolor=COLORS['red'],
                 alpha=ALPHAS['translucent'],
                 linewidth=0.25, size=5, marker='o', s=None,
                 c=None, cbar=True, cbar_label='', shrink=0.35, cmap=None,
                 orientation='horizontal', interval=None, tick_locs=None,
                 inherit=True, label='', xlabel='', ylabel='',
                 title='', title_pad=0.965, suptitle=False, length_scale=True,
                 xscale='linear', yscale='linear', minor_date_ticks=True,
                 rows=1, cols=1, pos=1, fmt=None, pad=0.225,
                 sharex=None, sharey=None,
                 twinx=None, twiny=None, aligned=True,
                 xinvert=False, yinvert=False, legend=None,
                 projection=DEFAULT['projection'],
                 tight_layout='auto', dpi=DEFAULT['dpi'],
                 save='', close=True, returnplot=False, **kwargs):
    """
    Draw markers on a subplot. Use other functions for full customizability.

    :param x: (arr) - input x array
    :param y: (arr) - input y array
    :param figsize: (str/tup) - wide/tall/auto or tuple width x height of fig
    :param ax: (mpl.axes) - plot axis
    :param stats: (boolean/str) - whether to show stats and if str, the loc
    :param xlim: (tup) - left and right x axis limit in a tuple, respectively
    :param ylim: (tup) - left and right y axis limit in a tuple, respectively
    :param norm: (boolean) - whether to normalize the y
    :param anom: (boolean) - whether to subtract the average of y from y
    :param norm_anom: (boolean) - whether to get the normalized anomaly of y
    :param cumsum: (boolean) - whether to take the cumulative sum of y
    :param data_lim: (tup) - shortcut for vmin and vmax
    :param vmin: (scalar) - lower limit of color bar
    :param vmax: (scalar) - upper limit of color bar
    :param matchcolor: (boolean) - whether to match edgecolor with facecolor
    :param color: (str) - facecolor and edgecolor of plotted scatter marker
    :param facecolor: (str) - facecolor of plotted scatter marker
    :param edgecolor: (str) - edgecolor of plotted scatter marker
    :param alpha: (scalar/str) - transparency of the plotted scatter marker
    :param linewidth: (scalar) - width of plotted scatter marker edges
    :param size: (scalar) - size of plotted scatter marker
    :param marker: (scalar) - style of plotted scatter marker
    :param s: (arr) - array to map size to
    :param c: (arr) - array to map color to
    :param cbar: (boolean) - whether to show color bar
    :param cbar_label: (str) - label of color bar
    :param shrink: (scalar) - size of color bar
    :param cmap: (str) - color map
    :param orientation: (str) - orientation of color bar
    :param interval: (scalar) - interval of tick marks on color bar
    :param tick_locs: (array) - input own tick marks on color bar
    :param inherit: (boolean) - whether to inherit previous labels
    :param label: (str) - label of line to be used in legend
    :param xlabel: (str) - label of x axis
    :param ylabel: (str) - label of y axis
    :param title: (str) - title of subplot
    :param title_pad: (scalar) - distance between box and title
    :param suptitle: (boolean) - whether to make a figure title
    :param length_scale: (scalar) - whether to scale the labels based on length
    :param xscale: (str) - linear or log scale of x axis
    :param yscale: (str) - linear or log scale of y axis
    :param minor_date_ticks: (str) - whether to have date ticks on top axis
    :param rows: (int) - number of rows for subplots
    :param cols: (int) - number of columns for subplots
    :param pos: (int) - position of current subplot
    :param fmt: (str) - format of color bar labels
    :param pad: (scalar) - padding of color bar from plot
    :param sharex: (mpl.axes) - share x axis ticks with another subplot
    :param sharey: (mpl.axes) - share y axis ticks with another subplot
    :param twinx: (mpl.axes) - share x axis and have another y axis
    :param twiny: (mpl.axes) - share x axis and have another x axis
    :param aligned: (boolean) - whether to keep left and right ticks aligned
    :param xinvert: (boolean) - whether to flip x axis
    :param yinvert: (boolean) - whether to flip y axis
    :param legend: (str) - location of legend
    :param projection: (cartopy.crs) - projection of plotted scatter
    :param tight_layout: (str) - on or auto adjust layout of subplots
    :param dpi: (int) - dots per inch to save the figure
    :param save: (str) - if filename is input, will save an image file
    :param close: (boolean) - whether to close figure after saving
    :param returnplot: (boolean) - whether to return plotted scatter
    :param kwargs: (kwargs) - additional keyword arguments
    :return ax: (mpl.axes) - plot axis
    :return plot: (mpl.axes) - optional scatter plot
    """
    _set_figsize_logic(figsize=figsize, rows=rows,
                       cols=cols, pos=pos, dpi=dpi)

    x = _get_dt_from_pd_logic(x)
    x, xtext, xticklabels = _get_xtext_logic(x=x)
    x, y = _get_x_to_y_logic(x, y)
    y = _get_stats_logic(ax, y, norm=norm, anom=anom,
                         norm_anom=norm_anom, cumsum=cumsum)
    origin_ylim, ylim = _get_ylim_logic(y, ylim)
    origin_xlim, xlim = _get_xlim_logic(x, xlim)

    ax, rows, cols = _get_ax_logic(ax=ax, twinx=twinx, twiny=twiny,
                                   rows=rows, cols=cols, pos=pos,
                                   projection=projection)

    if c is not None:
        base, base2 = _get_bases_logic(c)
        vmin, vmax = _get_vmin_vmax_logic(data=c, base=base2,
                                          vmin=vmin, vmax=vmax,
                                          data_lim=data_lim)

        oom = get_order_mag(vmax - vmin)
        interval = _get_interval_logic(interval=interval,
                                       vmin=vmin, vmax=vmax,
                                       base=base, oom=oom)
        fmt = _get_fmt_logic(fmt=fmt, interval=interval)
        vmin, vmax = _fix_vmin_vmax_logic(vmin=vmin, vmax=vmax, data=c,
                                          interval=interval)
        (tick_locs,
            cbar_count) = _get_tick_locs_cbar_count_logic(tick_locs=tick_locs,
                                                          vmin=vmin, vmax=vmax,
                                                          interval=interval)
        if cmap is None:
            cmap = 'viridis'

        cmap = get_cmap(cmap, cbar_count)
        edgecolor = None
        facecolor = COLORS['gray']

    if s is not None:
        size = np.abs(s)
    else:
        size = scale_it(ax, np.abs(size), 25, exp=False)

    plot = ax.scatter(x, y, marker=marker,
                      linewidths=linewidth,
                      s=size, c=c, cmap=cmap,
                      vmin=vmin, vmax=vmax,
                      **kwargs
                      )

    if cbar and cmap is not None:
        set_cbar(ax, plot, label=cbar_label, fmt=fmt,
                 pad=pad, shrink=shrink,
                 tick_size=8, label_size=10,
                 orientation=orientation,
                 tick_locs=tick_locs)
    else:
        if color is not None:
            facecolor = color
            edgecolor = color
        if matchcolor:
            edgecolor = facecolor

    if inherit:
        ax, xlabel, ylabel, title, xlim, ylim = \
            set_inherited(ax, xlabel, ylabel, title,
                          xlim, ylim, origin_xlim, origin_ylim)

    linewidth = scale_it(ax, linewidth, 0.2)

    if projection is not None:
        plt.setp(plot, transform=projection)

    plt.setp(plot, facecolor=facecolor, edgecolor=edgecolor,
             alpha=alpha, label=label)

    set_axes(ax, xlim=xlim, ylim=ylim,
             xscale=xscale, yscale=yscale,
             xinvert=xinvert, yinvert=yinvert)

    #  need ax and ylim set
    _show_stats_logic(ax, y, stats)

    _settings_logic(ax=ax,
                    x=x,
                    twinx=twinx,
                    twiny=twiny,
                    xticks=None,
                    xlabel=xlabel,
                    ylabel=ylabel,
                    title=title,
                    title_pad=title_pad,
                    suptitle=suptitle,
                    aligned=aligned,
                    length_scale=length_scale,
                    xtext=xtext,
                    xticklabels=xticklabels,
                    minor_date_ticks=minor_date_ticks)

    rows, cols = _set_share_logic(ax=ax, rows=rows, cols=cols,
                                  sharex=sharex, sharey=sharey,
                                  xlabel=xlabel, ylabel=ylabel)

    set_legend(ax, loc=legend)

    _save_logic(save=save, tight_layout=tight_layout, close=close,
                dpi=dpi, pos=pos, rows=rows, cols=cols)

    if returnplot:
        return ax, plot
    else:
        return ax


def plot(*plot_args, **plot_kwargs):
    """
    Plot multiple line/bar/scatter plots at once using this syntax
    x, y, 'label', 'ptype/color/linestyle/marker'

    Example - plot a red dashed line with circle marker and a black bar plot
    plot(x, y, 'line plot', 'line/red/--/o', x2, y2, 'bar plot', 'bar/black')

    Equivalent shorthand
    plot(x, y, 'line plot', 'l/r/--/o', x2, y2, 'bar plot', 'b/k')

    Example 2 - plot a green solid line, blue bar plot, yellow scatter plot
                with a title, ylabel, and xlabel
    plot(x, y, 'labl', 'l/r', x2, y2, 'labl2', 'b/b', x3, y3, 'labl3', 's/y',
         title='title', ylabel='a ylabel', xlabel='one xlabel')

    Example 3 - adjust figsize while still stacking all the plots
    plot(x, y, 'labl', 'l', x2, y2, 'labl2', 'b', figsize=(8, 5), stack=True)

    Example 4 - plot two separate figures
    plot(x, y, 'labl', 'l', x2, y2, 'labl2', 'b', stack=False)

    :param stack: (bool) whether to keep stacking if figsize input is provided
    :return ax_list: (list) - list of axes
    """
    plot_inputs = zip(plot_args[::4],
                      plot_args[1::4],
                      plot_args[2::4],
                      plot_args[3::4])

    figsize = plot_kwargs.get('figsize', 'na')
    stack = plot_kwargs.get('stack', True)

    if figsize == 'na':
        set_figsize()

    ax_list = []

    for i, plot_input in enumerate(plot_inputs):
        if stack and i > 0:
            plot_kwargs['figsize'] = 'na'
        x, y, label, style = plot_input
        ptype, color, linestyle, marker = _parse_style(style)

        vis_dict = dict(label=label, color=color,
                        linestyle=linestyle, marker=marker,
                        **plot_kwargs)

        if ptype in ['b', 'bar']:
            _pop_keys(vis_dict, 'bar')
            ax = plot_bar(x, y, **vis_dict)
        elif ptype in ['s', 'scatter']:
            _pop_keys(vis_dict, 'scatter')
            if vis_dict['marker'] == '':
                vis_dict['marker'] = 'o'
            ax = plot_scatter(x, y, **vis_dict)
        else:
            _pop_keys(vis_dict, 'line')
            ax = plot_line(x, y, **vis_dict)

        ax_list.append(ax)

    return ax_list


def plot_hist(x=None, y=None, ptype='bar', align='edge', bar_vals=None,
              width='auto', norm=False, cumsum=False, **kwargs):
    """
    Plot histogram using plot line/bar/scatter.

    :param x: (int/arr) - number of bins or array of bin edges
    :param y: (arr) - array of items
    :param ptype: (str) - whether to plot line, bar, or scatter
    :param align: (str) - whether to align bars on edge or center
    :param bar_vals: (str) - format of bar vals
    :param width: (str/scalar) - width of plotted bars when vertical
    :param norm: (boolean) - whether to normalize the y
    :param cumsum: (boolean) - whether to take the cumulative sum of y
    :param kwargs: (kwargs) - additional keyword arguments
    :return ax: (mpl.axes) - plot axis
    """
    if y is None:
        y = x
        x = None

    try:
        int(x)
        refresh_x = x + 1
    except:
        refresh_x = 0

    if norm:
        weights = np.ones_like(y) / float(len(y))
        normed = 0
    else:
        weights = None
        normed = False

    try:
        if x is None or refresh_x:
            if not refresh_x:
                ymin = np.min(y)
                ymax = np.max(y)
                oom = get_order_mag(ymax - ymin)
                base = np.power(5, oom)
                ymin = round_to(ymin, base=base)
                ymax = round_to(ymax, base=base)
                x = np.arange(ymin, ymax, base)
            if ymin == ymax or refresh_x:
                ymin = np.min(y)  # refresh it
                ymax = np.max(y)
                if refresh_x == 0:
                    refresh_x += 7
                x = np.linspace(ymin, ymax, refresh_x)

        y = np.clip(y, np.min(x), np.max(x))
        hist_counts, bin_edges = np.histogram(y, x,
                                              normed=normed,
                                              weights=weights)
        x, y = bin_edges[:-1], hist_counts
        if width == 'auto':
            width = np.average(np.diff(x))
    except:
        text_hist = Counter(y)
        y = list(text_hist.values())
        x = list(text_hist.keys())
        align = 'center'

    if bar_vals is None:
        if not norm:
            bar_vals = '%1d'
        else:
            bar_vals = '%.2f'

    if ptype == 'bar':
        plot_bar(x, y, align=align, width=width, bar_vals=bar_vals,
                 cumsum=cumsum, **kwargs)
    elif ptype == 'scatter':
        plot_scatter(x, y, cumsum=cumsum, **kwargs)
    else:
        plot_line(x, y, cumsum=cumsum, **kwargs)


def plot_heatmap(df, figsize=None, ax=None, mask=None, mask2=None,
                 size=12, cmap='RdBu_r', orientation='vertical',
                 edgecolor=COLORS['black'],
                 xrotation=0, yrotation=0,
                 data_lim=None, vmin=None, vmax=None,
                 inherit=True, label='', xlabel='', ylabel='',
                 title='', title_pad=1.025, suptitle=False, length_scale=True,
                 xticklabels=None, yticklabels=None,
                 rows=1, cols=1, pos=1, fmt=None, pad=0.3,
                 cbar=True, cbar_label='', shrink=0.2,
                 interval=None, tick_locs=None,
                 xinvert=False, yinvert=True,
                 tight_layout='auto', dpi=DEFAULT['dpi'],
                 save='', close=True, returnplot=False, **kwargs):
    """
    Draw a heatmap on a subplot. Use other functions for full customizability.

    :param df: (pd.DataFrame) - dataframe to be converted into heatmap
    :param mask: (pd.DataFrame) - dataframe containing booleans to show text
    :param mask2: (pd.DataFrame) - dataframe containing booleans to show text
    :param size: (scalar) - size of text over masks
    :param figsize: (str/tup) - wide/tall/auto or tuple width x height of fig
    :param ax: (mpl.axes) - plot axis
    :param cmap: (str) - color map
    :param orientation: (str) - orientation of color bar
    :param data_lim: (tup) - shortcut for vmin and vmax
    :param vmin: (scalar) - lower limit of color bar
    :param vmax: (scalar) - upper limit of color bar
    :param xrotation: (scalar) - degrees to rotate x major tick labels
    :param yrotation: (scalar) - degrees to rotate y major tick labels
    :param inherit: (boolean) - whether to inherit previous labels
    :param label: (str) - label of line to be used in legend
    :param xlabel: (str) - label of x axis
    :param ylabel: (str) - label of y axis
    :param title: (str) - title of subplot
    :param title_pad: (scalar) - distance between box and title
    :param suptitle: (boolean) - whether to make a figure title
    :param length_scale: (scalar) - whether to scale the labels based on length
    :param xticklabels: (list) - manually set x major tick labels
    :param yticklabels: (list) - manually set y major tick labels
    :param rows: (int) - number of rows for subplots
    :param cols: (int) - number of columns for subplots
    :param pos: (int) - position of current subplot
    :param fmt: (str) - format of color bar labels
    :param pad: (scalar) - padding of color bar
    :param cbar: (boolean) - whether to show color bar
    :param cbar_label: (str) - label of color bar
    :param shrink: (scalar) - size of color bar
    :param interval: (scalar) - interval of tick marks on color bar
    :param tick_locs: (array) - input own tick marks on color bar
    :param xinvert: (boolean) - whether to flip x axis
    :param yinvert: (boolean) - whether to flip y axis
    :param tight_layout: (str) - on or auto adjust layout of subplots
    :param dpi: (int) - dots per inch to save the figure
    :param save: (str) - if filename is input, will save an image file
    :param close: (boolean) - whether to close figure after saving
    :param returnplot: (boolean) - whether to return plotted heatmap
    :param kwargs: (kwargs) - additional keyword arguments
    :return ax: (mpl.axes) - plot axis
    :return plot: (mpl.axes) - optional line plot
    """
    _set_figsize_logic(figsize=figsize, rows=rows,
                       cols=cols, pos=pos, dpi=dpi)

    if ax is None:
        ax = plt.subplot(rows, cols, pos)

    base, base2 = _get_bases_logic(df)
    vmin, vmax = _get_vmin_vmax_logic(data=df,
                                      base=base2,
                                      vmin=vmin,
                                      vmax=vmax,
                                      data_lim=data_lim)
    oom = get_order_mag(vmax - vmin)
    interval = _get_interval_logic(interval=interval,
                                   vmin=vmin, vmax=vmax,
                                   base=base, oom=oom)
    fmt = _get_fmt_logic(fmt=fmt, interval=interval)
    vmin, vmax = _fix_vmin_vmax_logic(vmin=vmin, vmax=vmax, data=df,
                                      interval=interval)
    (tick_locs,
        cbar_count) = _get_tick_locs_cbar_count_logic(tick_locs=tick_locs,
                                                      vmin=vmin, vmax=vmax,
                                                      interval=interval)

    cmap = get_cmap(cmap, cbar_count)
    im = ax.pcolor(df,
                   cmap=cmap,
                   vmin=vmin,
                   vmax=vmax,
                   edgecolors=edgecolor,
                   **kwargs)

    ax.set_yticks(np.arange(df.shape[0]) + 0.5, minor=False)
    ax.set_xticks(np.arange(df.shape[1]) + 0.5, minor=False)

    ax.patch.set(hatch='+',
                 edgecolor=COLORS['gray'],
                 color=COLORS['gray'],
                 alpha=0.45, lw=0.25)

    if xinvert:
        ax.invert_yaxis()

    if yinvert:
        ax.invert_yaxis()

    if xticklabels is None:
        xticklabels = df.columns

    if yticklabels is None:
        yticklabels = df.index

    set_major_tick_labels(ax,
                          xticklabels=xticklabels,
                          yticklabels=yticklabels,
                          xrotation=xrotation,
                          yrotation=yrotation)

    set_labels(ax, xlabel=xlabel, ylabel=ylabel, suptitle=suptitle,
               title=title, title_pad=title_pad, length_scale=length_scale)

    ax.grid(False)

    if cbar:
        set_cbar(ax, im, label=cbar_label, fmt=fmt,
                 pad=pad, shrink=shrink,
                 tick_size=8, label_size=10,
                 orientation=orientation,
                 tick_locs=tick_locs)

    df_nan = np.ma.masked_invalid(df)

    if mask is not None:
        _set_heatmap_mask(ax, df_nan, mask, size)

    if mask2 is not None:
        _set_heatmap_mask(ax, df_nan, mask2, size)

    _save_logic(save=save, tight_layout=tight_layout, close=close,
                dpi=dpi, pos=pos, rows=rows, cols=cols)

    if returnplot:
        return ax, im
    else:
        return ax


def plot_cbar(cmap,
              fig=None,
              left=0.05,
              bottom=0.95,
              width=0.95,
              height=0.05,
              label='',
              fmt='%1.0f',
              label_size=12,
              drawedges=True,
              label_color=COLORS['gray'],
              ticks=None,
              boundaries=None,
              tick_size=8,
              tick_color=COLORS['gray'],
              color=COLORS['black'],
              pad=0.075,
              aspect=25.5,
              shrink=0.2,
              length=0,
              tick_width=0.25,
              direction='out',
              orientation='horizontal',
              cax=None,
              **kwargs):
    """
    Plot lone color bar.

    :param cmap: (list/str) - a list containing RGB or Python/NCL cmap name
    :param fig: (boolean) - input figure
    :param left: (scalar) - left padding from figure edge
    :param bottom: (scalar) - bottom padding from figure left edge
    :param width: (scalar) - percent width of figure
    :param height: (scalar) - percent height of figure
    :param fmt: (str) - format of color bar labels
    :param label_size: (scalar) - size of color bar label
    :param label_color: (scalar) - color of color bar label
    :param ticks: (array) - input own tick marks on color bar
    :param tick_size: (scalar) - size of color bar tick labels
    :param tick_color: (scalar) - color of color bar tick labels
    :param color: (scalar) - color of color bar tick marks
    :param drawedges: (scalar) - whether to draw color edges
    :param pad: (scalar) - padding of color bar from plot
    :param aspect: (int) - aspect ratio of color bar
    :param shrink: (scalar) - size of color bar
    :param length: (scalar) - length of color bar tick marks
    :param tick_width: (scalar) - width of color bar tick marks
    :param direction: (str) - direction of color bar tick marks
    :param orientation: (str) - orientation of color bar
    :param cax: (mpl.axes) - plot axis to attach to
    :param kwargs: (kwargs) - additional keyword arguments
    :return cbar: (mpl.ColorBar) - matplotlib color bar
    """
    if fig is None:
        fig = set_figsize(8, 4)

    if boundaries is None and ticks is not None:
        boundaries = ticks

    ax = fig.add_axes([left, bottom, width, height])

    cmap = get_cmap(cmap)

    cbar = mpl.colorbar.ColorbarBase(ax, ticks=ticks,
                                     boundaries=boundaries,
                                     cmap=cmap,
                                     orientation=orientation)
    cbar.ax.tick_params(labelsize=tick_size,
                        direction=direction,
                        length=length,
                        width=tick_width,
                        tick2On=True,
                        labelcolor=label_color,
                        color=color)
    cbar.set_label(label,
                   size=label_size,
                   color=label_color)
    return cbar


def init_map(lat1=-90, lat2=90, lon1=-180, lon2=180,
             latlim=None, lonlim=None, region=None,
             rows=1, cols=1, pos=1, figsize=None, ax=None,
             title='', suptitle=False,
             length_scale=True, lat_labels='auto', lon_labels='auto',
             projection=DEFAULT['projection'], central_longitude=0,
             land=False, ocean=False, lakes=True,
             coastlines=True, states=True, countries=True, rivers=False,
             tight_layout='auto', dpi=DEFAULT['dpi'], save='', close=True):
    """
    Initialize a projected map.

    :param lat1: (scalar) lower limit of latitude
    :param lat2: (scalar) upper limit of latitude
    :param lon1: (scalar) left limit of longitude
    :param lon2: (scalar) right limit of longitude
    :param latlim: (tuple) shortcut for lat1 and lat2
    :param lonlim: (tuple) shortcut for lon1 and lon2
    :param region: (str) region to quickly subset lat and lon extent (na or us)
    :param rows: (int) - number of rows for subplots
    :param cols: (int) - number of columns for subplots
    :param pos: (int) - position of current subplot
    :param figsize: (str/tup) - wide/tall/auto or tuple width x height of fig
    :param ax: (mpl.axes) - plot axis
    :param title: (str) - title of subplot
    :param length_scale: (scalar) - whether to scale the labels based on length
    :param lat_labels: (array) - list of latitudes to show on map
    :param lon_labels: (array) - list of longitudes to show on map
    :param projection: (cartopy.crs) - projection of map
    :param central_longitude: (scalar) - longitude to center the map on
    :param land: (boolean) - whether to color fill land
    :param ocean: (boolean) - whether to color fill land
    :param lakes: (boolean) - whether to color fill lakes
    :param coastlines: (boolean) - whether to draw coastline
    :param states: (boolean) - whether to draw state borders
    :param countries: (boolean) - whether to draw country borders
    :param rivers: (boolean) - whether to draw rivers
    :param tight_layout: (str) - on or auto adjust layout of subplots
    :param dpi: (int) - dots per inch to save the figure
    :param save: (str) - if filename is input, will save an image file
    :param close: (boolean) - whether to close figure after saving
    :return ax: (mpl.axes) - plot axis
    """

    _set_figsize_logic(figsize=figsize, rows=rows,
                       cols=cols, pos=pos, dpi=dpi)

    projection = _get_projection_logic(projection)

    if ax is None:
        ax = plt.subplot(rows, cols, pos, projection=projection)

    lat1, lat2, lon1, lon2 = _get_lat_lon_lim_logic(latlim, lonlim,
                                                    lat1, lat2, lon1, lon2,
                                                    region=region,
                                                    central_longitude=
                                                    central_longitude)

    ax.set_extent([lon1, lon2, lat1, lat2], projection)

    _add_features(ax, land, ocean, coastlines,
                  states, countries, lakes, rivers)

    set_latlons(ax,
                lat_labels=lat_labels, lon_labels=lon_labels,
                central_longitude=central_longitude)

    set_labels(ax, title=title, length_scale=length_scale)

    _save_logic(save=save, tight_layout=tight_layout, close=close,
                dpi=dpi, pos=pos, rows=rows, cols=cols)

    return ax


def get_side_bars_recs(x, sidebar_count, colors=True):
    """
    Output some recommended values to show side by side bars.

    :param x: (arr) - input x array
    :param sidebar_count: (int) - how many bars side by side
    :param colors: (boolean) - whether to return colors
    :return width: (scalar) - adjusted width of color bars
    :return align: (str) - edge or center based on sidebar_count
    :return x_list: (list) - adjusted x values
    :return colors: (list) - list of colors
    """
    if sidebar_count == 0:
        raise IOError('Unable to have 0 side bars per x!')
    if sidebar_count == 1:
        if colors:
            return 0.833333333, 'center', [x], [COLOR_LIST[0]]
        else:
            return 0.833333333, 'center', [x]

    if sidebar_count % 2 == 0:
        align = 'edge'
    else:
        align = 'center'

    width = _get_width_logic(x) / sidebar_count

    x_shift_end = sidebar_count // 2
    x_shift_start = -(sidebar_count - x_shift_end)
    x_shifts = np.arange(x_shift_start, x_shift_end)
    if align is 'center':
        extra_x_shift = len(x_shifts) // 2 + 1
        x_shifts += extra_x_shift

    x_list = []
    for x_shift in x_shifts:
        try:
            x_list.append(mdates.date2num(x) + width * x_shift)
        except:
            x_list.append(x + width * x_shift)

    if colors:
        colors = COLOR_LIST[0:sidebar_count]
        return width, align, x_list, colors
    else:
        return width, align, x_list


def set_bar_vals(ax, size=7.5,
                 color=COLORS['black'],
                 alpha=ALPHAS['translucent'],
                 orientation='auto',
                 inherit_color=False,
                 pad_remover=1,
                 fmt='%d',
                 yinvert=False):
    """
    Label the rectangles in bar plots with its respective values.
    Adaptation of: "http://composition.al/blog/2015/11/29/a-better-way-to-\
    add-labels-to-bar-charts-with-matplotlib/"

    :param ax: (mpl.axes) - plot axis
    :param size: (scalar) - size of bar labels
    :param color: (str) - color of bar labels
    :param alpha: (scalar/str) - transparency of bar labels
    :param orientation: (str) - orientation of the labels
    :param inherit_color: (boolean) - whether to inherit color for labels
    :param pad_remover: (scalar): - space to remove between ylim and labels
    :param fmt: (str) - format of color bar labels
    :param yinvert (boolean) - whether to invert the y values of labels
    :return ax: (mpl.axes) - plot axis
    """
    try:
        pad_remover = scale_it(ax, pad_remover, 0.1, exp=True)

        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()

        if xmin > xmax:
            xmin, xmax = xmax, xmin

        if ymin > ymax:
            ymin, ymax = ymax, ymin

        y_height = ymax - ymin

        rects = ax.patches
        size = scale_it(ax, size, 1, exp=True) / np.log(len(rects))
        if len(rects) > 5:
            size *= 3

        if orientation is 'auto':
            if len(str(int(ymax))) > 2:
                orientation = 'vertical'
            else:
                orientation = 'horizontal'

        if orientation is 'vertical':
            rotation = 90
            height_mult = 0.02
            limit_mult = 2
        else:
            rotation = 0
            height_mult = 0.015
            limit_mult = 1

        pos_ct = 1  # to dampen future
        neg_ct = 1  # ylim increases
        orient_add = 0

        for rect in rects:
            x = plt.getp(rect, 'x')
            y = rect.get_height()
            if plt.getp(ax, 'yscale') is 'log':
                label_position = y
                if orientation is 'vertical':
                    label_position += y / 50
            else:
                label_position = y + (y_height * height_mult)

            if y < 0:
                va = 'top'
                if orientation is 'horizontal':
                    orient_add = label_position / 60
                label_position += (y_height * -2 * height_mult)
            else:
                va = 'bottom'

            if label_position >= (ymax - ymax / 5):
                ymax += (ymax * pad_remover / 6.5 /
                         pos_ct * limit_mult + orient_add)
                pos_ct += 15
            if label_position <= (ymin - ymin / 5):
                ymin += (ymin * pad_remover / 8 /
                         neg_ct * limit_mult + orient_add)
                neg_ct += 15

            if inherit_color:
                color = plt.getp(rect, 'facecolor')

            ax.set_ylim(ymin, ymax)

            if yinvert:
                label_position *= -1

            if (ymin <= y < ymax) and (xmin < x < xmax):
                ax.text(rect.get_x() + rect.get_width() / 2., label_position,
                        fmt % y, size=size, alpha=alpha, color=color,
                        ha='center', va=va, rotation=rotation)

    except:
        print('Unable to set bar vals!')

    return ax


def set_inline_label(ax, line, label=None,
                     xval=None, size=6, alpha=ALPHAS['translucent'],
                     color=None, ha='center', va='center',
                     bbox=dict(facecolor=COLORS['white'],
                               edgecolor=COLORS['white'],
                               alpha=ALPHAS['transparent']),
                     **kwargs):
    """
    Automatically adds an inline label to line
    https://github.com/cphyc/matplotlib-label-lines

    :param ax: (mpl.axes) - plot axis
    :param line: (mpl.Line2D) - line to be labeled
    :param label: (str) - label of line
    :param xval: (scalar) - x value of label; defaults to median
    :param size: (scalar) - size of label
    :param alpha: (scalar) - opacity of label
    :param ha: (str) - horizontal alignment of label
    :param va: (str) - vertical alignment of label
    :param bbox: (dict) - dictionary of box surrounding label
    :param kwargs: (kwargs) - additional keyword arguments
    """
    if isinstance(line, list):
        line = line[0]

    xdata = line.get_xdata()
    ydata = line.get_ydata()

    try:
        if xval is None:
            xval = np.median(xdata)
    except:
        xval = xdata[int(len(xdata) / 2)]

    if isinstance(xval, datetime.datetime):
        xdata = pd.to_datetime(xdata).to_pydatetime()
    elif isinstance(xval, str):
        xval = pd.to_datetime(xval).to_pydatetime()
        xdata = pd.to_datetime(xdata).to_pydatetime()

    x_idx = np.where(xdata == xval)[0]

    if not x_idx:
        print('xval outside range of x in set_label_inline!')
        return

    yval = ydata[x_idx]

    if not label:
        label = line.get_label()

    size = scale_it(ax, size, 2, exp=True)

    try:
        if xval is None:
            xval = np.median(xdata)
    except:
        xval = xdata[int(len(xdata) / 2)]

    if color is None:
        color = plt.getp(line, 'color')

    ax.text(xval, yval, label,
            color=color,
            alpha=alpha,
            size=size,
            ha=ha,
            va=va,
            bbox=bbox,
            **kwargs
            )


def annotate_point(ax, x, y, label='', xytext=(0, 0),
                   size=SIZES['marker']['smaller'],
                   textcoords='offset points', transform=False,
                   projection=DEFAULT['projection'],
                   bbox=dict(boxstyle='round, pad=0.3',
                             facecolor=COLORS['black'],
                             alpha=ALPHAS['transparent']),
                   **kwargs
                   ):
    """
    Annotate a point on a subplot.

    :param ax: (mpl.axes) - plot axis
    :param x: (scalar) - input x location to annotate
    :param y: (scalar) - input y location to annotate
    :param label: (str) - label of line to be used in legend
    :param xytext: (tup) - x, y offset from input x and y for annotation
    :param size: (scalar) - size of annotation
    :param textcoords: (str) - type of coordinates
    :param transform: (boolean) - whether to use input projection
    :param projection: (cartopy.crs) - projection of plotted scatter
    :param bbox: (dict) - dictionary of boxstyle, facecolor, and alpha of box
    :param kwargs: (kwargs) - additional keyword arguments
    :return ax: (mpl.axes) - plot axis
    """
    if transform:
        x, y = ax.projection.transform_point(x, y, src_crs=projection)
    ax.annotate(label, xy=(x, y), xytext=xytext, ha='left', va='center',
                textcoords=textcoords, size=size, bbox=bbox, **kwargs)
    return ax


def set_figsize(width=None, height=None, figsize='wide',
                rows=1, cols=1, pos=1, dpi=DEFAULT['dpi'], **kwargs):
    """
    Set figure size; can be wide, tall, auto, or input tuple.

    :param width: (scalar) - width of figure
    :param height: (scalar) - height of figure
    :param figsize: (str/tup) - wide/tall/auto or tuple width x height of fig
    :param rows: (int) - number of rows for subplots
    :param cols: (int) - number of columns for subplots
    :param pos: (int) - position of current subplot
    :param dpi: (int) - dots per inch to save the figure
    :param kwargs: (kwargs) - additional keyword arguments
    """
    if width is not None and height is not None:
        figsize = (width, height)
    else:
        if figsize is 'wide' and pos == 1:
            fig_width = 10 + rows * 1.75
            fig_height = 3.5 + cols * 1.25
            figsize = (fig_width, fig_height)
        elif figsize is 'tall' and pos == 1:
            fig_width = 3.5 + rows * 1.25
            fig_height = 12 + cols * 1.75
            figsize = (fig_width, fig_height)
        elif figsize is 'auto' and pos == 1:
            fig_width = 8 + rows * 1.5
            fig_height = 4.5 + cols * 1.5
            figsize = (fig_width, fig_height)

    if isinstance(figsize, tuple):
        fig = plt.figure(figsize=figsize, dpi=dpi, **kwargs)
        return fig


def set_ax(rows=1, cols=1, pos=1, **kwargs):
    """
    Create plot axis

    :param rows: (int) - number of rows for subplots
    :param cols: (int) - number of columns for subplots
    :param pos: (int) - position of current subplot
    :param kwargs: (kwargs) - additional keyword arguments
    :return ax: (mpl.axes) - plot axis
    """
    return plt.subplot(rows, cols, pos, **kwargs)


def set_date_ticks(ax, minor_date_ticks=True):
    """
    Use logic on the length of date range to decide the tick marks.

    :param ax: (mpl.axes) - plot axis
    :param minor_date_ticks: (boolean) - whether to show the top date ticks
    :return major_xlocator: (str) - locator of major tick
    :return major_xinterval: (str) - interval between each major tick
    :return major_xformatter: (str) - formatter of major tick
    :return minor_xlocator: (str) - locator of minor tick
    :return minor_xinterval: (str) - interval between each minor tick
    :return minor_xformatter: (str) - formatter of minor tick
    :return dt_bool: (boolean) - whether the x axis is datetimes
    """
    geom = plt.getp(ax, 'geometry')
    nrows = geom[0]
    ncols = geom[1]

    xlim = plt.getp(ax, 'xlim')
    if xlim[0] < 700000:
        dt_bool = False
        return [None] * 6 + [dt_bool]
    else:
        dt_bool = True

    xlim_dts = mdates.num2date(xlim)

    dt_dict = td2dict(xlim_dts[-1] - xlim_dts[0])
    ndays = dt_dict['days']

    if ndays < 0:
        dt_dict = td2dict(xlim_dts[0] - xlim_dts[-1])
        ndays = dt_dict['days']

    if ndays > 10950:
        major_xlocator = 'years'
        major_xformatter = '%Y'
        major_xinterval = int(ndays / 2000)

        major_xlocator2 = None
        major_xformatter2 = None
        major_xinterval2 = None

        minor_xlocator = 'years'
        minor_xformatter = '\'%y'
        minor_xinterval = int(ndays / 8000)
        minor_xshow = int(ndays / 8000)

        for i in range(0, 10):
            if major_xinterval % minor_xinterval != 0:
                major_xinterval += 1
            else:
                break

        if minor_xshow >= minor_xinterval / 2:
            minor_xshow -= int(minor_xinterval / 1.75)

        if minor_xshow <= minor_xinterval:
            minor_xshow += 1

    elif 3000 < ndays <= 10950:
        major_xlocator = 'years'
        major_xformatter = '%Y'
        major_xinterval = 1 + int(ndays / 3000)

        major_xlocator2 = None
        major_xformatter2 = None
        major_xinterval2 = None

        minor_xlocator = 'years'
        minor_xformatter = '\'%y'
        minor_xinterval = 1 + int(ndays / 3300)
        minor_xshow = 1 + int(ndays / 3300)

        if major_xinterval >= minor_xinterval:
            minor_xinterval -= 1

        for i in range(0, 10):
            if major_xinterval % minor_xinterval != 0:
                major_xinterval += 1
            else:
                break

        if minor_xshow >= minor_xinterval / 2:
            minor_xshow -= int(minor_xshow / 1.3)

        if minor_xshow == 0:
            minor_xshow = 1

    elif 1825 < ndays <= 3000:
        major_xlocator = 'months'
        major_xformatter = '%B'
        major_xinterval = 10 + int(ndays / 1850)

        major_xlocator2 = 'months'
        major_xformatter2 = '%Y'
        major_xinterval2 = 8

        minor_xlocator = 'months'
        minor_xformatter = '%b'
        minor_xinterval = 1 + int(ndays / 600)
        minor_xshow = 1 + int(ndays / 725)

        if minor_xshow >= minor_xinterval / 2:
            minor_xshow -= int(minor_xshow / 1.25)

        for i in range(0, 10):
            if major_xinterval % minor_xinterval != 0:
                major_xinterval += 1
            else:
                break

        for i in range(0, 10):
            if (major_xinterval2 % major_xinterval != 0
                    or major_xinterval2 == 0):
                major_xinterval2 += 1
            else:
                break

    elif 217 < ndays <= 1825:
        major_xlocator = 'months'
        major_xformatter = '%b %d'
        major_xinterval = 3 + int(ndays / 1000) * 2

        major_xlocator2 = 'months'
        major_xformatter2 = '%Y'
        major_xinterval2 = 4 + int(ndays / 800)

        minor_xlocator = 'months'
        minor_xformatter = '%b'
        minor_xinterval = 1 + int(ndays / 600)
        minor_xshow = 1 + int(ndays / 725)

        if minor_xshow >= minor_xinterval / 2:
            minor_xshow -= int(minor_xshow / 1.5)

        for i in range(0, 10):
            if major_xinterval % minor_xinterval != 0:
                major_xinterval += 1
            else:
                break

        for i in range(0, 10):
            if (major_xinterval2 % major_xinterval != 0
                    or major_xinterval2 == 0):
                major_xinterval2 += 1
            else:
                break

    elif 6 < ndays <= 217:
        major_xlocator = 'days'
        major_xformatter = '%b %d'
        major_xinterval = 2 + int(ndays / 15) * 2

        major_xlocator2 = None
        major_xformatter2 = None
        major_xinterval2 = None

        minor_xlocator = 'days'
        minor_xformatter = '%d'
        minor_xinterval = 1 + int(ndays / 50)
        minor_xshow = 1 + int(ndays / 35)

        if minor_xshow >= minor_xinterval:
            minor_xshow -= int(minor_xshow / 2.25)

        for i in range(0, 10):
            if major_xinterval % minor_xinterval != 0:
                major_xinterval += 1
            else:
                break

    elif 1 < ndays <= 6:
        major_xlocator = 'hours'
        major_xformatter = '%H:%M'
        major_xinterval = ndays * 5

        major_xlocator2 = 'hours'
        major_xformatter2 = '%m/%d'
        major_xinterval2 = 24

        minor_xlocator = 'hours'
        minor_xformatter = '%H'
        minor_xinterval = int(ndays / 1.5)
        minor_xshow = 1 + int(minor_xinterval / 2)

        if minor_xshow >= minor_xinterval:
            minor_xshow -= int(minor_xshow / 2.25)

        for i in range(0, 10):
            if major_xinterval % minor_xinterval != 0:
                major_xinterval += 1
            else:
                break

        for i in range(0, 25):
            if (major_xinterval2 % major_xinterval != 0
                    or major_xinterval2 == 0):
                major_xinterval2 -= 1
            else:
                break

        if minor_xshow <= minor_xinterval:
            minor_xshow += 1

    elif 0 <= ndays <= 1:
        nminutes = (dt_dict['days'] * 1440
                    + dt_dict['hours'] * 60
                    + dt_dict['minutes']
                    )

        major_xlocator = 'minutes'
        major_xformatter = '%I:%M %p'
        major_xinterval = int(nminutes / 3)

        major_xlocator2 = 'minutes'
        major_xformatter2 = '%b %d'
        major_xinterval2 = int(nminutes / 1.5)

        minor_xlocator = 'minutes'
        minor_xformatter = '%H:%M'
        minor_xinterval = int(nminutes / 12)
        minor_xshow = 1

        if minor_xshow >= 3 and major_xlocator != 'years':
            minor_xshow = int(minor_xshow / 1.5)
        elif minor_xshow >= 3 and major_xlocator == 'years':
            minor_xshow -= int(minor_xshow / 1.5)

        if nminutes > 360:
            major_xinterval = round_to(major_xinterval, base=15)
            minor_xinterval = round_to(minor_xinterval, base=15)
            major_xinterval2 = round_to(major_xinterval2, base=15)

        if major_xinterval % minor_xinterval != 0:
            minor_xinterval = int(major_xinterval / 3)

        for i in range(0, 60):
            if major_xinterval % minor_xinterval != 0:
                minor_xinterval += 1
            else:
                break

        if major_xinterval2 % major_xinterval != 0:
            major_xinterval2 = major_xinterval

    if minor_xshow <= 0:
        minor_xshow = 1

    if major_xinterval2 is not None:
        if major_xinterval2 <= 0:
            major_xinterval2 = major_xinterval

    set_major_ticks(ax,
                    xlocator=major_xlocator,
                    xformatter=major_xformatter,
                    xinterval=major_xinterval)
    set_major_tick_labels(ax, size=8)

    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    prettify_ax(ax2, ticks=False)

    if major_xlocator2 is not None and nrows == 1:
        set_major_ticks(ax2,
                        xlocator=major_xlocator2,
                        xformatter=major_xformatter2,
                        xinterval=major_xinterval2)
        set_major_tick_labels(ax2, bottom=True, top=False,
                              pad=24, size=6)
    else:
        set_major_tick_labels(ax2, xticklabels=[])
        set_major_ticks(ax2, xticks=[])

    if minor_date_ticks:
        set_minor_ticks(ax2,
                        xlocator=minor_xlocator,
                        xformatter=minor_xformatter,
                        xinterval=minor_xinterval,
                        top=True, bottom=False)
        set_minor_tick_labels(ax2, top=True, size=7.5)
        set_minor_grid(ax2, xalpha=0.25)

        for label in ax2.get_xminorticklabels():
            label.set_visible(False)  # find a better way?
        for label in ax2.get_xminorticklabels()[0::minor_xshow * ncols]:
            label.set_visible(True)

    return (major_xlocator, major_xinterval, major_xformatter,
            minor_xlocator, minor_xinterval, minor_xformatter, dt_bool)


def set_cbar(ax, im,
             fig=False,
             label='',
             fmt='%1.0f',
             label_size=7.5,
             drawedges=True,
             label_color=COLORS['gray'],
             tick_locs=None,
             tick_size=5,
             tick_color=COLORS['gray'],
             color=COLORS['black'],
             pad=0.1,
             aspect=25.5,
             shrink=0.2,
             length=0,
             width=0.25,
             direction='out',
             orientation='horizontal',
             cax=None,
             **kwargs):
    """
    Set color bar for a map.

    :param ax: (mpl.axes) - plot axis
    :param im: (mpl.collections/contour) - plotted map
    :param fig: (boolean) - whether to plot a figure wide colorbar
    :param fmt: (str) - format of color bar labels
    :param label_size: (scalar) - size of color bar label
    :param label_color: (scalar) - color of color bar label
    :param tick_locs: (array) - input own tick marks on color bar
    :param tick_size: (scalar) - size of color bar tick labels
    :param tick_color: (scalar) - color of color bar tick labels
    :param color: (scalar) - color of color bar tick marks
    :param drawedges: (scalar) - whether to draw color edges
    :param pad: (scalar) - padding of color bar from plot
    :param aspect: (int) - aspect ratio of color bar
    :param shrink: (scalar) - size of color bar
    :param length: (scalar) - length of color bar tick marks
    :param width: (scalar) - width of color bar tick marks
    :param direction: (str) - direction of color bar tick marks
    :param orientation: (str) - orientation of color bar
    :param cax: (mpl.axes) - plot axis to attach to
    :param kwargs: (kwargs) - additional keyword arguments
    :return cbar: (mpl.ColorBar) - matplotlib color bar
    """
    try:
        pad = scale_it(ax, pad, 0.00075, exp=True)
        label_size = scale_it(ax, label_size, 1.25, exp=True)
        tick_size = scale_it(ax, tick_size, 1.25, exp=True)
        width = scale_it(ax, width, 0.05, exp=True)
        shrink = scale_it(ax, shrink, 0.075)
        aspect = scale_it(ax, aspect, 1.25)

        geom = plt.getp(plt.getp(ax, 'subplotspec'), 'geometry')
        nrows = geom[0]
        ncols = geom[1]

        shrink *= (nrows + 0.5) / 1.5
        tick_size += (nrows + ncols)

        if orientation == 'vertical':
            shrink *= 2
            pad /= 3

        if fmt == '%.2f':
            rotation = 45
        else:
            rotation = 0

        try:
            if not fig:
                    cbar = plt.colorbar(im, orientation=orientation,
                                        pad=pad,
                                        drawedges=drawedges,
                                        shrink=shrink,
                                        format=fmt,
                                        ticks=tick_locs,
                                        aspect=aspect,
                                        cax=cax,
                                        **kwargs)
            else:
                figure = plt.getp(ax, 'figure')
                cbar = figure.colorbar(im, ax=plt.getp(figure, 'axes'),
                                       orientation=orientation,
                                       pad=pad,
                                       drawedges=drawedges,
                                       shrink=shrink * 1.75,
                                       format=fmt,
                                       ticks=tick_locs,
                                       aspect=aspect,
                                       cax=cax,
                                       **kwargs)
        except:
            cbar = plt.colorbar(im,
                                orientation=orientation,
                                drawedges=drawedges,
                                format=fmt,
                                ticks=tick_locs,
                                cax=cax,
                                **kwargs)

        cbar.ax.tick_params(labelsize=tick_size,
                            rotation=rotation,
                            direction=direction,
                            length=length,
                            width=width,
                            tick2On=True,
                            labelcolor=label_color,
                            color=color)

        cbar.set_label(label, size=label_size, color=label_color)

        return cbar

    except:
        report_err(comment='Could not set color bar; please set manually!')


def get_cmap(colors, n=None, r=False, start=0, stop=1, **kwargs):
    """
    Converts a list of colors into a color map or discretizes a registered cmap
    http://matplotlib.org/examples/color/colormaps_reference.html
    http://www.ncl.ucar.edu/Document/Graphics/color_table_gallery.shtml

    :param colors: (list/str) - a list containing RGB or Python/NCL cmap name
    :param n: (int) - number of colors in cmap
    :param r: (boolean) - reverse colormap
    :param start: (scalar) - value to start on the cmap between 0 and 1
    :param stop: (scalar) - value to end on the cmap between 0 and 1
    :param kwargs: (kwargs) - additional keyword arguments
    :return cmap: (mpl.cmap) - color map
    """
    try:
        if '_r' in colors:
            colors = colors[:-2]
            r = True
    except:
        pass

    if colors in NCL_CMAP_NAMES:
        if r:
            color_list = get_color_list(NCL_CMAPS[colors].values[0])[::-1]
            cmap = LinearSegmentedColormap.from_list('cmap',
                                                     colors=color_list)
        else:
            cmap = NCL_CMAPS[colors].values[0]
        if n is None:
            n = NCL_CMAPS[colors].values[1]
    else:
        if isinstance(colors, str):
            if r:
                colors += '_r'
            if n is None:
                n = 10
            cmap = plt.get_cmap(colors, **kwargs)
        elif isinstance(colors, mpl.colors.LinearSegmentedColormap):
            return colors
        else:
            if r:
                colors = colors[::-1]
            if n is None and len(colors) > 2:
                n = len(colors)
            elif n is None:
                n = 10
            if not isinstance(colors[0], str):
                if (np.array(colors) > 1).any():
                    for i, tup in enumerate(colors):
                        colors[i] = np.array(tup) / 255.
            cmap = LinearSegmentedColormap.from_list('mycmap', colors=colors,
                                                     **kwargs)
    colors = cmap(np.linspace(start, stop, cmap.N))

    return LinearSegmentedColormap.from_list('mycmap', colors=colors, N=n)


def get_color_list(cmap, hexcodes=False, **kwargs):
    """
    Converts a registered colormap into a list of RGB tuples or hexcodes

    :param cmap_name: (mpl.cmap/str) - actual colormap or name of color
    :param hexcodes: (boolean) - whether to return a list of hexcodes
    :param kwargs: (kwargs) - additional keyword arguments
    :return cmap: (list) - list of RGB tuples or hexcodes
    """
    if isinstance(cmap, str):
        if cmap in NCL_CMAP_NAMES:
            cmap = NCL_CMAPS[cmap].values[0]
        else:
            cmap = plt.get_cmap(cmap)

    if not hexcodes:
        color_list = [cmap(i)[:3] for i in range(cmap.N)]
    else:
        color_list = [mpl.colors.rgb2hex(cmap(i)[:3])
                      for i in range(cmap.N)]

    return color_list


def set_latlons(ax,
                color=COLORS['black'],
                alpha=ALPHAS['semi opaque'],
                size=4,
                top=False,
                bottom=True,
                left=True,
                right=False,
                lat_labels='auto',
                lon_labels='auto',
                central_longitude=0,
                **kwargs):
    """
    Set lat lon labels for a map.

    :param ax: (mpl.axes) - plot axis
    :param color: (scalar) - color of  lat lon labels
    :param alpha: (scalar/str) - transparency of lat lon labels
    :param size: (scalar) - size of lat lon labels
    :param bottom: (boolean) - whether to show bottom lon labels
    :param top: (boolean) - whether to show top lon labels
    :param left: (boolean) - whether to show left lat labels
    :param right: (boolean) - whether to show right lat labels
    :param lat_labels: (array) - list of latitudes to show on map
    :param lon_labels: (array) - list of longitudes to show on map
    :param kwargs: (kwargs) - additional keyword arguments
    :return gl: (ax.gridlines) - gridlines
    """
    from cartopy.mpl.gridliner import (LONGITUDE_FORMATTER,
                                       LATITUDE_FORMATTER
                                       )
    size = scale_it(ax, size, 1, exp=True)

    geom = plt.getp(plt.getp(ax, 'subplotspec'), 'geometry')
    nplots = geom[0] * geom[1]

    size += nplots
    linewidth = np.log(nplots + 1) / 85 + 0.35

    gl = ax.gridlines(draw_labels=True,
                      linewidth=linewidth,
                      color=COLORS['black'],
                      alpha=ALPHAS['translucid'],
                      linestyle=(0, (16, 4)), **kwargs)  # length, how often

    if lon_labels is not None and lon_labels is not 'auto':
        gl.xlocator = mticker.FixedLocator(lon_labels)
    elif not lon_labels:
        gl.xlabels_top = False
        gl.xlabels_bottom = False
    if lat_labels is not None and lat_labels is not 'auto':
        gl.ylocator = mticker.FixedLocator(lat_labels)
    elif not lat_labels:
        gl.ylabels_left = False
        gl.ylabels_right = False
    else:
        if central_longitude != 0:
            base_range = np.arange(-360, 420, 60)
            base_range -= central_longitude
            base_range = np.delete(base_range,
                                   np.where(base_range == -180)[0])
            gl.xlocator = mticker.FixedLocator(base_range)

    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

    gl.xlabels_top = top
    gl.ylabels_bottom = bottom
    gl.xlabels_left = left
    gl.ylabels_right = right

    gl.xlabel_style = {'size': size, 'color': color, 'alpha': alpha}
    gl.ylabel_style = {'size': size, 'color': color, 'alpha': alpha}

    return gl


def set_figtext(ax, text, size=12, pad=0,
                loc='bottom center',
                color=COLORS['black'],
                alpha=ALPHAS['translucent'],
                fha=None, fva=None, **kwargs):
    """
    Add text to the side of a figure.

    loc choices - center, center bottom, center left, center right,
    upper left, upper right, bottom left, bottom right.

    :param ax: (mpl.axes) - plot axis
    :param text: (str) - text to put on the figure
    :param loc: (str) - location of the text
    :param size: (int) - size in points
    :param color: (str) - color of text
    :param alpha: (scalar/str) - transparency of text
    :param fha: (boolean) - force the horizontal alignment to be input str
    :param fva: (boolean) - force the vertical alignment to be input str
    :param kwargs: (kwargs) - additional keyword arguments
    """
    size = scale_it(ax, size, 1, exp=True)
    pad = scale_it(ax, pad, 0.005, exp=True)

    loc_keywords = get_loc_keywords(loc)

    if 'lower' in loc_keywords:
        if 'center' in loc_keywords:  # lower center
            ha = 'center'
            va = 'top'
            x = 0.5
            y = -0.09 + pad
        elif 'right' in loc_keywords:
            ha = 'left'
            if 'corner' in loc_keywords:  # lower corner right
                va = 'center'
                x = 0.925
                y = -0.04 + pad
            else:  # lower right
                va = 'bottom'
                x = 0.925 + pad
                y = 0.125
        elif 'left' in loc_keywords:
            ha = 'right'
            if 'corner' in loc_keywords:  # lower corner left
                va = 'center'
                x = 0.855
                y = -0.04 + pad
            else:  # lower left
                va = 'bottom'
                x = 0.05
                y = 0.125

    elif 'upper' in loc_keywords:
        if 'center' in loc_keywords:
            ha = 'center'
            va = 'center'
            x = 0.5
            y = 0.975 - pad
        elif 'right' in loc_keywords:
            ha = 'left'
            if 'corner' in loc_keywords:
                va = 'center'
                x = 0.925
                y = 0.975 - pad
            else:
                va = 'top'
                x = 0.925 + pad
                y = 0.9
        elif 'left' in loc_keywords:
            ha = 'right'
            if 'corner' in loc_keywords:
                va = 'center'
                x = 0.855
                y = 0.975 - pad
            else:
                va = 'top'
                x = 0.05
                y = 0.9
    else:
        va = 'center'
        if 'right' in loc_keywords:
            x = 0.925 + pad
            y = 0.5
            ha = 'left'
        elif 'left' in loc_keywords:
            x = 0.05
            y = 0.5
            ha = 'right'
        else:
            x = 0.5
            y = 0.5
            ha = 'center'

    if fva is not None:
        va = fva
    if fha is not None:
        ha = fha

    plt.figtext(x, y, text,
                ha=ha, va=va,
                wrap=True,
                size=size,
                color=color,
                alpha=alpha,
                **kwargs)


def set_axtext(ax, text, loc='bottom center', xy=None,
               size=12, color=COLORS['black'],
               xpad=None, ypad=None,
               alpha=ALPHAS['translucent'],
               fha=None, fva=None,
               **kwargs):
    """
    :param ax: (mpl.axes) - plot axis
    :param text: (str) - text to put on the subplot
    :param loc: (str) - location of the text
    :param xy: (tup) - coordinate to set text
    :param size: (int) - size in points
    :param color: (str) - color of text
    :param xpad: (scalar) - padding in the x axis direction
    :param ypad: (scalar) - padding in the y axis direction
    :param alpha: (scalar/str) - transparency of text
    :param fha: (boolean) - force the horizontal alignment to be input str
    :param fva: (boolean) - force the vertical alignment to be input str
    :param kwargs: (kwargs) - additional keyword arguments
    """
    size = scale_it(ax, size, 1, exp=True)

    if xy is None:
        loc_keywords = get_loc_keywords(loc)
        xtick_diff = np.average(np.diff(plt.getp(ax, 'xticks')))
        ytick_diff = np.average(np.diff(plt.getp(ax, 'yticks')))

        if ax.get_xlim()[0] > 700000:
            if 'lower' in loc_keywords:
                loc_keywords.remove('lower')
                va = 'bottom'
                ha = ''.join(loc_keywords)
                if ha is 'left':
                    xy = (ax.get_xlim()[0] + xtick_diff * 0.025,
                          ax.get_ylim()[0] + ytick_diff * 0.025)
                elif ha is 'right':
                    xy = (ax.get_xlim()[1] - xtick_diff * 0.025,
                          ax.get_ylim()[0] + ytick_diff * 0.025)
                else:
                    xy = ((ax.get_xlim()[0] + ax.get_xlim()[1]) / 2,
                          ax.get_ylim()[0] + ytick_diff * 0.025)

            elif 'upper' in loc_keywords:
                loc_keywords.remove('upper')
                va = 'top'
                ha = ''.join(loc_keywords)
                if ha is 'left':
                    xy = (ax.get_xlim()[0] + xtick_diff * 0.025,
                          ax.get_ylim()[1])
                elif ha is 'right':
                    xy = (ax.get_xlim()[1] - xtick_diff * 0.025,
                          ax.get_ylim()[1])
                else:
                    xy = ((ax.get_xlim()[0] + ax.get_xlim()[1]) / 2,
                          ax.get_ylim()[1])

            else:
                loc_keywords.remove('center')
                va = 'center'
                ha = ''.join(loc_keywords)
                if ha is 'left':
                    xy = (ax.get_xlim()[0] + xtick_diff * 0.025,
                          ax.get_ylim()[1] / 2)
                elif ha is 'right':
                    xy = (ax.get_xlim()[1] - xtick_diff * 0.025,
                          ax.get_ylim()[1] / 2)
                else:
                    ha = 'center'
                    xy = ((ax.get_xlim()[0] + ax.get_xlim()[1]) / 2,
                          ax.get_ylim()[1] / 2)

            xy = (mdates.num2date(xy[0]), xy[1])

        else:
            if 'lower' in loc_keywords:
                loc_keywords.remove('lower')
                va = 'bottom'
                ha = ''.join(loc_keywords)
                if ha is 'left':
                    xy = (ax.get_xlim()[0] + ax.get_xlim()[1] * 0.025,
                          ax.get_ylim()[0] + ytick_diff * 0.025)
                elif ha is 'right':
                    xy = (ax.get_xlim()[1] * 0.985,
                          ax.get_ylim()[0] + ytick_diff * 0.025)
                else:
                    xy = (ax.get_xlim()[1] / 2,
                          ax.get_ylim()[0] + ytick_diff * 0.025)

            elif 'upper' in loc_keywords:
                loc_keywords.remove('upper')
                va = 'top'
                ha = ''.join(loc_keywords)
                if ha is 'left':
                    xy = (ax.get_xlim()[0] + ax.get_xlim()[1] * 0.025,
                          ax.get_ylim()[1])
                elif ha is 'right':
                    xy = (ax.get_xlim()[1] * 0.985,
                          ax.get_ylim()[1])
                else:
                    xy = (ax.get_xlim()[1] / 2,
                          ax.get_ylim()[1])

            else:
                loc_keywords.remove('center')
                va = 'center'
                ha = ''.join(loc_keywords)
                if ha is 'left':
                    xy = (ax.get_xlim()[0] + ax.get_xlim()[1] * 0.025,
                          ax.get_ylim()[1] / 2)
                elif ha is 'right':
                    xy = (ax.get_xlim()[1] * 0.985,
                          ax.get_ylim()[1] / 2)
                else:
                    ha = 'center'
                    xy = (ax.get_xlim()[1] / 2,
                          ax.get_ylim()[1] / 2)
    else:
        ha = 'left'
        va = 'center'

    if isinstance(xy[0], str):
        xy = (pd.to_datetime(xy[0]).to_pydatetime(), xy[1])

    if fva is not None:
        va = fva
    if fha is not None:
        ha = fha

    if xpad is not None:
        xy = (xy[0] + xpad, xy[1])

    if ypad is not None:
        xy = (xy[0], xy[1] + ypad)

    ax.annotate(text, xy=xy, size=size,
                color=color, alpha=alpha,
                ha=ha, va=va, **kwargs)


def get_loc_keywords(loc):
    """
    Return the location keywords based on input loc.

    :param loc: (str) - location of the text
    :return loc_keywords: (list) - list of the location keywords
    """
    loc = loc.lower()
    loc_keywords = []
    if 'top' in loc or 'upper' in loc or 'north' in loc:
        loc_keywords.append('upper')
    elif 'bottom' in loc or 'lower' in loc or 'south' in loc:
        loc_keywords.append('lower')
    if 'right' in loc or 'east' in loc or 'east' in loc:
        loc_keywords.append('right')
    elif 'left' in loc or 'west' in loc:
        loc_keywords.append('left')
    if 'center' in loc or 'middle' in loc:
        loc_keywords.append('center')
    if 'corner' in loc:
        loc_keywords.append('corner')
    return loc_keywords


def set_share(ax1, ax2, axis='x', xlabel='', ylabel=''):
    """
    Match the tick locations of another axis and hide the current tick labels.

    :param ax1: (mpl.axes) - plot axis to adapt
    :param ax2: (mpl.axes) - plot axis to mimic ticks
    :param axis: (str) - share x or y axis
    :param xlabel: (str) - label of x axis
    :param ylabel: (str) - label of y axis
    :return ax1, ax2: (mpl.axes) - plot axes
    """
    if 'x' in axis:
        xlim = plt.getp(ax2, 'xlim')
        ax1.set_xlim(xlim)
        plt.setp(ax1.get_xticklabels(), visible=False)
        ax1.set_xlabel(xlabel, labelpad=12)
    if 'y' in axis:
        ylim = plt.getp(ax2, 'ylim')
        ax1.set_ylim(ylim)
        plt.setp(ax1.get_yticklabels(), visible=False)
        ax1.set_ylabel(ylabel, labelpad=12)
    return ax1, ax2


def get_region_latlim(region, lat1=-90, lat2=90, lon1=-180, lon2=180,
                      tup=False, sliceit=False, w2e=False):
    """
    Get latitudinal and longitudinal extents of select regions.

    :param region: (str) - acronym of region [us/na/nino34/nh/sh]
    :param lat1: (scalar) lower limit of latitude
    :param lat2: (scalar) upper limit of latitude
    :param lon1: (scalar) left limit of longitude
    :param lon2: (scalar) right limit of longitude
    :param central_longitude: (scalar) - longitude to center the map on
    :param tup: (bool) - whether to return a tuple of extents
    :param sliceit: (bool) - whether to return a slice type of extents
    :return lat1, lat2, lon1, lon2: (scalar) - individual extents
    :return latlim, lonlim: (tuple) - tuple extents
    :return lat_slice, lon_slice: (slice) - slice extents
    """
    if region == 'us':
        lat1 = 50
        lat2 = 22
        lon1 = -128
        lon2 = -65
    elif region == 'na':
        lat1 = 73
        lat2 = 10
        lon1 = -176
        lon2 = -65
    elif region == 'nino34':
        lat1 = -5
        lat2 = 5
        lon1 = -120
        lon2 = -170
    elif region == 'nh':
        lat1 = 0
        lat2 = 90
    elif region == 'sh':
        lat1 = -90
        lat2 = 0
    elif region == 'wh':
        lon1 = -180
        lon2 = 0
    elif region == 'eh':
        lon1 = 0
        lon2 = 180
    elif region == None or region == '':
        pass
    else:
        print('Region not found!')

    if w2e:
        lon1 = lonw2e(lon1)
        lon2 = lonw2e(lon2)

    if tup:
        return (lat1, lat2), (lon1, lon2)
    elif sliceit:
        return slice(lat1, lat2), slice(lon1, lon2)
    else:
        return lat1, lat2, lon1, lon2


def set_twin(ax1, ax2, axis='x', title_pad=1.09,
             xlabel='', ylabel='', title='', suptitle=False,
             aligned=True, length_scale=False):
    """
    Create another y axis on the same subplot.

    :param ax1: (mpl.axes) - plot axis on the right to adapt
    :param ax2: (mpl.axes) - plot axis on the left or the one to mimic
    :param axis: (str) - twin x or y axis
    :param xlabel: (str) - label of x axis
    :param ylabel: (str) - label of y axis
    :param title: (str) - title of subplot
    :param suptitle: (boolean) - whether to make a figure title
    :param aligned: (boolean) - whether to keep left and right ticks aligned
    :param scale: (scalar) - scaling exponent
    :return ax1, ax2: (mpl.axes) - plot axes
    """
    children1 = ax1.get_children()
    children2 = ax2.get_children()
    ylabel2 = plt.getp(ax2, 'ylabel')
    xlabel = plt.getp(ax2, 'xlabel')
    title = plt.getp(ax2, 'title')

    try:
        plotlist1 = list(filter(lambda x:
                                isinstance(x, mpl.lines.Line2D),
                                children1
                                )
                         )
        if len(plotlist1) == 1:
            plot1 = plotlist1[0]
            color1 = plt.getp(plot1, 'color')
        else:
            plot1 = list(filter(lambda x:
                                isinstance(x, mpl.patches.Rectangle),
                                children1)
                         )[0]
            color1 = plt.getp(plot1, 'facecolor')

        plotlist2 = list(filter(lambda x:
                                isinstance(x, mpl.lines.Line2D),
                                children2)
                         )
        if len(plotlist2) == 1:
            plot2 = plotlist2[0]
            color2 = plt.getp(plot2, 'color')
        else:
            plot2 = list(filter(lambda x:
                                isinstance(x, mpl.patches.Rectangle),
                                children2)
                         )[0]
            color2 = plt.getp(plot2, 'facecolor')
    except Exception:
        color1 = COLORS['gray']
        color2 = COLORS['gray']
        print('Unable to get color for twinx.')

    if 'x' in axis:
        set_borders(ax2, spines=['left'], color=color2)
        set_borders(ax2, spines=['right'], color=color1)

        if aligned:
            yticks2 = np.linspace(ax2.get_yticks()[0],
                                  ax2.get_yticks()[-1],
                                  len(ax2.get_yticks())
                                  )
            yticks1 = np.linspace(ax1.get_yticks()[0],
                                  ax1.get_yticks()[-1],
                                  len(ax2.get_yticks())
                                  )
            set_major_grid(ax2)
        else:
            yticks2 = None
            yticks1 = None
            set_major_grid(ax1, ycolor=color1, yalpha=ALPHAS['translucent'])
            set_major_grid(ax2, ycolor=color2, yalpha=ALPHAS['translucent'])

        set_borders(ax1, all_=False)

        set_major_ticks(ax2,
                        yticks=yticks2,
                        axes=['y'],
                        bottom=True,
                        left=True,
                        right=False,
                        top=True,
                        color=color2)
        set_minor_ticks(ax2,
                        axes=['y'],
                        bottom=True,
                        left=True,
                        right=False,
                        top=True,
                        color=color2)
        set_major_tick_labels(ax2,
                              axes=['y'],
                              left=True,
                              right=False,
                              color=color2)
        set_minor_tick_labels(ax2,
                              axes=['y'],
                              left=True,
                              right=False,
                              color=color2)

        set_labels(ax2, xlabel=xlabel, ylabel=ylabel2, title_pad=title_pad,
                   title=title, suptitle=suptitle, ylabel_color=color2)

        set_major_ticks(ax1,
                        yticks=yticks1,
                        axes=['y'],
                        bottom=False,
                        left=False,
                        right=True,
                        top=False,
                        color=color1)
        set_minor_ticks(ax1,
                        axes=['y'],
                        bottom=False,
                        left=False,
                        right=True,
                        top=False,
                        color=color1)
        set_major_tick_labels(ax1,
                              axes=['y'],
                              left=False,
                              right=True,
                              color=color1)
        set_minor_tick_labels(ax1,
                              axes=['y'],
                              left=False,
                              right=True,
                              color=color1)

        set_labels(ax1, ylabel=ylabel, ylabel_color=color1,
                   length_scale=length_scale)

    return ax1, ax2


def set_axes(ax, xlim=None, ylim=None,
             xscale=None, yscale=None,
             xinvert=False, yinvert=False, **kwargs):
    """
    Modify subplot axes settings.

    :param ax: (mpl.axes) - plot axis
    :param xlim: (tup) - left and right x axis limit in a tuple, respectively
    :param ylim: (tup) - left and right y axis limit in a tuple, respectively
    :param xscale: (str) - linear or log scale of x axis
    :param yscale: (str) - linear or log scale of y axis
    :param xinvert: (boolean) - whether to flip x axis
    :param yinvert: (boolean) - whether to flip y axis
    :param kwargs: (kwargs) - additional keyword arguments
    :return ax: (mpl.axes) - plot axis
    """
    if xlim is None:
        xlim = plt.getp(ax, 'xlim')
    if ylim is None:
        ylim = plt.getp(ax, 'ylim')

    if xscale is None:
        xscale = plt.getp(ax, 'xscale')
    if yscale is None:
        yscale = plt.getp(ax, 'yscale')

    if isinstance(xlim[0], str):
        xlim = pd.to_datetime(xlim).to_pydatetime()

    ax.set(xlim=xlim, ylim=ylim, xscale=xscale, yscale=yscale, **kwargs)

    if xinvert:
        ax.invert_xaxis()

    if yinvert:
        ax.invert_yaxis()

    return ax


def set_major_tick_labels(ax, axes='both',
                          xticklabels=None,
                          yticklabels=None,
                          pad=1.25, size=10,
                          color=COLORS['gray'],
                          bottom=True, top=False,
                          left=True, right=False,
                          xrotation=0, yrotation=0, **kwargs):
    """
    Modify major tick label settings.

    :param ax: (mpl.axes) - plot axis
    :param axes: (list) - x and/or y axis to change
    :param xticklabels: (list) - manually set x major tick labels
    :param yticklabels: (list) - manually set y major tick labels
    :param pad: (scalar) - distance between ticks and major tick labels
    :param size: (scalar) - size of major tick labels
    :param color: (str) - color of major tick labels
    :param bottom: (boolean) - whether to show bottom major tick labels
    :param top: (boolean) - whether to show top major tick labels
    :param left: (boolean) - whether to show left major tick labels
    :param right: (boolean) - whether to show right major tick labels
    :param xrotation: (scalar) - degrees to rotate x major tick labels
    :param yrotation: (scalar) - degrees to rotate y major tick labels
    :param scale: (scalar) - scaling exponent
    :param kwargs: (kwargs) - additional keyword arguments
    :return ax: (mpl.axes) - plot axis
    """
    size = scale_it(ax, size, 1.25, exp=True)
    pad = scale_it(ax, pad, 0.1)

    if xticklabels is not None:
        ax.set_xticklabels(xticklabels)

    if yticklabels is not None:
        ax.set_yticklabels(yticklabels)

    if color is 'xinherit':
        color = plt.getp(plt.getp(ax, 'xmajorticklabels')[0], 'color')

    if color is 'yinherit':
        color = plt.getp(plt.getp(ax, 'ymajorticklabels')[0], 'color')

    if axes is 'both':
        axes = ['x', 'y']

    for axis in axes:
        ax.tick_params(axis=axis,
                       which='major',
                       labelsize=size,
                       labelcolor=color,
                       labelleft=left,
                       labelright=right,
                       labeltop=top,
                       labelbottom=bottom, **kwargs)

        ax.tick_params(axis=axis, which='major',
                       pad=pad)  # this doesn't play well with others...

    plt.setp(ax.xaxis.get_majorticklabels(), rotation=xrotation)
    plt.setp(ax.yaxis.get_majorticklabels(), rotation=yrotation)

    return ax


def set_minor_tick_labels(ax, axes='both',
                          xticklabels=None, yticklabels=None,
                          pad=1.25,
                          size=9,
                          color=COLORS['gray'],
                          bottom=False, top=False,
                          left=False, right=False,
                          xrotation=0, yrotation=0, **kwargs):
    """
    Modify minor tick label settings.

    :param ax: (mpl.axes) - plot axis
    :param axes: (list) - x and/or y axis to change
    :param xticklabels: (list) - manually set x minor tick labels
    :param yticklabels: (list) - manually set y minor tick labels
    :param pad: (scalar) - distance between ticks and minor tick labels
    :param size: (scalar) - size of minor tick labels
    :param color: (str) - color of minor tick labels
    :param bottom: (boolean) - whether to show bottom minor tick labels
    :param top: (boolean) - whether to show top minor tick labels
    :param left: (boolean) - whether to show left minor tick labels
    :param right: (boolean) - whether to show right minor tick labels
    :param xrotation: (scalar) - degrees to rotate x minor tick labels
    :param yrotation: (scalar) - degrees to rotate y minor tick labels
    :param scale: (scalar) - scaling exponent
    :param kwargs: (kwargs) - additional keyword arguments
    :return ax: (mpl.axes) - plot axis
    """

    size = scale_it(ax, size, 1.25, exp=True)
    pad = scale_it(ax, pad, 0.1)

    if xticklabels is not None:
        ax.set_xticklabels(xticklabels, minor=True)

    if yticklabels is not None:
        ax.set_yticklabels(yticklabels, minor=True)

    if axes is 'both':
        axes = ['x', 'y']

    for axis in axes:
        ax.tick_params(axis=axis,
                       which='minor',
                       labelsize=size,
                       labelcolor=color,
                       labelleft=left,
                       labelright=right,
                       labeltop=top,
                       labelbottom=bottom, **kwargs)

        ax.tick_params(axis=axis, which='minor',
                       pad=pad)  # this doesn't play well with others...

    plt.setp(ax.xaxis.get_minorticklabels(), rotation=xrotation)
    plt.setp(ax.yaxis.get_minorticklabels(), rotation=yrotation)

    return ax


def set_major_ticks(ax, axes='both',
                    xticks=None, yticks=None, direction='out', width=0.1,
                    size=2, color=COLORS['light gray'],
                    left=True, right=False, bottom=True, top=False,
                    xlocator=None, xinterval=None, xformatter=None, **kwargs):
    """
    Modify major tick settings.

    :param ax: (mpl.axes) - plot axis
    :param axes: (list) - x and/or y axis to change
    :param xticks: (list) - manually set x major ticks
    :param yticks: (list) - manually set y major ticks
    :param direction: (str) - direction of tick
    :param width: (str) - width of major ticks
    :param size: (str) - length of major ticks
    :param color: (str) - color of major ticks
    :param bottom: (boolean) - whether to show bottom major tick
    :param top: (boolean) - whether to show top major tick
    :param left: (boolean) - whether to show left major tick
    :param right: (boolean) - whether to show right major tick
    :param xlocator: (str) - auto, years, months, days, hours, interval of tick
    :param xinterval: (str) - interval of date ticks
    :param xformatter: (str) - how to display the major tick labels
    :param kwargs: (kwargs) - additional keyword arguments
    :return ax: (mpl.axes) - plot axis
    """
    size = scale_it(ax, size, 1, exp=True)
    width = scale_it(ax, width, 0.1)

    date = False
    locator = None

    if xticks is not None:
        ax.set_xticks(xticks)
    elif isinstance(xlocator, str):
        if xlocator == 'auto':
            locator = AutoDateLocator()
        elif xlocator == 'years':
            locator = YearLocator(base=int(xinterval))
        elif xlocator == 'months':
            locator = MonthLocator(interval=xinterval)
        elif xlocator == 'days':
            locator = DayLocator(interval=xinterval)
        elif xlocator == 'hours':
            locator = HourLocator(interval=xinterval)
        elif xlocator == 'minutes':
            locator = MinuteLocator(interval=xinterval)
        date = True
    elif isinstance(xlocator, int) or isinstance(xlocator, float):
        locator = MultipleLocator(xlocator)

    if xformatter is not None:
        if date:
            if xformatter is 'auto'and locator is not None:
                ax.xaxis.set_major_formatter(AutoDateFormatter(locator))
            else:
                ax.xaxis.set_major_formatter(DateFormatter(xformatter))
        else:
            ax.xaxis.set_major_formatter(FormatStrFormatter(xformatter))

    if locator is not None:
        ax.xaxis.set_major_locator(locator)

    if yticks is not None:
        ax.set_yticks(yticks)

    if axes is 'both':
        axes = ['x', 'y']

    for axis in axes:
        ax.tick_params(axis=axis,
                       which='major',
                       direction=direction,
                       left=left,
                       right=right,
                       bottom=bottom,
                       top=top,
                       size=size,
                       width=width,
                       color=color,
                       **kwargs)
    return ax


def set_minor_ticks(ax, axes='both',
                    xticks=None, yticks=None, direction='out', width=0.1,
                    size=2, color=COLORS['light gray'],
                    left=False, right=False, bottom=True, top=False,
                    xlocator=None, xinterval=3, xformatter=None, **kwargs):
    """
    Modify minor tick settings.

    :param ax: (mpl.axes) - plot axis
    :param axes: (list) - x and/or y axis to change
    :param xticks: (list) - manually set x minor ticks
    :param yticks: (list) - manually set y minor ticks
    :param direction: (str) - direction of tick
    :param width: (str) - width of minor ticks
    :param size: (str) - length of minor ticks
    :param color: (str) - color of minor ticks
    :param bottom: (boolean) - whether to show bottom minor tick
    :param top: (boolean) - whether to show top minor tick
    :param left: (boolean) - whether to show left minor tick
    :param right: (boolean) - whether to show right minor tick
    :param xlocator: (str) - auto, years, months, days, hours, interval of tick
    :param xinterval: (str) - interval of date ticks
    :param xformatter: (str) - how to display the minor tick labels
    :return ax: (mpl.axes) - plot axis
    """
    # size = scale_it(ax, size, scale=scale, what='tick')

    size = scale_it(ax, size, 1, exp=True)
    width = scale_it(ax, width, 0.1)

    date = False
    locator = None

    if xticks is not None:
        ax.set_xticks(xticks)
    elif isinstance(xlocator, str):
        if xlocator == 'years':
            locator = YearLocator(base=int(xinterval))
        elif xlocator == 'months':
            locator = MonthLocator(interval=xinterval)
        elif xlocator == 'days':
            locator = DayLocator(interval=xinterval)
        elif xlocator == 'hours':
            locator = HourLocator(interval=xinterval)
        elif xlocator == 'minutes':
            locator = MinuteLocator(interval=xinterval)
        date = True
    elif isinstance(xlocator, int) or isinstance(xlocator, float):
        locator = MultipleLocator(xlocator)

    if locator is not None:
        ax.xaxis.set_minor_locator(locator)

    if xformatter is not None:
        if date:
            if xformatter is 'auto' and locator is not None:
                ax.xaxis.set_minor_formatter(AutoDateFormatter(locator))
            else:
                ax.xaxis.set_minor_formatter(DateFormatter(xformatter))
        else:
            ax.xaxis.set_minor_formatter(FormatStrFormatter(xformatter))

    if yticks is not None:
        ax.set_yticks(yticks)

    if axes is 'both':
        axes = ['x', 'y']

    for axis in axes:
        ax.tick_params(axis=axis,
                       which='minor',
                       direction=direction,
                       left=left,
                       right=right,
                       bottom=bottom,
                       top=top,
                       size=size,
                       width=width,
                       color=color,
                       **kwargs)
    return ax


def set_major_grid(ax, xgrid=True, ygrid=True, linestyle=(0, (16, 4)),
                   linewidth=0.095,
                   xcolor=COLORS['black'], ycolor=COLORS['black'],
                   xalpha=ALPHAS['translucid'], yalpha=ALPHAS['translucid'],
                   **kwargs):
    """
    Modify major grid settings.

    :param ax: (mpl.axes) - plot axis
    :param xgrid: (boolean) - whether to show vertical major grid
    :param ygrid: (boolean) - whether to show horizontal major grid
    :param linestyle: (str) - linestyle of major grid
    :param xcolor: (str) - color of vertical major grid
    :param ycolor: (str) - color of horizontal major grid
    :param xalpha: (scalar) - transparency of vertical major grid
    :param yalpha: (scalar) - transparency of horizontal major grid
    :param kwargs: (kwargs) - additional keyword arguments
    :return ax: (mpl.axes) - plot axis
    """
    geom = plt.getp(plt.getp(ax, 'subplotspec'), 'geometry')
    nplots = geom[0] * geom[1] / 100

    linewidth = scale_it(ax, linewidth, 0.15, exp=True)
    linewidth = np.log(nplots + 1) + linewidth

    if xgrid:
        ax.xaxis.grid(b=xgrid,
                      which='major',
                      linestyle=linestyle,
                      linewidth=linewidth,
                      alpha=xalpha,
                      **kwargs
                      )
    else:
        ax.yaxis.grid(b=xgrid,
                      which='major',
                      alpha=0,
                      **kwargs
                      )

    if ygrid:
        ax.yaxis.grid(b=ygrid,
                      which='major',
                      color=ycolor,
                      linestyle=linestyle,
                      linewidth=linewidth,
                      alpha=yalpha,
                      **kwargs
                      )
    else:
        ax.yaxis.grid(b=ygrid,
                      which='major',
                      alpha=0,
                      **kwargs
                      )

    return ax


def set_minor_grid(ax, xgrid=True, ygrid=True, linestyle=(0, (5, 5)),
                   linewidth=0.095,
                   xcolor=COLORS['black'], ycolor=COLORS['black'],
                   xalpha=ALPHAS['translucent'], yalpha=ALPHAS['translucent'],
                   **kwargs):
    """
    Modify minor grid settings.

    :param ax: (mpl.axes) - plot axis
    :param xgrid: (boolean) - whether to show vertical minor grid
    :param ygrid: (boolean) - whether to show horizontal minor grid
    :param linestyle: (str) - linestyle of minor grid
    :param xcolor: (str) - color of vertical minor grid
    :param ycolor: (str) - color of horizontal minor grid
    :param xalpha: (scalar) - transparency of vertical minor grid
    :param yalpha: (scalar) - transparency of horizontal minor grid
    :param kwargs: (kwargs) - additional keyword arguments
    :return ax: (mpl.axes) - plot axis
    """
    linewidth = scale_it(ax, linewidth, 0.45)

    if xgrid:
        ax.xaxis.grid(b=xgrid,
                      which='minor',
                      linestyle=linestyle,
                      linewidth=linewidth,
                      alpha=xalpha,
                      **kwargs
                      )
    else:
        ax.yaxis.grid(b=xgrid,
                      which='minor',
                      alpha=0,
                      **kwargs
                      )

    if ygrid:
        ax.yaxis.grid(b=ygrid,
                      which='minor',
                      color=ycolor,
                      linestyle=linestyle,
                      linewidth=linewidth,
                      alpha=yalpha,
                      **kwargs
                      )
    else:
        ax.yaxis.grid(b=ygrid,
                      which='minor',
                      alpha=0,
                      **kwargs
                      )

    return ax


def set_borders(ax, all_=True,
                bottom=True, top=True, left=True, right=True,
                spines='all', color=COLORS['light gray'],
                alpha=ALPHAS['semi opaque']):
    """
    Modify border settings.

    :param ax: (mpl.axes) - plot axis
    :param all: (boolean) - whether to show all borders
    :param bottom: (boolean) - whether to show bottom border
    :param top: (boolean) - whether to show top border
    :param left: (boolean) - whether to show left border
    :param right: (boolean) - whether to show right border
    :param spines: (list) - borders to be affected
    :param color: (str) - color of borders
    :param alpha: (str) - transparency of borders
    :return ax: (mpl.axes) - plot axis
    """
    if spines is 'all':
        spines = ['top', 'bottom', 'left', 'right']

    for spine in spines:
        ax.spines[spine].set_color(color)
        ax.spines[spine].set_alpha(alpha)
        if not all_:
            ax.spines[spine].set_visible(False)

    if not left:
        ax.spines['left'].set_visible(False)
    if not right:
        ax.spines['right'].set_visible(False)
    if not bottom:
        ax.spines['bottom'].set_visible(False)
    if not top:
        ax.spines['top'].set_visible(False)

    return ax


def set_labels(ax,
               xlabel=None,
               ylabel=None,
               title=None,
               title_size=13.5,
               title_color=COLORS['black'],
               title_alpha=ALPHAS['semi opaque'],
               title_pad=0.965,
               xlabel_size=11,
               xlabel_color=COLORS['black'],
               xlabel_alpha=ALPHAS['semi opaque'],
               xlabel_pad=0.05,
               ylabel_size=11,
               ylabel_color=COLORS['black'],
               ylabel_alpha=ALPHAS['semi opaque'],
               ylabel_pad=0.05,
               length_scale=True,
               suptitle=False,
               ):
    """
    Add and modify title and label settings.

    :param ax: (mpl.axes) - plot axis
    :param xlabel: (str) - label of x axis
    :param ylabel: (str) - label of y axis
    :param title: (str) - title of subplot
    :param title_size: (scalar) - size of title
    :param title_color: (str) - color of title
    :param title_alpha: (scalar) - transparency of title
    :param title_pad: (scalar) - distance between box and title
    :param xlabel_size: (scalar) - size of x label
    :param xlabel_color: (str) - color of x label
    :param xlabel_alpha: (scalar) - transparency of x label
    :param xlabel_pad: (scalar) - distance between ticks and x label
    :param ylabel_size: (scalar) - size of y label
    :param ylabel_color: (str) - color of y label
    :param ylabel_alpha: (scalar) - transparency of y label
    :param ylabel_pad: (scalar) - distance between ticks and y label
    :param length_scale: (scalar) - whether to scale the labels based on length
    :param suptitle: (boolean) - whether to make a figure title
    :return ax: (mpl.axes) - plot axis
    """
    title_size = scale_it(ax, title_size, 3, exp=True)
    title_pad = 2 * title_pad - scale_it(ax, title_pad, 0.005)
    if suptitle:
        title_pad += title_pad / 35
        title_size += title_size / 3

    xlabel_size = scale_it(ax, xlabel_size, 3, exp=True)
    xlabel_pad = scale_it(ax, xlabel_pad, 1)

    ylabel_size = scale_it(ax, ylabel_size, 3, exp=True)
    ylabel_pad = scale_it(ax, ylabel_pad, 1)

    if title is None:
        title = plt.getp(ax, 'title')

    if ylabel is None:
        ylabel = plt.getp(ax, 'ylabel')

    if xlabel is None:
        xlabel = plt.getp(ax, 'xlabel')

    if length_scale:
        length_scale = len(str(title)) / 3
        title_size -= length_scale
        ylabel_size -= length_scale / 2
        xlabel_size -= length_scale / 2

    if suptitle:
        plt.suptitle(title,
                     size=title_size,
                     color=title_color,
                     alpha=title_alpha,
                     y=title_pad)
    else:
        ax.set_title(title,
                     size=title_size,
                     color=title_color,
                     alpha=title_alpha,
                     y=title_pad)

    xlabel_pad += 2
    ax.set_xlabel(xlabel,
                  size=xlabel_size,
                  color=xlabel_color,
                  alpha=xlabel_alpha,
                  labelpad=xlabel_pad)

    ylabel_pad += 5
    ax.set_ylabel(ylabel,
                  size=ylabel_size,
                  color=ylabel_color,
                  alpha=ylabel_alpha,
                  labelpad=ylabel_pad)

    return ax


def set_legend(ax, size=12,
               color=COLORS['black'], alpha=ALPHAS['translucent'],
               loc='best', frame=False, ncol=1, nscatter=1, **kwargs):
    """
    Add and modify legend settings.

    :param ax: (mpl.axes) - plot axis
    :param size: (str) - size of legend labels
    :param color: (str) - color of legend labels
    :param alpha: (str) - transparency of legend labels
    :param loc: (str) - location of legend
    :param frame: (boolean) - whether to have a box around legend
    :param ncol: (int) - number of legend columns
    :param nscatter: (int) - number of scatter points to show in legend
    :param kwargs: (kwargs) - additional keyword arguments
    :return ax: (mpl.axes) - plot axis
    """
    if plt.getp(ax, 'legend_handles_labels')[1]:
        size = scale_it(ax, size, 1, exp=True)
        start_locs = ['lower', 'upper', 'center']

        try:
            if loc is not 'best':
                loc_keywords = get_loc_keywords(loc)
                if loc_keywords[0] not in start_locs:
                    loc_keywords = loc_keywords[::-1]
                loc = ' '.join(loc_keywords)
        except:
            pass

        legend = ax.legend(loc=loc,
                           ncol=ncol,
                           fontsize=size,
                           frameon=frame,
                           scatterpoints=nscatter,
                           **kwargs
                           )

        for text in legend.get_texts():
            plt.setp(text, size=size, alpha=alpha, color=color)

        return ax


def set_inherited(ax, xlabel='', ylabel='', title='',
                  xlim=None, ylim=None, origin_xlim=None, origin_ylim=None):
    """
    Get inputs from existing plot and set them again.

    :param ax: (mpl.axes) - plot axis
    :param xlabel: (str) - label of x axis
    :param ylabel: (str) - label of y axis
    :param title: (str) - title of subplot
    :param xlim: (tup) - left and right x axis limit in a tuple, respectively
    :param ylim: (tup) - left and right y axis limit in a tuple, respectively
    :return ax: (mpl.axes) - plot axis
    """
    if xlabel is '':
        xlabel = plt.getp(ax, 'xlabel')
    if ylabel is '':
        ylabel = plt.getp(ax, 'ylabel')
    if title is '':
        title = plt.getp(ax, 'title')

    prev_xlim = plt.getp(ax, 'xlim')
    try:
        if origin_xlim is None:
            origin_xlim = xlim
        try:
            int(xlim[0])
        except:
            xlim = mdates.date2num(xlim)

        if xlim is None:
            xlim = prev_xlim
        elif xlim[0] > prev_xlim[0] and xlim[1] < prev_xlim[1]:
            xlim = (prev_xlim[0], prev_xlim[1])
        elif xlim[0] > prev_xlim[0]:
            xlim = (prev_xlim[0], xlim[1])
        elif xlim[1] < prev_xlim[1]:
            xlim = (xlim[0], prev_xlim[1])
    except:
        print('Unable to inherit xlim!')

    prev_ylim = plt.getp(ax, 'ylim')
    if ylim is None:
        ylim = prev_ylim
    elif ylim[0] > prev_ylim[0] and ylim[1] < prev_ylim[1]:
        ylim = (prev_ylim[0], prev_ylim[1])
    elif ylim[0] > prev_ylim[0]:
        ylim = (prev_ylim[0], ylim[1])
    elif ylim[1] < prev_ylim[1]:
        ylim = (ylim[0], prev_ylim[1])

    if origin_xlim is not None:
        xlim = origin_xlim

    if origin_ylim is not None:
        ylim = origin_ylim

    return ax, xlabel, ylabel, title, xlim, ylim


def savefig(file_path, tight_layout=True, both=False, dpi=DEFAULT['dpi'],
            suffix='auto', close=True, **kwargs):
    """
    Save figure.

    :param file_path: (str) - path to file
    :param tight_layout: (boolean) - whether to save with tight layout
    :param both: (boolean) - whether to save both png and pdf
    :param suffix: (str/boolean) - whether to append png if not exist
    :param close: (boolean) - whether to close figure after saving
    :param kwargs: (kwargs) - additional keyword arguments
    :return file_path: (str) - path to file
    """
    if tight_layout:
        bbox_inches = 'tight'
    else:
        bbox_inches = None

    if both:
        png_path = file_path + '.png'
        plt.savefig(png_path, bbox_inches=bbox_inches, dpi=dpi)
        pdf_path = file_path + '.pdf'
        plt.savefig(pdf_path, bbox_inches=bbox_inches)
    elif suffix is 'auto':
        if not file_path.endswith('.png') and not file_path.endswith('.pdf'):
            file_path += '.png'
            print('Suffix .png was appended to filepath!')
        plt.savefig(file_path, bbox_inches=bbox_inches, dpi=dpi, **kwargs)

    utils(close=close)

    return file_path


def utils(close=False, figsize=None, ax=False, rows=1, cols=1, pos=1,
          tight_layout=False, projection=None):
    """
    :param close: (boolean) - whether to close subplots
    :param figsize: (str/tup) - wide/tall/auto or tuple width x height of fig
    :param ax: (boolean) - whether to return subplot
    :param rows: (boolean) - whether to close subplots
    :param cols: (boolean) - whether to close subplots
    :param pos: (boolean) - whether to close subplots
    :param tight_layout: (boolean) - whether to save with tight layout
    :param projection: (cartopy.crs) - projection of map
    """
    if figsize is not None:
        fig = plt.figure(figsize=figsize)
        return fig
    if ax:
        projection = _get_projection_logic(projection)
        return plt.subplot(rows, cols, pos, projection=projection)
    if tight_layout:
        try:
            plt.tight_layout()
        except:
            print('Unable to set tight layout!')
    if close:
        plt.close('all')


def scale_it(ax, value, order_mag=1, exp=False):
    """
    Scale matplotlib plots

    :param ax: (mpl.axes) - plot axis
    :param value: (scalar) - value to be scaled
    :param order_mag: (scalar) - the order of magnitude to scale by
    :param exp: (boolean) - whether scaling should be exponential
    :return scaled_value: (scalar) - scaled value
    """
    bbox = ax.get_window_extent()
    width, height = bbox.width / 72., bbox.height / 72.

    geom = plt.getp(ax, 'geometry')
    nrows = geom[0]
    ncols = geom[1]

    nplots = nrows * ncols
    size_drop = np.power(nplots, 0.2)

    if height > width:
        major = height
        minor = width
    else:
        major = width
        minor = height
    base_term = height + width
    power_term = (minor + (major / 2) / major)
    factor = np.sqrt(np.log(np.power(base_term, power_term)) / 2)
    if exp:
        return np.power(value + factor * order_mag, 1.05) / size_drop
    else:
        return (value + factor * order_mag)


def scale_it_bokeh(p, value, order_mag=1, exp=False):
    """
    Scale bokeh plots

    :param p: (bokeh.figure) - bokeh figure
    :param value: (scalar) - value to be scaled
    :param order_mag: (scalar) - the order of magnitude to scale by
    :param exp: (boolean) - whether scaling should be exponential
    :return scaled_value: (scalar) - scaled value
    """
    width, height = p.plot_width / 36, p.plot_height / 36

    if height > width:
        major = height
        minor = width
    else:
        major = width
        minor = height
    base_term = height + width
    power_term = (minor + (major / 2) / major)

    factor = np.sqrt(np.log(base_term * power_term) / 2)

    if exp:
        return np.power(value + factor * order_mag, 1.05)
    else:
        return value + factor * order_mag

############################################################################
# Private utils to clean up code...


def _set_figsize_logic(sidebar_pos=None,
                       figsize=None,
                       rows=1, cols=1,
                       pos=1, dpi=None):
    if sidebar_pos is None:
        if figsize is not None and pos == 1:
            set_figsize(figsize=figsize, rows=rows,
                        cols=cols, pos=pos, dpi=dpi)
        elif figsize is None and pos == 1:
            set_figsize(figsize='wide', rows=rows,
                        cols=cols, pos=pos, dpi=dpi)
    else:
        if figsize is not None and pos == 1 and sidebar_pos == 1:
            set_figsize(figsize=figsize, rows=rows,
                        cols=cols, pos=pos, dpi=dpi)
        elif figsize is None and pos == 1 and sidebar_pos == 1:
            set_figsize(figsize='wide', rows=rows,
                        cols=cols, pos=pos, dpi=dpi)


def _get_xtext_logic(x=None):
    xtext = False
    xstr = False
    xticklabels = None

    try:
        xstr = isinstance(x[0], str)
    except Exception:
        xstr = isinstance(x, str)

    if xstr:
        xticklabels = copy.copy(x)
        x = np.arange(len(xticklabels))
        xtext = True

    return x, xtext, xticklabels


def _get_x_to_y_logic(x, y):
    if y is None:
        y = copy.copy(x)
        x = range(len(y))
    return x, y


def _get_xlim_logic(x, xlim, pad=0, align='edge'):
    origin_xlim = xlim  # store past xlim
    try:
        if xlim is None:
            if align == 'edge':
                xlim = (np.min(x) - pad / 3, np.max(x) + pad * 1.25)
            else:
                xlim = (np.min(x) - pad * 1.25, np.max(x) + pad * 1.25)
    except TypeError:
        if xlim is None:
            xdiff = x[1] - x[0]
            if align == 'edge':
                xlim = (x[0] - xdiff / 5, x[-1] + xdiff)
            else:
                xlim = (x[0] - xdiff / 2, x[-1] + xdiff / 1.5)
    return origin_xlim, xlim


def _get_ylim_logic(y, ylim):
    origin_ylim = ylim
    try:
        if ylim is None:
            ylim = (np.min(y), np.max(y))
    except TypeError:
        ylim = None
    return origin_ylim, ylim


def _get_ax_logic(ax=None, twinx=None, twiny=None,
                  rows=1, cols=1, pos=1,
                  transform=False, projection=None):
    if twinx is None and twiny is None:
        if ax is None:
            if projection is not None:
                ax = plt.subplot(rows, cols, pos, projection=projection)
            else:
                ax = plt.subplot(rows, cols, pos)
    else:
        if twinx is not None:
            ax = twinx.twinx()
            rows = plt.getp(twinx, 'geometry')[0]
            cols = plt.getp(twinx, 'geometry')[1]

    return ax, rows, cols


def _get_bases_logic(data=None):
    if isinstance(data, pd.DataFrame):
        data = data.values

    try:
        maxmin_diff = (np.percentile(data, 95) -
                       np.abs(np.percentile(data, 5))
                       )
    except:
        maxmin_diff = np.max(data) - np.abs(np.min(data))

    maxmin_diff = np.abs(maxmin_diff)

    if maxmin_diff <= 0.005:
        base = 0.0125
        base2 = 0.025
    elif maxmin_diff <= 0.05:
        base = 0.025
        base2 = 0.05
    elif maxmin_diff <= 0.35:
        base = 0.05
        base2 = 0.1
    elif maxmin_diff <= 1:
        base = 0.1
        base2 = 0.2
    else:
        base = 5
        base2 = 5

    return base, base2


def _get_vmin_vmax_logic(data=None, base=1,
                         vmin=None, vmax=None,
                         data_lim=None):
    if isinstance(data, pd.DataFrame):
        data = data.values

    if data_lim is None:
        if vmin is None:
            try:
                vmin = round_to(np.percentile(data, 7.5),
                                prec=5,
                                base=base)
            except ValueError:
                vmin = round_to(np.nanpercentile(data, 7.5),
                                prec=5,
                                base=base)
        if vmax is None:
            try:
                vmax = round_to(np.percentile(data, 97.5),
                                prec=5,
                                base=base)
            except ValueError:
                vmax = round_to(np.nanpercentile(data, 97.5),
                                prec=5,
                                base=base)
        if vmin == vmax:
            vmin = np.percentile(data, 10)
            vmax = np.percentile(data, 97.5)
    else:
        vmin = data_lim[0]
        vmax = data_lim[1]

    return vmin, vmax


def _get_stats_logic(ax, y,
                     norm=False,
                     anom=False,
                     norm_anom=False,
                     cumsum=False,
                     ):
    if anom:
        y = get_anom(y)
    if norm:
        y = get_norm(y)
    if norm_anom:
        y = get_norm_anom(y)
    if cumsum:
        y = np.cumsum(y)
    return y


def _show_stats_logic(ax, y, stats):
    if stats:
        stats_str = get_stats(y, show=False)
        if isinstance(stats, str):
            set_axtext(ax, stats_str, loc=stats)
        else:
            set_axtext(ax, stats_str, loc='top left')


def _get_interval_logic(interval=None,
                        vmin=None, vmax=None,
                        base=1, oom=1):
    if interval is None:
        interval = (np.absolute(vmin) + np.absolute(vmax)) / 5.
        if interval > 1:
            interval = round_to(interval, base=base)
            if interval == 0:
                interval = 1
            if (vmax - vmin) % interval != 0:
                interval = np.power(10, oom) / 2
                vmin += (vmax - vmin) % interval
        elif interval < 0.1:
            interval = round_to(interval, base=base)
            if interval == 0:
                interval = 0.01
        elif interval < 1:
            interval = round_to(interval, base=base)
            if interval == 0:
                interval = 0.1
    vmax_vmin_total = np.abs(vmax) + np.abs(vmin)
    if interval < vmax_vmin_total / 150.:
        interval = round_to(vmax_vmin_total / 2., 5) / interval
    return interval


def _get_fmt_logic(fmt=None, interval=None):
    interval = np.abs(interval)
    if fmt is None:
        if interval < 0.25:
            fmt = '%.2f'
        elif interval < 1:
            fmt = '%.1f'
        elif interval >= 1:
            fmt = '%1d'
    return fmt


def _fix_vmin_vmax_logic(vmin=None, vmax=None,
                         data=None, interval=1):
    if isinstance(data, pd.DataFrame):
        data = data.values

    if vmin == vmax:
        vmin = np.min(data)
        vmax = vmin + interval * 10

    return vmin, vmax


def _get_tick_locs_cbar_count_logic(tick_locs=None, vmin=None,
                                    vmax=None, interval=1):
    if tick_locs is None:
        tick_locs = np.arange(vmin, vmax + interval, interval)

    cbar_count = len(tick_locs) - 1

    if len(tick_locs) > 20:
        tick_locs = tick_locs[::4]
    elif len(tick_locs) > 10:
        tick_locs = tick_locs[::2]

    return tick_locs, cbar_count


def _save_logic(save='', tight_layout='auto', close=False,
                dpi=None, pos=1, rows=1, cols=1):
    if not close and pos == (rows * cols):
        utils(tight_layout=True)
    if save is not '':
        if tight_layout == 'on' or (tight_layout == 'auto' and
                                    pos == (rows * cols)):
            savefig(save, close=close, tight_layout=True, dpi=dpi)
        else:
            savefig(save, close=close, tight_layout=False, dpi=dpi)
    else:
        if tight_layout == 'on' or (tight_layout == 'auto' and
                                    pos == (rows * cols)):
            utils(tight_layout=True)


def _set_share_logic(ax=None, rows=1, cols=1,
                     sharex=None, sharey=None,
                     xlabel=None, ylabel=None):
    if sharex is not None:
        set_share(ax, sharex, axis='x', xlabel=xlabel)
        rows = plt.getp(sharex, 'geometry')[0]
        cols = plt.getp(sharex, 'geometry')[1]
    if sharey is not None:
        set_share(ax, sharey, axis='y', ylabel=ylabel)
        rows = plt.getp(sharey, 'geometry')[0]
        cols = plt.getp(sharey, 'geometry')[1]
    return rows, cols


def _set_datetime_logic(ax=None,
                        minor_date_ticks=False,
                        title_pad=0):
    major_xlocator, major_xinterval, major_xformatter, \
        minor_xlocator, minor_xinterval, minor_xformatter, dt_bool = \
        set_date_ticks(ax, minor_date_ticks=minor_date_ticks)

    if minor_date_ticks:
        title_pad += 0.14

    if dt_bool:
        return (major_xlocator, major_xinterval, major_xformatter,
                minor_xlocator, minor_xinterval, minor_xformatter,
                title_pad)
    else:
        return [None] * 6 + [title_pad]


def _settings_logic(ax=None, x=None, twinx=None, twiny=None, xticks=None,
                    major_xlocator=None, major_xinterval=None,
                    major_xformatter=None, xlabel='',
                    ylabel='', title='', suptitle=False, title_pad=0.965,
                    aligned=True, length_scale=True,
                    xtext=False, xticklabels=None,
                    minor_date_ticks=True):
    (major_xlocator, major_xinterval, major_xformatter,
        minor_xlocator, minor_xinterval, minor_xformatter, title_pad) = \
        _set_datetime_logic(ax=ax,
                            minor_date_ticks=minor_date_ticks,
                            title_pad=title_pad)

    if twinx is None and twiny is None:
        set_major_tick_labels(ax)
        try:
            set_major_ticks(ax, xticks=xticks,
                            xlocator=major_xlocator,
                            xinterval=major_xinterval,
                            xformatter=major_xformatter)
        except:
            set_major_ticks(ax)
        set_major_grid(ax)
        set_borders(ax)
        set_labels(ax, xlabel=xlabel, ylabel=ylabel, suptitle=suptitle,
                   title=title, title_pad=title_pad, length_scale=length_scale)
    else:
        if twinx is not None:
            set_twin(ax, twinx, axis='x', suptitle=suptitle,
                     title_pad=title_pad,
                     xlabel=xlabel, ylabel=ylabel, title=title,
                     aligned=aligned, length_scale=length_scale)

    if xtext:
        plt.xticks(x, xticklabels)


def _get_color_logic(color, facecolor, edgecolor, matchcolor):
    if color is not None:
        facecolor = color
        edgecolor = color
    if matchcolor:
        edgecolor = facecolor
    return facecolor, edgecolor


def _get_dt_from_pd_logic(x):
    if isinstance(x, pd.DatetimeIndex):
        return x.to_pydatetime()
    else:
        return x


def _get_width_logic(x):

    try:
        try:
            width = np.round(np.average(np.diff(x)), 0) / 1.2
        except (ValueError, IndexError, TypeError):
            width = 0.833333333
    except:
        days_multiplier = (x[1] - x[0]).total_seconds() / 3600. / 24.
        width = 0.833333333 * days_multiplier

    return width


def _set_heatmap_mask(ax, df, mask, size):
    for j, i in np.column_stack(np.where(mask)):
        try:
            ax.text(i + 0.5, j + 0.5, '{:.2f}'.format(df[j, i]),
                    color=COLORS['light gray'], alpha=0.75,
                    va='center', ha='center', size=size)
        except:
            pass


def _fix_contourf_logic(contourf, interval, vmin, vmax):
    if len(contourf) < 6:
        contourf = np.linspace(vmin, vmax, 8)
        interval = np.diff(contourf).mean()
        return contourf, interval
    else:
        return contourf, interval


def _balance_logic(balance, vmin, vmax):
    vmin_vmax_signs = np.sign([vmin, vmax])
    if balance:
        if 1 in vmin_vmax_signs and -1 in vmin_vmax_signs:
            if np.abs(vmin) >= np.abs(vmax):
                vmax = -vmin
            else:
                vmin = -vmax
            print('vmin and vmax were balanced!')
    return vmin, vmax


def _add_features(ax, land, ocean, coastlines, states,
                  countries, lakes, rivers):
    import cartopy.feature as cfeature

    if land:
        ax.add_feature(cfeature.LAND, zorder=100)
    if ocean:
        ax.add_feature(cfeature.OCEAN, zorder=100)
    if coastlines:
        ax.add_feature(cfeature.COASTLINE, linestyle='-',
                       alpha=.85, edgecolor='black')
    if states:
        feature_name = 'admin_1_states_provinces_lines'
        states_provinces = cfeature.NaturalEarthFeature(category='cultural',
                                                        name=feature_name,
                                                        scale='10m',
                                                        facecolor='none')
        ax.add_feature(states_provinces,
                       edgecolor='black',
                       linestyle='-',
                       alpha=.95)
    if countries:
        ax.add_feature(cfeature.BORDERS,
                       edgecolor='black',
                       linestyle='-',
                       alpha=.95)
    if lakes:
        ax.add_feature(cfeature.LAKES, alpha=0.95)

    if rivers:
        ax.add_feature(cfeature.RIVERS, alpha=0.95)


def _get_lat_lon_lim_logic(latlim, lonlim,
                           lat1, lat2, lon1, lon2,
                           central_longitude=0, region=None):
    if latlim is not None:
        lat1 = latlim[0]
        lat2 = latlim[1]
    if lonlim is not None:
        lon1 = lonlim[0] - central_longitude
        lon2 = lonlim[1] - central_longitude

    lat1, lat2, lon1, lon2 = get_region_latlim(region,
                                               lat1=lat1,
                                               lat2=lat2,
                                               lon1=lon1,
                                               lon2=lon2)

    return lat1, lat2, lon1, lon2


def _get_projection_logic(projection, lons=None, central_longitude=0):
    import cartopy.crs as ccrs
    if projection is None:
        if central_longitude != 0:
            lons -= central_longitude
            projection = ccrs.PlateCarree(central_longitude=central_longitude)
        else:
            projection = ccrs.PlateCarree()
    return projection


def _set_contour_logic(ax, lons2, lats2, data2, contour,
                       projection, fmt, clabel):
    if contour is not None:
        im1 = ax.contour(lons2,
                         lats2,
                         data2,
                         contour, linewidths=0.7, alpha=0.85,
                         colors='k', linestyles='solid',
                         transform=projection)
        if clabel:
            clabels = plt.clabel(im1, fontsize=8, inline=1, fmt=fmt)
            [txt.set_bbox(dict(facecolor='white',
                               edgecolor='none',
                               boxstyle='round',
                               pad=0, alpha=0.3)
                          ) for txt in clabels]


def _parse_style(style):
    style = str(style)
    styles = style.split('/')
    ptype = styles[0]

    try:
        color = styles[1]
    except:
        color = COLORS['red']

    try:
        linestyle = styles[2]
    except:
        linestyle = '-'

    try:
        marker = styles[3]
    except:
        marker = ''

    if ptype == '':
        ptype = 'line'

    if linestyle == '':
        linestyle = '-'

    return ptype, color, linestyle, marker


def _pop_keys(vis_dict, ptype):
    drop_dict = {'line': ['matchcolor', 'facecolor', 'edgecolor',
                          'width', 'height', 'align', 'sidebar_count',
                          'sidebar_pos', 'bar_vals', 'stack',
                          's', 'c', 'cbar', 'cmap', 'orientation',
                          'interval', 'tick_locs', 'fmt', 'pad', 'size'
                          ],
                 'bar': ['s', 'c', 'cbar', 'cmap', 'projection'
                         'interval', 'tick_locs', 'fmt', 'pad',
                         'marker', 'stack', 'size'
                         ],
                 'scatter': ['matchcolor', 'width', 'height',
                             'align', 'sidebar_count', 'stack',
                             'sidebar_pos', 'bar_vals'
                             ]
                 }

    for key in drop_dict[ptype]:
        vis_dict.pop(key, None)
    return vis_dict
