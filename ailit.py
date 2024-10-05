import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, DateFormatter
import numpy as np

# Read the CSV file and create a DataFrame
df = pd.read_csv('~/table.csv')

# Display the first few rows of the DataFrame to verify
print(df.head())

# Display basic information about the DataFrame
print(df.info())

# Display summary statistics
print(df.describe())

# Display the number of unique values in each column
print(df.nunique())

# Convert 'Date_Action_Filed' to datetime
df['Date_Action_Filed'] = pd.to_datetime(df['Date_Action_Filed'])

# Get unique non-NaN values of 'Name_of_Algorithm_Text' and 'Jurisdiction_Name' and sort in reverse alphabetical order
unique_algorithms = sorted(df['Name_of_Algorithm_Text'].dropna().unique(), reverse=True)
unique_jurisdictions = sorted(df['Jurisdiction_Name'].dropna().unique(), reverse=True)

# Create a mapping of algorithm names to numeric values
algorithm_to_num = {algo: i for i, algo in enumerate(unique_algorithms)}
jurisdiction_to_num = {jur: i for i, jur in enumerate(unique_jurisdictions)}

# First plot: Timeline of Algorithm Actions
plt1, ax1 = plt.subplots(figsize=(12, 8))
for algo in unique_algorithms:
    mask = df['Name_of_Algorithm_Text'] == algo
    ax1.scatter(df.loc[mask, 'Date_Action_Filed'], 
                [algorithm_to_num[algo]] * mask.sum(), 
                label=algo)

ax1.set_yticks(range(len(unique_algorithms)))
ax1.set_yticklabels(unique_algorithms)
ax1.set_xlabel('Date Action Filed')
ax1.set_ylabel('Name of Algorithm')
ax1.set_title('Timeline of Litigation Cases by AI model')
ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
plt1.tight_layout()
plt1.savefig('algorithm_timeline.png', bbox_inches='tight')

# Second plot: Number of Cases Over Time by Jurisdiction
plt2, ax2 = plt.subplots(figsize=(12, 8))

# Create a temporary DataFrame for the second plot
temp_df = df.copy()

# Consolidate New York jurisdictions
ny_jurisdictions = ['New York', 'New York (State)', 'New York (City)']
temp_df['Consolidated_Jurisdiction'] = temp_df['Jurisdiction_Name'].apply(lambda x: 'New York (All)' if x in ny_jurisdictions else x)

# Get unique non-NaN values of 'Consolidated_Jurisdiction' and sort in reverse alphabetical order
unique_consolidated_jurisdictions = sorted(temp_df['Consolidated_Jurisdiction'].dropna().unique(), reverse=True)

# Create a mapping of consolidated jurisdiction names to numeric values
consolidated_jurisdiction_to_num = {jur: i for i, jur in enumerate(unique_consolidated_jurisdictions)}

for jur in unique_consolidated_jurisdictions:
    mask = temp_df['Consolidated_Jurisdiction'] == jur
    ax2.scatter(temp_df.loc[mask, 'Date_Action_Filed'], 
                [consolidated_jurisdiction_to_num[jur]] * mask.sum(), 
                label=jur)

ax2.set_yticks(range(len(unique_consolidated_jurisdictions)))
ax2.set_yticklabels(unique_consolidated_jurisdictions)
ax2.set_xlabel('Date Action Filed')
ax2.set_ylabel('Jurisdiction Name')
ax2.set_title('Number of Cases Over Time by Jurisdiction')
ax2.xaxis.set_major_locator(YearLocator())
ax2.xaxis.set_major_formatter(DateFormatter('%Y'))
plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='xx-small', ncol=1)
plt2.tight_layout()
plt2.savefig('jurisdiction_timeline.png', bbox_inches='tight')

# Show both plots
plt.show()






