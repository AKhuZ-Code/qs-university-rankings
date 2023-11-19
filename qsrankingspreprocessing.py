# Import packages
import pandas as pd
import numpy as np
import math

# Read the csv file that came from the scraper python file
csv_file_path = 'qsrankingsdata.csv'
df = pd.read_csv(csv_file_path)

### Clean the data entries

# Extract the rank from the global rank column - to make it numeric
global_rank_pattern = r'^=?(\d+)-?\d*'
df['global_rank_num'] = df['global rank'].str.extract(global_rank_pattern)

# Replace NaN's to 0's for overall score
df['overall_score_mod'] = df['overall score'].fillna(0)

# Create a proxy score that is used for sorting the Universities
df['proxy score'] = pd.to_numeric(df['global_rank_num']) + pd.to_numeric(df['overall_score_mod'])/100

# Check results of the cleaning
#print(df.iloc[0])

### Compute the relative rank (in Australia)

# Split the dataframe by year - to create a proxy score grouped by Uni *and* year
df2021 = df[df['year'] == 2021]
df2022 = df[df['year'] == 2022]
df2023 = df[df['year'] == 2023]
df2024 = df[df['year'] == 2024]

# Compute proxy score for each year
df2021globalrank = df2021['proxy score']
df2022globalrank = df2022['proxy score']
df2023globalrank = df2023['proxy score']
df2024globalrank = df2024['proxy score']

# Initialise the Australian ranking with a '1' - this matches to the highest ranking Uni
df2021relrank = [1]

# Use a for loop to populate this list. This will match every Uni with their Australian rank. 
increment = 1
for i in range(1, len(df2021globalrank)):
    if df2021globalrank[i] > df2021globalrank[i - 1]:
        # If yes, add 1 to the previous value and append to the result list
        df2021relrank.append(df2021relrank[-1] + increment)
        increment = 1
    else:
        df2021relrank.append(df2021relrank[-1])
        increment = increment + 1

# Reset the index of the first item to zero, since this list comes from a later part of the dataframe col
df2022globalrank.reset_index(drop=True, inplace=True)

# Repeat the for-loop process used for Australian ranks - but now for 2022 data
df2022relrank = [1]
increment = 1
for i in range(1, len(df2022globalrank)):
    if df2022globalrank[i] > df2022globalrank[i - 1]:
        # If yes, add 1 to the previous value and append to the result list
        df2022relrank.append(df2022relrank[-1] + increment)
        increment = 1
    else:
        df2022relrank.append(df2022relrank[-1])
        increment = increment + 1

# Reset the index of the first item to zero, since this list comes from a later part of the dataframe col
df2023globalrank.reset_index(drop=True, inplace=True)

# Repeat the for-loop process used for Australian ranks - but now for 2023 data
df2023relrank = [1]
increment = 1
for i in range(1, len(df2023globalrank)):
    if df2023globalrank[i] > df2023globalrank[i - 1]:
        # If yes, add 1 to the previous value and append to the result list
        df2023relrank.append(df2023relrank[-1] + increment)
        increment = 1
    else:
        df2023relrank.append(df2023relrank[-1])
        increment = increment + 1

# Reset the index of the first item to zero, since this list comes from a later part of the dataframe col
df2024globalrank.reset_index(drop=True, inplace=True)

# Repeat the for-loop process used for Australian ranks - but now for 2024 data
df2024relrank = [1]
increment = 1
for i in range(1, len(df2024globalrank)):
    if df2024globalrank[i] > df2024globalrank[i - 1]:
        # If yes, add 1 to the previous value and append to the result list
        df2024relrank.append(df2024relrank[-1] + increment)
        increment = 1
    else:
        df2024relrank.append(df2024relrank[-1])
        increment = increment + 1

# Add relative rankings together, to add back to the dataframe
dfrelrank = df2021relrank + df2022relrank + df2023relrank + df2024relrank
df['relative rank by year'] = dfrelrank

# Filter out the columns we do not need
df = df[
    ['global rank',
    'uni name',
    'overall score',
    'international students ratio',
    'international faculty ratio',
    'faculty student ratio', 
    'citations_per_faculty',
    'academic reputation',
    'employer reputation',
    'international research network',
    'employment outcomes',
    'sustainability',
    'relative rank by year',
    'year']
]

# Save the file
csv_file_path = 'qsrankingsdataclean.csv'
df.to_csv(csv_file_path, index=False)

# Print completion message
print(f'DataFrame has been successfully processed and saved to {csv_file_path}')
