# Import the dependencies.
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
engine = create_engine("sqlite:////Users/yamilethcova/Documents/GitHub/Sqlalchemy-Challenge/Starter_Code_9/SurfsUp/Resources/hawaii.sqlite")
#Starter_Code 9/SurfsUp/Resources/hawaii.sqlite

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station 

# Create our session (link) from Python to the DB
#session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all availables API routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)
    date_measurement = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(measurement.prcp, measurement.date).\
        filter(measurement.date >= date_measurement).all()
    
    session.close()

    prpc_data={}
    
    precip = {date: prcp for prcp, date in results if prcp is not None}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stn():    
    session = Session(engine)
    results = session.query(station.station).all()
    session.close()

    stations = list(np.ravel(results))
   
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
    date_measurement = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= date_measurement).all() 
    session.close()
    
    return jsonify(list(np.ravel(results)))

@app.route("/api/v1.0/<start>")
def start_date_temp(start):
    session = Session(engine)
    start = dt.datetime.strptime(start, "%Y-%d-%m")


    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    
    temperatures = list(np.ravel(results))
    session.close()

    return jsonify(temperatures)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date_temp(start,end):
    session = Session(engine)

    start = dt.datetime.strptime(start, "%Y-%d-%m")
    end = dt.datetime.strptime(end, "%Y-%d-%m")

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date >= end).all()
    
    session.close()

    temp_data = []
    for min_temp, avg_temp, max_temp in results:
        temp_data.append({
            'TMIN': min_temp,
            'TAVG': avg_temp,
            'TMAX': max_temp
        })

        return jsonify(temp_data)

if __name__=='__main__':
    app.run(debug=True, port=3000)


