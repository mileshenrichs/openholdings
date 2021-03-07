import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .fetcher import IFetcher
from ..models import Holding
from ..utils.regex_util import is_ticker_symbol
from ..utils.string_conversion_util import (
    convert_percentage_string_to_float, 
    convert_comma_separated_integer_to_float,
    convert_dollars_string_to_float
)

class Vanguard(IFetcher):
    """A fetcher implementation for Vanguard funds.
    
    This fetcher requires the use of a headless Selenium browser due to the nature of Vanguard's
    holdings page.  The fetcher opens the page, then reads through all pages of the holdings table
    (30 holdings per page), exploring three different tabs: Stock, Bond, and Short-term reserve. 
    An unfortunate consequence of using Selenium and paging through potentially long tables is that
    the fetcher sometimes takes a considerable amount of time to scrape the holdings for a particular
    fund -- it may take anywhere from 10 seconds to over a minute for funds with thousands of holdings.

    Important note: since this fetcher relies on the Selenium automated browser, a Chrome driver executable
    must be installed on your machine and its path should be available in a 'CHROME_DRIVER_PATH' environment
    variable.  By default the browser will be configured to run headless.
    """

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(executable_path=os.environ['CHROME_DRIVER_PATH'], options=chrome_options)

    def fetch(self, ticker):
        self.driver.get(self.get_url_for_ticker(ticker))
        holdings = []
        try:
            # Make sure table tabs have loaded before trying to navigate the table
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.funds-tabsetBar'))
            )

            # Accumulate holdings across each asset class
            holdings.extend(self.read_stock_holdings())
            holdings.extend(self.read_bond_holdings())
            holdings.extend(self.read_cash_holdings())
        finally:
            self.driver.quit()
        return holdings

    def get_url_for_ticker(self, ticker):
        return 'https://investor.vanguard.com/etf/profile/portfolio/{}/portfolio-holdings'.format(ticker)

    def read_stock_holdings(self):
        """Page through "Stock" tab of the holdings table, collecting the fund's equities into a list.

        :returns: A list of Holding objects corresponding to the fund's equity holdings.
        """
        stock_holdings = []
        has_stock_holdings = self.switch_to_table_tab(0)
        if not has_stock_holdings:
            return stock_holdings
        table_data = self.read_table_into_2d_array()

        on_last_page_of_table = False
        while not on_last_page_of_table:
            for table_row in table_data:
                holding = Holding()
                holding_name, holding_ticker = self.parse_holding_name_and_ticker(table_row[0])
                holding.name = holding_name
                if is_ticker_symbol(holding_ticker):
                    holding.ticker = holding_ticker
                holding.percent_weighting = convert_percentage_string_to_float(table_row[3])
                holding.num_shares = convert_comma_separated_integer_to_float(table_row[4])
                holding.market_value_usd = convert_dollars_string_to_float(table_row[5])
                holding.asset_class = 'Stock'
                stock_holdings.append(holding)

            on_last_page_of_table = self.is_on_last_page_of_table()
            self.maybe_advance_table_page(on_last_page_of_table)
        return stock_holdings

    def read_bond_holdings(self):
        """Page through "Bond" tab of the holdings table, collecting the fund's bonds into a list.

        :returns: A list of Holding objects corresponding to the fund's bond holdings.
        """
        bond_holdings = []
        has_bond_holdings = self.switch_to_table_tab(1)
        if not has_bond_holdings:
            return bond_holdings
        table_data = self.read_table_into_2d_array()

        on_last_page_of_table = False
        while not on_last_page_of_table:
            for table_row in table_data:
                holding = Holding()
                holding_name, holding_ticker = self.parse_holding_name_and_ticker(table_row[0])
                holding.name = holding_name
                if is_ticker_symbol(holding_ticker):
                    holding.ticker = holding_ticker
                holding.percent_weighting = convert_percentage_string_to_float(table_row[6])
                holding.market_value_usd = convert_dollars_string_to_float(table_row[7])
                holding.asset_class = 'Bond'
                bond_holdings.append(holding)

            on_last_page_of_table = self.is_on_last_page_of_table()
            self.maybe_advance_table_page(on_last_page_of_table)
        return bond_holdings

    def read_cash_holdings(self):
        """Page through "Short-term reserves" tab of the holdings table, collecting the fund's reserves into a list.

        :returns: A list of Holding objects corresponding to the fund's cash holdings.
        """
        cash_holdings = []
        has_cash_holdings = self.switch_to_table_tab(2)
        if not has_cash_holdings:
            return cash_holdings
        table_data = self.read_table_into_2d_array()
        
        on_last_page_of_table = False
        while not on_last_page_of_table:
            for table_row in table_data:
                holding = Holding()
                holding_name, holding_ticker = self.parse_holding_name_and_ticker(table_row[0])
                holding.name = holding_name
                if is_ticker_symbol(holding_ticker):
                    holding.ticker = holding_ticker
                holding.percent_weighting = convert_percentage_string_to_float(table_row[4])
                holding.market_value_usd = convert_dollars_string_to_float(table_row[3])
                holding.asset_class = 'Cash'
                cash_holdings.append(holding)

            on_last_page_of_table = self.is_on_last_page_of_table()
            self.maybe_advance_table_page(on_last_page_of_table)
        return cash_holdings

    def switch_to_table_tab(self, tab_index):
        """Uses the webdriver to switch to a tab with the given index (i.e. "Stock" tab is index 0).

        :param tab_index: Integer index representing the tab to switch to.
        :returns: True if the fund has holdings of the switched-to tab type, False otherwise.
        """
        table_tab_bar_element = self.driver.find_element_by_css_selector('.funds-tabsetBar')
        tab_link_elements = table_tab_bar_element.find_elements_by_css_selector('li a')
        tab_link_elements[tab_index].click()

        # Table may be empty, otherwise wait for table to load
        try:
            time.sleep(.5)
            footnote_element = self.driver.find_element_by_css_selector('.summary-table-footnote')
            if footnote_element is not None and footnote_element.text == 'The fund includes no holdings of this type.':
                return False
        except NoSuchElementException:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.holdings-table.scrollingTableLeft'))
            )
            return True

    def is_on_last_page_of_table(self):
        table_pagination_text = self.driver.find_element_by_css_selector('.portfolio-pagination-links span:first-child').text
        pagination_split = table_pagination_text.split(' ')
        end_of_page_range = int(pagination_split[-3])
        total_holdings_count = int(pagination_split[-1])
        return end_of_page_range == total_holdings_count

    def read_table_into_2d_array(self):
        """Returns a 2D array populated with string values of a single page of a table's contents.

        For reasons beyond our understanding, Vanguard's holdings page markup actually has two <table> elements that
        seem to sit on top of one another.  The "left" table contains the first column of the table (name and ticker symbol)
        while the "right" table contains all the rest of the row's values.  This method abstracts this strange detail
        away from methods that are interested in the table's full contents.

        :returns: 2D array of strings representing the values of the holdings table currently displayed in the browser.
        """
        table = []
        # The stock names/tickers are populated in the "left" table, and the rest of the info is in the "right" table
        data_table_element_left = self.driver.find_element_by_css_selector('.holdings-table.scrollingTableLeft')
        data_table_element_right = self.driver.find_element_by_css_selector('.holdings-table.scrollingTableRight')
        table_row_elements_left = data_table_element_left.find_elements_by_css_selector('tr')
        table_row_elements_right = data_table_element_right.find_elements_by_css_selector('tr')

        for row_index in range(1, len(table_row_elements_right)):
            row_element_left = table_row_elements_left[row_index]
            row_element_right = table_row_elements_right[row_index]
            table_cell_elements_left = row_element_left.find_elements_by_css_selector('td span')
            table_cell_elements_right = row_element_right.find_elements_by_css_selector('td span')

            # Get the stock name from the "left" table
            table_row = [table_cell_elements_left[0].text]
            # Get the stock info (percent weighting, num shares, etc.) from the "right" table
            for i in range(1, len(table_cell_elements_right)):
                table_row.append(table_cell_elements_right[i].text)
            table.append(table_row)

        return table

    def maybe_advance_table_page(self, on_last_page_of_table):
        """Clicks the "Next" button below the table to move to the next page, if a next page exists.

        :param on_last_page_of_table: Boolean indicating whether the table is currently on its last page.
        """
        if not on_last_page_of_table:
            next_page_button_element = self.driver.find_element_by_css_selector('.portfolio-pagination-links span:last-child')
            next_page_button_element.click()

    def parse_holding_name_and_ticker(self, name_and_ticker):
        last_paren_index = name_and_ticker.rfind('(')
        holding_name = name_and_ticker[:last_paren_index]
        holding_ticker = name_and_ticker[last_paren_index + 1:-1]
        return (holding_name, holding_ticker)