import os
import csv
import json
from os.path import abspath
from .fetcher import IFetcher
from ..holding import Holding
from ..exceptions import FundNotFoundException
from ..utils.file_util import download_holdings_file, delete_holdings_file

class IShares(IFetcher):
    """A fetcher implementation for Blackrock iShares funds."""

    def fetch(self, ticker):
        holdings = []

        # Download fund holdings JSON file
        fund_details_url = self.get_url_for_ticker(ticker)
        fund_holdings_json_url = fund_details_url + '/1467271812596.ajax?tab=all&fileType=json'
        downloaded_filename = download_holdings_file(fund_holdings_json_url, 'json', ticker)

        # Read holdings from JSON
        with open(downloaded_filename, 'r', encoding='utf-8') as holdings_file:
            file_contents = holdings_file.read().encode().decode('utf-8-sig')
            holdings_obj = json.loads(file_contents)
            holdings_arr = holdings_obj['aaData']
            for holding_arr in holdings_arr:
                holding = Holding()
                holding.ticker = holding_arr[0]
                holding.name = holding_arr[1]
                holding.asset_class = holding_arr[3]
                holding.market_value_usd = holding_arr[4]['raw']
                holding.percent_weighting = round(holding_arr[5]['raw'] / 100, 4)
                holding.num_shares = holding_arr[7]['raw']
                holdings.append(holding)

        # Delete holdings file after reading
        delete_holdings_file(downloaded_filename)

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