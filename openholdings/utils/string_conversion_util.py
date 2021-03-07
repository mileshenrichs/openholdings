import re

def convert_percentage_string_to_float(percentage_string):
    """Converts a string of the form 'xx.xx%' to its equivalent decimal value.

    :param percentage_string: A string in percentage form to be converted.
    :returns: A floating-point number rounded to 4 decimal places (2 decimals in percentage form).
    """
    return round(float(percentage_string.replace('%', '')) / 100, 4)

def convert_comma_separated_integer_to_float(comma_separated_number_string):
    """Converts a string of the form 'x,xxx,xxx' to its equivalent float value.

    :param comma_separated_number_string: A string in comma-separated float form to be converted.
    :returns: A float representing the comma-separated number.
    """
    return float(comma_separated_number_string.replace(',', ''))

def convert_dollars_string_to_float(dollars_string):
    """Converts a string of the form '$x,xxx,xxx.xx' to its equivalent decimal value.

    :param dollars_string: A string in dollar and cents form to be converted.
    :returns: A floating-point number rounded to 2 decimal places.
    """
    return round(float(dollars_string.replace(',', '').replace('$', '')), 2)

def remove_ticker_suffix(ticker):
    """Removes the tail of a ticker string starting at the first occurrence of a space character.

    :param ticker: A string in the form of a ticker symbol, i.e. 'GOOG', 'KO', '2914 JP'
    :returns: The ticker string with the suffix removed, i.e. 'GOOG', 'KO', '2914'
    """
    prefix = ticker.split(' ')[0]

    # Remove any trailing special characters that might be left behind
    while not re.match(r'^[0-9A-Z]$', prefix[-1]):
        prefix = prefix[:-1]
    
    return prefix