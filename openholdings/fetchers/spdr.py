from openpyxl import load_workbook
from .fetcher import IFetcher
from ..holding import Holding
from ..utils.regex_util import is_ticker_symbol
from ..utils.file_util import download_holdings_file, delete_holdings_file
from ..utils.string_conversion_util import convert_percentage_string_to_float

class Spdr(IFetcher):
    """A fetcher implementation for State Street SPDR funds."""

    def fetch(self, ticker):
        # Download fund holdings spreadsheet file
        fund_holdings_spreadsheet_url = self.get_url_for_ticker(ticker)
        downloaded_filename = download_holdings_file(fund_holdings_spreadsheet_url, 'xlsx', ticker)

        # Parse holdings list from downloaded spreadsheet
        wb = load_workbook(filename=downloaded_filename)
        sheet = wb.active
        holdings = self.parse_holdings_from_spreadsheet(sheet)

        # Delete holdings file after reading
        wb.close()
        delete_holdings_file(downloaded_filename)
        return holdings

    def get_url_for_ticker(self, ticker):
        u = 'https://www.ssga.com/us/en/institutional/etfs/library-content/products/fund-data/etfs/us/holdings-daily-us-en-{}.xlsx'
        return u.format(ticker.lower())

    def parse_holdings_from_spreadsheet(self, sheet):
        """Read holdings spreadsheet into Holding objects.

        :param sheet: An openpyxl Worksheet to read holdings from.
        :returns: A list of Holdings read from the spreadsheet.
        """
        holdings = []

        current_row_index = 0
        for row in sheet.rows:
            current_row_index += 1
            # Skip first 5 rows, table starts on row 6
            if current_row_index < 6:
                continue
            # Once we've started reading the table, every row should start with the name of a holding.
            # Upon hitting a blank row, we know we've read through the entire table and can stop.
            if row[0].value is None:
                break

            holding = Holding()
            ticker = row[1].value.split(' ')[0]
            if is_ticker_symbol(ticker):
                holding.ticker = ticker
            holding.name = row[0].value
            if ticker != 'CASH_USD':
                holding.num_shares = int(row[6].value[:-4])
            holding.asset_class = 'Equity' if ticker != 'CASH_USD' and 'INSTITUTIONAL LIQ' not in holding.name else 'Cash'
            holding.percent_weighting = convert_percentage_string_to_float(row[4].value)
            holdings.append(holding)
        
        return holdings