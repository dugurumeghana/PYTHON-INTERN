import pandas as pd
import pandas as pd
# Load the dataset using absolute path
absolute_path = r'C:\Users\megha\Desktop\PROJECT\student-dataset.csv'
df = pd.read_csv(absolute_path)
# Display the first few rows of the dataset
print("First few rows:")
print(df.head())
# Display basic information about the dataset
print("\nInfo:")
print(df.info())
# Summary statistics
print("\nSummary Statistics:")
print(df.describe())
# Filter data based on a condition
# Filter data based on a condition
filtered_data = df[df['age'] > 100] 
# Assuming 'age' is the column name you want to filter on
# Sort data
sorted_data = df.sort_values(by='nationality')
# Group data by a categorical variable
grouped_data = df.groupby('english.grade')['math.grade'].mean()
# Calculate mean, median, and standard deviation
mean_value = df['age'].mean()
median_value = df['age'].median()
std_dev = df['age'].std()
print("Mean:", mean_value)
print("Median:", median_value)
print("Standard Deviation:", std_dev)
import matplotlib.pyplot as plt
import seaborn as sns
# Plot histogram
plt.figure(figsize=(8, 6))
sns.histplot(data=df, x='age', kde=True)
plt.title('Distribution of Numeric Column')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()
# Plot scatter plot
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='numeric_column_1', y='numeric_column_2')
plt.title('Relationship between Numeric Column 1 and Numeric Column 2')
plt.xlabel('Numeric Column 1')
plt.ylabel('Numeric Column 2')
plt.show()
