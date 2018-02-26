#!/usr/lib/python3.4

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
    print ("Grathering symbols...")
    symbolArray = webUrl.read()
    
    rows = json.loads(symbolArray)
    
    symbolNames = jsonArrayToSymbolNames(rows)
    
    return symbolNames
  else:
    print ("Received an error from server, cannot retrieve results " + str(webUrl.getcode()))


def cleanData(jsonObject):
  rows = []
  for key in jsonObject:
    quote = jsonObject[key]["quote"]
    rows.append(quote)
  return rows


def getData(symbols):
  # define a variable to hold the source URL
  # symbols: ["aapl", "fb", "tsla"]
  urlData = "https://api.iextrading.com/1.0/stock/market/batch?symbols=" + ",".join(symbols) + "&types=quote"
  # Open the URL and read the data
  webUrl = urllib.request.urlopen(urlData)
  if (webUrl.getcode() == 200):
    data = webUrl.read()
    # print cleaned data
    rows = cleanData(json.loads(data))
    # write results to csv
    directory = "csv_data"
    if not os.path.exists(directory):
      os.makedirs(directory)
    filename = directory + "/" + symbols[0] + ".csv"
    print("Downloading data to " + filename)
    writeToCsvFromRows(filename, rows)
    # insert rows into sql
  else:
    print ("Received an error from server, cannot retrieve results " + str(webUrl.getcode()))
    
if __name__ == "__main__":
  stepSize=100
  symbolNames = gatherSymbols()

  for i in range(0, len(symbolNames), stepSize):
    getData(symbolNames[i:i+stepSize])
 
