import finnhub
import requests
import pandas as pd
import datetime

finnhub_client = finnhub.Client(api_key="ciu35ihr01qkv67u3jdgciu35ihr01qkv67u3je0")


def get_stock_data(ticker_symbol, start_unix_time, end_unix_time):
    print(pd.DataFrame(finnhub_client.technical_indicator(
    symbol=f"{ticker_symbol}",
    resolution="D",
    _from={start_unix_time}, #user input from start_date
    to={end_unix_time},   #user input from end_date
    indicator="rsi",
    indicator_fields={"timeperiod": 6},
)))


user_ticker = input("Enter the stock ticker symbol: ").upper()

start_date = input("enter your start date: (format m/d/yyyy)")       
end_date = input("enter your end date: ")
start_date_format = datetime.datetime.strptime(start_date, "%m/%d/%Y")
end_date_format = datetime.datetime.strptime(end_date, "%m/%d/%Y")
start_unix_time = int(datetime.datetime.timestamp(start_date_format))
end_unix_time = int(datetime.datetime.timestamp(end_date_format))
print(int(start_unix_time))
print(int(end_unix_time))

get_stock_data(user_ticker, start_unix_time, end_unix_time)


















# r = requests.get(url="https://quotes-gw.webullfintech.com/api/bgw/quote/realtime?ids=913243250&includeSecu=1&more=1")
# d = r.json()

# index = d[0]

# tickerid = index['tickerId']
# symbol = index['symbol']
# open = index['open']
# close = index['close']
# high = index['high']
# low = index['low']


# print(tickerid, symbol, "Open: " + open + ",", "Close:"  + close + ",", "High: " + high + ",", "Low: " + low )


# import requests

# def fetch_stock_data_by_ticker(ticker_symbol):
#     url = f"https://quotes-gw.webullfintech.com/api/bgw/quote/realtime?symbols={ticker_symbol}&includeSecu=1&more=1"
#     try:
#         r = requests.get(url)
#         r.raise_for_status()  # Raise an exception if the response status code is an error
#         data = r.json()
#         if not data or 'error' in data or 'data' not in data:
#             print("Error: Stock data not found for the provided ticker.")
#             return

#         index = data['data'][0]
#         ticker_id = index['tickerId']
#         symbol = index['symbol']
#         open_price = index['open']
#         close_price = index['close']
#         high_price = index['high']
#         low_price = index['low']
#         print(f"Ticker ID: {ticker_id}, Symbol: {symbol}, Open: {open_price}, Close: {close_price}, High: {high_price}, Low: {low_price}")
#     except requests.exceptions.RequestException as e:
#         print("Error: Unable to fetch data. Please check your internet connection or try again later.")
#         return
#     except KeyError as e:
#         print("Error: Invalid data received from the API.")
#         return

# # Ask the user to input a ticker symbol
# user_ticker = input("Enter the ticker symbol of the stock you want to fetch: ")
# fetch_stock_data_by_ticker(user_ticker)
