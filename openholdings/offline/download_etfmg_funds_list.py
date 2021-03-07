"""
Stand-alone script that scrapes a list of all Blackrock iShares ETFs into a csv file saved locally within the same folder.

To run: python download_etfmg_funds_list.py
"""

import requests
from bs4 import BeautifulSoup
from utils.csv_writing import write_funds_to_csv

def main():
    funds = []
    etfmg_holdings_page_html = requests.get('https://etfmg.com/our-funds/', headers={'User-Agent': 'Mozilla/5.0'}).text
    soup = BeautifulSoup(etfmg_holdings_page_html, 'html.parser')
    fund_ticker_link_elements = soup.select('section.funds-listing td.ticker a')
    for fund_link_element in fund_ticker_link_elements:
        funds.append([fund_link_element.get_text(), fund_link_element['href']])

    write_funds_to_csv(funds, 'etfmg_funds.csv')

if __name__ == '__main__':
    main()