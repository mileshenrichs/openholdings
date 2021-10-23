from datetime import date
from .holding import Holding

class Bond(Holding):
    """A holding in the form of a bond, some fixed income security such as a bill, note, or long-term loan."""

    def __init__(self, name):
        super().__init__(name)

        self.coupon_rate = None
        """The coupon rate of this bond."""

        self.rating = None
        """The rating of this bond."""

        self.effective_date = None
        """The date at which this bond was issued."""

        self.maturity_date = None
        """The future date when this bond will mature."""

        self.next_call_date = None
        """The next upcoming call date for the bond."""

        self.quantity_held = None
        """The quantity of this bond held by the fund."""

        self.sector = None
        """The sector to which the bond belongs."""

    def __repr__(self):
        effective_date_str, maturity_date_str = None, None
        if isinstance(self.effective_date, date):
            effective_date_str = self.effective_date.strftime('%m/%d/%Y')
        if isinstance(self.maturity_date, date):
            maturity_date_str = self.maturity_date.strftime('%m/%d/%Y')
        return (('<Bond{{name={}, percent_weighting={}, market_value={}, coupon_rate={}, effective_date={}, ' + 
            'maturity_date={}, sector={}}}>').format(self.name, self.percent_weighting, self.market_value, self.coupon_rate, 
            effective_date_str, maturity_date_str, self.sector))