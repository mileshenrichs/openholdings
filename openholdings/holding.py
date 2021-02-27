class Holding:
    """A single holding in a fund, typically either an equity or bond."""
    
    def __init__(self):
        self.ticker = None
        self.name = None
        self.num_shares = None
        self.asset_class = None
        self.market_value_usd = None
        self.percent_weighting = None

    def __repr__(self):
        return 'Holding{{ticker={}, name={}, weighting={}}}'.format(self.ticker, self.name, self.percent_weighting)