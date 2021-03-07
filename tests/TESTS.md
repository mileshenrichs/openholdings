# Tests for openholdings

Programmatic tests have not been written yet.  For each ETF provider, a selection of funds have been chosen to manually test.  It it useful to test multiple funds from the same provider because different data formats are provided for different fund types (i.e. equities, bonds, currency, commodity funds).

## Invesco
Ticker | Description
------ | -----------
[QQQ](https://www.invesco.com/us/financial-products/etfs/holdings?audienceType=Investor&ticker=QQQ) | Equities, large-cap tech
[PGHY](https://www.invesco.com/us/financial-products/etfs/holdings?audienceType=Investor&ticker=PGHY) | Bonds
[UUP](https://www.invesco.com/us/financial-products/etfs/holdings?audienceType=Investor&ticker=UUP) | Currency futures, US Dollar
[KBWY](https://www.invesco.com/us/financial-products/etfs/holdings?audienceType=Investor&ticker=KBWY) | REITs (equities), but presented as if they were bonds

## Vanguard
Ticker | Description
------ | -----------
[VOO](https://investor.vanguard.com/etf/profile/overview/VOO/portfolio-holdings) | Equities, S&P 500
[VCEB](https://investor.vanguard.com/etf/profile/portfolio/VCEB/portfolio-holdings) | Bonds

## VanEck
Ticker | Description
------ | -----------
[REMX](https://www.vaneck.com/etf/equity/remx/holdings/) | Equities, numeric international tickers
[IHY](https://www.vaneck.com/etf/income/ihy/holdings/) | Bonds, extra row above table in spreadsheet

## ETFMG
Ticker | Description
------ | -----------
[ETHO](https://etfmg.com/funds/etho/) | Equities
[MJ](https://etfmg.com/funds/mj/) | Equities, but in a different format
[VALT](https://etfmg.com/funds/valt/) | Bonds, in same format as equities
[BDRY](https://etfmg.com/funds/bdry/) | Equities with invalid CUSIPs

## SPDR
Ticker | Description
------ | -----------
[SPY](https://www.ssga.com/us/en/institutional/etfs/funds/spdr-sp-500-etf-trust-spy) | Equities
[GNR](https://www.ssga.com/us/en/institutional/etfs/funds/spdr-sp-global-natural-resources-etf-gnr) | Equities, international, cash
[IBND](https://www.ssga.com/us/en/institutional/etfs/funds/spdr-bloomberg-barclays-international-corporate-bond-etf-ibnd) | Bonds, cash in multiple currencies