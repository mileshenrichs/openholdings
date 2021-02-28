import os
import csv
from os.path import abspath
from .fetcher import IFetcher
from ..holding import Holding
from ..exceptions import FundNotFoundException
from ..utils.regex_util import is_ticker_symbol
from ..utils.file_util import download_holdings_file, delete_holdings_file
from ..utils.string_conversion_util import (
    convert_percentage_string_to_float, 
    convert_comma_separated_integer_to_int, 
    convert_dollars_string_to_float
)

class Etfmg(IFetcher):
    """A fetcher implementation for ETFMG funds."""

    def fetch(self, ticker):
        holdings = []

        # Download fund holdings CSV file
        fund_holdings_csv_url = self.get_url_for_ticker(ticker)
        downloaded_filename = download_holdings_file(fund_holdings_csv_url, 'csv', ticker)

        # Read holdings from CSV.  There are two different CSV formats (field names and order) that ETFMG provides,
        # so it's necessary to check which type the CSV is before trying to parse the holding details.
        with open(downloaded_filename, mode='r', encoding='utf-8') as funds_file:
            reader = csv.DictReader(funds_file)
            holdings_table_is_type_1 = 'StockTicker' in reader.fieldnames
            for row in reader:
                holding = None
                if holdings_table_is_type_1:
                    holding = self.parse_holding_from_csv_type_1(row)
                else:
                    holding = self.parse_holding_from_csv_type_2(row)
                holdings.append(holding)

        # Delete holdings file after reading
        delete_holdings_file(downloaded_filename)

        return holdings

    def get_url_for_ticker(self, ticker):
        return 'https://etfmg.com/holdings/{}_fund_holdings.csv'.format(ticker)

    def parse_holding_from_csv_type_1(self, row):
        holding = Holding()
        ticker = row['StockTicker'].split(' ')[0]
        if is_ticker_symbol(ticker):
            holding.ticker = ticker
        holding.name = row['SecurityName']
        holding.percent_weighting = convert_percentage_string_to_float(row['Weightings'])
        if holding.name != 'Cash & Other':
            holding.num_shares = int(row['Shares'][:-3])
        holding.asset_class = 'Equity' if 'Cash' not in row['SecurityName'] else 'Cash'
        market_value = row['MarketValue'].strip()
        if market_value != '-':
            holding.market_value_usd = convert_dollars_string_to_float(market_value)
        return holding

    def parse_holding_from_csv_type_2(self, row):
        holding = Holding()
        ticker = row['Ticker Symbol'].split(' ')[0]
        if is_ticker_symbol(ticker):
            holding.ticker = ticker
        holding.name = row['Security Description']
        holding.percent_weighting = convert_percentage_string_to_float(row['% of Net Assets'])
        holding.num_shares = convert_comma_separated_integer_to_int(row['Shares/Par'].strip()[:-5])
        holding.asset_class = row['Segment Classification']
        market_value = row['Market Value Base'].strip()
        if market_value != '-':
            holding.market_value_usd = convert_dollars_string_to_float(market_value)
        return holding