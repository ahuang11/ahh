import pandas as pd
from ahh import era

df = pd.read_csv('kcmi_wx.csv')
df.index = era.time2dt(df['CST'], strf='infer')

# subselect rows based on index and a condition and all columns
sub_df = df.loc[(df.index < '2014/1/2'), :]
print(sub_df)
print('\n' * 10)

# subselect rows based on index and a condition and a column by name
sub_df = df.loc[(df.index < '2014/1/2'), 'CST']
print(sub_df)
print('\n' * 10)

# subselect rows based on index and two conditions and a column by name
sub_df = df.loc[(df.index > '2014/1/2') & (df.index < '2014/3/5'), 'CST']
print(sub_df)
print('\n' * 10)

# subselect rows based on index and two columns by names
sub_df = df.loc[(df.index < '2014/1/2'), ['CST', 'Mean TemperatureF']]
print(sub_df)
print('\n' * 10)

# subselect rows based on position and a column by name
sub_df = df.iloc[0:5]['CST']
print(sub_df)
print('\n' * 10)

# subselect rows and columns based on position
sub_df = df.iloc[0:5, 0:2]
print(sub_df)
print('\n' * 10)

# subselect rows on position and columns by name
sub_df = df.ix[0:5, ['CST', 'Max TemperatureF', 'Mean TemperatureF']]
print(sub_df)
print('\n' * 10)

# subselect rows on index and columns by name
sub_df = df.ix[(df.index < '2014/1/3'), ['CST', 'Max TemperatureF', 'Mean TemperatureF']]
print(sub_df)
print('\n' * 10)

# subselect rows on index and columns by position
sub_df = df.ix[(df.index < '2014/1/3'), 0:7]
print(sub_df)
print('\n' * 10)

# subselect rows based on index and a condition and one column
sub_df = df.loc[(df['Max TemperatureF'] > 80), 'Max TemperatureF']
print(sub_df)
print('\n' * 10)

# subselect rows based on index and a condition and one column
sub_df = df.loc[(df['Max TemperatureF'] > 90), 'Max TemperatureF']
print(sub_df)
print('\n' * 10)

# subselect rows based on index and a condition and one column
sub_df = df.loc[(df['Max TemperatureF'] > 90) & (df['Min TemperatureF'] > 70), ['Max TemperatureF', 'Min TemperatureF']]
print(sub_df)
print('\n' * 10)

# replacing values based on condition
import copy
sub_df = copy.copy(df)
print(sub_df)
sub_df.ix[(df['Max TemperatureF'] > 90) & (df['Min TemperatureF'] > 70), 'Events'] = 'HOT STUFF'
print(sub_df.loc[sub_df.index > '2014/06/17', 'Events'])
print('\n' * 10)
print('\n' * 10)