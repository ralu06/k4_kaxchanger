from tkinter import *
from tkinter import ttk
import configparser
import json
import requests

DEFAULTPADDING = 4

class Exchanger(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, width="400", height="150")
        config = configparser.ConfigParser()
        config.read("config.ini")

        self.api_key = config['fixer.io']['API_KEY']
        self.all_symbols_ep = config['fixer.io']['ALL_SYMBOLS_EP']
        self.rate_ep = config['fixer.io']['RATE_LATEST_EP']

        #Variables de control
        self.strInQuantity = StringVar(value="")
        self.oldInQuantity = self.strInQuantity.get()
        self.strInQuantity.trace('w', self.validarCantidad)

        self.strInCurrency = StringVar()
        self.strOutCurrency = StringVar()

        self.pack_propagate(0)

        frErrorMessages = ttk.Frame(self, height=40)
        frErrorMessages.pack(side=BOTTOM, fill=X)
        frErrorMessages.pack_propagate(0)

        self.lblErrorMessages = ttk.Label(frErrorMessages, text="", width=50, foreground='red', anchor=CENTER)
        self.lblErrorMessages.pack(side=BOTTOM, fill=BOTH, expand=True)


        frInCurrency = ttk.Frame(self)
        frInCurrency.pack_propagate(0)

        lblQ = ttk.Label(frInCurrency, text="Cantidad")
        lblQ.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady=DEFAULTPADDING)

        self.inQuantityEntry = ttk.Entry(frInCurrency, font=('Helvetica', 24, 'bold'), width=10, textvariable=self.strInQuantity)
        self.inQuantityEntry.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady=DEFAULTPADDING)

        self.inCurrencyCombo = ttk.Combobox(frInCurrency, width=25, height=5, textvariable=self.strInCurrency)
        self.inCurrencyCombo.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady=DEFAULTPADDING)
        self.inCurrencyCombo.bind('<<ComboboxSelected>>', self.convertirDivisas)

        frInCurrency.pack(side=LEFT, fill=BOTH, expand=True)

        frOutCurrency = ttk.Frame(self)
        frOutCurrency.pack_propagate(0)

        lblQ = ttk.Label(frOutCurrency, text="Cantidad")
        lblQ.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady=DEFAULTPADDING)

        self.outQuantityLbl = ttk.Label(frOutCurrency, font=('Helvetica', 26), anchor=E, width=10)
        self.outQuantityLbl.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady=DEFAULTPADDING, ipady=2)

        self.outCurrencyCombo = ttk.Combobox(frOutCurrency, width=25, height=5, textvariable=self.strOutCurrency)
        self.outCurrencyCombo.pack(side=TOP, fill=X, padx=DEFAULTPADDING, pady=DEFAULTPADDING)
        self.outCurrencyCombo.bind('<<ComboboxSelected>>', self.convertirDivisas)
        
        frOutCurrency.pack(side=LEFT, fill=BOTH, expand=True)

        url = self.all_symbols_ep.format(self.api_key)
        self.accesoAPI(url, self.getCurrencies)



    def validarCantidad(self, *args):
        try:
            v = float(self.strInQuantity.get())
            self.oldInQuantity = v
            self.convertirDivisas()
        except:
            self.strInQuantity.set(self.oldInQuantity)
        

    def accesoAPI(self, url, callback, **args):
        response = requests.get(url)

        if response.status_code == 200:
            callback(response.text, **args)
        else:
            msgError = 'Error en acceso a {}. response-code: {}'.format(url, response.status_code)
            raise Exception(msgError)        


    def convertirDivisas(self, *args):
        base = 'EUR'
        _from = self.strInCurrency.get()
        _from = _from[:3]
        _to = self.strOutCurrency.get()
        _to = _to[:3]
        symbols = _from+","+_to
        
        if self.strInCurrency.get() and self.strOutCurrency.get() and self.strInQuantity.get(): 
            self.lblErrorMessages.config(text='Conectando ...')

            url = self.rate_ep.format(self.api_key, base, symbols)
            self.accesoAPI(url, self.showConversionRate)
            
            #valor_label = Cantidad / tasa_conversion * tasa_conversion2



    def showConversionRate(self, textdata):
        data = json.loads(textdata)
        if data['success']:
            tasa_conversion = []
            for tasa in data['rates']:
                tasa_conversion.append(data['rates'][tasa])
            self.lblErrorMessages.config(text='')
        else:
            msgError = "{} - {}".format(data['error']['code'], data['error']['type'] )
            print(msgError)
            raise Exception(msgError)


        valor_label = round(float(self.strInQuantity.get()) / tasa_conversion[0] * tasa_conversion[1], 5)
        self.outQuantityLbl.config(text=valor_label)



    def getCurrencies(self, textdata):
        currencies = json.loads(textdata)
        result = []
        symbols = currencies['symbols']
        for symbol in symbols:
            text = "{} - {}".format(symbol, symbols[symbol])
            result.append(text)
        
        self.inCurrencyCombo.config(values = result)
        self.outCurrencyCombo.config(values = result)



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