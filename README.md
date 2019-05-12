# Surfs Up!

## Step 1 - Climate Analysis and Exploration
A jupyter notebook is created to gather climatological data from Honolulu, Hawaii from a SQLite file to perform the following analysis:

Precipitation Analysis
![Precipitation](Images/Precipitation_plot.png)

Station Analysis
![Station](Images/Temperature_histogram.png)

Temperature Analysis
![Temperature1](Images/Average_temperature.png)
![Temperature2](Images/Daily_Normals.png)




Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! To help with your trip planning, you need to do some climate analysis on the area. The following outlines what you need to do.

## Step 1 - Climate Analysis and Exploration

To begin, use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All of the following analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

* Use the provided [starter notebook](climate_starter.ipynb) and [hawaii.sqlite](Resources/hawaii.sqlite) files to complete your climate analysis and data exploration.

* Choose a start date and end date for your trip. Make sure that your vacation range is approximately 3-15 days total.

* Use SQLAlchemy `create_engine` to connect to your sqlite database.

* Use SQLAlchemy `automap_base()` to reflect your tables into classes and save a reference to those classes called `Station` and `Measurement`.

