import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Folder path containing the CSV files
folder_path = "Datasets"

# Get a list of all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

# print all the datasets
print(csv_files)
# Initialize an empty DataFrame to store the merged data
merged_data = pd.DataFrame()

# Iterate through the CSV files
for file in csv_files:
    # Read each CSV file
    file_path = os.path.join(folder_path, file)
    data = pd.read_csv(file_path)
    print(data)

    # Append the data to the merged_data DataFrame
    merged_data = merged_data.append(data, ignore_index=True)

# Filter the dataset based on the "PointOfConnection" column, find OTA2201 and BEN2201 Points
filtered_data = merged_data[merged_data["PointOfConnection"].isin(["OTA2201", "BEN2201"])]

# Convert trading date and trading period to datetime when trading period ends
filtered_data["TradingEnd"] = pd.to_datetime(filtered_data["TradingDate"]) + pd.to_timedelta((filtered_data["TradingPeriod"])*30, unit="minutes")

# Print the updated dataset
print(filtered_data)

# Save the filtered data to a new CSV file
filtered_data.to_csv("dataset_OTA2201_BEN2201.csv", index=False)

# Create plots to show the fortnight's price trends
# Create plots to show the fortnight's price trends
# Fig1: Convert TradingPeriod to categorical for correct sorting
filtered_data["TradingTime"] = pd.to_datetime(filtered_data["TradingEnd"]).dt.strftime("%H:%M")
print("tradingtime")
print(filtered_data['TradingTime'])

filtered_data['TradingPeriod'] = pd.Categorical(filtered_data['TradingPeriod'], ordered=True)

# Create a facet grid of line plots for each day
g = sns.FacetGrid(filtered_data, col='TradingDate', hue='PointOfConnection', col_wrap=7)
g.map(sns.lineplot, 'TradingPeriod', 'DollarsPerMegawattHour')

# Set labels and title
g.set_axis_labels('Trading Period', 'Price (Dollars Per Megawatt Hour)')
g.fig.suptitle('Price Trend for 14 Days')

# Add a legend
g.add_legend(loc='upper right')
handles = g._legend.legendHandles
handles[0].set_color('#F7781F')
handles[1].set_color('#1E07F3')

# Adjust the spacing between subplots
g.tight_layout()

# Adjust the spacing between subplots
plt.subplots_adjust(bottom=0.2)
plt.subplots_adjust(top=0.8)

plt.savefig(r'Figures//14_days_price_trend.png')
# Show the plot
plt.show()


# Capture the trend over 48 trading periods
# Line plots for each PointOfConnection
# Sort TradingTime in ascending order
filtered_data = filtered_data.sort_values("TradingTime")
fig2 = plt.figure(figsize=(10, 6))
sns.lineplot(data=filtered_data, x="TradingTime", y="DollarsPerMegawattHour", hue="PointOfConnection",palette={"OTA2201": "#F7781F", "BEN2201": "#1E07F3"})
plt.xlabel("Trading Time")
plt.ylabel("Price (Dollars Per Megawatt Hour)")
plt.title("Price Trend for OTA2201 and BEN2201")
plt.xticks(rotation=90)
plt.grid(True)
plt.legend()
plt.savefig(r'Figures//lineplot_tradingperiod.png')
plt.show()

# Box plots for each PointOfConnection
# Sort TradingTime in ascending order
filtered_data = filtered_data.sort_values("TradingTime")
plt.figure(figsize=(10, 6))
sns.boxplot(data=filtered_data, x="TradingTime", y="DollarsPerMegawattHour", hue="PointOfConnection",palette={"OTA2201": "#F7781F", "BEN2201": "#1E07F3"})
plt.xlabel("Trading Time")
plt.ylabel("Price (Dollars Per Megawatt Hour)")
plt.title("Price Trend for OTA2201 and BEN2201")
plt.xticks(rotation=90)
plt.grid(True)
plt.legend()
plt.savefig(r'Figures//boxplot_tradingperiod.png')
plt.show()

# Filter the dataset for the specified trading periods
# Convert TradingEnd to datetime and format as time
filtered_data["TradingTime"] = pd.to_datetime(filtered_data["TradingEnd"]).dt.strftime("%H:%M")
filtered_data["TradingTime"] = filtered_data["TradingTime"].astype(str)

# Sort TradingTime in ascending order
time_values = ['07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00','17:30', '18:00', '18:30']

filtered_data = filtered_data[filtered_data["TradingTime"].isin(time_values)]
filtered_data = filtered_data.sort_values("TradingTime")

# Display the details
print("Details:")
print(filtered_data["TradingTime"].dtype)

# Create the box plot
plt.figure(figsize=(10, 6))
sns.boxplot(data=filtered_data, x="TradingTime", y="DollarsPerMegawattHour", hue="PointOfConnection",palette={"OTA2201": "#FD7F10", "BEN2201": "#0000FF"})
plt.xlabel("Trading Time")
plt.ylabel("Price (Dollars Per Megawatt Hour)")
plt.title("Price Trend for Morning and Afternoon Peak Time")
plt.xticks(rotation=90)
plt.grid(True)
plt.savefig(r'Figures//boxplot_tradingtime_details.png')
plt.show()

# Calculate statistics for each trading period and point of connection
# convert trading period to the time of the day
filtered_data["TradingTime"] = pd.to_datetime(filtered_data["TradingEnd"]).dt.strftime("%H:%M")
print(filtered_data["TradingTime"])

statistics = filtered_data.groupby(["TradingTime","TradingPeriod","PointOfConnection"])["DollarsPerMegawattHour"].describe()

# Display the statistics
print("Statistics by Trading Period and PointOfConnection:")
print(statistics)

statistics.to_csv("statisticsfordetailedTradingPeriods.csv", index=True)

# Filter the dataset for "BEN2201" PointOfConnection
ben_data = filtered_data[filtered_data["PointOfConnection"] == "BEN2201"]

# Calculate statistics for BEN2201
ben_statistics = ben_data.groupby(["TradingTime"])["DollarsPerMegawattHour"].describe().round(2)

# Display statistics for BEN2201
print("Statistics for PointOfConnection BEN2201:")
print(ben_statistics)
ben_statistics.to_csv(r'ben_statistics.csv')

# Filter the dataset for "OTA2201" PointOfConnection
ota_data = filtered_data[filtered_data["PointOfConnection"] == "OTA2201"]

# Calculate statistics for OTA2201
ota_statistics = ota_data.groupby(["TradingTime"])["DollarsPerMegawattHour"].describe().round(2)
ota_statistics.to_csv(r'ota_statistics.csv')

# Display statistics for OTA2201
print("Statistics for PointOfConnection OTA2201:")
print(ota_statistics)
