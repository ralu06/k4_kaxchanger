from tkinter import *
from tkinter import ttk
import configparser
import json
import requests # peticiones http

DEFAULTPADDING = 4

class Exchanger(Tk):

    def __init__(self, parent):
        ttk.Frame.__init__(self, width="400", height="150")
        config = configparser.ConfigParser()
        config.read("config.ini")

        self.api_key = config['fixer.io']['API_KEY']
        self.all_symbols_ep = config['fixer.io']['ALL_SYMBOLS_EP']
        self.rate_ep = config['fixer.io']['RATE_LATEST_EP']

        currencies = self.getCurrencies()

        #variables de control
        self.strInQuantity = StringVar(value="")
        self.strInQuantity.trace('w', self.convertirDivisas)

        self.strInCurrency =StringVar()
        self.strOutCurrency = StringVar()

        self.pack_propagate(0)
        frInCurrency = ttk.Frame(self)
        frInCurrency.pack_propagate(0)

        lblQ = ttk.Label(frInCurrency, text="Cantidad")
        lblQ.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady=DEFAULTPADDING)

        self.inQuantityEntry = ttk.Entry(frInCurrency, font=('Helvetica', 24, 'bold'), width=10, textvariable=self.strInQuantity)
        self.inQuantityEntry.pack(side=TOP, fill=X)

        self.inCurrencyCombo = ttk.Combobox(frInCurrency, width=25, height=5, values=currencies, textvariable=self.strInCurrency)
        self.inCurrencyCombo.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady=DEFAULTPADDING)
        self.inCurrencyCombo.bind('<<ComboboxSelected>>', self.convertirDivisas)

        frInCurrency.pack(side=LEFT, fill=BOTH, expand=True)

        frOutCurrency = ttk.Frame(self)
        frOutCurrency.pack_propagate(0)

        lblQ = ttk.Label(frOutCurrency, text="Cantidad")
        lblQ.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady=DEFAULTPADDING)

        self.outQuantityLbl = ttk.Label(frOutCurrency, font=('Helvetica', 24), anchor=E, width=10)
        self.outQuantityLbl.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady=DEFAULTPADDING)

        self.outCurrencyCombo = ttk.Combobox(frOutCurrency, width=25, height=5, values=currencies, textvariable=self.strOutCurrency)
        self.outCurrencyCombo.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady=DEFAULTPADDING)
        self.outCurrencyCombo.bind('<<ComboboxSelected>>', self.convertirDivisas)

        frOutCurrency.pack(side=LEFT, fill=BOTH, expand=True)

    def convertirDivisas (self, *args):  #array de argumentos
        print("in", self.strInCurrency.get())
        print("out", self.strOutCurrency.get())
        print("Cantidad", self.strInQuantity.get())


    def getCurrencies(self):
        response = requests.get(self.all_symbols_ep.format(self.api_key))

        if response == 200:
            currencies = json.loads(response.text)
            result = []
            symbols = currencies['symbols']
            for symbol in symbols:
                text = "{} - {}".format(symbol, symbols[symbol])
                result.append(text)
            return result
        else:
            print("Se ha producido un error al consultar symbols:", response.status_code)
   

class MainApp(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.geometry("400x150")
        self.title("Exchanger fixer.io")
        self.exchanger = Exchanger(self)
        self.exchanger.place(x=0, y=0)

    def start(self):
        self.mainloop()

if __name__ == '__main__':
    exchanger = MainApp()
    exchanger.start()



