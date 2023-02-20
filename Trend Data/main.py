import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

# Introduction
# Google Trends gives us an estimate of search volume. Let's explore if search popularity relates
# to other kinds of data. Perhaps there are patterns in Google's search volume and the price of
# Bitcoin or a hot stock like Tesla. Perhaps search volume for the term "Unemployment Benefits"
# can tell us something about the actual unemployment rate?
#
# Data Sources:
#
# Unemployment Rate from FRED
# Google Trends
# Yahoo Finance for Tesla Stock Price
# Yahoo Finance for Bitcoin Stock Price
# Import Statements
# [1]
# Read the Data
# Download and add the .csv files to the same folder as your notebook.
#
# [2]
df_tesla = pd.read_csv('data/TESLA Search Trend vs Price.csv')
df_tesla.name = "tesla"
#
df_btc_search = pd.read_csv('data/Bitcoin Search Trend.csv')
df_btc_search.name = "btc_search"
df_btc_price = pd.read_csv('data/Daily Bitcoin Price.csv')
df_btc_price.name = "btc_price"
#
df_unemployment = pd.read_csv('data/UE Benefits Search vs UE Rate 2004-19.csv')
df_unemployment.name = "unemployment"
# Data Exploration
# Tesla
# Challenge:
#
# What are the shapes of the dataframes?
dataframes = [df_tesla, df_unemployment, df_btc_search, df_btc_price]

for frame in dataframes:
    print(f"the shape of {frame} is {frame.shape}")

# How many rows and columns?
for frame in dataframes:
    print(f" {frame.name} has {frame.shape[0]} rows")
    print(f" {frame.name} has {frame.shape[1]} columns")

# What are the column names?

for frame in dataframes:
    print(f"the columns of {frame.name} are {frame.columns}")

# Complete the f-string to show the largest/smallest number in the search data column
# Try the .describe() function to see some useful descriptive statistics
# What is the periodicity of the time series data (daily, weekly, monthly)?
# What does a value of 100 in the Google Trend search popularity actually mean?
# [1]
print(f'Largest value for Tesla in Web Search: {df_tesla.TSLA_USD_CLOSE.max()}')
print(f'Smallest value for Tesla in Web Search: {df_tesla.TSLA_USD_CLOSE.min()}')
df_tesla.describe()
# Largest value for Tesla in Web Search:
# Smallest value for Tesla in Web Search:
#
# Unemployment Data
# [2]
print('Largest value for "Unemployemnt Benefits" '
      f'in Web Search: {df_unemployment.UE_BENEFITS_WEB_SEARCH.max()}')
df_unemployment.describe()
# Largest value for "Unemployemnt Benefits" in Web Search:
#
# Bitcoin
# [6]
print(f'largest BTC News Search: {df_btc_search.BTC_NEWS_SEARCH.max()}')
df_btc_search.describe()
# largest BTC News Search:
#
# Data Cleaning
# Check for Missing Values
# Challenge: Are there any missing values in any of the dataframes? If so, which row/rows have
# missing values? How many missing values are there?
#
for frame in dataframes:
    print(f"does {frame.name} have any missing values? {frame.isna().values.any()}")
    if frame.isna().values.any() == True:
        frame.dropna(0, inplace=True)
        print(f"{frame.name} has had its NaN values replaced with 0s")

# [7]
# print(f'Missing values for Tesla?: ')
# print(f'Missing values for U/E?: ')
# print(f'Missing values for BTC Search?: ')
# Missing values for Tesla?:
# Missing values for U/E?:
# Missing values for BTC Search?:
#
# [8]
# print(f'Missing values for BTC price?: ')
# Missing values for BTC price?:
#
# [5]
# print(f'Number of missing values: ')
# Number of missing values:
#
# Challenge: Remove any missing values that you found.
#
# Convert Strings to DateTime Objects
# Challenge: Check the data type of the entries in the DataFrame MONTH or DATE columns. Convert
# any strings in to Datetime objects. Do this for all 4 DataFrames. Double check if your type
# conversion was successful.
#

for frame in dataframes:
    if "MONTH" in frame:
        frame.MONTH = pd.to_datetime(frame.MONTH)
    if "DATE" in frame:
        frame.DATE = pd.to_datetime(frame.DATE)

# Converting from Daily to Monthly Data
# Pandas .resample() documentation

df_btc_price = df_btc_price.resample('M', on='DATE').last()
# Data Visualisation

# Tesla Stock Price v.s. Search Volume
# Challenge: Plot the Tesla stock price against the Tesla search volume using a line chart and
# two different axes. Label one axis 'TSLA Stock Price' and the other 'Search Trend'.
#
plt.title('Tesla Web Search vs Price', fontsize=18)
price_axis = plt.gca()
search_axis = price_axis.twinx()

price_axis.set_ylabel("TESLA Price", color='#E6232E', fontsize=14)
search_axis.set_ylabel("Search Volume", color='skyblue', fontsize=14)

# Set the minimum and maximum values on the axes
price_axis.set_ylim([0, 600])
search_axis.set_xlim([df_tesla.MONTH.min(), df_tesla.MONTH.max()])

price_axis.plot(df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE, linewidth=3, color='#E6232E')
search_axis.plot(df_tesla.MONTH, df_tesla.TSLA_WEB_SEARCH, linewidth=3)

years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')

price_axis.xaxis.set_major_locator(years)
price_axis.xaxis.set_major_formatter(years_fmt)
search_axis.xaxis.set_minor_locator(months)

plt.show()

# Challenge: Add colours to style the chart. This will help differentiate the two lines and the
# axis labels. Try using one of the blue colour names for the search volume and a HEX code for a
# red colour for the stock price.
#
# Hint: you can colour both the axis labels and the lines on the chart using keyword arguments (
# kwargs).
#
# Challenge: Make the chart larger and easier to read.
#
# Increase the figure size (e.g., to 14 by 8).
# Increase the font sizes for the labels and the ticks on the x-axis to 14.
# Rotate the text on the x-axis by 45 degrees.
# Make the lines on the chart thicker.
# Add a title that reads 'Tesla Web Search vs Price'
# Keep the chart looking sharp by changing the dots-per-inch or DPI value.
# Set minimum and maximum values for the y and x axis. Hint: check out methods like set_xlim().
# Finally use plt.show() to display the chart below the cell instead of relying on the automatic
# notebook output.
# How to add tick formatting for dates on the x-axis.
#
# Bitcoin (BTC) Price v.s. Search Volume
# Challenge: Create the same chart for the Bitcoin Prices vs. Search volumes.
#
# Modify the chart title to read 'Bitcoin News Search vs Resampled Price'
# Change the y-axis label to 'BTC Price'
# Change the y- and x-axis limits to improve the appearance
# Investigate the linestyles to make the BTC price a dashed line
# Investigate the marker types to make the search datapoints little circles
# Were big increases in searches for Bitcoin accompanied by big increases in the price?
# Unemployement Benefits Search vs. Actual Unemployment in the U.S.
# Challenge Plot the search for "unemployment benefits" against the unemployment rate.
#
# Change the title to: Monthly Search of "Unemployment Benefits" in the U.S. vs the U/E Rate
# Change the y-axis label to: FRED U/E Rate
# Change the axis limits
# Add a grey grid to the chart to better see the years and the U/E rate values. Use dashes for
# the line style
# Can you discern any seasonality in the searches? Is there a pattern?
# Challenge: Calculate the 3-month or 6-month rolling average for the web searches. Plot the
# 6-month rolling average search data against the actual unemployment. What do you see in the
# chart? Which line moves first?
#
# Including 2020 in Unemployment Charts
# Challenge: Read the data in the 'UE Benefits Search vs UE Rate 2004-20.csv' into a DataFrame.
# Convert the MONTH column to Pandas Datetime objects and then plot the chart. What do you see?
