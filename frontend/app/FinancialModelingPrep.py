import requests
import json
import pandas as pd
#import datetime
from datetime import datetime, timedelta
import os
from getpass import getpass
import time

class FinancialModelingAPI(object):

    def __init__(self):
        """
        Initiates base variables:
            base_url - https://financialmodelingprep.com/api/v3/
            API_KEY - stored locally when entered on the first instatiation of the class
        """
        self.base_url = "https://financialmodelingprep.com/api/v3/"
        self.API_KEY = self.get_api_key()

    def get_api_key(self):
        """
        Create credentials to be stored locally on first run to avoid coding
        in function cals throughout the rest of the code
        :TODO have these be encrypted and backed by database instead of local
        """

        json_file = 'fmp_credentials.json'

        if os.path.exists(json_file):
            with open(json_file) as f: 
                data = json.load(f)

            return data 

        else:
            API_KEY = getpass("Input API_KEY: ")
            creds = {
                'apikey': API_KEY
                }

            with open(json_file, 'w') as f:
                json.dump(creds, f)
            
            return creds

class Calendars(FinancialModelingAPI):

    def __init__(self):
        #self.base_url = "https://financialmodelingprep.com/api/v3/"
        FinancialModelingAPI.__init__(self)


    def validate_dates(self, from_date, to_date):
        """
        Runs checks against the dates provided for the Calendar API
        Checks:
            1) Validates that dates are chonological when passed
            2) Ensures that both a from & to date are passed not just one

        returns a default of the last 90 days from todays date backwards
        if no values are passed, this is the deault max term for
        calendar APIs
        """
        # Ensure both date variables are used if custom values are passed
        if (from_date is None and to_date is not None) or (from_date is not None and to_date is None):
            raise ValueError("both a from_date and to_date must be provided")

        # Ensure that dates provided are in chronological order
        if from_date is not None and to_date is not None:

            if time.strptime(from_date, "%Y-%m-%d") > time.strptime(to_date, "%Y-%m-%d"):
                raise ValueError("from_date must be before the to_date")

        if from_date is not None and to_date is not None:
            return {
                'from_date': from_date,
                'to_date': to_date
            }
        else:
            return {
                'from_date': (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
                'to_date': datetime.now().strftime("%Y-%m-%d")
            }


    def ipo_calendar(self, from_date=None, to_date=None):
        """
        Returns the IPO's listed on https://financialmodelingprep.com/
        Params: date format 'yyyy-mm-dd'
            from_date - defaults to today-90 days 
            to_date - defaults to today
        """

        dates = self.validate_dates(from_date, to_date)
        endpoint = "ipo_calendar"

        params = {
            "from": dates['from_date'],
            "to":  dates['to_date'],
            "apikey": self.API_KEY['apikey']
            } 

        response = requests.get(self.base_url + endpoint, params=params)
        response = json.loads(response.text)

        return response


    def earning_calendar(self, from_date=None, to_date=None):
        """
        Returns the Earnings reports listed on https://financialmodelingprep.com/
        Params: date format 'yyyy-mm-dd'
            from_date - defaults to today-90 days 
            to_date - defaults to today
        """

        dates = self.validate_dates(from_date, to_date)
        endpoint = "earning_calendar"

        params = {
            "from": dates['from_date'],
            "to":  dates['to_date'],
            "apikey": self.API_KEY['apikey']
            } 

        response = requests.get(self.base_url + endpoint, params=params)
        response = json.loads(response.text)

        return response


    def historical_earning_calendar(self, symbol, limit=80):
        """
        Returns the earnings history for the ticker provided
        Params:
            symbol - symbol for the company of interest, stock list can be found - here https://stockanalysis.com/stocks/
        """
        endpoint = "historical/earning_calendar/" + symbol.upper()

        params = {
            "apikey": self.API_KEY['apikey']
            } 

        response = requests.get(self.base_url + endpoint, params=params)
        response = json.loads(response.text)


        return response


class CompanyValuation(FinancialModelingAPI):

    def __init__(self):
        #self.base_url = "https://financialmodelingprep.com/api/v3/"
        FinancialModelingAPI.__init__(self)

    def company_profile(self, symbol):
        """
        Returns the company profile for the ticker provided
        Params:
            symbol - symbol for the company of interest, stock list can be found - here https://stockanalysis.com/stocks/
        """
        endpoint = "profile/" + symbol.upper()

        params = {
            "apikey": self.API_KEY['apikey']
            } 

        response = requests.get(self.base_url + endpoint, params=params)
        response = json.loads(response.text)
        return response


    def company_quote(self, symbol):
        """
        Returns the company profile for the ticker provided
        Params:
            symbol - symbol for the company of interest, stock list can be found - here https://stockanalysis.com/stocks/
        """
        endpoint = "quote/" + symbol.upper()

        params = {
            "apikey": self.API_KEY['apikey']
            } 

        response = requests.get(self.base_url + endpoint, params=params)
        response = json.loads(response.text)
        return response


    def company_key_executives(self, symbol):
        """
        Returns the company profile for the ticker provided
        Params:
            symbol - symbol for the company of interest, stock list can be found - here https://stockanalysis.com/stocks/
        """
        endpoint = "key-executives/" + symbol.upper()

        params = {
            "apikey": self.API_KEY['apikey']
            } 

        response = requests.get(self.base_url + endpoint, params=params)
        response = json.loads(response.text)

        return response


    def company_income_statements(self, symbol, period=None, limit=10, datatype=None):
        """
        Returns the company profile for the ticker provided
        Params:
            symbol - symbol for the company of interest, stock list can be found - here https://stockanalysis.com/stocks/
            :TODO create download csv functionality
        """

        if datatype is not None and datatype !='csv':
            raise ValueError("datatype only accepts 'csv' as a value")

        endpoint = "income-statement/" + symbol.upper()

        params = {
            "period": period,
            "limit": limit,
            "datatype": datatype,
            "apikey": self.API_KEY['apikey']
            } 

        if datatype is not None:  
            if datatype.lower() == 'csv':
                response = requests.get(self.base_url + endpoint, params=params)
                return response
        else:                

            response = requests.get(self.base_url + endpoint, params=params)
            response = json.loads(response.text)
            
            return response


    def company_balance_sheet_statements(self, symbol, period=None, limit=10, datatype=None):
        """
        Returns the company profile for the ticker provided
        Params:
            symbol - symbol for the company of interest, stock list can be found - here https://stockanalysis.com/stocks/
            :TODO create download csv functionality
        """

        if datatype is not None and datatype !='csv':
            raise ValueError("datatype only accepts 'csv' as a value")

        endpoint = "balance-sheet-statement/" + symbol.upper()

        params = {
            "period": period,
            "limit": limit,
            "datatype": datatype,
            "apikey": self.API_KEY['apikey']
            } 

        if datatype is not None:  
            if datatype.lower() == 'csv':
                response = requests.get(self.base_url + endpoint, params=params)
                return response
        else:                

            response = requests.get(self.base_url + endpoint, params=params)
            response = json.loads(response.text)
            
            return response


    def company_cash_flow_statements(self, symbol, period=None, limit=10, datatype=None):
        """
        Returns the company profile for the ticker provided
        Params:
            symbol - symbol for the company of interest, stock list can be found - here https://stockanalysis.com/stocks/
            :TODO create download csv functionality
        """

        if datatype is not None and datatype !='csv':
            raise ValueError("datatype only accepts 'csv' as a value")

        endpoint = "cash-flow-statement/" + symbol.upper()

        params = {
            "period": period,
            "limit": limit,
            "datatype": datatype,
            "apikey": self.API_KEY['apikey']
            } 

        if datatype is not None:  
            if datatype.lower() == 'csv':
                response = requests.get(self.base_url + endpoint, params=params)
                return response
        else:                

            response = requests.get(self.base_url + endpoint, params=params)
            response = json.loads(response.text)
            
            return response


    def company_sec_filings(self, symbol, period=None, doc_type=None, limit=500):
        """
        Returns the company profile for the ticker provided
        Params:
            symbol - symbol for the company of interest, stock list can be found - here https://stockanalysis.com/stocks/
        """
        endpoint = "sec_filings/" + symbol.upper()

        params = {
            "period": period,
            "limit": limit,
            "type": doc_type,
            "apikey": self.API_KEY['apikey']
            } 

        response = requests.get(self.base_url + endpoint, params=params)
        response = json.loads(response.text)
        
        return response


    def company_income_statement_growth(self, symbol, limit=40):
        """
        Returns the company profile for the ticker provided
        Params:
            symbol - symbol for the company of interest, stock list can be found - here https://stockanalysis.com/stocks/
            :TODO create download csv functionality
        """
        endpoint = "income-statement-growth/" + symbol.upper()

        params = {
            "smybol": symbol,
            "limit": limit,
            "apikey": self.API_KEY['apikey']
            } 

        response = requests.get(self.base_url + endpoint, params=params)
        response = json.loads(response.text)
        
        return response



class StockMarket(FinancialModelingAPI):

    def __init__(self):
        #self.base_url = "https://financialmodelingprep.com/api/v3/"
        FinancialModelingAPI.__init__(self)


    def most_active_stock(self):
        """
        Returns the most active stock companies, updated daily
        """
        endpoint = "actives"
        
        params = {
            "apikey": self.API_KEY['apikey']
            } 

        response = requests.get(self.base_url + endpoint, params=params)
        response = json.loads(response.text)
        
        return response

    def most_gainer_stock(self):

        """
        Returns the most gaining stock companies, updated daily
        """
        endpoint = "gainers"
        
        params = {
            "apikey": self.API_KEY['apikey']
            } 

        response = requests.get(self.base_url + endpoint, params=params)
        response = json.loads(response.text)
        
        return response   


    def most_loser_stock(self):
        """
        Returns the most losing stock companies, updated daily
        """
        endpoint = "losers"
        
        params = {
            "apikey": self.API_KEY['apikey']
            } 

        response = requests.get(self.base_url + endpoint, params=params)
        response = json.loads(response.text)
        
        return response   


if __name__ == '__main__':
    FinancialModelingAPI().get_api_key()