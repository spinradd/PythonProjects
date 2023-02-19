import pandas as pd

df = pd.read_csv("data/salaries_by_college_major.csv")

# print(df.head()) # first five rows of table
#
# print(df.shape) # how many rows of our table
#
# print(df.columns) # print field names
#
# print(df.isna()) # tells if if any NaNs present
#
# print(df.tail()) # last 5 rows of table
#
df_nanless = df.dropna()  # create a new table without NaN values
#
# # to find stats of the highest starting salary
# highest_sal = df_nanless["Starting Median Salary"].max()
#
# # which row earns max
# row_of_max = df_nanless["Starting Median Salary"].idxmax()
#
# # which college major earns max
# print(df_nanless["Undergraduate Major"].loc[row_of_max])

# What college major has the highest mid-career salary?
# How much do graduates with this major earn? (Mid-career is defined as having 10+ years of
# experience).

highest_mid_career_sal_row = df_nanless["Mid-Career Median Salary"].idxmax()
highest_mid_career_sal_major = df_nanless["Undergraduate Major"].loc[
    highest_mid_career_sal_row]
print(f"highest mid career salary major: {highest_mid_career_sal_major} at ${df_nanless['Mid-Career Median Salary'].max()}")

# Which college major has the lowest starting salary and
# how much do graduates earn after university?

lowest_mid_career_sal_row = df_nanless["Starting Median Salary"].idxmin()
lowest_mid_career_sal_major = df_nanless["Undergraduate Major"].loc[
    lowest_mid_career_sal_row]
print(f"lowest starting salary major: {lowest_mid_career_sal_major} at ${df_nanless['Starting Median Salary'].min()}")

# Which college major has the lowest mid-career salary and
# how much can people expect to earn with this degree?


lowest_mid_career_sal_row = df_nanless["Mid-Career Median Salary"].idxmin()
lowest_mid_career_sal_major = df_nanless["Undergraduate Major"].loc[
    lowest_mid_career_sal_row]
print(f"lowest mid career salary major: {lowest_mid_career_sal_major} at ${df_nanless['Mid-Career Median Salary'].min()}")


# find top 5 majors with the highest potential

highest_potential = df_nanless.sort_values("Mid-Career 90th Percentile Salary", ascending=False)
print(highest_potential[["Undergraduate Major", "Mid-Career 90th Percentile Salary"]].head())

variation_col = df_nanless["Mid-Career 90th Percentile Salary"] - df_nanless["Mid-Career 10th Percentile Salary"]
df_nanless.insert(1, "Variation", variation_col)

low_variation = df_nanless.sort_values("Variation", ascending=False)
print(low_variation[["Undergraduate Major", "Variation"]].head())

# which category of majors has the highest average salary?
print(df_nanless.groupby("Group").mean())


