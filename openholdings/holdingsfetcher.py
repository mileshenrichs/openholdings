from .fetchers.vaneck import VanEck
from .fetchers.vanguard import Vanguard
from .fetchers.ishares import IShares
from .fetchers.etfmg import Etfmg
from .fetchers.spdr import Spdr

class HoldingsFetcher:
    def __init__(self, etf_ticker):
        self.etf_ticker = etf_ticker

    def fetch(self):
        return Spdr().fetch(self.etf_ticker)