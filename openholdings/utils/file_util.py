import requests
import os

def download_holdings_file(holdings_file_url, file_extension, ticker):
    """Download a holdings list file (CSV, Excel, PDF, Json) from a URL and save it locally.

    :param holdings_file_url: The URL from which the holdings file can be downloaded.
    :param file_extension: The expected file type ('csv', 'xlsx', 'pdf', 'json').
    :param ticker: The fund ticker symbol to ensure a unique file name when saved.
    :returns: The filename of the downloaded holdings file.
    """
    r = requests.get(holdings_file_url, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True)
    filename = 'holdings-{}.{}'.format(ticker, file_extension)
    open(filename, 'wb').write(r.content)
    return filename

def delete_holdings_file(holdings_filename):
    """Deletes a downloaded holdings file from the local filesystem.

    :param holdings_filename: The name of the holdings file to delete.
    """
    os.remove(holdings_filename)