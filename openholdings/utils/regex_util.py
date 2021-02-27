import re

def is_percentage(value):
    """Checks whether a string is a percentage (i.e. 1.50%, 13.00%, .85%).

    :param value: A string to evaluate.
    :returns: True if string is in the form of a percentage value.
    """
    return re.match(r'-?\d*.\d+%', value)

def is_ticker_symbol(value):
    """Checks whether a string is a possibly valid stock ticker symbol.

    :param value: A string to evaluate.
    :returns: True if string is in the form of a valid stock ticker symbol.
    """
    return re.match(r'[A-Z]{1,6}', value)