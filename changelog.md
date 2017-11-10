
## CHANGELOG:
### - v1.0.3
    - Add data files to wheel?
### - v1.0.2
    - Missing data folder in pip so this version fixes?
### - v1.0.1
    - Now available on pip!
### - v1.0.0
    - Accidentally bloated the repo in past version so deleted the old one and started anew
    - Begin semantic versioning
    - Cleaned up duplicate/unnecessary files
### -v0.6.2
    - Updated readme with something more enticing
    - Updated requirements for newer versions
    - Moved changelog from README.md to changelog.md
    - Added tests
    - Removed era.cdf2dt()
    - Added dt input to exp.arr_1d()
    - Added exception handling to functions in ext
    - Added lower input in pre.read_csv()
    - Added sci.get_norm() and renamed sci.regress to sci.get_regression()
    - Many under-the-hood cleanup and bug fixes in vis
    - Removed mpl.use('agg') in vis
    - Changed defaults in vis
    - Added suptitle in vis
    - Improved xarray compatibility in vis.plot_map()
    - Added vis.plot() to plot multiple lines in a shortcut method
    - Separated histogram functionality in plot_bar() to plot_hist()
    - Added vis.plot_cbar() to plot just a color bar
    - Renamed vis.set_color_bar() to vis.set_cbar()
    - Added vis.get_region_latlim()
    - Improved set_inherited algorithm
    - Set tight_layout as default in savefig()
    - Cleaned up sketches folder
### -v0.6.1
    - Update readme
    - New ext.get_ocean_mask() to mask out ocean/land
    - New sci.regress() to fit a regression line
    - NCL_CMAPS now supported for Python 2.7
    - vis.plot_map() now has central_longitude and mask_ocean/mask_land input
    - vis.plot_line() can now detect maximum ylim from previous lines
### -v0.6.0
    - Updated pre.wget_fi() and example
    - Added pre.gen_fi_list() and pre.wget_list() and examples
    - Fixed bug with era.clockit()
    - Allowed fourth argument with ext.parallelize()
    - Bug fixes with vis.plot_bar() histograms and example
### -v0.5.9
    - Changed input order of ext.round_to()
    - Changed default cmap for vis.plot_cmap()
    - Set tight_layout input to be 'auto' for vis.functions()
    - Use percentile to determine vmin and vmax in vis.plot_map()
    - Added couple exception handlings in vis.functions()
    - Better handling of color bar ticks, format, and contours in vis.plot_map()
### -v0.5.8
    - New era.td2dict() that breakdowns datetime.timedelta into more intuitive time units
    - Refactored era.clockit()
    - Added ticks input to vis.prettify_ax()
    - Revamped vis.set_date_ticks()
    - Modified vis.set_minor_ticks default color and fixed xlocator 'years' input
    - Modified defaults for vis.set_major_grid() linestyle
    - Modified vis.set_minor_grid() defaults
### -v0.5.7
    - Added ext.strip_2ws() which reduces two spaces to one space
    - Ported over NCL colormaps for use with vis.get_cmap() and updated example
    - New vis.prettify_bokeh() to be used on bokeh plots and example
    - Better handling of xarrays for vis.plot_map()
    - Added vis.set_inline_label() to add inline labels and built in vis.plot_line()
    - vis.set_figsize() now returns fig
    - Added vis.get_color_list() to get either a list of RGB tuples or hexcodes from cmap
    - Updated requirements.txt and setup.py
### -v0.5.6
    - Fixed elapsed seconds in era.clockit()
    - Bug fixes to contour/contour2/stipple in vis.plot_map() and examples made
    - Bug fix to vis.plot_heatmap() getting the max/min
    - vis.get_cmap() now more intelligent in choosing n
### -v0.5.5
    - Made 2010 as default year for era.jul2dt() and new method of reading the calendar
    - era.clockit() prints more straightforward time elapsed and new functionality to save, show, and return_dt
    - era.mth2terc() merged into era.dt2seas() with additional inputs to limit to four season or have rolling seasons
    - New era.shift_months() which allows shifting datetimes by input number of months
    - Bug fix in vis.set_date_ticks() to prevent freezes
    - era.dt2jul/jul2dt/dt2seas/dtnow_and_clockit/shift_months/time2dt() examples created
### -v0.5.4
    - ext.ahh() now handles xarrays proficiently and prints out average/median
    - Added ext.ahhh() which can pass as many unnamed variables as preferred, but no modifyable settings
    - Added ext.ahh_xr_check() used as a helper in ext.ahh/ahhh()
    - ext.glob() now prints out the original glob_str if it errors out
    - Format of color bars in vis.functions() are now intelligently chosen if not provided
    - Better handling of the tick_locs/interval of color bars
    - Intelligently choose the orientation of bar values
    - vis.set_figsize() now can easily accept width/height
    - vis.set_ax() is added to create plot axes easily
    - Fixed bug with vis.get_cmap()
### -v0.5.3
    - Hotfixed bugs from previous version (undefined kwargs) and added some error handling
    - Improved vis/set_axtext_AND_set_figtext examples
    - Added vis/get_cmap example
    - New functionality in vis.get_cmap()
    - Modified vis.set_latlons() and vis.set_major/minor_grid() defaults and scaling
### -v0.5.2
    - Made a part of pre.read_csv() into era.spawn_date_times()
    - Fixed exp.arr_1d() xy return
    - Revised ext.mkdir() to utilize built in os.makedirs()
    - Added km2mi input to sci.convert()
    - Added capability and example for mapping data to size or color in vis.plot_scatter()
    - Added length_scale inputs to enable/disable scaling of labels based on length in vis.functions()
    - Added **kwargs input to vis.functions() where applicable for more flexibility
    - Added more handling with vis.set_date_ticks()
    - Added fha/fva inputs to vis.set_figtext() and vis.set_axtext()
    - Added inheritance to vis.functions()
    - Added vis.get_cmap() used to discretize registered color maps and also create color maps from list of colors
    - Added various color lists to vis used in vis.get_cmap()
### - v0.5.1
    - Added ext.append_to_fn() and example
    - Added xy input to exp.arr_1d()
    - Modified exp.arr_df() to return more ready df
    - Added weekdays_initial/short/long constant strings to ext.MISC
    - Added filename to ext.report_err() output
    - Modified pre.mkdir() to utilize os.makedirs instead of calling to system
    - Modified pre.read_csv() to take in any arguments from pd.read_csv and dropna to not default to True
    - Added region and shrink inputs to various vis functions
    - Added latlim/lonlim input to vis.init_map() and vis.plot_bounds()
    - Improved vis.plot_line() to take in x-axis text labels
    - Modified functionality of input bar_vals to take in the format of the labels
    - New logic to handle when vis.set_bar_vals() is called in vis.plot_bar()
    - New functionality in vis.plot_heatmap() and improved color bar interval handling and deprecated cbar_count input
    - vis.set_latlons() default grid color and alpha modified
### - v0.5.0
    - Added vis.plot_heatmap() and example
    - Fixed some bugs in vis.set_bar_vals() and vis.get_side_bars_recs()
    - Remove to do list in readme
### - v0.4.9
    - ext.glob() now can raise errors if there's mismatch in expected and found number of files and also better reporting
    - Created ext.report_err() for informative error reports on exceptions and easy logging
    - Modified pre.merge() to not use a pandas resample module
    - Improved vis.plot_map() countries/states/coastlines and bug fixes
    - Set default dpi to be 115
    - Tweaked vis.set_bar_vals() height
    - Adjusted vis.set_latlons() defaults
    - Added vis.plot_map() and ext.report_err() examples
### - v0.4.8
    - vis.plot_map() input fmt and contourf changed
    - vis.plot_functions() tight_layout defaults
    - Improved vis.plot_map() data limit detection
    - New vis.set_figsize() defaults and handling
    - Added manual vis.plot_map() contourf limits
    - Added rivers input to vis.plot_map() and vis.init_map()
    - Added functionality to allow text labels to bar plots
    - Changed vis.set_date_ticks() format defaults
    - Added aspect ratio and changed defaults to vis.set_color_bar()
    - Added ability to turn off certain lat/lon labels in vis.set_latlons() and changed color defaults
    - Added examples for vis ... plot_functions()
### - v0.4.7
    - Added examples for ext... flatten(), split_consec(), formalize_str(), p(), parallelize(), round_to(), and get_order_mag()
    - Set era.time2dt() strf input default to 'infer'
    - Added opportunity to add constant args to ext.parallelize()
    - Added pre.make_xr() to create basic xarrays quickly
    - Changed figsize defaults for vis.set_figsize()
    - Fixed bug for ext.flatten()
### - v0.4.6
    - Improved handling of era.cdf2dt()
    - Added era.mth2terc() converting months to seasonal terciles
    - Added some more datasets for exp.arr_ds()
    - Fixed exp.arr_df()
    - Added months_initial into ext.MISC
    - Added ext.ahh() ignore input and created examples for it
    - Added ext.glob() safeguards for expected length check and empty lists
    - Added additional handling of file existing for pre.export_nc() by appending _1
    - Added strip input to pre.read_csv()
    - Added pre.merge() which merges two dataframes
    - Added pre.save() to save a .pkl and .csv given a df
    - Added sci.get_anom() which just takes the data and subtracts the climatology
    - Added sci.get_terc_avg() which takes monthly values and does a rolling mean
    - Added input ax for vis.plot_functions()
    - Revised vis.set_figsize() defaults
    - Added additional vis.set_figtext() rha/rva to reverse horizontal/vertical alignment
    - Revised vis.set_axtext() to handle datetimes better and also input optional xy location
    - Added xarray reference notebook
### - v0.4.5
    - Added reverse input to era.dt2num()
    - Added no_zeros input to exp.arr_1d()
    - Added vis.COLOR_LIST containing a list of default colors to use in order
    - Changed bar plots opacity to be semi opaque
    - Added sidebar_count and sidebar_pos inputs to vis.plot_bar()
    - Improved logic for width and limits for x datetimes
    - Added vis.get_side_bars_recs() to get recommended values for side by side bars
    - Added inherit_color input to set_bar_vals
    - Improved set_date_ticks to set xintervals more logically if the time resolution is too coarse
### - v0.4.4
    - Added additional functionality to exp.arr_1d() including negative values and seeding random
    - Added exp.arr_ds() and exp.arr_df() for quick access to saved datasets and dataframes
    - Removed some unnecessary printing
    - Added fp input to pre.join_cwd() to use originating file path
    - Set vis.plot_bar() width to default to 0.833 and fixed the xmax if edge
    - Added vis.set_bar_vals() to show values of bar plot
### - v0.4.3
    - Removed "contains"; see documentation instead
    - Added new module named exp (experimenting) to help testing
    - Added exp.arr_1d() and exp.arr_dt() to create arrays easily
    - Added ext.MISC containing miscallenous lists of constants
    - Added ext.parallelize() to multiprocess
    - Modified pre.wget_fi() to simplify getting file and quiet mode
    - Created pre.mkdir() to create directory if it doesn't exist
    - Added MinuteLocator in vis.set_major/minor_ticks()
    - Revamped and renamed vis.prettify_plot() to vis.prettify_ax()
    - Improved vis.set_legend() logic to automatically set
    - Revamped vis.set_date_ticks() to be more practical
### - v0.4.2
    - Improved era.str2spec()
    - Added sci.get_corr() to get the Pearsonr correlation
    - Optimized sci.get_c()
    - Added option to remove drawedges on color bar
    - Added input to vis.plot_functions() to allow changes to xinterval and whether to show minor date ticks
    - Modified when and which data stipples are drawn from vis.plot_map()
    - Added histogram functionality to plot_line()
    - Modified how legend takes inputs
    - Added normalization to histograms
    - Changed vis.set_figsize() defaults
    - Added handling for days less than one day for set_date_ticks()
    - Added drawedges input for set_color_bar()
    - Added ext.glob() which gets all the filenames and sorts them for a given wildcard filename
### - v0.4.1
    - pre.read_csv() now takes additional arguments and can merge date and time columns to return datetime index
    - Major revamp to size, length, and width scaling and default sizes
    - New dpi input to vis.functions(); new default is 175 dpi
    - Slowly deprecating the vis.DEFAULT dict
    - Color bar tick marks will now never extend past the color bars due to newly discovered input
    - New grid styles for vis.plot_functions()
    - Revamped vis.set_figtext() and vis.set_axtext() with additional available locations
    - Added smart function to figure out the location keywords
    - Bug fix with year locator and fixes to some docstrings
    - Added tight_layout input to vis.utils()
    - Added sci.get_c() using Pythagorean Theorem
    - Changed how sci.get_stats() returned str looks
    - vis.plot_functions() now can accept only one input
    - vis.plot_functions() prettily plot date ticks now
### - v0.4.0
    - Added vis.set_inherited() to inherit inputs when overlaying two plots
    - Removed useless input from vis.set_major_tick_labels()
    - Made legend size larger
    - Bugfix with vis.plot_bar() with text hist input
    - Updated examples
### - v0.3.9
    - Added new functionality to era.time2dt() to combine year/month/day/hour/min/sec into one arr
    - Removed pre.ncdump() since pre.peek_nc() was essentially the same and improved on it
    - Added new pre.read_csv() where it reads a time series csv and tries to create a datetme index
    - Dropped cartopy imports under specific vis.functions() so that vis package is more accessible
    - Completely dropped vis.plot() with vis.plot_line/bar/scatter() replacing it.
    - Renamed inputs in vis.plot_map()
    - Added default close into vis.functions() to close axes after saving
    - Shifted vis.annotate_point() xytext offset to (0, 0) and horizontal alignment to left
    - Modified figsize logic to have a base figsize
    - Adjusted default size for text in vis.set_colorbar()/vis.set_latlons()/vis.set_major_tick_labels
    - Added more inputs into vis.utils()
    - Updated and implemented new examples
### - v0.3.8
    - Fixed bugs with twinx in vis.plot_line/bar/scatter()
    - Added a sketch with data derived from Fitbit
    - Added new era.dt2num() used to convert datetimes into matplotlib workable values
### - v0.3.7
    - Added sci.sind/cosd/tand/asind/acosd/atand() that evaluates/returns degrees
    - Added potential fix to known issues
### - v0.3.6
    - Fixed incorrect docstrings
    - Added era.str2spec() which converts string into specific time values
    - Upgraded ext.ahh() to handle long 1D arrays and pandas dataframes
    - Changed ext.ahh()'s center input is no longer default True and condensed min/max
    - Fixed bug in pre.join_cwd()
    - Fixed various bugs in vis.functions()
    - Added more sketches
### - v0.3.5
    - Added input "up" into pre.join_cwd()
    - Added input "returnplot" and "fmt" to vis.plot_map()
    - Added vis.set_figsize()
    - Modified aesthetics of vis.functions() in general
    - Added vis jupyter notebook examples
    - Cleaned up sketches
    - Fixed bug with xinvert/yinvert for vis.plot_line/bar/scatter()
### - v0.3.4
    - Added one example and fixed bugs for vis.plot_bar()
    - Added pre.join_cwd()
    - Made vis.savefig() close plots after saving
    - Made vis.set_date_ticks() set tick labels' sizes to smallest
### - v0.3.3
    - Renamed vis.saveit() to vis.savefig()
    - Added era.dt2spec() and era.cdf2dt()
    - Fixed bugs and documentation page
### - v0.3.2
    - Moved known issues up to the top.
    - Added netCDF4 to requirement.
    - Modified some sizes in vis.DEFAULT dictionary
    - Increased zorder of land and ocean features in vis.plot_map()
    - Added functionality of vis.init_map()
    - Changed input names for vis.plot_bounds()
    - Changed how saving works and some visuals in vis.plot_line/bar/scatter()
    - Removed arrowprops in annotate_point
    - Added pandas_fun reference script in sketches (usage of .loc/.iloc/.ix and replacement)
### - v0.3.1
    - Added some Python 3.5 compatibility
    - Fixed docstrings for some functions
    - Refactored and added new functionality to vis.plot_map()
    - Added new vis.set_colorbar(), vis.set_latlons(), vis.set_axtext()
    - Added new ext.round_to_nearest_mag()
### - v0.3.0
    - Complete vis package refactor with many new functions for customizability
    - Added ext.formalize_str(), ext.round_to(), and ext.get_order_mag()
    - Added new return for sci.get_stats()
    - Added new function sci.get_counts()
    - Added new examples under a Jupyter notebook.
### - v0.2.1
    - Sphinx is awesome - now documentation has link to source code!
    - Added mission statements
    - Added flexibility with era.time2dt to prevent errors
    - Added new function, ext.flatten()
### - v0.2.0
    - Fixed docstrings!
    - Sphinx documentation now implemented!
    - Fixed bug with era.jul2dt()
### - v0.1.9
    - Added vis.plot_hist() that plots a histogram with the capabilities of showing stats
    - Added linewidth to vis.plot_bounds()
    - Added back matplotlib.use('agg') so show=True won't work
    - Expanded on examples/sketches
    - Added sci.get_stats() that returns basic stats
    - Fixed some docstrings (many more to go...)
### - v0.1.8
    - Added new function: vis.plot_bounds() that creates filled/outlined boxes on maps
    - Expanded plot_map_example.py with vis.plot_bounds() example usage
    - Added simple_data_analysis.py in sketches
    - Added new experiments folder where I develop functions
### - v0.1.7
    - Moved pre.time2dt() to era.time2dt()
    - Added era.dt2seas() aka datetime to seasons
    - Made num2date default True in pre.read_nc()
    - Made xarray a requirement
### - v0.1.6
    - Added new package era.py
    - Updated ext.ahh() to handle multiple variables and more options
    - The name of pre.py is now "prepatory" instead of "pre-analysis"
    - Transferred multiple functions to other packages for optimization purposes
    - ext.dt2jul() moved to era.dt2jul()
    - ext.jul2dt() moved to era.jul2dt()
    - ext.clockit() moved to era.clockit()
    - ext.peek_nc() moved to pre.peek_nc()
    - ext.time2dt() moved to pre.time2dt()
    - ext.export_nc() moved to pre.export_nc()
    - ext.read_nc() moved to pre.read_nc() and now has option to glob multiple files
    - vis.plot_map() now has contourf option or flat colors
    - Moved back cartopy imports to the top
### - v0.1.5
    - Discontinued docstrings.py; will try another method of documentation soon
    - Fixed inconsistency with lat and lon names in ext.export_nc()
    - Added pre.grb2nc()
    - Revised input directory to be in_dir/out_dir and now returns file names for pre.functions()
    - Adjusted vis.plot() default inputs and fixed some inconsistencies
    - Renamed setup_figsize to figsize in vis.plot_map() and added a suptitle input
    - Created a sketches/my_sleep as an unrefined reference
### - v0.1.4
    - Logic implemented into ext.get_idc() where right_lon < left_lon to swap them
    - ext.get_lvl_idc is now ext.get_lvls_idc and ext.get_times_idc is now ext.get_times_idc
    - ext.create_dt_arr is now ext.time2dt and returns type pd.DatetimeIndex()
    - Off-by-one bug fixed for sci.functions()
    - vis.plot() is now scalable and includes bar graphs
    - vis.plot() also can format dates
    - vis.plot_map() default cmap is RdBu_r now.
### - v0.1.3
    - new ext.peek_nc(), similar to pre.ncdump()
    - Added check if .nc is missing from suffix, automatically add it in ext.read_nc()
    - Added significantly more flexibility in ext.export_nc()
    - Added scalability to vis.plot(), vis.prettify_plot(), and vis.set_labels()
    - Added function level examples
### - v0.1.2
    - Spelling and grammar corrections
    - Link to examples changed and images dumped into folder
    - Fixed ext.ahh() to prevent showing misleading types and handle masked better
    - Fixed ext.lonw2e() to handle scalars
    - Put the imports of cartopy in plot_map() since installation can be crappy
### - v0.1.1
    - Spelling and grammar corrections
    - Link to examples changed and images dumped into folder
    - Fixed ext.ahh() to prevent showing misleading types and handle masked better
    - Fixed ext.lonw2e() to handle scalars
    - Put the imports of cartopy in plot_map() since installation can be crappy
### - v0.1.0
    - Enhanced ext.ahh() to handle 0 length variables
    - Lessened the inputs in ext.lonw2e()
    - Added ext.get_lvl_idc(), ext.get_time_idc(), ext.get_closest()
    - Fixed bug in ext.export_nc()
    - Added ext.clockit() to time your code easily!
    - Added sci.get_avg() to handle all your averaging needs
    - Replaced vis.global_map() with vis.plot_map() that uses Cartopy
    - Modified in_depth_example.py and added map_example.py
### - v0.0.9
    - Exception handling for ext.ahh()
    - Added input to only read extras for ahh.read_nc()
### - v0.0.8
    - Updated ext.ahh() to work with multidimensional arrays
    - Added new ext.export_nc function!
    - Convert between Julian day to datetime effortlessly!
    - Quickly get datetime now with ext.dtnow()!
### - v0.0.7
    - Overhauled ext.ahh() to produce more info
    - Renamed ext.ahh(name='old') to ext.ahh(n='new')
    - Can add pretty labels and legends separately
    - If ext.get_idc() is empty, print warning message
    - Added datetime to Julian day conversion function
### - v0.0.6
    - Debug your code easier with ext.p()!
    - Bug fix with xlim not working properly in vis.plot()
    - Cleaned up example.py
### - v0.0.5
    - In-depth example usage is now available!
    - Completely revamped ext.ahh()
    - Fixed sci.convert()
    - Latitude and longitude optional in ext.read_nc
    - New pre.ncdump() which dumps netCDF4 metadata
    - pre.concat_nc() now supports other directories
    - Removed sci.get_atavg and ext.locate_valid_start
    - Renamed lon360 to lonw2e
    - Added ability to convert longitudes from east to west
    - Aesthetic improvements and more error messages
### - v0.0.4
    - Added ext.lon360() which converts west longitudes to east
    - Added "maxmin" and "w2e" inputs to ext.get_idc()
    - Added "directory" input to pre.wget_fi()
    - Added "interval" input to vis.plot()
    - Fixed bug where xlabel and ylabel wasn't set for single plot
### - v0.0.3
    - Added easily accessible docstrings.py for easier referencing
    - Linked the docstrings.py in README.md
    - Reorganized README.md for better logical progression
    - Added requirements to setup.py
### - v0.0.2
    - Added new package: pre.py
    - New functions pre.py: wget_fi() and concat_nc()
    - Renamed ext.eval() to ext.ahh()
    - Function ext.ahh() no longer has unnest=True as default
    - Added "bare" input to ext.ahh
    - Enhanced ext.read_nc() to include more options
    - Enhanced vis.plot() to include exception handling notices
    - Removed "name" input in vis.plot() and changed "save" input
    - New function in vis.py: global_map
    - New function in sci.py: get_norm_anom
    - Aesthetic changes all over
    - Complies with Flake8 and Codacy
### - v0.0.1
    - Creation of ahh with vis, sci, and ext packages.