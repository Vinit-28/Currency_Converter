
#Importing the Utility For the Application #
from CurrencyConverterUtils import *


# Class to Provide the Functionalities of the Currency Converter Application #
class CurrencyConverter:

    # Initializing and Getting the Utilities Ready #
    def __init__(self):
        
        self.currencyConverterHelper = CurrencyConverterUtilities()
        self.utilities = self.currencyConverterHelper.getCountryCurrencyList()
        self.countries, self.currencies, self.currencyCodes = [], [], []
        self.fromIndex, self.toIndex = 0, 1
        # Initializing Country Names, Currency Names, Currency Codes #
        for country in self.utilities:
            self.countries.append(country)
            temp_list = self.utilities[country].split('\t')
            self.currencies.append(temp_list[0])
            self.currencyCodes.append(temp_list[1])
        
        self.fromCountry, self.fromCurrency, self.fromCurrencyCode = self.countries[self.fromIndex], self.currencies[self.fromIndex], self.currencyCodes[self.fromIndex] 
        self.toCountry, self.toCurrency, self.toCurrencyCode = self.countries[self.toIndex], self.currencies[self.toIndex], self.currencyCodes[self.toIndex] 

    
    # Method to Change the Combo Box Values according to the User Action #
    def changeComboboxValues(self, countryCombobox, currencyCombobox, CurrencyCodeCombobox, previousSelectedCountry, previousSelectedCurrency, previousSelectedCurrencyCode, change):

        selectedCountry = countryCombobox.get()
        selectedCurrency = currencyCombobox.get()
        selectedCurrencyCode = CurrencyCodeCombobox.get()
        
        newIndex = None
        listToSearch = self.currencyCodes
        searchFor = selectedCurrencyCode

        if selectedCountry != "" and selectedCountry != previousSelectedCountry:
            listToSearch, searchFor = self.countries, selectedCountry
        elif selectedCurrency != "" and selectedCurrency != previousSelectedCurrency:
            listToSearch, searchFor = self.currencies, selectedCurrency
        
        
        # To and From are selected to be the Same #
        if (change == "from" and (searchFor == self.toCountry or searchFor == self.toCurrency or searchFor == self.toCurrencyCode) ):
            newIndex = self.fromIndex
            messagebox.showerror("Error","From and To can't be Same!!!")
        
        elif (change == "to" and (searchFor == self.fromCountry or searchFor == self.fromCurrency or searchFor == self.fromCurrencyCode) ):
            newIndex = self.toIndex
            messagebox.showerror("Error","From and To can't be Same!!!")
 
        else:
            for index in range(len(listToSearch)):
                if searchFor == listToSearch[index]:
                    newIndex = index
                    break
        
        countryCombobox.current(newIndex)
        currencyCombobox.current(newIndex)
        CurrencyCodeCombobox.current(newIndex)

        if change == "from":
            self.fromIndex = newIndex
            self.fromCountry, self.fromCurrency, self.fromCurrencyCode = self.countries[newIndex], self.currencies[newIndex], self.currencyCodes[newIndex]
        else:
            self.toIndex = newIndex
            self.toCountry, self.toCurrency, self.toCurrencyCode = self.countries[newIndex], self.currencies[newIndex], self.currencyCodes[newIndex]
            self.convertButton.config(text=f"Convert to {self.currencyCodes[newIndex]}")
        

    # Method to get the Selected Date from the Calendar and formatting it to Display on the Screen #
    def formatAndSetDate(self):
        date = self.calendar.get_date()
        temp_list = date.split('/')
        
        self.date.delete(0,END)
        self.date.insert(0,("20" + temp_list[2] + "-" + temp_list[1] + "-" + temp_list[0]))
        
        self.calWindow.destroy()


    # Method to Display Calendar #
    def showCalendar(self):
        self.calWindow = Toplevel(self.root)
        self.calWindow.geometry("300x250")
        self.calWindow.config(bg="black")

        self.calendar = Calendar(self.calWindow, selectmode="day")
        self.calendar.pack(pady=20, expand=True)

        self.getDateButton = Button(self.calWindow, text="Done", fg="black", bg="white", font=("times",10,"bold"), command=self.formatAndSetDate)
        self.getDateButton.pack(pady=5,expand=True)
        self.calWindow.mainloop()


    # Method to Send Data for the Conversion and Displaying it on the Screen # 
    def convertAndDisplayResult(self):
        
        if self.amount.get() == "" or self.date.get() == "" :
            messagebox.showerror("Error", "All Fields are Required to be Filled!!!")
        else:
            try:
                result = self.currencyConverterHelper.getCurrencyConversionResults(self.currencyCodes[self.fromIndex], self.currencyCodes[self.toIndex], float(self.amount.get()), self.date.get())
                self.convertedAmountLabel.config(text=f"Converted Amount :- ")
                self.convertedAmount.config(text=f"{self.currencyCodes[self.toIndex]}  {round(result,5)}")

            except Exception as error:
                self.convertedAmountLabel.config(text="")
                self.convertedAmount.config(text="")
                messagebox.showerror("Error",error.__doc__)


    # Method to Start the Application or Entry Gate for the Application #
    def startApplication(self):

        # Initializing Root Window #
        self.root = Tk()
        self.root.title("Currency Converter")
        self.root.geometry("700x600")
        self.root.config(bg="black")
        Label(self.root, text="Currency Converter", fg="white", bg="black", font=("times",22,"bold")).place(x=220,y=30)


        # Placing "Select From" on the Screen #
        Label(self.root, text="Select From :- ", fg="white", bg="black", font=("times",12,"bold")).place(x=30,y=150)
        self.fromCountryCombobox = Combobox(self.root, values=self.countries,)
        self.fromCountryCombobox.place(x=30,y=200)
        self.fromCountryCombobox.current(0)


        self.fromCurrencyCombobox = Combobox(self.root, values=self.currencies)
        self.fromCurrencyCombobox.place(x=250,y=200)
        self.fromCurrencyCombobox.current(0)


        self.fromCurrencyCodeCombobox = Combobox(self.root, values=self.currencyCodes)
        self.fromCurrencyCodeCombobox.place(x=470,y=200)
        self.fromCurrencyCodeCombobox.current(0)

        self.fromCountryCombobox.bind("<<ComboboxSelected>>", lambda e: self.changeComboboxValues(self.fromCountryCombobox, self.fromCurrencyCombobox, self.fromCurrencyCodeCombobox, self.fromCountry, self.fromCurrency, self.fromCurrencyCode, change="from"))
        self.fromCurrencyCombobox.bind("<<ComboboxSelected>>", lambda e: self.changeComboboxValues(self.fromCountryCombobox, self.fromCurrencyCombobox, self.fromCurrencyCodeCombobox, self.fromCountry, self.fromCurrency, self.fromCurrencyCode, change="from"))
        self.fromCurrencyCodeCombobox.bind("<<ComboboxSelected>>", lambda e: self.changeComboboxValues(self.fromCountryCombobox, self.fromCurrencyCombobox, self.fromCurrencyCodeCombobox, self.fromCountry, self.fromCurrency, self.fromCurrencyCode, change="from"))


        # Placing "Select To" on the Screen #
        Label(self.root, text="Select To :- ", fg="white", bg="black", font=("times",12,"bold")).place(x=30,y=280)
        self.toCountryCombobox = Combobox(self.root, values=self.countries,)
        self.toCountryCombobox.place(x=30,y=330)
        self.toCountryCombobox.current(1)


        self.toCurrencyCombobox = Combobox(self.root, values=self.currencies)
        self.toCurrencyCombobox.place(x=250,y=330)
        self.toCurrencyCombobox.current(1)


        self.toCurrencyCodeCombobox = Combobox(self.root, values=self.currencyCodes)
        self.toCurrencyCodeCombobox.place(x=470,y=330)
        self.toCurrencyCodeCombobox.current(1)

        self.toCountryCombobox.bind("<<ComboboxSelected>>", lambda e: self.changeComboboxValues(self.toCountryCombobox, self.toCurrencyCombobox, self.toCurrencyCodeCombobox, self.toCountry, self.toCurrency, self.toCurrencyCode, change="to"))
        self.toCurrencyCombobox.bind("<<ComboboxSelected>>", lambda e: self.changeComboboxValues(self.toCountryCombobox, self.toCurrencyCombobox, self.toCurrencyCodeCombobox, self.toCountry, self.toCurrency, self.toCurrencyCode, change="to"))
        self.toCurrencyCodeCombobox.bind("<<ComboboxSelected>>", lambda e: self.changeComboboxValues(self.toCountryCombobox, self.toCurrencyCombobox, self.toCurrencyCodeCombobox, self.toCountry, self.toCurrency, self.toCurrencyCode, change="to"))


        # Taking User Input (Amount) #
        Label(self.root, text="Enter Amount :- ", fg="white", bg="black", font=("times",12,"bold")).place(x=30,y=430)

        self.amount = Entry(self.root, width=15)
        self.amount.place(x=30,y=460)


        # Taking User Input (Date) #
        Label(self.root, text="Enter Date (YYYY-MM-DD) :- ", fg="white", bg="black", font=("times",12,"bold")).place(x=250,y=430)

        self.date = Entry(self.root, width=15)
        self.date.place(x=250,y=460)
        currentDate = Calendar(self.root, selectmode="day").get_date()
        temp_list = currentDate.split('/')

        self.date.insert(0,("20" + temp_list[2] + "-" + temp_list[1] + "-" + temp_list[0]))
        

        calImage = Image.open("Calendar.png")
        calImage = calImage.resize((25,25))
        calImage = ImageTk.PhotoImage(image = calImage)


        # Placing Calendar Button on the Screen #
        self.calButton = Button(self.root, image=calImage, width=23,height=18, command=self.showCalendar)
        self.calButton.place(x=390,y=460)


        # Displaying Result #
        self.convertedAmountLabel = Label(self.root, fg="white", bg="black", font=("times",12,"bold"))
        self.convertedAmountLabel.place(x=500,y=430)

        self.convertedAmount = Label(self.root, fg="white", bg="black", font=("times",12, "bold"))
        self.convertedAmount.place(x=500,y=460)


        # Convert Button #
        self.convertButton = Button(self.root, text="Convert to EUR", fg="black", bg="white", font=("times",10,"bold"), command=self.convertAndDisplayResult)
        self.convertButton.place(x=280,y=540)
        

        # Running Application #
        self.root.mainloop()

