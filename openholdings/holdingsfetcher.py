from .fetchers.vaneck import VanEck

class HoldingsFetcher:
    def __init__(self, etf_ticker):
        self.etf_ticker = etf_ticker

    def fetch(self):
        return VanEck().fetch(self.etf_ticker)