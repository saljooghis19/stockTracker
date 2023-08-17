import finnhub
import pandas as pd
import datetime
from config import API_KEY
# import matplotlib.pyplot as plt
import mplfinance as mpf

finnhub_client = finnhub.Client(api_key=API_KEY)

stock_data = pd.DataFrame()


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

# Ask if the user wants to see the news
show_news = input("Do you want to see the news for this stock? (yes/no): ").lower()

# Get news using the correctly formatted dates, only if the user wants to see it
if show_news == "yes":
    news = get_stock_news(user_ticker, start_date_format.strftime("%Y-%m-%d"), end_date_format.strftime("%Y-%m-%d"))

    if news and 'items' in news:
        print("Latest News for", user_ticker)
        for item in news['items']:
            print(item['headline'])
            print(item['url'])
            
    else:
        print(f"No news is available for {user_ticker}")
else:
    print("News display is skipped.")

# Ask if the user wants to export the data
export_data = input("Do you want to export the data to a CSV file? (yes/no): ").lower()

if export_data == "yes":
    # Create a list of dictionaries with the data you want to export, currently not working. need to fix line 109 as it is not retrieving data
    data_to_export = []

    for index, row in stock_data.iterrows():
        data_entry = {
            "Date": datetime.datetime.fromtimestamp(row['t']).strftime("%Y-%m-%d"),
            "Open": row['o'],
            
        }
        data_to_export.append(data_entry)
    
    print(data_to_export)

    # Specify the filename for the CSV file from the ticker selected
    csv_filename = f"{user_ticker}_data.csv"

    # Export the data to the CSV file
    try:
        df = pd.DataFrame(data_to_export)
        df.to_csv(csv_filename, index=False)
        print(f"Data exported to {csv_filename} successfully.")
    except Exception as e:
        print(f"Error exporting data: {e}")
else:
    print("Data export is skipped.")


