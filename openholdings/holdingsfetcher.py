from .fetchers.vaneck import VanEck
from .fetchers.vanguard import Vanguard
from .fetchers.ishares import IShares

class HoldingsFetcher:
    def __init__(self, etf_ticker):
        self.etf_ticker = etf_ticker

    def fetch(self):
        return IShares().fetch(self.etf_ticker)