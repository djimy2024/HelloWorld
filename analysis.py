# analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Load the dataset
df = pd.read_csv("data.csv")

print("----- SAMPLE DATA -----")
# By default, the first 5 lines of data are displayed so you can quickly glance at the contents of the DataFrame.
print(df.head()) 

#Data Cleaning
#Remove duplicates
df = df.drop_duplicates()

# Renowned column (eg if there is space)
df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]

print("\n----- CLEANED DATA INFO -----")
# displays information about the data type of the DataFrame.
print(df.info()) 

# 3. Exploratory Data Analysis (EDA)
print("\n----- SUMMARY STATISTICS -----")
# static descriptive display for numeric columns.
print(df.describe()) 

# Calculate Statistics on a specific column (Ex: Age, Sales)
if "age" in df.columns: # Check if the column "age" exists in the DataFrame df.
    # calculate the average of the column.
    print("\nMean age:", df["age"].mean()) 
    # find the median of the column.
    print("Median age:", df["age"].median()) 
    #Calculate standard deviation to measure how much data varies or how far it deviates from the mean.
    print("Standard deviation age:", df["age"].std()) 

# 4. Visualizations
sns.set(style="whitegrid")

# Histogram
if "age" in df.columns: # Check if the column "age" exists in the DataFrame df.
    # Create a graphics window 6 inches wide and 4 inches high.
    plt.figure(figsize=(6,4))
    # the number of “bins” or “bars” in the histogram. It divides the data into 20 groups.
    sns.histplot(df["age"], bins=20, kde=True) 
    # Enter a title for the graphic.
    plt.title("Age Distribution") 
    # Save the graphic as a PNG image in the same script file.
    plt.savefig("histogram_age.png") 
    plt.show() # Show the graphic on the screen.

# Scatter plot 
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns #select columns with numeric data types (integer and decimal).
# Select all numeric columns and have at least 2 columns for analyses that require multiple columns.
if len(numeric_cols) >= 2: 
    # Create a graphics window 6 inches wide and 4 inches high.
    plt.figure(figsize=(6,4)) 
    # shows the relationship between two numeric columns.
    sns.scatterplot(x=df[numeric_cols[0]], y=df[numeric_cols[1]])
    # Enter a title for the graphic. 
    plt.title(f"{numeric_cols[0]} vs {numeric_cols[1]}")
    # Save the graphic as a PNG image in the same script file.
    plt.savefig("scatter.png") 
    plt.show() # Show the graphic on the screen.

# Correlation heatmap
numeric_df = df.select_dtypes(include=["int64", "float64"]) # This creates a new DataFrame containing only numeric columns in df.
# check if the DataFrame is empty (no rows).
if not numeric_df.empty: 
    # Create a graphics window 6 inches wide and 4 inches high.
    plt.figure(figsize=(8,6)) 
    sns.heatmap(numeric_df.corr(), annot=True, cmap="Blues")
    # Enter a title for the graphic.
    plt.title("Correlation Heatmap") 
    # Save the graphic as a PNG image in the same script file.
    plt.savefig("heatmap.png") 
    # Show the graphic on the screen.
    plt.show() 
else:
    print("No numeric columns available for correlation heatmap.")

print("\nAnalysis complete! Charts saved as images.")
