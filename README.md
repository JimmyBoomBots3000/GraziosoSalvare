# GraziosoSalvare
A full stack Python web app to query a MongoDB database.

## About the Project
The Grazioso Salvare web-app is an interactive tool designed to assist in easily locating ideal candidate animals for search-and-rescue training.  The dashboard displays a data table showing animals from an animal shelter database using pre-defined search criteria.  The accompanying interactive map shows the exact location of selected animals.

## Tools Used
MongoDB was selected as the model component for this project, which is ideal for large amount of semi-structured data.  MongoDB offers quickly and easily interfaceable access to this data.
The view and controller components of this application utilize Dash.  Dash enables quick development of custom interfaces and displays in web applications using Python, for which MongoDB also has a native driver.  This makes them an ideal pair for a full-stack application such as this one.

## Development
~~This tool requires installation of or access to an installation of MongoDB as well as a local installation of Python.  It has been tested using Python 3.9 and MongoDB 4.2.~~  This application is now hosted on Heroku at [graziososalvare.herokuapp.com/](https://graziososalvare.herokuapp.com) and accesses a database hosted on MongoDB Atlas.  
The application uses a custom database access Python class to instantiate and query the database.  A Python script utilizing Dash components was written for the front-end application.  This script contains the query logic that provides the one-click access to custom searches using radio buttons.  Queried data is in turn displayed in a table that pages results by 10.  The front-end script also utilizes Dash components to provide the map feature and a pie chart showing the percentage of animals of each breed for a selected query.

## Usage
The application initially displays a table, with unfiltered data from the database.  Below the table is a pie chart showing breed, by percentage, of all animals within the selected filter, as well as an unmarked map.

![](images/new_1.png)

Selecting a radio button in the header section will filter the table to animals ideally suited to each purpose, as provided for in the specification.  The pie chart is updated to reflect the breakdown of breeds in this selection.

![](images/new_2.png)

Each row in the table represents an animal in the database.  Selecting a row will show the animal’s location on the interactive map.  Clicking the marker on the map will display the animals name and breed.

![](images/new_3.png)