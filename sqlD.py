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
def createSqlTable():
  database = "pythonsqlite.db"
  
  sql_create_quote_table = """CREATE TABLE IF NOT EXISTS quote (symbol TEXT PRIMARY KEY, companyName text, primaryExchange text, sector text, calculationPrice text, open real, openTime integer, close real, closeTime integer, high real, low real, latestPrice real, latestSource real, latestTime text, latestUpdate integer, latestVolume integer, iexRealtimePrice real, iexRealtimeSize real, iexLastUpdated text, delayedPrice real, delayedPriceTime integer, previousClose real, change real, changePercent real, iexMarketPercent real, iexVolume integer, avgTotalVolume integer, iexBidPrice real, iexBidSize integer, iexAskPrice real, iexAskSize real, marketCap integer, peRatio real, week52High real, week52Low real, ytdChange real);"""
  
  # create a database connection
  conn = create_connection(database)
  if conn is not None:
    # create projects table
    create_table(conn, sql_create_quote_table)
  else:
    print("Error! Cannot create the database connection.")

if __name__ == "__main__":
  createSqlTable()
