# Spotify Data ETL

This project will conduct the full ETL process to extract data from the Kaggle API, perform necessary cleansing and transformation operations, and load the data into a MySQL database.

This project is designed in a scalable and efficient way, allowing the easy addition of other API sources.

It relies on a config file being parsed into the main function in the main.py file. This config will then be parsed through the ETL process, selecting the appropriate api to use, extracting data, cleaning, transforming, loading, and then visualising the data.


## Process

Follow these steps for running this app:
1. Edit the kaggle-config.yaml file to extract the data you want. Details on how to do this are below in the *Configuration File Set Up* section.
2. Run the following commands:
```bash
chmod +x ./run_app.sh
./run_app.sh
```

This will execute the run_app file which runs the ETL process.

# Configuration File Set Up
This section will detail how to fill out the config file used by this app.

## To Do:

- [ ] Extend the config to parse visualisation properties properly.