import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#Precipitation query

last_12_months = dt.date(2017, 8, 23) - dt.timedelta(days=365)
most_active_station = 'USC00519281'


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
#List all routes that are available.
    return (
        f"Climate Analysis and Exploration APP!<br>"
        f"<br/>"
        f"You can navigate through the following links to get information about the Hawaii climate "
        f"from 2010-01-01 to 2017-08-23: <br>"
        f"<br/>"
        f"Precipitation data: <br>"
        f"<a href= '/api/v1.0/precipitation'>Precipitation</a>"
        f"<br/>"
        f"<br/>"
        f"Stations data: <br>"
        f"<a href= '/api/v1.0/stations'>Stations</a>"
        f"<br/>"
        f"<br/>"
        f"Temperature data: <br>"
        f"<a href= '/api/v1.0/tobs'>Temperature</a>"
        f"<br/>"
        f"<br/>"
        f"To get information about the temperature data from a specific date, add the following to the path: "
        f"/api/v1.0/'start_date/end_date'<br>"
        f"Where date should have the following format: year-month-day. <br> " 
        f"Example: "
        f"<a href= '/api/v1.0/2016-08-24' >current_link/api/v1.0/2016-08-24</a>"
        f"<br/>"
        f"<br/>"
        f"To get information about the temperature data from a specific range of dates, add the following to the path: "
        f"/api/v1.0/'start_date/end_date'<br>"
        f"Where date should have the following format: year-month-day. <br> " 
        f"Example: "
        f"<a href= '/api/v1.0/2016-08-24/2017-08-23' >current_link/api/v1.0/2016-08-24/2017-08-23</a>"
        )


@app.route("/api/v1.0/precipitation")
def precipitation():
#Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
    measurement_ordered_by_date = session.query(Measurement).order_by(Measurement.date.desc())
    precipitation_scores = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > last_12_months).all()

    # Convert list of tuples into normal list
    prcp_results = []
    
    for precipitation in precipitation_scores:
        prcp_dict = {}
        prcp_dict["date"] = precipitation[0]
        prcp_dict["precipitation_score"] = precipitation[1]
        prcp_results.append(prcp_dict)

    return jsonify(prcp_results)

@app.route("/api/v1.0/stations")
def stations():

#Return a JSON list of stations from the dataset.
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).all()

    stations_list = []
    
    for station in active_stations:
        station_dict = {}
        station_dict["Station"] = station[0]
        station_dict["n_observations"] = station[1]
        stations_list.append(station_dict)

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
#query for the dates and temperature observations from a year from the last data point.
#Return a JSON list of Temperature Observations (tobs) for the previous year.
    temperature_query = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.station == most_active_station).\
                filter(Measurement.date >= last_12_months).all()
    
    temperature_list = []
    
    for temperature in temperature_query:
        temp_dict = {}
        temp_dict["Date"] = temperature[0]
        temp_dict["Temperature (F)"] = temperature[1]
        temperature_list.append(temp_dict)

    return jsonify(temperature_list)


@app.route("/api/v1.0/<start>")
def start_date(start):
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    start_date= start

    range_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date == start_date).all()

    results = list(np.ravel(range_query))
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def range_date(start,end):
    start_date = start
    end_date = end
    range_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    results = list(np.ravel(range_query))
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)