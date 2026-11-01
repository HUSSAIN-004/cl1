# 11. AQI Trends using Matplotlib

import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------
# 1. Import Dataset
# -----------------------------------
df = pd.read_csv("data/City_Air_Quality.csv", parse_dates=["Date"])

# -----------------------------------
# 2. Explore Dataset
# -----------------------------------
print(df.head())
print(df.info())
print(df.describe())

# -----------------------------------
# 3. Relevant Variables
# Date, AQI, PM2.5, PM10, CO
# -----------------------------------

# -----------------------------------
# 4. Overall AQI Trend
# -----------------------------------
plt.figure(figsize=(10, 4))

plt.plot(df["Date"], df["AQI"], color="purple")

plt.title("AQI Over Time")
plt.xlabel("Date")
plt.ylabel("AQI")

plt.show()

# -----------------------------------
# 5. Individual Pollutant Trends
# -----------------------------------
fig, ax = plt.subplots(3, 1, figsize=(10, 7), sharex=True)

for a, col in zip(ax, ["PM2.5", "PM10", "CO"]):
    a.plot(df["Date"], df[col])
    a.set_ylabel(col)
    a.set_title(f"{col} Trend")

plt.suptitle("Pollutant Levels Over Time")

plt.tight_layout()

plt.show()

# -----------------------------------
# 6. Bar Plot of Monthly Average AQI
# -----------------------------------
monthly = df.groupby(df["Date"].dt.month)["AQI"].mean()

monthly.plot.bar(
    figsize=(8, 4),
    color="skyblue",
    title="Monthly Average AQI"
)

plt.xlabel("Month")
plt.ylabel("Average AQI")

plt.show()

# -----------------------------------
# 7. AQI Distribution (Box Plot)
# -----------------------------------
plt.figure(figsize=(6, 4))

plt.boxplot(df["AQI"])

plt.title("AQI Distribution")
plt.ylabel("AQI")

plt.show()

# -----------------------------------
# 8. Scatter Plot (AQI vs PM2.5)
# -----------------------------------
plt.figure(figsize=(7, 5))

plt.scatter(
    df["PM2.5"],
    df["AQI"],
    c=df["PM10"],
    cmap="viridis",
    alpha=0.7
)

plt.colorbar(label="PM10")

plt.xlabel("PM2.5")
plt.ylabel("AQI")
plt.title("AQI vs PM2.5")

plt.show()

# -----------------------------------
# 9. Correlation (Relationship)
# -----------------------------------
print("\nCorrelation Matrix:")
print(df[["AQI", "PM2.5", "PM10", "CO"]].corr())