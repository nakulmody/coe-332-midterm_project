# ISS Tracking Program

## Description

The purpose of this folder is to introduce ourselves to redis databases and learn how to incorporate them into our scripts and web APIs to perform higher level computations.

In this folder, we interact with a web API and a redis database to injest data from the ISS website and push to database and eventually perform summary statistics on them.

This application uses docker, so please ensure you have that library.

## Explanation of scripts

iss_tracker.py - This is the main script for this project. It holds all 3 functions (range_data, data_set_closest, average_speed) which provide the summary statistics found in the output. This is also where the main function can be found which is where we interact with our web API and output our results.

API Reference: https://spotthestation.nasa.gov/trajectory_data.cfm

test_iss_tracker.py - This is our unit testing file for the iss_tracker script. It tests the 3 functions that were created in the main script including the normal case, and most edge cases. 

docker-compose.yml - yml file that helps us create 2 containers, one for the redis database and one for flask to run on

requirments.txt - Text file that holds all the dependencies that need to be pip installed upon running program.

1. Open up 2 Windows:

We want to open up 2 windows, one that has access to the directory with the files.

We do this because when running our flask and redis applications, we are unable to use the

terminal to hit our endpoints. By creating 2 windows we are going to use one of the windows to run our docker

image which in turn runs flask and our redis database, and make the other window hit our endpoints to look at our

computations. 

2. Build the Docker Image:

We compose our docker image to help create our containers and run our code eventually. This is done in the window in the directory.

Navigate to the directory containing the Dockerfile and iss_tracker.py, then run the following command to build the Docker image:

docker compose up --build -d

What this does:

docker-compose works along with Dockerfile in setting up the environments.

We use --build to build our image and environments. The -d helps us use the terminal after running.

It creates 2 containers and installs all the dependencies from the requirments.txt file.

3. Run the Docker Container

Once the image is built, load up flask in the container and start compiling the script.

docker run testing

What this does:

We just name the instance of running the image testing. We don't have to worry about initializing ports since this is done
in the yml file.


4. Access the Flask API

After the container starts, you can access the API in a browser or using curl. We do this in the other window that has been untouched.

It does not matter whether this is in the directory or not since we are accessing the API using ports.

We can then use the GET keyword to call API endpoints that end up calling functions to get our
summary statistics

Ex.
We can type the below line in the terminal to run our API endpoint "/now" and receive summary statistics based on the closest data point to the current time

curl http://localhost:5000/now

5. Stopping the Container

To stop the running container, press Ctrl + C in the terminal where it is running.

Make sure to close the containers after my writing docker compose down



## Interpreting output
IF RUNNING API ENDPOINTS IN ORDER AS SEEN ON COE332 Website:

The first endpoint (/epochs) the entire data set. It is given as a list of dictionaries with EPOCH, X coordinates, Y coordinates, and Z Coordiates as well as velocities in the x,y, and z directions. If given a limit and offset it will apply accordingly and give limit number of datapoints after the offset.

The next endpoint (/epochs/<epoch>) gives the state vectors of a specific data point.

The next endpoint (/epochs/<epoch>/location) gives the location of the ISS at that point in time. It will give the latitude, longitude, altitude, and the relative location (what state, country it is above)

The next endpoint (/epochs/<epoch>/speed) will print the instantaneuous speed at a time.

The last endopoint (/now) will return the state vectors for the closest data set based on the current time. It will also return the instantaneuous speed and the location.

## Use of AI

AI was used in this project, specifically when dealing with the datetime library as I am not familiar with the functions and syntax. Additionally, some of the unit testing was created with the help of AI as unit testing for flask and redis is difficult and was not covered in clas. It was also used in the creation of the docker file because I was confused on how that worked (still not sure if done correctly). The last thing that an AI was used for was the creation of the directions for how to build/run program. A bit of this was confusing for me so I used Chat GPT to help clear this up. Disclaimer: Not sure if this is written correctly since this past week has been extremely difficult for me, and I haven't been able to come to class since I was so busy with midterms from other classes. Sorry!! I will pick up the slack this week!








