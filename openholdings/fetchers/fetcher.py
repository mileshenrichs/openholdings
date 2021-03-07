from abc import ABCMeta, abstractmethod

class IFetcher(metaclass=ABCMeta):
    """An interface that each fetcher must implement, containing a single fetch() method."""

    @abstractmethod
    def fetch(self, ticker):
        """Fetch a list of holdings for a given ticker that belongs to a given investment management firm.

        :param ticker: The ticker of a fund to retrieve holdings for.
        :returns: A list of Holdings (Equity, Bond, or Cash objects) that make up the ETF.
        """
        raise NotImplementedError