import pandas as pd
import numpy as np

df = pd.read_csv('flattened_ecommerce_data.csv')

# find columns with missing values
def missing_data(df):
    missing_data = df.isnull().sum()
    return(missing_data[missing_data > 0])

# calculate percentage of missing values
total_rows = len(df)
missing_data = df.isnull().sum()
percentage_missing = (missing_data / total_rows) * 100

# missing report
def missing_report(missing_data, percentage_missing):
    report_df = pd.DataFrame({
        'Column': missing_data.index,
        'Missing Values': missing_data.values,
        'Percentage Missing': percentage_missing.values
    }).sort_values(by='Percentage Missing', ascending=False)
    
    return report_df

missing_report = missing_report(missing_data, percentage_missing)

# drop columns with more than 50% missing values
df.drop(columns=missing_report[missing_report['Percentage Missing'] > 50]['Column'], inplace=True)

# leftover columns with missing data, user_first_touch_timestamp and device.language
left_missing = df.isnull().sum()
print(left_missing[left_missing > 0])

# replace values with median timestamp or should we drop?
df['user_first_touch_timestamp'].fillna(df['user_first_touch_timestamp'].median(), inplace=True)

# replace missing values with the most common language
df['device.language'].fillna(df['device.language'].mode()[0], inplace=True)

# check no more missing data
missing_data = df.isnull().sum().sum()
print("number of missing data:" + str(missing_data))

# copy of df to check any duplicates
df_copy = df.copy()
# convert unhashable columns to strings in the copy, then check duplicates
df_copy = df_copy.applymap(lambda x: str(x) if isinstance(x, (list, dict, np.ndarray)) else x)
duplicate_rows = df_copy[df_copy.duplicated()]
print("number of duplicates:" + str(len(duplicate_rows)))
# no duplicate rows in df

print(df.columns)


# Check the number of unique values in each column
unique_values = df.nunique()
print(unique_values[unique_values==1])
print(unique_values[unique_values==1].index)

drop_cols = unique_values[unique_values==1].index
df = df.drop(columns=drop_cols)

print(df.columns)
