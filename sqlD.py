import sqlite3

def create_connection(db_file):
  """ create a database connection to the SQLite database
      specified by db_file
      :param db_file: database file
      :return: Connection object or None
  """
  try:
    conn = sqlite3.connect(db_file)
    return conn
  except Error as e:
    print(e)
 
  return None

# Accepts a connection object and an SQL statement... Executes CREATE TABLE 
def create_table(conn, create_table_sql):
  try:
    c = conn.cursor()
    c.execute(create_table_sql)
  except Error as e:
    print(e)

# Creates tables
def createSqlTables():
  database = "stockInfo.db"
  sql_create_chart_table = """CREATE TABLE IF NOT EXISTS chart (symbol text PRIMARY KEY, date text, open real, high real, low real, close real, volume integer, unadjustedVolume integer, change real, changePercent real, vwap real, label text, changeOverTime real);"""
  sql_create_quote_table = """CREATE TABLE IF NOT EXISTS quote (symbol text PRIMARY KEY, companyName text, primaryExchange text, sector text, calculationPrice text, open real, openTime integer, close real, closeTime integer, high real, low real, latestPrice real, latestSource real, latestTime text, latestUpdate integer, latestVolume integer, iexRealtimePrice real, iexRealtimeSize real, iexLastUpdated text, delayedPrice real, delayedPriceTime integer, previousClose real, change real, changePercent real, iexMarketPercent real, iexVolume integer, avgTotalVolume integer, iexBidPrice real, iexBidSize integer, iexAskPrice real, iexAskSize real, marketCap integer, peRatio real, week52High real, week52Low real, ytdChange real, FOREIGN KEY(symbol) REFERENCES chart(symbol));"""
  sql_create_stats_table = """CREATE TABLE IF NOT EXISTS stats (companyName text, marketcap integer, beta real, week52high real, week52low real, week52change real, shortInterest integer, shortDate text, dividendRate real, dividendYield real, exDividendDate text, latestEPS real, latestEPSDate text, sharesOutstanding integer, float integer, returnOnEquity real, consensusEPS real, numberOfEstimates integer, symbol text, EBITDA integer, revenue integer, grossProfit integer, cash integer, debt integer, ttmEPS real, revenuePerShare real, revenuePerEmployee real, peRatioHigh real, peRatioLow real, EPSSurpriseDollar real, EPSSurprisePercent real, returnOnAssets real, returnOnCapital real, profitMargin real, priceToSales real, priceToBook real, day200MovingAvg real, day50MovingAvg real, institutionPercent real, insiderPercent real, shortRatio real, year5ChangePercent real, year2ChangePercent real, year1ChangePercent real, ytdChangePercent real, month6ChangePercent real, month3ChangePercent real, month1ChangePercent real, day5ChangePercent real, FOREIGN KEY(symbol) REFERENCES chart(symbol));"""
  # create a database connection
  conn = create_connection(database)
  if conn is not None:
    # create tables
    create_table(conn, sql_create_chart_table)
    create_table(conn, sql_create_quote_table)
    create_table(conn, sql_create_stats_table)
  else:
    print("Error! Cannot create the database connection.")





def select_lastrow_chart(conn):
    """
    Query last row in the chart table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM chart ORDER BY date DESC LIMIT 1")
 
    rows = cur.fetchall()
    
    return(rows)

def importLastChartRow():
  database = "stockInfo.db"
 
    # create a database connection
  conn = create_connection(database)
  with conn:
    print("Querying last row in chart...")
    return select_lastrow_chart(conn)


if __name__ == "__main__":
  createSqlTables()
  print(importLastChartRow())