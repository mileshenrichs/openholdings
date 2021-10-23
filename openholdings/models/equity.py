from .holding import Holding

class Equity(Holding):
    """A holding in the form of an equity, stock held in a company."""

    def __init__(self, name):
        super().__init__(name)

        self.ticker = None
        """The ticker symbol for the equity."""

        self.num_shares = None
        """The number of shares the ETF holds of this equity."""

        self.sector = None
        """The sector to which the equity belongs."""

    def __repr__(self):
        return '<Equity{{name={}, cusip={}, isin={}, sedol={}, ticker={}, percent_weighting={}, market_value={}, num_shares={}, sector={}}}>'.format(self.name, 
            self.identifier_cusip, self.identifier_isin, self.identifier_sedol, self.ticker, self.percent_weighting, self.market_value, self.num_shares, self.sector)