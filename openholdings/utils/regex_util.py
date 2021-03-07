import re

def is_percentage(value):
    """Checks whether a string is a percentage (i.e. 1.50%, 13.00%, .85%).

    :param value: A string to evaluate.
    :returns: True if string is in the form of a percentage value.
    """
    return re.match(r'-?\d*(.\d+)?%', value)

def is_ticker_symbol(value):
    """Checks whether a string is a possibly valid stock ticker symbol.

    Examples: 'GOOG', 'BRK/B', '263750 KS', 'EMBRAC B SS'

    :param value: A string to evaluate.
    :returns: True if string is in the form of a valid stock ticker symbol.
    """
    return re.match(r'^[A-Z0-9/]{1,7}(\s+[ABC])?(\s+[A-Z]{1,3})?$', value)

def is_cusip(value):
    """Checks whether a string is a valid CUSIP identifier.

    Regex from here: https://regex101.com/r/vN3tE5/1

    :param value: A string to evaluate.
    :returns: True if string is in the form of a valid CUSIP number."""
    return re.match(r'^([\w\d]{6})([\w\d]{2})([\w\d]{1})$', value)

def is_sedol(value):
    """Checks whether a string is a valid SEDOL identifier.

    Regex from here: https://en.wikipedia.org/wiki/SEDOL

    :param value: A string to evaluate.
    :returns: True if string is in the form of a valid SEDOL identifier."""
    return re.match(r'^[0-9BCDFGHJKLMNPQRSTVWXYZ]{6}\d$', value)

def is_isin(value):
    """Checks whether a string is an ISIN identifier.

    :param value: A string to evaluate.
    :returns: True if string is in the form of a valid ISIN identifier."""
    return True

def is_number(value):
    """Checks whether a string is a floating point number.

    This method checks whether a string is a floating point number by first removing any commas
    then attempting to cast the string to a float. If the cast fails, then return false.

    :param value: A string to evaluate.
    :returns: True if the string can be cast to a floating point number."""
    try:
        float(value.replace(',', ''))
    except ValueError:
        return False
    return True
