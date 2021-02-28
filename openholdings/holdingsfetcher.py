from .fetchers.vaneck import VanEck
from .fetchers.vanguard import Vanguard
from .fetchers.ishares import IShares
from .fetchers.etfmg import Etfmg

class HoldingsFetcher:
    def __init__(self, etf_ticker):
        self.etf_ticker = etf_ticker

    def fetch(self):
        return Etfmg().fetch(self.etf_ticker)