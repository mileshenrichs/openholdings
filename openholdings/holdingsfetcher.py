from .fetchers.vaneck import VanEck
from .fetchers.vanguard import Vanguard

class HoldingsFetcher:
    def __init__(self, etf_ticker):
        self.etf_ticker = etf_ticker

    def fetch(self):
        return Vanguard().fetch(self.etf_ticker)