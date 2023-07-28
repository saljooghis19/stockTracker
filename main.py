import finnhub
import pandas as pd
import datetime
# import matplotlib.pyplot as plt
import mplfinance as mpf

finnhub_client = finnhub.Client(api_key="ciu35ihr01qkv67u3jdgciu35ihr01qkv67u3je0")


def parse_date(date_str):
    # Check if the input matches m/d/yyyy format, if it does it converts it into yyyy/mm/dd
    if "/" in date_str:
        date_format = "%m/%d/%Y"
    else:
        date_format = "%Y-%m-%d"

    try:
        date_format_parsed = datetime.datetime.strptime(date_str, date_format)
    except ValueError:
        raise ValueError("Invalid date format. Please use either m/d/yyyy or yyyy-mm-dd.")

    return date_format_parsed


def get_stock_news(ticker_symbol, start_date, end_date):
    start_date_format = parse_date(start_date).strftime("%Y-%m-%d")
    end_date_format = parse_date(end_date).strftime("%Y-%m-%d")
    news = finnhub_client.company_news(symbol=ticker_symbol, _from=start_date_format, to=end_date_format)
    return news



def get_stock_data(ticker_symbol, start_unix_time, end_unix_time):
    data = pd.DataFrame(finnhub_client.stock_candles(
        symbol=f"{ticker_symbol}",
        resolution="D",
        _from=start_unix_time,
        to=end_unix_time,
        indicator="rsi",
        # indicator_fields={"timeperiod": 6},
        
    ))
    print(data)

def averageStock(ticker_symbol, start_unix_time, end_unix_time):
    data = finnhub_client.stock_candles(
        symbol=f"{ticker_symbol}",
        resolution="D",
        _from=start_unix_time,
        to=end_unix_time
    )

    if 'c' not in data or not data['c']:
        return None or 0
    closing_prices = data['c']
    average_price = sum(closing_prices) / len(closing_prices)
    
    return average_price
    

  


# Convert UNIX timestamp to datetime with the user input date we get
user_ticker = input("Enter the stock ticker symbol: ").upper() 
start_date = input("Enter your start date (format m/d/yyyy): ")
end_date = input("Enter your end date (format m/d/yyyy): ")
start_date_format = datetime.datetime.strptime(start_date, "%m/%d/%Y")
end_date_format = datetime.datetime.strptime(end_date, "%m/%d/%Y")
start_unix_time = int(datetime.datetime.timestamp(start_date_format))
end_unix_time = int(datetime.datetime.timestamp(end_date_format))

get_stock_data(user_ticker, start_unix_time, end_unix_time)

avg_price = averageStock(user_ticker, start_unix_time, end_unix_time)

# Check if the result is not None before printing
if avg_price is not None:
    print(f"Average Stock Price for {user_ticker}: ${avg_price}")
else:
    print(f"No data available for {user_ticker} within the specified date range.")

news = get_stock_news(user_ticker, start_date, end_date)

if news and 'items' in news:
    print("Latest News for", user_ticker)
    for item in news['items']:
        print(item['headline'])
        print(item['url'])
        print("------")
else:
    print(f"No news is available for {user_ticker}")

# ---------------------------------------------------------



  
    # turn the data we get from the stock and convert it into cleaner look using DataFrame which is passed on from data
    # df = pd.DataFrame(data)
    # df['t'] = pd.to_datetime(df['t'], unit='s')  
    # df.rename(columns={'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'Close'}, inplace=True)  # mplfinance cant read o, h, l, c -> rename it to Open, High, etc...
    # df.set_index('t', inplace=True) #pass the parameter t which reads column named t in the DataFrame, setting it to true makes the apply work correctly without ommiting format

    # mpf.plot(df, type='candle', title=f'{ticker_symbol} Daily Candlestick Chart')

    # plt.figure(figsize=(12, 6))
    # plt.plot(df['t'], df['c'], label='Closing price', color='blue')
    # plt.xlabel('Date')
    # plt.ylabel('Price')
    # plt.title(f'{ticker_symbol} RSI Analysis')
    # plt.legend()
    # plt.grid(True)
    # plt.show()






# -----------------------------------------------------

# import finnhub
# import requests
# import pandas as pd
# import datetime

# finnhub_client = finnhub.Client(api_key="ciu35ihr01qkv67u3jdgciu35ihr01qkv67u3je0")


# def get_stock_data(ticker_symbol, start_unix_time, end_unix_time):
#     print(pd.DataFrame(finnhub_client.technical_indicator(
#     symbol=f"{ticker_symbol}",
#     resolution="D",
#     _from={start_unix_time}, #user input from start_date
#     to={end_unix_time},   #user input from end_date
#     indicator="rsi",
#     # indicator_fields={"timeperiod": 6},
# )))


# user_ticker = input("Enter the stock ticker symbol: ").upper()

# start_date = input("enter your start date: (format m/d/yyyy)")       
# end_date = input("enter your end date: ")
# start_date_format = datetime.datetime.strptime(start_date, "%m/%d/%Y")
# end_date_format = datetime.datetime.strptime(end_date, "%m/%d/%Y")
# start_unix_time = int(datetime.datetime.timestamp(start_date_format))
# end_unix_time = int(datetime.datetime.timestamp(end_date_format))
# # print(int(start_unix_time))
# # print(int(end_unix_time))

# get_stock_data(user_ticker, start_unix_time, end_unix_time)






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

