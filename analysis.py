# analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Chaje dataset la
df = pd.read_csv("data.csv")

print("----- SAMPLE DATA -----")
print(df.head())

# 2. Data Cleaning
# Retire duplicates
df = df.drop_duplicates()

# Ranplase missing values (si genyen)
df = df.fillna(method='ffill')  # ranplase ak dènye valè ki disponib

# Renome kolòn (egzanp si gen espas)
df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]

print("\n----- CLEANED DATA INFO -----")
print(df.info())

# 3. Exploratory Data Analysis (EDA)
print("\n----- SUMMARY STATISTICS -----")
print(df.describe())

# Kalkile estatistik sou yon kolòn espesifik (ex: age, price, sales)
if "age" in df.columns:
    print("\nMean age:", df["age"].mean())
    print("Median age:", df["age"].median())
    print("Standard deviation age:", df["age"].std())

# 4. Visualizations
sns.set(style="whitegrid")

# Histogram
if "age" in df.columns:
    plt.figure(figsize=(6,4))
    sns.histplot(df["age"], bins=20, kde=True)
    plt.title("Age Distribution")
    plt.savefig("histogram_age.png")
    plt.show()

# Scatter plot (si gen de kolòn nimerik)
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
if len(numeric_cols) >= 2:
    plt.figure(figsize=(6,4))
    sns.scatterplot(x=df[numeric_cols[0]], y=df[numeric_cols[1]])
    plt.title(f"{numeric_cols[0]} vs {numeric_cols[1]}")
    plt.savefig("scatter.png")
    plt.show()

# Correlation heatmap
numeric_df = df.select_dtypes(include=["int64", "float64"])
if not numeric_df.empty:
    plt.figure(figsize=(8,6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="Blues")
    plt.title("Correlation Heatmap")
    plt.savefig("heatmap.png")
    plt.show()
else:
    print("No numeric columns available for correlation heatmap.")

print("\nAnalysis complete! Charts saved as images.")
