# Spotify Data ETL

This project will conduct the full ETL process to extract data from the Kaggle API, perform necessary cleansing and transformation operations, and load the data into a MySQL database.

This project is designed in a scalable and efficient way, allowing the easy addition of other API sources.

It relies on a config file being parsed into the main function in the main.py file. This config will then be parsed through the ETL process, selecting the appropriate api to use, extracting data, cleaning, transforming, loading, and then visualising the data.


## To Do:

- [] Extend the config to parse visualisation properties properly.