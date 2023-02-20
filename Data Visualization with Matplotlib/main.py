import pandas as pd
import matplotlib.pyplot as plt

# Get the Data
# Either use the provided .csv file or (optionally) get fresh (the freshest?) data from running
# an SQL query on StackExchange:
#
# Follow this link to run the query from StackExchange to get your own .csv file
#
# select dateadd(month, datediff(month, 0, q.CreationDate), 0) m, TagName, count(*) from PostTags
# pt join Posts q on q.Id=pt.PostId join Tags t on t.Id=pt.TagId where TagName in ('java','c',
# 'c++','python','c#','javascript','assembly','php','perl','ruby','visual basic','swift','r',
# 'object-c','scratch','go','swift','delphi') and q.CreationDate < dateadd(month, datediff(month,
# 0, getdate()), 0) group by dateadd(month, datediff(month, 0, q.CreationDate), 0), TagName order
# by dateadd(month, datediff(month, 0, q.CreationDate), 0)
# Import Statements
# Data Exploration
# Challenge: Read the .csv file and store it in a Pandas dataframe
#

df = pd.read_csv("data/QueryResults.csv")

# Challenge: Examine the first 5 rows and the last 5 rows of the of the dataframe
#

first_five = {print(f"first five: {df.head()}")}

last_five = {print(f"last five: {df.tail()}")}

first_five
last_five


# Challenge: Check how many rows and how many columns there are. What are the dimensions of the
# dataframe?
#

shape = df.shape

print(f"rows: {shape[0]}, columns: {shape[1]}")

# Challenge: Count the number of entries in each column of the dataframe
#

number_of_non_nans = df.count()

print(number_of_non_nans)

# Challenge: Calculate the total number of post per language. Which Programming language has had
# the highest total number of posts of all time?
#
# Some languages are older (e.g., C) and other languages are newer (e.g., Swift). The dataset
# starts in September 2008.
#

total_searches_descending = df.groupby("TagName").sum().sort_values("Number of Searches", ascending=False)
print(total_searches_descending)

# Challenge: How many months of data exist per language? Which language had the fewest months
# with an entry?
#
list_of_languages = df["TagName"].unique().tolist()
for lang in list_of_languages:
    number_months = sum(df.TagName == lang)
    print(f"{lang} had {number_months} months searched")

smallest_searched = df.groupby("TagName").sum().sort_values("Number of Searches", ascending=True)


# Data Cleaning
# Let's fix the date format to make it more readable. We need to use Pandas to change format from
# a string of "2008-07-01 00:00:00" to a datetime object with the format of "2008-07-01"
#

for i, row in df.iterrows():
    df.at[i, "m"] = str(df.m.loc[i]).split(" ")[0]

print(df)

# Data Manipulation
# Challenge: What are the dimensions of our new dataframe? How many rows and columns does it
# have? Print out the column names and print out the first 5 rows of the dataframe.
#

# pivot the dataframe

reshaped_df = df.pivot(index="m", columns="TagName", values="Number of Searches")
print(reshaped_df)
print(reshaped_df.shape)

# remove NaNs
reshaped_df.fillna(0, inplace=True)
print(reshaped_df)

#
# Data Visualisaton with with Matplotlib
# Challenge: Use the matplotlib documentation to plot a single programming language (e.g.,
# java) on a chart.
#

# index_for_lang =  df.index.

# plt.plot(reshaped_df['python'])
# plt.xlabel("Time")
# plt.ylabel("Number of Searches")
# plt.title("Python Searches Over Time")
# plt.show()

# Challenge: Show two line (e.g. for Java and Python) on the same chart.
#
for lang in reshaped_df.columns:
    plt.plot(reshaped_df.index, reshaped_df[lang])
plt.xlabel("Time")
plt.ylabel("Number of Searches")
plt.title("Python Searches Over Time")
# plt.show()

# Smoothing out Time Series Data
# Time series data can be quite noisy, with a lot of up and down spikes. To better see a trend we
# can plot an average of, say 6 or 12 observations. This is called the rolling mean. We calculate
# the average in a window of time and move it forward by one overservation. Pandas has two handy
# methods already built in to work this out: rolling() and mean().

# for lang in roll_df.columns:
#     plt.plot(roll_df.index, roll_df[lang])
# plt.xlabel("Time")
# plt.ylabel("Number of Searches")
# plt.title("Python Searches Over Time")
# plt.show()

roll_df = reshaped_df.rolling(window=6).mean()

plt.figure(figsize=(16, 10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts', fontsize=14)
plt.ylim(0, 35000)

# plot the roll_df instead
for column in roll_df.columns:
    plt.plot(roll_df.index, roll_df[column],
             linewidth=3, label=roll_df[column].name)

plt.legend(fontsize=16)

plt.show()