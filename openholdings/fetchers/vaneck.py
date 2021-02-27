from openpyxl import load_workbook
import requests
import shutil
import os
from .fetcher import IFetcher
from ..holding import Holding
from ..utils.regex_util import is_percentage, is_ticker_symbol
from ..utils.file_util import download_holdings_file, delete_holdings_file

class VanEck(IFetcher):
    """A fetcher implementation for VanEck funds."""

    def fetch(self, ticker):
        # Download holdings file (VanEck provides an Excel spreadsheet)
        spreadsheet_url = self.get_url_for_ticker(ticker)
        downloaded_filename = download_holdings_file(spreadsheet_url, 'xlsx', ticker)

        # Parse holdings list from downloaded spreadsheet
        wb = load_workbook(filename=downloaded_filename, read_only=True)
        sheet = wb.active
        holdings = self.parse_holdings_from_spreadsheet(sheet)

        # Clean up and return holdings list
        wb.close()
        delete_holdings_file(downloaded_filename)
        return holdings

    def get_url_for_ticker(self, ticker):
        return 'https://www.vaneck.com/etf/equity/{}/holdings/download/xlsx/'.format(ticker.lower())

    def parse_holdings_from_spreadsheet(self, sheet):
        """Read holdings spreadsheet into Holding objects.

        :param sheet: An openpyxl Worksheet to read holdings from.
        :returns: A list of Holdings read from the spreadsheet.
        """
        holdings = []

        for row in sheet.rows:
            if row[7].value is not None and is_percentage(row[7].value):
                holding = Holding()
                ticker = row[1].value.split(' ')[0]
                if is_ticker_symbol(ticker):
                    holding.ticker = ticker
                holding.name = row[2].value
                if row[4].value is not None:
                    holding.num_shares = int(row[4].value.replace(',', ''))
                holding.asset_class = row[5].value
                holding.market_value_usd = round(float(row[6].value.replace(',', '').replace('$', '')), 2)
                holding.percent_weighting = round(float(row[7].value[:-1]) / 100, 4)
                holdings.append(holding)
        
        return holdings