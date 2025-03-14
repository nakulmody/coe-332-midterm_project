# ISS Tracking Program

## Description

The purpose of this folder is to introduce ourselves to web APIs and learn how to incorporate them into our scripts to reduce the load on users. 

In this folder, we interact with a web API to injest data from the ISS website and perform summary statistics on them.

This application uses docker, so please ensure you have that library.

## Explanation of scripts

iss_tracker.py - This is the main script for this project. It holds all 3 functions (range_data, data_set_closest, average_speed) which provide the summary statistics found in the output. This is also where the main function can be found which is where we interact with our web API and output our results.

API Reference: https://spotthestation.nasa.gov/trajectory_data.cfm

test_iss_tracker.py - This is our unit testing file for the iss_tracker script. It tests the 3 functions that were created in the main script including the normal case, and most edge cases. 

1. Build the Docker Image

Navigate to the directory containing the Dockerfile and iss_tracker.py, then run the following command to build the Docker image:

docker build -t iss_tracker .

What this does:

docker build starts the build process.

-t iss_tracker tags the image with the name iss_tracker.

. indicates that the Dockerfile is in the current directory.

2. Run the Docker Container

Once the image is built, start the container using:

docker run -p 5000:5000 iss_tracker

What this does:

docker run starts a new container from the iss_tracker image.

-p 5000:5000 maps port 5000 of the container to port 5000 on the host machine, making the Flask API accessible.

iss_tracker is the name of the Docker image.

3. Access the Flask API

After the container starts, you can access the API in a browser or using curl

We can then use the GET keyword to call API endpoints that end up calling functions to get our
    summary statistics

Ex.
We can type the below line in the terminal to run our API endpoint "/now" and receive summary statistics based on the closest data point to the current time

curl http://localhost:5000/now

4. Stopping the Container

To stop the running container, press Ctrl + C in the terminal where it is running.



## Interpreting output
IF RUNNING API ENDPOINTS IN ORDER AS SEEN ON COE332 Website:

The first lines print the entire data set. It is given as a list of dictionaries with EPOCH, X coordinates, Y coordinates, and Z Coordiates as well as velocities in the x,y, and z directions.

The next function will print certain data points based on our limit and offset. This will be based on user input on the flask API.

The next function will be printing a specific data points' state vectors. This will also bebased on user input on the flask API.

The next function will print the instantaneuous speed at a time. This will also bebased on user input on the flask API.

The last endopoint will print the state vectors for the closest data set based on the current time. It will also print the instantaneuous speed.

## Use of AI

AI was used in this project, specifically when dealing with the datetime library as I am not familiar with the functions and syntax. Additionally, some of the unit testing was created with the help of AI as I forgot a few edge cases that needed to be checked. It was also used in the creation of the docker file because I was confused on how that worked (still not sure if done correctly). The last thing that an AI was used for was the creation of the directions for how to build/run program. A bit of this was confusing for me so I used Chat GPT to help clear this up. Disclaimer: Not sure if this is written correctly since this past week has been extremely difficult for me, and I haven't been able to come to class since I was so busy with midterms from other classes. Sorry!! I will pick up the slack this week!








