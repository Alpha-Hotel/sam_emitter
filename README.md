# Threat Control Tool

## Overview

The Threat Control Tool was developed during the Bravo Hackathon in July 2022 by multiple different developers. 

### Dan App

This is the web application portion of the tool. It is written in ReactJS and was based off of the
create-react-app framework created by Facebook. It can be developed in a standalone mode if desired.

### SAM Emitter Services

The web services of the tool are written using python WebSockets to improve data availability to the UI. The
API can be accessed by going to http://localhost:6969/ and http://localhost:7060/

## Development

NOTE: Run all commands below from root <code>base-ui-project/</code> directory.

### To start the entire platform

<code>docker-compose up -d</code>

This starts the services and the web application at the same time

### To start Dan App

<code>cd dan-app</code>  
<code>npm install</code> *If needed  
<code>npm start</code>

**This will only start the web application and will not leverage any of the services.  
There will be no data available in the app if started this way.

### To start SAM Emitter services

From the root base-ui-project directory:  
<code>docker-compose up sam-emitter-services</code>

After changes, the services can be rebuilt using:  
<code>docker-compose up --no-deps --build sam-emitter-services </code>

## Deployment

**Create the docker images**  
<code>docker-compose build</code>

OR

<code>docker build -f Dockerfile --no-cache -t dan-app .</code>  
<code>docker build -f Dockerfile --no-cache -t sam-emitter-services .</code>

**Save the images**  
<code>docker save dan-app:latest | gzip > dan-app-< buildDate >.tar.gz</code>  
<code>docker save sam-emitter-services:latest | gzip > sam-emitter-services-< buildDate >.tar.gz</code>  

**Load the docker image:**  
<code>docker load -i dan-app.tar.gz</code>  
<code>docker load -i sam-emitter-services.tar.gz</code>  

**Run the image:**  
<code> docker-compose -f docker-compose-prod.yml up -d </code>   

** Note **  You may need to run a <code>docker container prune</code> if it gives you an error about finding images
