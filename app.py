# Import the dependencies.
import numpy as np
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
Base.prepare(autoload_with=engine)

# Save references to each table
measurement=Base.classes.measurement
station=Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return last 12 months of precipitation analysis"""
    # Precipitation last 12 months
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp_results=session.query(measurement.date,measurement.prcp).filter(measurement.date>=query_date).all()
    session.close()
    # Create a dictionary from the row data and append to a list of all_passengers
    twelve_month_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        twelve_month_precipitation.append(precipitation_dict)
    return jsonify(twelve_month_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all stations
    stations_results = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(
    func.count(measurement.station).desc()).all()
    session.close()
    # Convert list of tuples into normal list
    station_names = list(np.ravel(stations_results))
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return dates and temperatures of most active station"""
    # Query the dates and temperature observations of the most active station
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_results=session.query(measurement.tobs).filter(measurement.station=='USC00519281').filter(measurement.date>=query_date).all()
    session.close()
    # Convert list of tuples into normal list
    tobs_names = list(np.ravel(tobs_results))
    return jsonify(tobs_names)

@app.route("/api/v1.0/start")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range"""

    # Query the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range
    start_date=dt.date(2017, 7, 23)
    start_date_results=session.query(func.tmin(measurement.tobs),func.tmax(measurement.tobs),func.tavg(measurement.tobs)).filter(start_date).all()
    session.close()
    return jsonify(start_date_results)

@app.route("/api/v1.0/start/<end>")
def start_end():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range"""

    # Query the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range
    start_end_date=dt.date(2017, 7, 23)-dt.date(2016, 8, 23)
    start_end_date_results=session.query(func.tmin(measurement.tobs),func.tmax(measurement.tobs),func.tavg(measurement.tobs)).filter(start_end_date).all()
    session.close()
    return jsonify(start_end_date_results)

if __name__ == '__main__':
    app.run(debug=True)
