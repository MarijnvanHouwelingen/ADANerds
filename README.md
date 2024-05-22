# Readme
This file contains an overview of the source code of Group 6 for Assignment 2 (Advanced Data Architectures Year 2023-2024)


# The architecture:
The source code contains a simplified implementation of the application DataLodge in assignment 1.


## Bounded contexts
The following Bounded contexts were chosen in this implementation, which can be found in the folder 'Restful-API':
- Account: The account bounded contexts containing the following tables: user, profile and notfication settings. 
- Listing: The listing bounded context containing the following table: listing
- Booking: The booking bounded context containing the following table: booking

## Service implementation
The service implementation for every bounded context and the authentication service is done with Connexion, flask and SQLAlchemy. 

Connexion is a package that converts API endpoints configured in an Openapi format. The Openapi file for each bounded context service can be found in the 'openapi' folder. 
The resources of each HTTP request can be found in the bounded context name python file (account.py, listing.py, booking.py). The Openapi file refers to these resources in the resources tab per HTTP Method. 
SQLAlchemy was used as the ORM for this project. The Data access objects can be found in the corresponding DOA python files of each bounded context and the authentication service. 

The database file (db.py) creates the SQLAlchemy engine which is a bigquerry engine. Every bounded context has a different bigquery table and thus a different engine. 

The _pub files in each bounded context correspond to a publication message when triggered by an action.
- Account: When the PUT method is send and the user reports another user (report: true), then a message will be pubished on a dedicated topic.
- Booking: When the PUT method is send and the user wants a refund (refund:true), then a message will be published on a dedicated topic.

## FAAS
In this implementation, there are three microservices that are initiation with google functions:
- account_service
- picture_service
- refund_service

### Account_service
The account service detect  when a user has been reported (look at the PUT method in the users table for the publishing event) via a dedicated topic in the pub/sub eventbus. It gives a notification when it does.

### Picture_service
The picture service is an HTTP service that gives users the possibility to upload pictures of listings into a dedicated storage bucket. The service is accesible via the api-gateway and has authentication with the authentication service.

### Refund_servce
The refund service detect when a user wants a refund (look at the PUT method in the booking bounded context) via a dedicated topic on the pub/sub event bus. A notification will be made by this microservice.

## Authentication
For Authentication we use Bearer authentication in combination with JWT tokens. A user first has to register with the /register endpoint in the api-gateway. The user than gets a Bearer token which can be used to access the bounded contexts and picture service. The authentication service provided the bearer token and ensures that the token provided is valid when users try to access.

## API-Gateway
A KrakenD api gateway has been as a reverse proxy for all users. So that users do not have to access each URL independently. As mentioned, the api gateway uses the KrakenD to redirect the users to the correct URLs when giving the correct endpoint. Authentication is done by the authentication service, thus KrakenD only serves as a reverse-proxy. 


# Contributers:
- Marijn van Houwelingen 
- Edde Jansen
- Kyra Jongman
- Mark van Vlierden
- Floor Halkes
