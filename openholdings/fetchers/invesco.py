import csv
from .fetcher import IFetcher
from ..models import Holding
from ..utils.regex_util import is_ticker_symbol
from ..utils.file_util import download_holdings_file, delete_holdings_file
from ..utils.string_conversion_util import (
    convert_percentage_string_to_float, 
    convert_comma_separated_integer_to_float, 
    convert_dollars_string_to_float
)

class Invesco(IFetcher):
    """A fetcher implementation for Invesco funds."""

    def fetch(self, ticker):
        # Download holdings CSV file
        fund_holdings_csv_url = self.get_url_for_ticker(ticker)
        downloaded_filename = download_holdings_file(fund_holdings_csv_url, 'csv', ticker)

        # Parse holdings list from downloaded CSV
        holdings = []
        with open(downloaded_filename, mode='r', encoding='utf-8') as holdings_file:
            reader = csv.DictReader(holdings_file)
            for row in reader:
                holding = Holding()
                ticker = row['Holding Ticker'].split(' ')[0]
                if is_ticker_symbol(ticker):
                    holding.ticker = ticker
                holding.name = row['Name']
                holding.num_shares = convert_comma_separated_integer_to_float(row['Shares/Par Value'])
                holding.asset_class = 'Equity' if 'cash' not in holding.name.lower() else 'Cash'
                holding.market_value_usd = convert_dollars_string_to_float(row['MarketValue'])
                holding.percent_weighting = convert_percentage_string_to_float(row['Weight'])
                holdings.append(holding)

        # Delete holdings file after reading
        delete_holdings_file(downloaded_filename)
        return holdings

    def get_url_for_ticker(self, ticker):
        u = 'https://www.invesco.com/us/financial-products/etfs/holdings/main/holdings/0?audienceType=Investor&action=download&ticker={}'
        return u.format(ticker)