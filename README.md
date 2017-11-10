# ahh - Andrew Huang Helps? v1.0.3

### Functions that I can easily reference, and maybe you too!

## HOW TO GET IT:
New-school method:
1. `pip install ahh`

2. Ensure your packages version (`pip list`) match with ones listed in requirements.txt

Old-school method:
1. Type `git clone https://github.com/ahuang11/ahh.git`

2. Go into ahh folder (where setup.py is)

3. Type `pip install -e .` (may need to be in bash first!)

4. In a Python script, type `from ahh import pre, era, vis, sci, ext`

## MOTIVATION TO GET STARTED:

#### Perhaps you've wrote these lines one too many times just to create a map that looks like this.
```python
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

fig = plt.figure(figsize=(12, 8))
projection = ccrs.PlateCarree()
ax = plt.axes(projection=projection)
im = ax.contourf(da.lon, da.lat, da[0].values, transform=projection, cmap='RdBu_r')
_ = plt.colorbar(im, orientation='horizontal', shrink=0.5, pad=0.05)
_ = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
_ = ax.coastlines()
plt.grid()
```
![Before Map](/readme_images/map_before.png)

#### With this package, it's simplified down to just this (and a prettier map)!
```python
from ahh import vis

ax = vis.plot_map(da[0], da.lat, da.lon)
```
![After Map](/readme_images/map_after.png)

#### Or perhaps you don't deal too much with maps, but you do a lot with timeseries plots.
```python
import matplotlib.pyplot as plt

plt.plot(x, y, label='Blue', linestyle='--')
plt.legend() # equivalent to below
```
![Before Map](/readme_images/timeseries_before.png)

#### Compare that with this package's version!
```python
from ahh import vis

vis.plot_line(x, y, label='Red', linestyle='--')
```
![After Map](/readme_images/timeseries_after.png)

#### Best of all, the functions are super flexible (and have a lot of cool features built into them!)
```python
from ahh import vis

vis_dict = dict(rows=2, # specify number of subplots
                sidebar_count=2, # specify number of side by side bars
                xlabel='x', title='Vis Demonstration', suptitle=True,
                title_pad=0.9, figsize='na') # set shared settings

vis.set_figsize(15, 8) # set figure size
vis.plot_bar(x, y, label='Red Bars', ylabel='Values', **vis_dict)
vis.plot_bar(x, y2, label='Blue Bars', sidebar_pos=2, color='blue', **vis_dict)

vis.plot_hist(['Chicken'] * 5 + ['Egg'] * 2 + ['Spam'], # random data
              rows=2, pos=2, ptype='bar',
              ylabel='Count', color='orange', # labels and color
              cumsum=True, save='vis_demonstration') # get cumulative count and save
```
![After Map](/readme_images/vis_demonstration.png)

#### But data exploration doesn't begin with visualizations! Check out ext.ahh() too!
```python
from ahh import ext

ext.ahh(ds=arr_ds, arr=x) # name=data
```

```
            Name: ds
          Length: 366
      Dimensions: (366, 73, 144)
   Unnested Type: <class 'numpy.float64'>
Overarching Type: <class 'numpy.ndarray'>
Minimum, Maximum: 188.290, 315.300
 Average, Median: 277.191, 282.670

Snippet of values:
[ 238.1  238.1  238.1  238.1  238.1 ...,  238.1  238.1  238.1  238.1  238.1]


            Name: arr
          Length: 15
      Dimensions: (15,)
   Unnested Type: <class 'numpy.int64'>
Overarching Type: <class 'numpy.ndarray'>
Minimum, Maximum: 1.000, 15.000
 Average, Median: 8.000, 8.000

Snippet of values:
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15]
```

#### Interested in seeing more? There's way more in the [examples](https://github.com/ahuang11/ahh/tree/master/examples) page!

## AVAILABLE MODULES:
pre | sci | ext | era | vis | exp
--- | --- | --- | --- | --- | ---
pre-analysis | scientific | extraneous | era of time | visualization | experimenting

### Documentation here: https://ahuang11.github.io/ahh/
### Random, but awesome, tips: https://github.com/ahuang11/ahhsumtips

## KNOWN ISSUES AND HACKS:
- Installation of cartopy/basemap can be a bit tedious; easy way to install cartopy and basemap if you have Anaconda: 'conda install -c conda-forge cartopy' and 'conda install -c anaconda basemap'
- Updates to packages listed in requirements may break this package; recommend creating a Python 3 environment and install the specific package versions listed in requirements.txt
- In version 0.6.2, I accidentally bloated the repo so I decided to reset the repo and start semantic versioning beginning at v1.0.0; you may want to `rm -rf ahh` and `git clone https://github.com/ahuang11/ahh.git` again (or newly available, `pip install ahh`)!