from .holding import Holding

class Future(Holding):
    """A holding in the form of a futures contract, likely for a currency or a commodity."""

    def __init__(self, name):
        super().__init__(name)

        self.contract_code = None
        """A four- or five-character code uniquely identifying the futures contract."""

        self.contract_expiry_date = None
        """The date at which this futures contract expires."""

        self.quantity_held = None
        """The number of futures contracts of this type that are held."""

    def __repr__(self):
        return '<Future{{name={}, percent_weighting={}, market_value={}, contract_code={}, expiry_date={}}}>'.format(self.name, 
            self.percent_weighting, self.market_value_usd, self.contract_code, self.contract_expiry_date)