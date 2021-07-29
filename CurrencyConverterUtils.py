
# Importing The Utilities #
from tkinter import *
from tkinter.ttk import Combobox
from tkcalendar import calendar_
from tkinter import messagebox
from tkcalendar.calendar_ import Calendar
from PIL import Image, ImageTk
from requests import get


# Class to Provide the Utility Methods to Convert an Amount between Currencies #
class CurrencyConverterUtilities:

    # Initializing the Utilities #
    def __init__(self) :
        self.countryCurrencyList = dict()
        self.apiKey = "d7d25f019b8c8a6f6ed5e82fe3c765a5"
        self.url = "https://api.currencyscoop.com/v1/historical"+f"?api_key={self.apiKey}"


    # Getting the list of Currencies along with their Currency Names and Currency Codes(Short Form) #
    def getCountryCurrencyList(self):
        with open("CountryWithCurrencyCodes.txt", "r") as file:
            for line in file:
                lst = line.split("\t")
                if len(lst) == 3 :
                    self.countryCurrencyList[lst[0]] = (lst[1] + "\t" + lst[2][:-1])

        return self.countryCurrencyList


    # Making a Get Request to the Website to get the Information about Currency Exchange and Perform Conversion #
    def getCurrencyConversionResults(self, fromCurrency, toCurrency, amount, date):

        parameters = {
            "base" : fromCurrency,
            "symbols" : toCurrency,
            "date" : date,
        }
        response = get(url=self.url, params=parameters) 
        # If Request Falied Exception Will be Raised #
        response.raise_for_status()    
        return (amount * response.json()['response']['rates'][toCurrency])  
