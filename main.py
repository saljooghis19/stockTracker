import finnhub
import pandas as pd
import datetime
from config import API_KEY

finnhub_client = finnhub.Client(api_key=API_KEY)

class StockAnalyzer:
    def __init__(self, ticker_symbol, start_date, end_date):
        self.ticker_symbol = ticker_symbol
        self.start_date = start_date
        self.end_date = end_date
        self.start_date_format = datetime.datetime.strptime(start_date, "%m/%d/%Y")
        self.end_date_format = datetime.datetime.strptime(end_date, "%m/%d/%Y")
        self.start_unix_time = int(datetime.datetime.timestamp(self.start_date_format))
        self.end_unix_time = int(datetime.datetime.timestamp(self.end_date_format))

    def parse_date(self, date_str):
        if "/" in date_str:
            date_format = "%m/%d/%Y"
        else:
            date_format = "%Y-%m-%d"

        try:
            date_format_parsed = datetime.datetime.strptime(date_str, date_format)
        except ValueError:
            raise ValueError("Invalid date format. Please use either m/d/yyyy or yyyy-mm-dd.")

        return date_format_parsed

    def get_stock_news(self):
        start_date_format = self.parse_date(self.start_date).strftime("%Y-%m-%d")
        end_date_format = self.parse_date(self.end_date).strftime("%Y-%m-%d")
        news = finnhub_client.company_news(symbol=self.ticker_symbol, _from=start_date_format, to=end_date_format)
        return news

    def get_stock_data(self):
        data = pd.DataFrame(finnhub_client.stock_candles(
            symbol=f"{self.ticker_symbol}",
            resolution="D",
            _from=self.start_unix_time,
            to=self.end_unix_time,
            indicator="rsi",
            # indicator_fields={"timeperiod": 6},
        ))
        print(data)

    def average_stock(self):
        data = finnhub_client.stock_candles(
            symbol=f"{self.ticker_symbol}",
            resolution="D",
            _from=self.start_unix_time,
            to=self.end_unix_time
        )

        if 'c' not in data or not data['c']:
            return None
        closing_prices = data['c']
        average_price = sum(closing_prices) / len(closing_prices)

        return average_price

    def analyze(self):
        self.get_stock_data()
        avg_price = self.average_stock()

        if avg_price is not None:
            print(f"Average Stock Price for {self.ticker_symbol}: ${avg_price}")
        else:
            print(f"No data available for {self.ticker_symbol} within the specified date range.")

        show_news = input("Do you want to see the news for this stock? (yes/no): ").lower()

        if show_news == "yes":
            news = self.get_stock_news()
            if news and 'items' in news:
                print("Latest News for", self.ticker_symbol)
                for item in news['items']:
                    print(item['headline'])
                    print(item['url'])
            else:
                print(f"No news is available for {self.ticker_symbol}")
        else:
            print("News display is skipped.")

        export_data = input("Do you want to export the data to a CSV file? (yes/no): ").lower()

        if export_data == "yes":
            data_to_export = []
            # ... (loop and data export logic)

            csv_filename = f"{self.ticker_symbol}_data.csv"

            try:
                df = pd.DataFrame(data_to_export)
                df.to_csv(csv_filename, index=False)
                print(f"Data exported to {csv_filename} successfully.")
            except Exception as e:
                print(f"Error exporting data: {e}")
        else:
            print("Data export is skipped.")

# Main execution
user_ticker = input("Enter the stock ticker symbol: ").upper()
start_date = input("Enter your start date (format m/d/yyyy): ")
end_date = input("Enter your end date (format m/d/yyyy): ")

analyzer = StockAnalyzer(user_ticker, start_date, end_date)
analyzer.analyze()