class Holding:
    """A single holding in a fund.  Subclasses of Holding include Equity, Bond, and Cash."""
    
    def __init__(self, name):
        self.name = name
        """The name of the security."""

        self.identifier_cusip = None
        """The CUSIP identifier for the security, if available and applicable."""

        self.identifier_isin = None
        """The ISIN identifier for the security, if available and applicable."""

        self.identifier_figi = None
        """The FIGI identifier for the security, if available and applicable."""

        self.identifier_sedol = None
        """The SEDOL identifier for the security, if available and applicable."""

        self.percent_weighting = None
        """The percentage of the fund's resources that are contributed to this holding."""

        self.market_value = None
        """The total market value of this holding.  In almost all cases this will be in US Dollars unless 
        otherwise indicated by the Cash object's currency field."""