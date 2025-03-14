#!/usr/bin/env python3

import requests
import json
import xmltodict
import datetime
import math
import logging
import redis
from flask import Flask, Response, request, jsonify

logging.basicConfig(level=logging.ERROR)

app = Flask(__name__)
rd = redis.Redis(host='127.0.0.1', port=6379, db=0)

def fetching_data():
    """
    This is a helper function that is just meant to grab data from the url

    Output:
    List of dictionaries
    """
    if(rd.dbsize() == 0):
        url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
        response = requests.get(url)
        data = xmltodict.parse(response.content)
        # Sifted manually through the conversion to get to the useful data
        list_data = data['ndm']['oem']['body']['segment']['data']['stateVector']
        rd.set("iss_data", json.dumps(list_data))



def calc_speed(list_data, index):
    """
    This is a helper function that calculates the instaneuous
        speed at a given EPOCH.
    """
    x_dot = list_data[index]['X_DOT']["#text"]
    y_dot = list_data[index]['Y_DOT']["#text"]
    z_dot = list_data[index]['Z_DOT']["#text"]
    insta_velo = ((float(x_dot) ** 2) + (float(y_dot) ** 2) + (float(z_dot) ** 2))
    insta_velo = math.sqrt(insta_velo)
    return insta_velo





def range_data(list_data: list, key_string: str) -> tuple:
    """
    This function finds the range for the data set, specifically, the earliest and latest
    times. These values are then returned as a tuple.

    Inputs:

    list_data:
    Type: list
    Holds all the data from the ISS website as a list where each index is a data point
    Each index is a dictionary where the keys are either the time (EPOCH),
    position (x,y,z) in km, or velocity (x,y,z) in km/s
    
    key_string:
    Type: String
    This is the key for the dictionary

    Output:
    Type: tuple
    The first value of the tuple is the earliest time in data set
    The second value of the tuple is the latest time in data set
    """

    logging.info("Finding the range of the dataset.")
    earliest_time = list_data[0][key_string]
    latest_time = list_data[0][key_string]

    for data_point in list_data:
        if data_point[key_string] < earliest_time:
            earliest_time = data_point[key_string]
            logging.debug(f"New earliest time found: {earliest_time}")
        if data_point[key_string] > latest_time:
            latest_time = data_point[key_string]
            logging.debug(f"New latest time found: {latest_time}")

    logging.info(f"Earliest: {earliest_time}, Latest: {latest_time}")
    return (earliest_time, latest_time)



@app.route('/epochs', methods = ['GET'])
def get_epochs() -> Response:
    """
    Calls helper function to get data and finds whether putting the data limitations based on input
    It only prints out a certain number of data using the limit and offset value if limit and offset
    values given
    """
    list_data = json.loads(rd.get("iss_data"))
    limit = int(request.args.get("limit", 0))
    offset = int(request.args.get("offset", 0))
    if(limit <= 0 or offset <= 0):
        return list_data
    list_specific = []
    for i in range(offset, offset + limit):
        list_specific.append(list_data[i])
    
    return list_specific

@app.route('/epochs/<epoch>/location', methods = ['GET'])
def get_location(epoch):
    

@app.route('/epochs/<epoch>', methods = ['GET'])
def specific_data(epoch):
    """
    This function is reponsible for getting all the state vectors for
    a specific EPOCH based on the user. 
    """
    specific = epoch
    index = None
    list_data = json.loads(rd.get("iss_data"))
    for i in range(len(list_data)):
        if(specific == list_data[i]['EPOCH']):
            index = i
            break

    return list_data[index]

@app.route('/epochs/<epoch>/speed', methods = ['GET'])
def get_speed(epoch):
    """
    This function returns the speed at a given EPOCH
    """
    specific = epoch
    index = None
    list_data = json.loads(rd.get("iss_data"))
    for i in range(len(list_data)):
        if(specific == list_data[i]['EPOCH']):
            index = i
            break
    
    insta_speed = calc_speed(list_data,index)
    answer = f"The instantaneous speed at this time is {insta_speed}\n"
    return answer

@app.route('/now', methods = ['GET'])
def state_close_to_now():
    """
    This function finds the closest data point to the current time
        and prints the state vectors along with its instaneous speed
    """

    list_data = json.loads(rd.get("iss_data"))
    closest_data = data_set_closest(list_data, 'EPOCH')
    index = None
    for i in range(len(list_data)):
        if(closest_data[0] == list_data[i]['EPOCH']):
            index = i
            break

    insta_speed = calc_speed(list_data, index)
    answer = f"The closest data point has a date/time of {closest_data[0]}\n"
    answer += f"The x,y,z coordinates of the ISS at this point are {closest_data[1]} {closest_data[2]} {closest_data[3]}\n"
    answer += f"The velocity components at this time are {closest_data[4]} km/s in the x-direction " \
        f"{closest_data[5]} km/s in the y-direction {closest_data[6]} km/s in the z-direction.\n"
    answer += f"The instantaneous velocity at this time is {insta_speed}\n"
    return answer

    

    


def data_set_closest(list_data: list, key_string: str) -> list:
    """
    This function returns the data point closest to the current time.
    It will compare the current UTC time and find the data point closest to the current time
    and retrieve all the information about that point.

    Inputs:

    list_data:
    Type: list
    Holds all the data from the ISS website as a list where each index is a data point
    Each index is a dictionary where the keys are either the time (EPOCH),
    position (x,y,z) in km, or velocity (x,y,z) in km/s

    key_string:
    Type: String
    This is the key for the dictionary

    Output:
    Type: List
    List that stores the time, the state vectors, and the velocities of the ISS
    at that point.
    """
    # These 2 lines were created with the help of AI
    logging.info("Finding the closest data point to the current time.")
    cur_date = datetime.datetime.now(datetime.timezone.utc)
    closest_index_date = datetime.datetime.strptime(list_data[0][key_string], "%Y-%jT%H:%M:%S.%fZ").replace(tzinfo=datetime.timezone.utc)
    index_of = 0

    for index in range(len(list_data)):
        # This line was also created with the help of AI
        loop_date = datetime.datetime.strptime(list_data[index][key_string], "%Y-%jT%H:%M:%S.%fZ").replace(tzinfo=datetime.timezone.utc)
        if abs(loop_date - cur_date) < abs(closest_index_date - cur_date):
            closest_index_date = loop_date
            index_of = index
            logging.debug(f"New closest time found: {closest_index_date}")
    
    closest_data = []
    for key in list_data[index_of].keys():
        if key == 'EPOCH':
            closest_data.append(list_data[index_of][key])
        else:
            closest_data.append(list_data[index_of][key]['#text'])
    
    logging.info(f"Closest data point: {closest_data}")
    return closest_data

def average_speed(list_data: list, closest_data: list) -> tuple:
    """
    This function computes the average speed of the entire data
    set. It uses the general formula for speed. It also calculaltes
    the instantaneous speed closest to now.
    
    Inputs:

    list_data:
    Type: list
    Holds all the data from the ISS website as a list where each index is a data point
    Each index is a dictionary where the keys are either the time (EPOCH),
    position (x,y,z) in km, or velocity (x,y,z) in km/s

    closest_data
    Type: list
    Holds the specific data point that is closest to the current time. Instead of being
    a dictionary it holds it as an array where the first index is the time, the next three
    are the x,y,z coordinates, and the last 3 are the velocites in x,y, and z.

    Output:

    Type: Tuple
    The first value will hold the average speed of the entire data set and the second
    value will hold the instantaneous speed based on the data point closest to now 
    (provided as input as closest data)
    """

    logging.info("Calculating average and instantaneous speed.")
    total_speed = 0
    num_data = 0
    
    for data in list_data:
        data_speed = (float(data['X_DOT']['#text']) ** 2) + (float(data['Y_DOT']['#text']) ** 2) + (float(data['Z_DOT']['#text']) ** 2)
        data_speed = math.sqrt(data_speed)
        total_speed += data_speed
        num_data += 1
    
    avg_speed = total_speed / num_data
    insta_velo = (float(closest_data[4]) ** 2) + (float(closest_data[5]) ** 2) + (float(closest_data[6]) ** 2)
    insta_velo = math.sqrt(insta_velo)
    
    logging.info(f"Average speed: {avg_speed} km/s, Instantaneous speed: {insta_velo} km/s")
    return (avg_speed, insta_velo)

        


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    fetching_data()



