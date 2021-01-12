# buticc-webapp
Repository for the Bug Ticket Classifier web application building with Flask

## Requirements

* Linux OS
* Python 3 
* Package Installer for Python (pip), installation instructions 
[here](https://pip.pypa.io/en/stable/installing/).

## Installation

To install Python required  the project please run the following commands at the project root :
```bash
$ python3 -m pip install --user virtualenv && \ 
pip install -r requirements.txt
```

## How to run ? 

To run the Flask server, launch with Python 3 the "controller.py"

* In **non production mode** the server will start on the localhost (127.0.0.0) using the port number 5000
* In **production mode** the server will start on the IP 0.0.0.0 and port 80 due to the Docker containerisation 

Production mode = AWS deployment using a Docker image.

## System Overview

### AWS Infrastructure

![AWS Infrastructure](https://raw.githubusercontent.com/qperez/buticc-webapp/main/doc/AWS_Infrastructure.png)


### Flask Server Starting

![flask server starting](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/qperez/buticc-webapp/main/doc/app_launching_state_diag.puml)

### Application Programming Interface

#### /predict/ticket
![API predict ticket](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/qperez/buticc-webapp/main/doc/API/API_predict_ticket.puml)


