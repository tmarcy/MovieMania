# Project Title

My Movie

## The project in short

Simple Google App Engine Web Application example with minimal style, written in Python 2.7, using Mashape Market API and 
The Open Movie Database sites API (see references in "Built With" section).
The app is able to search for a movie and give all informations about it.

## Specifications

* A form is used to retrieve user and movie data.
* The app verifies that the email address inserted by user is correct.
* The app response shows: movie poster, title, year, genre, director, cast and plot. 
* User data and searches are saved automatically in the Datastore.
* Two API GET are given to show statistics about searches types and about users and their searches.
* An API POST is given: it allows inserting a new search in the Datastore; 
in this case, parameters control is not required.

## Before starting
* Add a lib folder to the project, in which you have to install the libraries listed in "requirements.txt" file.
* You must be logged in Mashape Market site in order to use its API; the site, also, provide you with an API key: 
paste it in the variable named "MASHAPE_KEY", before you run this project.
* You must ask for an API key here: http://www.omdbapi.com/apikey.aspx, in order to use the service; paste it in the 
variable named "API_KEY" before you run this project.
Please, PAY ATTENTION: be sure to select "FREE" type account in the site.

## Built With

* [Google App Engine](https://cloud.google.com/appengine) - Platform used
* [Flask](http://flask.pocoo.org/) - The microframework for Python used
* [OMDb API](http://www.omdbapi.com/) - API used
* [IMG4Me](https://market.mashape.com/seikan/img4me-text-to-image-service) - API used

## Author

**Marcella Tincani** - [Marcella](https://github.com/tmarcy)
