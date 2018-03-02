# Automated Stock Trading Program

Builds a database of stock information from the iextrading.com API. 

Creates a table in the database from various websites, representing financial advisors daily "buy"/"sell" recommendations.

Continuously compiled database then used for data analysis and forecasting.

Machine learning run by Python's Keras/Tensorflow package(s) to identify a weighted scale of financial advisors' recommendations based on individual, average financial return of investments.

Machine learning run by R's Caret package to identify iex APIs' most useful information in predicting optimal financial return of investments.

Program will combine all data analysis and forecasting algorithms to make optimal "buy"/"sell" decisions.

"Buy"/"sell" decisions will be executed in a Charles Schwab brokerage account.

Dependencies:
- Python version 3.6.4
- Anaconda3
- Sqlite3 version 3.19.3 (2017-06-27)
- R version 3.4.3 (2017-11-30) -- "Kite-Eating Tree"
