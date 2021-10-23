import os
import csv
import json
from os.path import abspath
from datetime import date, datetime
from .fetcher import IFetcher
from ..models.internal import HoldingFieldBag
from ..models import Holding
from ..exceptions import FundNotFoundException
from ..utils.file_util import download_holdings_file, delete_holdings_file
from ..utils.regex_util import is_ticker_symbol, is_cusip, is_percentage, is_sedol, is_isin, is_number
from ..utils.holding_factory import create_holding

class IShares(IFetcher):
    """A fetcher implementation for Blackrock iShares funds."""

    def fetch(self, ticker):
        holdings_field_bags = []

        # Download fund holdings JSON file
        fund_details_url = self.get_url_for_ticker(ticker)
        fund_holdings_json_url = fund_details_url + '/1467271812596.ajax?tab=all&fileType=json'
        downloaded_filename = download_holdings_file(fund_holdings_json_url, 'json', ticker)

        # Read holdings from JSON
        with open(downloaded_filename, 'r', encoding='utf-8') as holdings_file:
            file_contents = holdings_file.read().encode().decode('utf-8-sig')
            holdings_obj = json.loads(file_contents)
            holdings_arr = holdings_obj['aaData']
            if self.is_holdings_file_in_stock_format(holdings_arr):
                holdings_field_bags = self.parse_holdings_stock_format(holdings_arr)
            elif self.is_holdings_file_in_bond_format(holdings_arr):
                holdings_field_bags = self.parse_holdings_bond_format(holdings_arr)
            elif self.is_holdings_file_in_commodities_format(holdings_arr):
                holdings_field_bags = self.parse_holdings_commodities_format(holdings_arr)

        # Delete holdings file after reading
        delete_holdings_file(downloaded_filename)

        # Convert holding field bags into concrete holding instances
        holdings = [create_holding(field_bag) for field_bag in holdings_field_bags]

        return holdings

    def get_url_for_ticker(self, ticker):
        """Reads ticker-URL pairs from iShares funds list CSV file to find the URL for a given ticker.

        iShares' website is unique in that the URLs for ETF detail pages aren't a pure function of the ETF's ticker
        symbol.  The mappings of ETF ticker -> details page URL are located in a locally saved CSV file which is
        read from in order to determine the correct URL.

        :param ticker: The ticker of the fund to fetch holdings for.
        :returns: A string URL pointing to the details page for the given fund.
        :raises FundNotFoundException: If no record for the ticker exists in the iShares funds list CSV file.
        """
        current_directory = os.path.dirname(os.path.realpath(__file__))
        funds_csv_file_path = abspath(os.path.join(current_directory, '..', 'offline', 'ishares_funds.csv'))
        with open(funds_csv_file_path, mode='r', encoding='utf-8') as funds_file:
            reader = csv.reader(funds_file)
            for fund in reader:
                if fund[0] == ticker:
                    return fund[1]
        raise FundNotFoundException(ticker)

    def is_holdings_file_in_stock_format(self, holdings_arr):
        return len(holdings_arr[0]) == 18

    def is_holdings_file_in_bond_format(self, holdings_arr):
        return len(holdings_arr[0]) == 27

    def is_holdings_file_in_commodities_format(self, holdings_arr):
        return len(holdings_arr[0]) == 26

    def parse_holdings_stock_format(self, holdings_arr):
        field_bags = []
        for holding_arr in holdings_arr:
            field_bag = HoldingFieldBag()
            field_bag.name = holding_arr[1]

            if is_cusip(holding_arr[8]):
                field_bag.identifier_cusip = holding_arr[8]
            if is_isin(holding_arr[9]):
                field_bag.identifier_isin = holding_arr[9]
            if is_sedol(holding_arr[10]):
                field_bag.identifier_sedol = holding_arr[10]

            field_bag.percent_weighting = round(holding_arr[5]['raw'] / 100, 4)
            field_bag.market_value = holding_arr[6]['raw']

            if is_ticker_symbol(holding_arr[0]):
                field_bag.ticker = holding_arr[0]

            field_bag.num_shares = float(holding_arr[7]['raw'])

            if holding_arr[2] != '-':
                field_bag.sector = holding_arr[2]

            if holding_arr[3] in ('Money Market', 'Cash', 'Cash Collateral and Margins'):
                field_bag.currency = 'USD'
            elif holding_arr[3] == 'Futures':
                field_bag.contract_code = holding_arr[0]
                future_expiration_date = self.parse_future_expiration_date_from_description(holding_arr[1])
                if isinstance(future_expiration_date, date):
                    field_bag.contract_expiry_date = future_expiration_date
                field_bag.quantity_held = float(holding_arr[7]['raw'])

            field_bags.append(field_bag)
        return field_bags

    def parse_holdings_bond_format(self, holdings_arr):
        field_bags = []
        for holding_arr in holdings_arr:
            field_bag = HoldingFieldBag()
            field_bag.name = holding_arr[0]

            if is_cusip(holding_arr[7]):
                field_bag.identifier_cusip = holding_arr[7]
            if is_isin(holding_arr[8]):
                field_bag.identifier_isin = holding_arr[8]
            if is_sedol(holding_arr[9]):
                field_bag.identifier_sedol = holding_arr[9]

            field_bag.percent_weighting = round(holding_arr[4]['raw'] / 100, 4)
            field_bag.market_value = holding_arr[5]['raw']

            if holding_arr[17]['display'] != '-': # If there is a maturity date
                field_bag.coupon_rate = round(holding_arr[18]['raw'] / 100, 4)
                field_bag.effective_date = datetime.strptime(holding_arr[25], '%b %d, %Y')
                field_bag.maturity_date = datetime.strptime(holding_arr[17]['display'], '%b %d, %Y')
                if holding_arr[1] != '-':
                    field_bag.sector = holding_arr[1]
            else:
                field_bag.currency = 'USD'

            field_bags.append(field_bag)
        return field_bags

    def parse_holdings_commodities_format(self, holdings_arr):
        field_bags = []
        for holding_arr in holdings_arr:
            field_bag = HoldingFieldBag()
            field_bag.name = holding_arr[0]

            if is_cusip(holding_arr[7]):
                field_bag.identifier_cusip = holding_arr[7]
            if is_isin(holding_arr[8]):
                field_bag.identifier_isin = holding_arr[8]
            if is_sedol(holding_arr[9]):
                field_bag.identifier_sedol = holding_arr[9]

            field_bag.percent_weighting = round(holding_arr[4]['raw'] / 100, 4)
            field_bag.market_value = holding_arr[5]['raw']

            if holding_arr[17]['display'] != '-': # If there is a maturity date
                if holding_arr[2] == 'Futures':
                    field_bag.contract_expiry_date = datetime.strptime(holding_arr[17]['display'], '%b %d, %Y')
                else:
                    field_bag.effective_date = datetime.strptime(holding_arr[24], '%b %d, %Y')
                    field_bag.maturity_date = datetime.strptime(holding_arr[17]['display'], '%b %d, %Y')
                    if holding_arr[1] != '-':
                        field_bag.sector = holding_arr[1]
            else:
                field_bag.currency = 'USD'

            field_bags.append(field_bag)
        return field_bags

    def parse_future_expiration_date_from_description(self, description):
        date_suffix = ' '.join(description.split(' ')[-2:])
        expiration_date = datetime.strptime(date_suffix, '%b %y')
        return expiration_date
