"""
The "holding factory" converts a HoldingFieldBag object, which contains the union of the fields of each 
holding type, to an instance of the appropriate Holding subclass (either Equity, Bond, Future, or Cash).

It does so through the create_holding() function, which accepts a HoldingFieldBag object and returns a Holding subclass.
"""

from ..models import Equity, Bond, Future, Cash

# Fields of the Holding superclass that all subclasses inherit
COMMON_HOLDING_FIELDS = ['identifier_cusip', 'identifier_isin', 'identifier_figi', 'identifier_sedol', 'percent_weighting', 'market_value']

def copy_over_fields(source_obj, destination_obj, fields_to_copy):
    for field in fields_to_copy:
        setattr(destination_obj, field, getattr(source_obj, field))

def is_cash(field_bag):
    return field_bag.currency is not None

def is_bond(field_bag):
    return field_bag.ticker is None and field_bag.contract_code is None \
        and (field_bag.maturity_date is not None or field_bag.effective_date is not None or field_bag.coupon_rate is not None)

def is_future(field_bag):
    return field_bag.contract_code is not None or field_bag.contract_expiry_date is not None

def create_cash_holding(field_bag):
    cash = Cash(field_bag.name)
    cash_fields = ['currency']
    copy_over_fields(field_bag, cash, COMMON_HOLDING_FIELDS + cash_fields)
    return cash

def create_bond_holding(field_bag):
    bond = Bond(field_bag.name)
    bond_fields = ['coupon_rate', 'rating', 'effective_date', 'maturity_date', 'next_call_date', 'quantity_held', 'sector']
    copy_over_fields(field_bag, bond, COMMON_HOLDING_FIELDS + bond_fields)
    return bond

def create_future_holding(field_bag):
    future = Future(field_bag.name)
    future_fields = ['contract_code', 'contract_expiry_date', 'quantity_held']
    copy_over_fields(field_bag, future, COMMON_HOLDING_FIELDS + future_fields)
    return future

def create_equity_holding(field_bag):
    equity = Equity(field_bag.name)
    equity_fields = ['ticker', 'num_shares', 'sector']
    copy_over_fields(field_bag, equity, COMMON_HOLDING_FIELDS + equity_fields)
    return equity

def create_holding(field_bag):
    """Factory method that accepts a HoldingFieldBag, determines the appropriate entity type,
    and returns a new instance of that entity, copying over all relevant fields.

    :param field_bag: A HoldingFieldBag produced as a result of parsing a fund's holdings list.
    :returns: A Holding subclass of the appropriate type based on the available fields in the bag.
    """
    if is_cash(field_bag):
        return create_cash_holding(field_bag)
    elif is_bond(field_bag):
        return create_bond_holding(field_bag)
    elif is_future(field_bag):
        return create_future_holding(field_bag)
    else:  # Equity is the catch-all
        return create_equity_holding(field_bag)