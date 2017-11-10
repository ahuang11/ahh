from ahh import vis, ext, sci
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from scipy.stats import pearsonr

sleep_df = pd.read_pickle('sleep_data_fmt.pkl')
sleep_hours = sleep_df['minutes'] / 60
sleep_quality = sleep_df['quality'] * 100

sleep_df_interp = sleep_df
sleep_df_interp['minutes'][sleep_df_interp.index[0]] = 9
sleep_hours_interp = sleep_df_interp['minutes'].interpolate() / 60

wx_df = pd.read_csv('kcmi_wx.csv') # https://www.wunderground.com/history/airport/KCMI/2014/1/1/
tmp = wx_df['Mean TemperatureF']

x = mdates.date2num(sleep_df_interp.index)
xx = np.linspace(x.min(), x.max(), len(sleep_df_interp.index))

z4 = np.polyfit(x, sleep_hours_interp, 4)
p4 = np.poly1d(z4)

sleep_fit = p4(xx)

fig, ax = vis.plot(sleep_df.index, sleep_hours, y2=sleep_fit,
         bar=True, bar_dates=True, save='andrew_sleep', sharex=True,
         figsize=(70, 20), major='months', interval=3, width=0.65,
         title="Andrew's Daily Sleep (2014 - 2016)", ylabel='Hours',
         titlescale=4, fontscale=3.5, labelscale=3.5, linewidth2=5,
         minor='years')

years = range(2014,2017)
yearly_sleep_avg_list = []
yearly_sleep_std_list = []

months = range(1, 13)
monthly_sleep_avg_list = []
monthly_sleep_std_list = []
sleep_quality_avg_list = []
yr_monthly_sleep_avg_list = []
yr_monthly_quality_avg_list = []

sleep_masked = np.ma.masked_array(sleep_hours, np.isnan(sleep_hours))
quality_masked = np.ma.masked_array(sleep_quality, np.isnan(sleep_quality))

for year in years:
    year_idc = np.where(pd.DatetimeIndex(sleep_df.index).year == year)[0]
    yearly_sleep_avg_list.append(np.ma.average(sleep_masked[year_idc]))
    yearly_sleep_std_list.append(np.std(sleep_hours[year_idc]))

for month in months:
    month_idc = np.where(pd.DatetimeIndex(sleep_df.index).month == month)[0]
    monthly_sleep_avg_list.append(np.ma.average(sleep_masked[month_idc]))
    monthly_sleep_std_list.append(np.std(sleep_hours[month_idc]))
    sleep_quality_avg_list.append(np.ma.average(quality_masked[month_idc]))

months_avg = np.ones(len(months)) * np.average(monthly_sleep_avg_list)
quality_months_avg = np.ones(len(months)) * np.average(sleep_quality_avg_list)

caption = """
Yearly Avg: 2014:{avg2014:02.2f}, 2015:{avg2015:02.2f}, 2016:{avg2016:02.2f} Yearly Std: 2014:{std2014:02.2f}, 2015:{std2015:02.2f}, 2016:{std2016:02.2f}
Monthly Avg: Jan:{jan:02.2f}, Feb:{feb:02.2f}, Mar:{mar:02.2f}, Apr:{apr:02.2f}, May:{may:02.2f}, Jun:{jun:02.2f}, Jul:{jul:02.2f}, Aug:{aug:02.2f}, Sep:{sep:02.2f}, Oct:{oct:02.2f}, Nov:{nov:02.2f}, Dec:{dec:02.2f}
Monthly Std: Jan:{jan_std:02.2f}, Feb:{feb_std:02.2f}, Mar:{mar_std:02.2f}, Apr:{apr_std:02.2f}, May:{may_std:02.2f}, Jun:{jun_std:02.2f}, Jul:{jul_std:02.2f}, Aug:{aug_std:02.2f}, Sep:{sep_std:02.2f}, Oct:{oct_std:02.2f}, Nov:{nov_std:02.2f}, Dec:{dec_std:02.2f}
"""

plt.figtext(0.5, 0.005, caption.format(
                                      avg2014=yearly_sleep_avg_list[0],
                                      std2014=yearly_sleep_std_list[0],
                                      avg2015=yearly_sleep_avg_list[1],
                                      std2015=yearly_sleep_std_list[1],
                                      avg2016=yearly_sleep_avg_list[2],
                                      std2016=yearly_sleep_std_list[2],
                                      jan=monthly_sleep_avg_list[0],
                                      feb=monthly_sleep_avg_list[1],
                                      mar=monthly_sleep_avg_list[2],
                                      apr=monthly_sleep_avg_list[3],
                                      may=monthly_sleep_avg_list[4],
                                      jun=monthly_sleep_avg_list[5],
                                      jul=monthly_sleep_avg_list[6],
                                      aug=monthly_sleep_avg_list[7],
                                      sep=monthly_sleep_avg_list[8],
                                      oct=monthly_sleep_avg_list[9],
                                      nov=monthly_sleep_avg_list[10],
                                      dec=monthly_sleep_avg_list[11],
                                      jan_std=monthly_sleep_std_list[0],
                                      feb_std=monthly_sleep_std_list[1],
                                      mar_std=monthly_sleep_std_list[2],
                                      apr_std=monthly_sleep_std_list[3],
                                      may_std=monthly_sleep_std_list[4],
                                      jun_std=monthly_sleep_std_list[5],
                                      jul_std=monthly_sleep_std_list[6],
                                      aug_std=monthly_sleep_std_list[7],
                                      sep_std=monthly_sleep_std_list[8],
                                      oct_std=monthly_sleep_std_list[9],
                                      nov_std=monthly_sleep_std_list[10],
                                      dec_std=monthly_sleep_std_list[11],
                                      ),
            ha='center', size=40, color='.5',
            )

plt.savefig("andrew_sleep")

for year in years:
  for month in months:
      yr_month_idc = np.where((pd.DatetimeIndex(sleep_df.index).month == month) & (pd.DatetimeIndex(sleep_df.index).year == year))[0]
      yr_monthly_sleep_avg_list.append(np.ma.average(sleep_masked[yr_month_idc]))
      yr_monthly_quality_avg_list.append(np.ma.average(quality_masked[yr_month_idc]))

start = datetime.datetime(2013, 12, 31)
dates = pd.date_range(start, periods=len(yr_monthly_sleep_avg_list), freq='m')

x = mdates.date2num(dates[:-2])
xx = np.linspace(x.min(), x.max(), len(dates))

z4 = np.polyfit(x, np.array(yr_monthly_sleep_avg_list[:-2]), 4)
p4 = np.poly1d(z4)

yearly_monthly_sleep_fit = p4(xx)

monthly_qual_norm = sci.get_norm_anom(np.array(yr_monthly_sleep_avg_list[:-2]))
monthly_hour_norm = sci.get_norm_anom(np.array(yr_monthly_quality_avg_list[:-2]))

coeff, pval = pearsonr(monthly_qual_norm, monthly_hour_norm)

plt.figure()
title_fmt = 'Monthly Average Hours of Sleep'
fig, ax = vis.plot(dates, yr_monthly_sleep_avg_list, y2=yearly_monthly_sleep_fit,
        ylabel='Hours', sharex=True, extra=True, xlabel='Month', bar_dates=True, linewidth2=2,
        title=title_fmt.format(coeff), ylabel2='Quality', bar=True, ylim=(7, 9.5), width=15,
        figsize=(20,15), major='months', interval=3, fontscale=1.5, labelscale=1.5, minor='years')
plt.savefig('yr_monthly_andrew_quality_hour.png')

plt.figure()
vis.plot(months, monthly_sleep_avg_list, y2=months_avg,
        ylabel='Hours', sharex=True, extra=True,
        title='Monthly Average Hours of Sleep (2014 - 2016)', xlabel='Month',
        save='monthly_andrew_sleep', figsize=(20,15), xlim=(1, 12))

plt.figure()
vis.plot(months, sleep_quality_avg_list, y2=quality_months_avg,
        ylabel='%', sharex=True, extra=True, xlabel='Month',
        title='Monthly Average Quality of Sleep (2014 - 2016)',
        save='monthly_andrew_quality', figsize=(20,15), xlim=(1, 12))

plt.figure()
hist, bins = np.histogram(sleep_hours, bins=20, range=(6, 11))
width = 0.7 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
vis.plot(center, hist, width=width, ylabel='Count',
         title='Hours of Sleep Histogram (2014 - 2016)', xlabel='Hours',
         save='histogram_andrew_sleep', figsize=(20,15), bar=True,
         xlim=(6, 11))

monthly_qual_norm = sci.get_norm_anom(np.array(monthly_sleep_avg_list))
monthly_hour_norm = sci.get_norm_anom(np.array(sleep_quality_avg_list))
coeff, pval = pearsonr(monthly_qual_norm, monthly_hour_norm)

plt.figure()
title_fmt = 'Monthly Quality of Sleep vs Hours of Sleep Correlation = {:.2f}'
vis.plot(months, monthly_sleep_avg_list, y2=sleep_quality_avg_list,
        ylabel='Hours', sharex=True, extra=True, xlabel='Month', extray=True,
        title=title_fmt.format(coeff), ylabel2='Quality',
        save='monthly_andrew_quality_hour', figsize=(20,15), xlim=(1, 12))


qual_norm = sci.get_norm_anom(quality_masked)
tmp_norm = sci.get_norm_anom(tmp)

qual_norm_cut = qual_norm[~qual_norm.mask]
tmp_norm_cut = tmp_norm[~qual_norm.mask]

coeff, pval = pearsonr(qual_norm_cut, tmp_norm_cut)

fig, ax = vis.plot(sleep_df.index, quality_masked, y2=tmp,
         dates=True, save='qual_vs_tmp', sharex=True,
         figsize=(70, 20), major='months', interval=3, extray=True,
         title="Sleep Quality vs Temperature Correlation: {}".format(coeff), ylabel='Sleep Quality',
         titlescale=4, fontscale=3.5, labelscale=3.5, linewidth2=5,
         minor='years')