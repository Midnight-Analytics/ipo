from FinancialMod=delingPrep import CompanyValuation, Calendars
from datetime import datetime, timedelta
import pandas as pd
import json

#exan = ipo_calendar.Calendars()
data = Calendars().ipo_calendar(from_date='2021-03-03', to_date='2021-03-31')
data = pd.json_normalize(data)
print(data)


print("Company Valuation")
profile = CompanyValuation()
ticker = 'AMZN'

print("Earning Calendar")
data = Calendars().historical_earning_calendar(ticker)
data = pd.json_normalize(data)
print(data)

print("Company Quote")
data = profile.company_quote(ticker)
data = pd.json_normalize(data)
print(data)

print("SEC Filings")
data = profile.company_sec_filings(ticker)
data = pd.json_normalize(data)
print(data)

print("Income Statements")
data = profile.company_income_statements(ticker)
data = pd.json_normalize(data)
print(data)

print("Balance Statements")
data = profile.company_balance_sheet_statements(ticker)
data = pd.json_normalize(data)
print(data)

print("Cash Flow Statements")
data = profile.company_cash_flow_statements(ticker)
data = pd.json_normalize(data)
print(data)


print("Income Statements Growth")
data = profile.company_income_statement_growth(ticker)
data = pd.json_normalize(data)
print(data)

