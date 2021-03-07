"""
Stand-alone script that scrapes a list of all Blackrock iShares ETFs into a csv file saved locally within the same folder.
This scraping is necessary because iShares' ETF details page URLs aren't a function of the ticker symbol but instead
are composed of unique fund IDs and a dash-cased long fund name.

Example URL: https://www.ishares.com/us/products/315979/ishares-virtual-work-and-life-multisector-etf
The ETF's ticker symbol is 'IWFH', but it doesn't appear in the URL.

This script is only ever run manually with the command `python download_ishares_funds_list.py`, but this is only needed
when Blackrock changes their ETF offerings, either by adding, removing, or renaming one or more of their funds.
Although this script isn't used during the fetching of ETF holdings, the `ishares_funds.csv` file it outputs is
used by the iShares fetcher.
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.csv_writing import write_funds_to_csv

def main():
    chrome_options = Options()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path=os.environ['CHROME_DRIVER_PATH'], options=chrome_options)

    funds = []
    try:
        print('Opening Selenium Webdriver...')
        driver.set_window_size(1600, 800)
        driver.get('https://www.ishares.com/us/products/etf-investments')
        show_all_button_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.show-more-or-less button'))
        )
        driver.execute_script('arguments[0].click();', show_all_button_element)

        print('Reading from funds table...')
        table_row_elements = driver.find_elements_by_css_selector('tr.desktop-table-row')
        for table_row_element in table_row_elements:
            fund_link_element = table_row_element.find_element_by_css_selector('a.tb_fundNames')
            ticker_span_element = fund_link_element.find_element_by_css_selector('.localExchangeTicker')
            ticker = ticker_span_element.text
            fund_url = fund_link_element.get_attribute('href')
            funds.append([ticker, fund_url])
    finally:
        driver.quit()

    print('Writing fund ticker symbols and URLs to csv file...')
    write_funds_to_csv(funds, 'ishares_funds.csv')
    print('Done!')

if __name__ == '__main__':
    main()