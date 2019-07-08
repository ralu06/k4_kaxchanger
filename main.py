from tkinter import *
from tkinter import ttk

import configparser
import json

import requests # peticiones http

config = configparser.ConfigParser()
config.read('config.ini')


inSymbol = input('Que mondeda quieres convertir:')
outSymbol = input('En que otra moneda:')

url = config['fixer.io']['RATE_LATEST_EP']
api_key = config['fixer.io']['API_KEY']

url = url.format(api_key, inSymbol, outSymbol)
response = requests.get(url)
if response.status_code == 200:
    print(response.text)
else:
    print("Se ha producido un error en la peticion:", response.status_code)
