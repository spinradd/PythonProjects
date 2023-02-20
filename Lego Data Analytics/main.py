import pandas as pd
import matplotlib.pyplot as plt

# Introduction
# Today we'll dive deep into a dataset all about LEGO. From the dataset we can ask whole bunch of
# interesting questions about the history of the LEGO company, their product offering, and which
# LEGO set ultimately rules them all:
#
# What is the most enormous LEGO set ever created and how many parts did it have?
# How did the LEGO company start out? In which year were the first LEGO sets released and how
# many sets did the company sell when it first launched?
# Which LEGO theme has the most sets? Is it one of LEGO's own themes like Ninjago or a theme they
# licensed liked Harry Potter or Marvel Superheroes?
# When did the LEGO company really expand its product offering? Can we spot a change in the
# company strategy based on how many themes and sets did it released year-on-year?
# Did LEGO sets grow in size and complexity over time? Do older LEGO sets tend to have more or
# fewer parts than newer sets?
# Data Source
#
# Rebrickable has compiled data on all the LEGO pieces in existence. I recommend you use download
# the .csv files provided in this lesson.
#
# Import Statements
# Data Exploration
# Challenge: How many different colours does the LEGO company produce? Read the colors.csv file
# in the data folder and find the total number of unique colours. Try using the .nunique() method
# to accomplish this.
#
df_colors = pd.read_csv("data/colors.csv")

num_of_colors = df_colors.name.nunique()
print(num_of_colors)
# Challenge: Find the number of transparent colours where is_trans == 't' versus the number of
# opaque colours where is_trans == 'f'. See if you can accomplish this in two different ways.
#

num_of_colors_filtered_true = df_colors[df_colors.is_trans == "t"]
num_of_colors_filtered_false = df_colors[df_colors.is_trans == "f"]

print(f"number of true colors: {num_of_colors_filtered_true.shape[0]}")
print(f"number of false colors: {num_of_colors_filtered_false.shape[0]}")

# The sets.csv data contains a list of sets over the years and the number of parts that each of
# these sets contained.
#
# Challenge: Read the sets.csv data and take a look at the first and last couple of rows.
#

df_sets = pd.read_csv("data/sets.csv")

sets_head = df_sets.head()
sets_tail = df_sets.tail()

print(sets_head)
print(sets_tail)

# Challenge: In which year were the first LEGO sets released and what were these sets called?
#

first_lego_year = df_sets.year.min()
first_lego_year_sets = df_sets[df_sets.year == first_lego_year]

print(first_lego_year_sets)


# Challenge: How many different sets did LEGO sell in their first year? How many types of LEGO
# products were on offer in the year the company started?
#

num_of_original_sets = first_lego_year_sets.shape[0]
print(num_of_original_sets)

# Challenge: Find the top 5 LEGO sets with the most number of parts.
#

df_sets_filtered = df_sets.sort_values("num_parts", ascending=False).head()
print(f"the top five largest sets by piece count \n {df_sets_filtered}")

# Challenge: Use .groupby() and .count() to show the number of LEGO sets released year-on-year.
# How do the number of sets released in 1955 compare to the number of sets released in 2019?
#

df_sets_by_year = df_sets.groupby("year", as_index=False).count()
print(df_sets_by_year)

df_sets_1955 = df_sets_by_year[df_sets_by_year.year == 1955].set_num.item()
df_sets_2019 = df_sets_by_year[df_sets_by_year.year == 2019].set_num.item()

print(f"The number of sets in 1955 was {df_sets_1955}, the number of sets in 2019 was {df_sets_2019}")

# Challenge: Show the number of LEGO releases on a line chart using Matplotlib.
#
df_sets_filtered = df_sets_by_year.sort_values("year", ascending=True)

# plt.plot(df_sets_filtered.year, df_sets_filtered.set_num)
# plt.show()

# Note that the .csv file is from late 2020, so to plot the full calendar years, you will have to
# exclude some data from your chart. Can you use the slicing techniques covered in Day 21 to
# avoid plotting the last two years? The same syntax will work on Pandas DataFrames.
#
# plt.plot(df_sets_filtered.year[:-2], df_sets_filtered.set_num[:-2])
# plt.show()

# Aggregate Data with the Python .agg() Function
# Let's work out the number of different themes shipped by year. This means we have to count the
# number of unique theme_ids per calendar year.
#

df_themes_by_year = df_sets.groupby("year", as_index=False).agg({"theme_id" : pd.Series.nunique})
print(df_themes_by_year.head())


# Challenge: Plot the number of themes released by year on a line chart. Only include the full
# calendar years (i.e., exclude 2020 and 2021).
#

# plt.plot(df_themes_by_year.year[:-2], df_themes_by_year.theme_id[:-2])
# plt.show()


# Line Charts with Two Seperate Axes
# Challenge: Use the .groupby() and .agg() function together to figure out the average number of
# parts per set. How many parts did the average LEGO set released in 1954 compared to say, 2017?
#
df_parts_by_year = df_sets.groupby("year", as_index=False).agg({"num_parts" : pd.Series.nunique})
print(df_parts_by_year.head())

parts_per_set_1955 = df_sets_by_year[df_sets_by_year.year == 1954].set_num.item()
parts_per_set_2019 = df_sets_by_year[df_sets_by_year.year == 2017].set_num.item()

print(f"The number of parts/set in 1954 was {parts_per_set_1955}, the number of parts/set in 2017 was {parts_per_set_2019}")

# Scatter Plots in Matplotlib
# Challenge: Has the size and complexity of LEGO sets increased over time based on the number of
# parts? Plot the average number of parts over time using a Matplotlib scatter plot. See if you
# can use the scatter plot documentation before I show you the solution. Do you spot a trend in
# the chart?
#

# themes_axis = plt.gca()
# parts_set_axis = plt.twinx()
#
# themes_axis.plot(df_themes_by_year.year[:-2], df_themes_by_year.theme_id[:-2])
# parts_set_axis.plot(df_parts_by_year.year[:-2], df_parts_by_year.num_parts[:-2])
#
# themes_axis.set_xlabel("Year")
# themes_axis.set_ylabel("Number of Themes")
# parts_set_axis.set_ylabel('Number of Parts')
#
# plt.show()

parts_per_set = df_sets.groupby("year", as_index=False).agg({"num_parts" : pd.Series.mean})
print(parts_per_set.head())

# plt.scatter(parts_per_set.year[:-2], parts_per_set.num_parts[:-2])
# plt.show()

# Number of Sets per LEGO Theme
# LEGO has licensed many hit franchises from Harry Potter to Marvel Super Heros to many others.
# But which theme has the largest number of individual sets?
#

# Database Schemas, Foreign Keys and Merging DataFrames
# The themes.csv file has the actual theme names. The sets .csv has theme_ids which link to the
# id column in the themes.csv.
#
# Challenge: Explore the themes.csv. How is it structured? Search for the name 'Star Wars'. How
# many ids correspond to this name in the themes.csv? Now use these ids and find the
# corresponding the sets in the sets.csv (Hint: you'll need to look for matches in the theme_id
# column)
#
df_themes = pd.read_csv("data/themes.csv", index_col=False)

star_wars_themes = df_themes[df_themes.name == "Star Wars"].shape[1]
print(f"the number of themes associated with star wars is {star_wars_themes}")
# Merging (i.e., Combining) DataFrames based on a Key

set_theme_count = df_sets["theme_id"].value_counts()
set_theme_count[:5]

set_theme_count = pd.DataFrame({'id': set_theme_count.index, 'set_count':set_theme_count.values})
print(set_theme_count.head())

merged_df = pd.merge(set_theme_count, df_themes, on="id")
print(merged_df[:3])

plt.figure(figsize=(14, 8))
plt.xticks(fontsize=14, rotation=45)
plt.yticks(fontsize=14)
plt.ylabel('Nr of Sets', fontsize=14)
plt.xlabel('Theme Name', fontsize=14)

plt.bar(merged_df.name[:10], merged_df.set_count[:10])
plt.show()

