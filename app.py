import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# import climate_starter
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station=Base.classes.station
session = Session(engine)


start_date=input("what is the start date?")
end_date = input("what is the end date?")
app = Flask(__name__)
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation </a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations </a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<a href='/api/v1.0/{start_date}'>/api/v1.0/start_date ='{start_date}'</a><br/>"
        f"<a href='/api/v1.0/{start_date}/{end_date}'>/api/v1.0/'{start_date}'-'{end_date}'</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def passengers():
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    session = Session(engine)
    results_prec = session.query(Measurement).all()
    
    # Create a dictionary from the row data and append to a list of all_passengers
    all_values = []
    for value in results_prec:
        value_dict = {}
        value_dict["date"] = value.date
        value_dict["prcp"] = value.prcp
        all_values.append(value_dict)

    return jsonify(all_values)

@app.route("/api/v1.0/stations")
def station():
    # Query all passengers
    # results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session = Session(engine)
    results_stations = session.query(Station).all()
    
    # Convert list of tuples into normal list
    # all_values = list(np.ravel(results))
    all_stations =[]
    for station in results_stations:
        station_dict = {}
        station_dict['station']=station.station
        station_dict['name']=station.name
        station_dict['latitude']=station.latitude
        station_dict['longtitude']=station.longitude
        station_dict['elevation']=station.elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>='2016-08-23').order_by(Measurement.date).all()
    all_temp =[]
    for temp in results_tobs:
        temp_dict = {}
        temp_dict['date']=temp.date
        temp_dict['tobs']=temp.tobs
        all_temp.append(temp_dict)

    return jsonify(all_temp)


@app.route("/api/v1.0/<start_date>")
def calc_start(start_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    all_start =[]
    for start in results:
        start_dict = {}
        start_dict['min_temp']=start[0]
        start_dict['average_temp']=start[1]
        start_dict['max_temp']=start[2]
        all_start.append(start_dict)
    
    return jsonify(all_start)

@app.route("/api/v1.0/<start_date>/<end_date>")
def calc(start_date,end_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    all_start =[]
    start_dict = {}
    start_dict['min_temp']=results[0][0]
    start_dict['average_temp']=results[0][1]
    start_dict['max_temp']=results[0][2]
    all_start.append(start_dict)
    
    return jsonify(all_start)

if __name__ == '__main__':
    app.run(debug=True)