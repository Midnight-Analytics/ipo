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
#        self.today = datetime.today()
#        self.today_plus_30 = self.today + timedelta(days=30)

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

        """

        dates = self.validate_dates(from_date, to_date)
        endpoint = "ipo_calendar"

        params = {
            "from": dates['from_date'],
            "to":  dates['to_date'],
            "apikey": self.API_KEY['apikey']
            } 

        response = requests.get(self.base_url + endpoint, params=params)

        return response.text

if __name__ == '__main__':
    FinancialModelingAPI().get_api_key()