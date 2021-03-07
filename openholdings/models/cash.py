from .holding import Holding

class Cash(Holding):
    """A holding in the form of cash or an otherwise highly liquid account."""

    def __init__(self, name):
        super().__init__(name)

        self.currency = 'USD'
        """The currency of this cash holding."""

    def __repr__(self):
        return '<Cash{{name={}, percent_weighting={}, market_value={}, currency={}}}>'.format(self.name, 
            self.percent_weighting, self.market_value, self.currency)