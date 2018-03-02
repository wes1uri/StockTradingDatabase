#!/usr/lib/python3.6

# Run in terminal with python3.6 ST.py command

# While running program, need to disable computer's auto-sleep mode bc it will 
# disconnect from the internet and the API calls will break.

import urllib.request
import json
import csv
import os
import sqlD

# https://api.iextrading.com/1.0/ref-data/symbols
# https://api.iextrading.com/1.0/stock/market/batch?symbols=aapl,fb,tsla&types=chart&range=5y


def writeToCsvFromRows(filename, rows, dataType):
  if dataType == "chart":
    fieldnames = ["date","open","high","low","close","volume","unadjustedVolume","change","changePercent","vwap","label","changeOverTime","symbol"]
  elif dataType == "quote":
    fieldnames = ["symbol","companyName","primaryExchange","sector","calculationPrice","open","openTime","close","closeTime","high","low","latestPrice","latestSource","latestTime","latestUpdate","latestVolume","iexRealtimePrice","iexRealtimeSize","iexLastUpdated","delayedPrice","delayedPriceTime","previousClose","change","changePercent","iexMarketPercent","iexVolume","avgTotalVolume","iexBidPrice","iexBidSize","iexAskPrice","iexAskSize","marketCap","peRatio","week52High","week52Low","ytdChange"]
  elif dataType == "stats":
    fieldnames = ["companyName","marketcap","beta","week52high","week52low","week52change","shortInterest","shortDate","dividendRate","dividendYield","exDividendDate","latestEPS","latestEPSDate","sharesOutstanding","float","returnOnEquity","consensusEPS","numberOfEstimates","symbol","EBITDA","revenue","grossProfit","cash","debt","ttmEPS","revenuePerShare","revenuePerEmployee","peRatioHigh","peRatioLow","EPSSurpriseDollar","EPSSurprisePercent","returnOnAssets","returnOnCapital","profitMargin","priceToSales","priceToBook","day200MovingAvg","day50MovingAvg","institutionPercent","insiderPercent","shortRatio","year5ChangePercent","year2ChangePercent","year1ChangePercent","ytdChangePercent","month6ChangePercent","month3ChangePercent","month1ChangePercent","day30ChangePercent","day5ChangePercent"]
  else:
    print("Error: Wrong data type.")
  
  with open(filename, 'w') as csvfile:

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
    print ("Connected to URL and gathering symbols...")
    symbolArray = webUrl.read()
    
    rows = json.loads(symbolArray)
    
    symbolNames = jsonArrayToSymbolNames(rows)
    
    return symbolNames
  else:
    print ("Received an error from server, cannot retrieve results " + str(webUrl.getcode()))


def cleanDictData(jsonObject, dataType):
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
    rows = cleanDictData(json.loads(data), dataType)
    # write results to csv
    directory = "tempData/" + symbols[0]
    if not os.path.exists(directory):
      os.makedirs(directory)
    filename = directory + "/" + dataType.replace('/','_') + ".csv"
    print("Downloading data to " + filename)
    writeToCsvFromRows(filename, rows, dataType)
  
  else:
    print ("Received an error from server, cannot retrieve quote or stats data " + str(webUrl.getcode()))


   
def cleanChartArray(jsonObject):
  rows = []
  for symbol in jsonObject:
    data = jsonObject[symbol]["chart"]
    for day in data:
      day["symbol"] = symbol
    rows += data
  # Change importLastChartRow to take in symbol so that it returns the last row per symbol
  # Put the following in the for loop above per symbol 
  latestChartRow = sqlD.importLastChartRow()
  
  latestChartDate = "1970-01-23"
  if latestChartRow:
    latestChartDate = latestChartRow[0][0]

  chartDataForDaysMissed = [row for row in rows if row["date"] > latestChartDate]
 
  return chartDataForDaysMissed
 
 
  
def updateChartData(symbols):
  # Grab the URL
  urlData = "https://api.iextrading.com/1.0/stock/market/batch?symbols=" + ",".join(symbols) + "&types=chart&range=5y"
  # Open the URL and read the data
  webUrl = urllib.request.urlopen(urlData)
  # Verify that it works
  if (webUrl.getcode() == 200):
    print ("Updating chart table...")
    chartArray = webUrl.read()
    rows = json.loads(chartArray)
    
    chartDataForDaysMissed = cleanChartArray(rows)
    if chartDataForDaysMissed:
      ### Print results to .csv
      directory = "tempData/" + symbols[0]
      if not os.path.exists(directory):
        os.makedirs(directory)
      filename = directory + "/chart.csv"
      print("Downloading data to " + filename)
      writeToCsvFromRows(filename, chartDataForDaysMissed, "chart")
    else:
      print("Chart data is up to date.")
    
  else:
    print ("Received an error from server, cannot retrieve chart data " + str(webUrl.getcode()))
    
#def loadAllCsvDataToDatabase():



if __name__ == "__main__":
  
  # Create a database if none exists
  sqlD.createSqlTables()
  
  stepSize=100
  symbolNames = gatherSymbols()

  for i in range(0, len(symbolNames), stepSize):
    updateChartData(symbolNames[i:i+stepSize])
    getData(symbolNames[i:i+stepSize],"quote")
    getData(symbolNames[i:i+stepSize],"stats")
    
  #loadAllCsvDataToDatabase()
  sqlD.loadAllCsvDataToDatabase()
    
