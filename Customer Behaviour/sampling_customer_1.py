import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde

df = pd.read_csv("customer_dataset_1.csv")
df = df[['Age', 'Gender', 'Payment Method', 'Churn']]


# Yea 100001 will create 100000 samples, don't ask me why
n_samples = 100001

# Step 1: Group by the categorical columns
grouped = df.groupby(['Gender', 'Payment Method', 'Churn'])

# Step 2: Stratify sampling from the categorical variables
# Sample proportionally from each group
categorical_sampled = grouped.apply(lambda x: x.sample(frac=n_samples/len(df), random_state=42)).reset_index(drop=True)

# Step 3: Apply KDE to the continuous 'Age' column within each categorical group
def kde_sample(group):
    # Apply KDE to the 'Age' column for each group
    age_kde = gaussian_kde(group['Age'])
    return age_kde.resample(len(group))[0]  # Resample to match the group size

# Step 4: Loop through the categorical groups and replace the 'Age' column with KDE samples
categorical_sampled['Age'] = categorical_sampled.groupby(['Gender', 'Payment Method', 'Churn'], group_keys=False).apply(kde_sample).values

# Rename the index to 'CustomerID'
categorical_sampled.index.name = 'CustomerID'

# Save the DataFrame to a CSV file with the index
categorical_sampled.to_csv('sampled_customer.csv', index=True)

