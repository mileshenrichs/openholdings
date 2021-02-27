def convert_percentage_string_to_float(percentage_string):
    """Converts a string of the form 'xx.xx%' to its equivalent decimal value.

    :param percentage_string: A string in percentage form to be converted.
    :returns: A floating-point number rounded to 4 decimal places (2 decimals in percentage form).
    """
    return round(float(percentage_string[:-1]) / 100, 4)

def convert_comma_separated_integer_to_int(comma_separated_number_string):
    """Converts a string of the form 'x,xxx,xxx' to its equivalent integer value.

    :param comma_separated_number_string: A string in comma-separated integer form to be converted.
    :returns: An integer representing the comma-separated number.
    """
    return int(comma_separated_number_string.replace(',', ''))

def convert_dollars_string_to_float(dollars_string):
    """Converts a string of the form '$x,xxx,xxx.xx' to its equivalent decimal value.

    :param dollars_string: A string in dollar and cents form to be converted.
    :returns: A floating-point number rounded to 2 decimal places.
    """
    return round(float(dollars_string.replace(',', '').replace('$', '')), 2)