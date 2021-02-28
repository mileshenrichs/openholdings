class FundNotFoundException(Exception):
    """
    Thrown when the requested fund could not be found.

    This exception may occur as a result of:
        * Querying for a ticker of a fund that doesn't exist
        * A typo or misspelling of a fund ticker
        * Querying for a newly established fund that openholdings doesn't know about.
          For example, if Blackrock releases a new iShares fund, you may need to run
          the `/offline/download_ishares_funds_list.py` script to make openholdings
          aware of its existence.
    """
    pass