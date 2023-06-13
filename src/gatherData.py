"""
File: "gatherData.py"
Author: Dorian ROUX
Date: June 2023
Brief: Use the Ergast Developer API to gather data regarding Formula1

Documentation: http://ergast.com/mrd/
> The API is free to use for any non-commercial purposes.
"""


# - Import Libraries - 
from bs4 import BeautifulSoup
import json
import os
import random
import re
import requests



# - Define Functions -

# -- Display a sample of a dictionnary --
def displayDictSample(dictionary: dict, numSample: int = 5):
    """Display a sample of a dictionnary.
    Args:
        dictionary (dict): the dictionnary to display.
        numSample (int, optional): the number of elements to display. Defaults to 5.
    """    
    key = random.sample(list(dictionary.keys()), k=numSample)
    str_ = f'Sample of the Dictionnary ({numSample} observations):'
    print(f"{str_}\n{'*' * len(str_)} \n")
    for k in sorted(key, reverse=False):
        print(k, dictionary[k])


# -- Update a dictionnary --
def updateDictionnary(inputDict: dict, outputDict: dict, inputKeys: list, outputKeys: list):
    """Update a dictionnary by adding a new key and value based on the existance of the inputKeys within the inputDict.
    Args:
        inputDict (dict): the input dictionnary.
        outputDict (dict): the output dictionnary.
        inputKeys (list): the list of keys to look for in the inputDict.
        outputKeys (list): the list of keys to add in the outputDict depending on the inputKeys.
    """    
    for i_, inputKey in enumerate(inputKeys):
        if inputKey in inputDict.keys():
            outputDict[outputKeys[i_]] = inputDict[inputKey]
    return outputDict


# -- Make a request to the Ergast Developer API --
def makeErgastRequest(requestContent: str, apiLimit: int = 1000, apiOffset: int = 0, apiExport: str = 'json'):
    """Make a request to the Ergast Developer API and return the response.
    Args:
        requestContent (str): the content of the request as a string. It is the content after the Ergast URL.
        apiLimit (int, optional): the number of information to request. Defaults to 1000.
        apiOffset (int, optional): the number of offset to setup. Defaults to 0.
        apiExport (str, optional): the type of exportation (JSON, XML). Defaults to 'json'.
    """    
    setupParameters = {'LIMIT' : apiLimit, 'OFFSET' : apiOffset, 'EXPORT' : apiExport}
    requestURL = f"http://ergast.com/api/f1/{requestContent}.{setupParameters['EXPORT']}?limit={setupParameters['LIMIT']}&offset={setupParameters['OFFSET']}"
    ErgastRequest = requests.get(requestURL, headers={}, data={})
    try:
        if ErgastRequest.status_code == 200:
            return ErgastRequest
        print(f'Request failed with status code {ErgastRequest.status_code}')
    except Exception as e:
        print(f'Error Caught while requesting the Ergast API: {e}')


def exportJSON(dictContent: dict, filePath: str):
    """Export a dictionnary as a JSON file.
    Args:
        dictContent (dict): the dictionary to export.
        filePath (str): the path where to export the file.
    """    
    if not os.path.exists(os.path.dirname(filePath)):
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
    with open(filePath, 'w') as fp:
        json.dump(dictContent, fp, indent=4)
          
    

# - CORE -
if __name__ == "__main__":
    
    # -- 1° | Get the SEASONS --
    seasonsReqs = makeErgastRequest('seasons').json()
    dictF1 = {seasonContent['season'] : dict() for seasonContent in seasonsReqs['MRData']['SeasonTable']['Seasons']}
    # dictF1['CURRENT_SEASON'] = max(list(dictF1.keys()))
    displayDictSample(dictF1, 5)

    print("\n")
    
    # -- 2.1° | Get the DRIVERS per SEASON --
    for seasonKey in dictF1.keys():
        driverReqs = makeErgastRequest(f'{seasonKey}/drivers').json()
        dictF1[seasonKey]['DRIVERS'] = dict()
        for driverContent in driverReqs['MRData']['DriverTable']['Drivers']:
            dictDriver = dict()
            dictDriver = updateDictionnary(driverContent, dictDriver, ['permanentNumber', 'code', 'givenName', 'familyName', 'dateOfBirth', 'nationality'], ['PERMANENT_NUMBER', 'CODE', 'FIRST_NAME', 'LAST_NAME', 'DATE_OF_BIRTH', 'NATIONALITY'])
            dictF1[seasonKey]['DRIVERS'][driverContent['driverId']] = dictDriver
    displayDictSample(dictF1[random.choice(list(dictF1.keys()))]['DRIVERS'], 5)

    print("\n")
    
    # -- 2.2° | Get the CONSTRUCTORS per SEASON --
    for seasonKey in dictF1.keys():
        constructorReqs = makeErgastRequest(f'{seasonKey}/constructors').json()
        dictF1[seasonKey]['CONSTRUCTORS'] = dict()
        for constructorContent in constructorReqs['MRData']['ConstructorTable']['Constructors']:
            dictConstructor = dict()
            dictConstructor = updateDictionnary(constructorContent, dictConstructor, ['name', 'nationality'], ['NAME', 'NATIONALITY'])
            dictF1[seasonKey]['CONSTRUCTORS'][constructorContent['constructorId']] = dictConstructor
    displayDictSample(dictF1[random.choice(list(dictF1.keys()))]['CONSTRUCTORS'], 5)

    print("\n")
    
    # -- 2.3° | Get the RACES per SEASON --
    for seasonKey in dictF1.keys():
        raceReqs = makeErgastRequest(f'{seasonKey}').json()
        dictF1[seasonKey]['RACES'] = dict()
        for raceContent in raceReqs['MRData']['RaceTable']['Races']:
            dictRace = dict()
            dictRace = updateDictionnary(raceContent['Circuit'], dictRace, ['circuitId'], ['CIRCUIT_ID'])
            dictRace['RACE'] = dict()
            dictRace['RACE'] = updateDictionnary(raceContent, dictRace['RACE'], ['raceName', 'date', 'time'], ['NAME', 'DATE', 'TIME'])
            dictRace = updateDictionnary(raceContent, dictRace, ['FirstPractice', 'SecondPractice', 'ThirdPractice', 'Sprint'], ['PRACTICE_1', 'PRACTICE_2', 'PRACTICE_3', 'SPRINT'])
            dictF1[seasonKey]['RACES'][raceContent['round']] = dictRace
    displayDictSample(dictF1[random.choice(list(dictF1.keys()))]['RACES'], 5)

    print("\n")
    
    # -- 2.4° | Get the RACES RESULTS per SEASON --
    for seasonKey in dictF1.keys():
        resultReqs = makeErgastRequest(f'{seasonKey}/results').json()
        dictF1[seasonKey]['RESULTS'] = dict()
        for resultContent in resultReqs['MRData']['RaceTable']['Races']:
            dictResult = dict()
            for driverContent in resultContent['Results']:
                dictResult[driverContent['position']] = dict()
                dictResult[driverContent['position']] = updateDictionnary(driverContent['Driver'], dictResult[driverContent['position']], ['driverId'], ['DRIVER_ID'])
                dictResult[driverContent['position']] = updateDictionnary(driverContent['Constructor'], dictResult[driverContent['position']], ['constructorId'], ['CONSTRUCTOR_ID'])
                dictResult[driverContent['position']] = updateDictionnary(driverContent, dictResult[driverContent['position']], ['grid', 'status', 'lap', 'Time', 'FastestLap', 'AverageSpeed'], ['GRID_POSITION', 'STATUS', 'N_LAPS', 'TIME', 'FASTEST_LAP', 'AVERAGE_SPEED'])
                dictF1[seasonKey]['RESULTS'][resultContent['round']] = dictResult
    displayDictSample(dictF1[random.choice(list(dictF1.keys()))]['RESULTS'], 5)
    
    print("\n")
    
    # -- 2.5° | Get the RACES RESULTS per LAP per SEASON --
    for seasonKey in dictF1.keys():
        dictF1[seasonKey]['LAPS'] = dict()
        n_races = len(makeErgastRequest(f'{seasonKey}').json()['MRData']['RaceTable']['Races'])
        for raceNum in range(1, n_races+1):       
            lapReqs = makeErgastRequest(f'{seasonKey}/{raceNum}/laps').json()

            if not lapReqs['MRData']['RaceTable']['Races']:
                dictF1[seasonKey]['LAPS'][raceNum-1] = dict()
                continue
            
            dictLaps = dict()
            for lapsContent in lapReqs['MRData']['RaceTable']['Races'][0]['Laps']:
                dictLaps[lapsContent['number']] = dict()
                for driverContent in lapsContent['Timings']:
                    dictLaps[lapsContent['number']][driverContent['driverId']] = dict()
                    dictLaps[lapsContent['number']][driverContent['driverId']] = updateDictionnary(driverContent, dictLaps[lapsContent['number']][driverContent['driverId']], ['position', 'time'], ['POSITION', 'TIME'])
            dictF1[seasonKey]['LAPS'][raceNum] = dictLaps
    displayDictSample(dictF1[random.choice(list(dictF1.keys()))]['LAPS'], 5)

    print("\n")
    
    # -- 3° | Export the data in a JSON file --
    pathFile = os.path.join('data', 'formula1-data.json')
    exportJSON(dictF1, pathFile)
    print(f"File exported in {pathFile}")