#!/usr/lib/python3.6

import urllib.request
import json
import csv
import os
import requests

def writeToCsvFromRows(filename, rows):
  if len(rows) > 0:
    with open(filename, 'w') as csvfile:
      fieldnames = rows[0].keys()

      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()

      for row in rows:
        writer.writerow(row)

# Takes in a jsonArray and returns a list of strings
def jsonArrayToSymbolNames(jsonArray):
  symbolNames = []

  for i in range(0, len(jsonArray)):
    symbolNames.append(str(jsonArray[i]["symbol"]))
    
  return symbolNames


def gatherSymbols():
  # Grab the URL
  urlData = "https://api.iextrading.com/1.0/ref-data/symbols"
  # Open the URL and read the data
  webUrl = urllib.request.urlopen(urlData)
  # Verify that it works
  if (webUrl.getcode() == 200):
    print ("Connected and gathering symbols...")
    symbolArray = webUrl.read()
    
    rows = json.loads(symbolArray)
    
    symbolNames = jsonArrayToSymbolNames(rows)
    
    return symbolNames
  else:
    print ("Received an error from server, cannot retrieve results " + str(webUrl.getcode()))


def cleanData(jsonObject, dataType):
  rows = []
  for key in jsonObject:
    data = jsonObject[key][dataType]
    rows.append(data)
  return rows


def getData(symbols,dataType):
  # define a variable to hold the source URL
  urlData = "https://api.iextrading.com/1.0/stock/market/batch?symbols=" + ",".join(symbols) + "&types=" + dataType
  # Open the URL and read the data
  webUrl = urllib.request.urlopen(urlData)
  if (webUrl.getcode() == 200):
    data = webUrl.read()
    # print cleaned data
    rows = cleanData(json.loads(data), dataType)
    # write results to csv
    directory = "poophead/" + symbols[0]
    if not os.path.exists(directory):
      os.makedirs(directory)
    filename = directory + "/" + dataType.replace('/','_') + ".csv"
    print("Downloading data to " + filename)
    writeToCsvFromRows(filename, rows)
    # insert rows into sql
  else:
    print ("Received an error from server, cannot retrieve results " + str(webUrl.getcode()))
    
def updateChartData(symbols):
  # Grab the URL
  urlData = "https://api.iextrading.com/1.0/stock/market/batch?symbols=" + ",".join(symbols) + "&types=chart/5y"
  # Open the URL and read the data
  webUrl = urllib.request.urlopen(urlData)
  # Verify that it works
  if (webUrl.getcode() == 200):
    print ("Updating chart table...")
    symbolArray = webUrl.read()
    
    rows = json.loads(symbolArray)
    
    chartDataForDaysMissed = cleanChartData(rows)
    
  else:
    print ("Received an error from server, cannot retrieve results " + str(webUrl.getcode()))

def cleanChartData(rows):
  # Use Sql-quoteTable "latestTime": "September 19, 2017", to find date since last execution
  dateSinceLastExecution
  
  return chartDataForDaysMissed 
  # Keep only data for days needed for update
  # Print results to .csv


if __name__ == "__main__":
  stepSize=100
  symbolNames = gatherSymbols()

  for i in range(0, len(symbolNames), stepSize):
    #getData(symbolNames[i:i+stepSize],"quote")
    #getData(symbolNames[i:i+stepSize],"stats")
    updateChartData(symbolNames[i:i+stepSize])
