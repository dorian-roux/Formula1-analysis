# Formula 1 - Data Analysis and Visualization

> This project does not aim to be commercialized in any way. It is a personal project for learning purposes only.


## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)



## About <a name = "about"></a>


## Getting Started <a name = "getting_started"></a>

To get started with this project, you will need to follow the instructions below.

1) Have both [Python 3.7 or higher](https://www.python.org/downloads/) and Jupiter Notebook installed.

2) Clone this repository using the following command:
    ```bash
    git clone https://github.com/dorian-roux/Formula1-analysis
    ``` 
3) Navigate to the repository and create virtual environment and activate it using the following commands:
    ```bash
    python -m venv ${YOUR_ENV_NAME}
    source ${YOUR_ENV_NAME}/bin/activate # For Linux
    ```
    You can replace `${YOUR_ENV_NAME}` with the name you want to give to your virtual environment.
    
4) Install the required packages using the following command:
    ```bash
    pip install -r requirements.txt
    ```

After those steps, you should be able to run the Notebooks.



## Usage <a name = "usage"></a>

### Ergast Developer API

The [Ergast Developer API](http://ergast.com/mrd/). is used to get the data for this project. It is an experimental web service which provides a historical record of motor racing data for non-commercial purposes.

### Generate the Data

To generate the data files `formula1-circuits.json` and `formula1-data.json`, you need to run the Notebook `DataF1-ErgastAPI.ipynb` which will generate the data in their corresponding folder. Those data will be used in the analysis and visualization Notebooks.

The data file `formula1-circuits.json` will contain the following information about the circuits based on the `CIRCUIT_ID` :
- **Circuit** : The name of the circuit.
- **Country** : The country where the circuit is located.
- **City** : The city where the circuit is located.
- **Coordinates** : The coordinates of the circuit. 

Example with the Silverstone circuit :
```json
"silverstone": {
    "CIRCUIT_NAME": "Silverstone Circuit",
    "COUNTRY": "UK",
    "CITY": "Silverstone",
    "COORDINATES": ["52.0786", "-1.01694"]
},
```

the data file `formula1-data.json` will contain global information regarding Formula 1. It contains the racing information based on the `YEAR`: 
- **Drivers** : Information about the drivers including their full name, birthdate and nationality.
- **Constructors** : Information about the constructors including their name and nationality.
- **Circuits** : Information about the circuits including their id, name and the date.
- **Laps** : Information about the laps including for each lap all the drivers position and time. The laps are not available for every year (most unlikely to be available for the early years).
- **Results** : Information about the results for each race including the driver, construction, grid position, final position, time, fastest lap and fastest lap ranking. The time of the driver is based on the time of the winner of the race (for instance D1 finished first in 1h30m00s and D2 finished second in 1h30m10s, D2 will have a time of +10s). Here also the availability of the fastest lap is not guaranteed for every year.

