class HoldingFieldBag:
    """A collection (or 'bag') of all Holding fields.

    An object of this type is created as an intermediate step in parsing individual ETF providers' holdings list documents,
    and based on the presence and value of certain fields, they are eventually copied into a concrete Holding instance
    (either an Equity, Bond, Future, or Cash object)."""

    def __init__(self):
        # Generic holding fields
        self.name = None
        self.identifier_cusip = None
        self.identifier_isin = None
        self.identifier_figi = None
        self.identifier_sedol = None
        self.percent_weighting = None
        self.market_value = None
        # Equity-specific fields
        self.ticker = None
        self.num_shares = None
        self.sector = None
        # Bond-specific fields
        self.coupon_rate = None
        self.rating = None
        self.effective_date = None
        self.maturity_date = None
        self.next_call_date = None
        # Future-specific fields
        self.contract_code = None
        self.contract_expiry_date = None
        # Bond and Future shared fields
        self.quantity_held = None
        # Cash-specific fields
        self.currency = None