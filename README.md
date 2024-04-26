# Snapp/Tapsi Ride Price Analytics
This project is a combo of a price checker and a price analytics scripts for Snapp and Tapsi ride-hailing services in Iran. 
The tool fetches the prices of rides from the Snapp and Tapsi APIs and then check the prices between two locations (one fixed destination and multiple origin candidates) at different times of the day and on different days of the week. 
This can also be used to analyze the price trends of rides over time and to compare the prices of rides between different locations. 
It can be used to help users make informed decisions about when and where to take a ride and to save money on ride-hailing services.

## Demo
[https://x.com/itsArmanj/status/1663319432666513409](https://x.com/itsArmanj/status/1663319432666513409)

## Gathering Data
`main.py` is the main script that fetches the prices of rides from the Snapp and Tapsi APIs.
This script gets called by a cron job on GitHub actions (`.github/workflows/prices.yml`). 
Each run adds multiple lines to `results.csv` file and commits the changes to the repository.

## Analyzing Data
The jupyter notebook `analytics.ipynb` is used to analyze the data in `results.csv` and to generate plots and tables that show the price trends of rides over time and the price differences between different locations.

## Considerations
- Read the code and fill in the necessary tokens and variables. Also, you'll need to define a repository secret `GH_TOKEN` in the repository settings.
- I wrote this a while ago and the API response format of Snapp and Tapsi might have changed since then. You have to check the APIs and update the code accordingly.

## License
MIT