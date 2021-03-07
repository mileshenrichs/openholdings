import csv
from datetime import datetime
from .fetcher import IFetcher
from ..models.internal import HoldingFieldBag
from ..exceptions import FundNotFoundException
from ..utils.regex_util import is_ticker_symbol, is_cusip, is_percentage, is_sedol, is_isin, is_number
from ..utils.file_util import download_holdings_file, delete_holdings_file
from ..utils.string_conversion_util import (
    convert_percentage_string_to_float, 
    convert_comma_separated_integer_to_float, 
    convert_dollars_string_to_float,
    remove_ticker_suffix
)
from ..utils.holding_factory import create_holding

class Etfmg(IFetcher):
    """A fetcher implementation for ETFMG funds."""

    def fetch(self, ticker):
        holdings_field_bags = []

        # Download fund holdings CSV file
        fund_holdings_csv_url = self.get_url_for_ticker(ticker)
        downloaded_filename = download_holdings_file(fund_holdings_csv_url, 'csv', ticker)

        # Read holdings from CSV.  There are two different CSV formats (field names and order) that ETFMG provides,
        # so it's necessary to check which type the CSV is before trying to parse the holding details.
        with open(downloaded_filename, mode='r', encoding='utf-8') as funds_file:
            reader = csv.DictReader(funds_file)
            if self.is_holdings_file_in_stock_format(reader):
                holdings_field_bags = self.parse_holdings_stock_format(reader)
            elif self.is_holdings_file_in_bond_format(reader):
                holdings_field_bags = self.parse_holdings_bond_format(reader)

        # Delete holdings file after reading
        delete_holdings_file(downloaded_filename)

        # Convert holding field bags into concrete holding instances
        holdings = [create_holding(field_bag) for field_bag in holdings_field_bags]

        return holdings

    def get_url_for_ticker(self, ticker):
        return 'https://etfmg.com/holdings/{}_fund_holdings.csv'.format(ticker)

    def is_holdings_file_in_stock_format(self, reader):
        return 'StockTicker' in reader.fieldnames

    def is_holdings_file_in_bond_format(self, reader):
        return 'Coupon Rate' in reader.fieldnames

    def parse_holdings_stock_format(self, reader):
        field_bags = []
        for row in reader:
            field_bag = HoldingFieldBag()
            # Recognize whether holding is a bond by checking for presence of percent sign (coupon rate)
            if '%' in row['SecurityName']:
                field_bag.name = self.parse_name_from_bond_description(row['SecurityName'])
                field_bag.coupon_rate = self.parse_coupon_rate_from_bond_description(row['SecurityName'])
                maturity_date_str = self.parse_maturity_date_from_bond_description(row['SecurityName'])
                field_bag.maturity_date = datetime.strptime(maturity_date_str, '%m/%d/%Y')
            else:
                field_bag.name = row['SecurityName']
            
            # Sometimes the value in the "CUSIP" field is actually a SEDOL identifier
            if is_cusip(row['CUSIP']):
                field_bag.identifier_cusip = row['CUSIP']
            elif is_sedol(row['CUSIP']):
                field_bag.identifier_sedol = row['CUSIP']
            
            field_bag.percent_weighting = convert_percentage_string_to_float(row['Weightings'])
            field_bag.market_value = convert_comma_separated_integer_to_float(row['MarketValue'])

            if is_ticker_symbol(row['StockTicker']):
                field_bag.ticker = remove_ticker_suffix(row['StockTicker'])

            # Bond check
            if '%' in row['SecurityName']:
                field_bag.quantity_held = float(row['Shares'])
            else:
                field_bag.num_shares = float(row['Shares'])

            if row['CUSIP'] == 'Cash&Other':
                field_bag.currency = 'USD'

            field_bags.append(field_bag)
        return field_bags

    def parse_holdings_bond_format(self, reader):
        field_bags = []
        for row in reader:
            field_bag = HoldingFieldBag()
            field_bag.name = row['Security Description']

            if is_cusip(row['Security Cusip']):
                field_bag.identifier_cusip = row['Security Cusip']
            if is_isin(row['Security ISIN']):
                field_bag.identifier_isin = row['Security ISIN']
            if is_sedol(row['Security Sedol']):
                field_bag.identifier_sedol = row['Security Sedol']
            
            field_bag.percent_weighting = convert_percentage_string_to_float(row['% of Net Assets'])

            if is_number(row['Market Value Base']):
                field_bag.market_value = convert_comma_separated_integer_to_float(row['Market Value Base'])

            if is_ticker_symbol(row['Ticker Symbol']):
                field_bag.ticker = remove_ticker_suffix(row['Ticker Symbol'])

            if is_number(row['Shares/Par']):
                field_bag.num_shares = convert_comma_separated_integer_to_float(row['Shares/Par'])

            if field_bag.name == 'CASH AND OTHER REC PAY':
                field_bag.currency = row['Trading Currency']

            field_bags.append(field_bag)
        return field_bags

    def parse_name_from_bond_description(self, description):
        """ETFMG's bond ETFs list bond information (name, coupon rate, and maturity date) as
        a single field, i.e: 'HONEYWELL INTL INC 0.41138% 08/19/2022'.

        This and the following two methods parse out the respective bond fields.
        """
        desc_parts = description.split(' ')
        end_idx = 0
        while end_idx < len(desc_parts) and not is_percentage(desc_parts[end_idx]):
            end_idx += 1
        return ' '.join(desc_parts[:end_idx])

    def parse_coupon_rate_from_bond_description(self, description):
        desc_parts = description.split(' ')
        return convert_percentage_string_to_float(desc_parts[-2])

    def parse_maturity_date_from_bond_description(self, description):
        desc_parts = description.split(' ')
        return desc_parts[-1]