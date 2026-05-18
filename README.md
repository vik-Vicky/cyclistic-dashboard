# cyclistic-dashboard
Interactive executive dashboard built with Python (Dash/Plotly) to analyze Cyclistic bike-share data. Features geospatial mapping, trend analysis to compare member vs. casual rider behavior.
# Cyclistic Executive Data Dashboard 🚲

An interactive web application built with **Python**, **Dash**, and **Plotly** to analyze and visualize bike-share data for the Cyclistic project. This dashboard provides executive-level insights by comparing the behavior patterns of "Member" vs. "Casual" riders.

## 📊 Project Overview
This project processes over **423,000 cleaned records** to identify key differences in how different user types utilize the bike-share service. The goal is to provide data-driven recommendations for marketing strategies aimed at converting casual riders into annual members.

**⚠️ Technical Note on Data Selection:** > To ensure maximum performance and comply with the 25MB file size limit on the free hosting tier, this dashboard focuses on **2020 data**. This allowed for a higher resolution of trends and more detailed station mapping within the platform's constraints.

## ✨ Key Features
* **Real-time Filtering**: Filter data by Year, User Type, Day of the Week, and specific Station names.
* **Outlier Management**: Automatically filters out trips longer than **120 minutes** to ensure data quality and realistic averages.
* **Interactive Geospatial Map**: 
    * *Network View*: Visualizes the entire station distribution.
    * *Strategic View*: Focuses on the **Top 25** most active stations for resource optimization.
* **Behavioral Heatmaps**: Identifies peak demand hours to assist in bike redistribution efforts.
* **Duration Analysis**: Displays average trip lengths (Cleaned Metrics) categorized by user type and weekday.

## 🛠️ Technical Stack
* **Language**: Python
* **Data Manipulation**: Pandas (Feature Engineering & Cleaning)
* **Dashboard Framework**: Dash (Plotly)
* **Visualizations**: Plotly Express (Histograms, Bar Charts, Density Heatmaps, Scatter Mapbox)

## 🏗️ Data Engineering (Feature Engineering)
Before visualization, the following **time-based features** were extracted from the raw timestamps to enable granular analysis:
* `year`: Extracted from the `started_at` column.
* `day_of_week`: Calculated using the `.dt.day_name()` method.
* `hour`: Extracted to identify peak traffic periods.
* `ride_length`: Calculated as the total duration in minutes (`ended_at` - `started_at`).

## 📸 Dashboard Preview

![Dashboard Screenshot](dashboard_final.png)

## Cyclistic Bike-Share Analysis Dashboard 🚲

**Live Demo:** [View the interactive dashboard here](https://cyclistic-dashboard.onrender.com)

---
*Developed as part of the Google Data Analytics Capstone Project.*
