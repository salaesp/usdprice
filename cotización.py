import requests
import itertools
import threading
import time
import sys
import os
import random

messages = [
  "Discovering new ways of making you wait.",
"Your time is very important to us. Please wait while we ignore you.",
"Still faster than Windows update.",
"We are not liable for any broken screens as a result of waiting.",
"Bored of slow loading spinner?, buy more RAM!",
"Kindly hold on until I finish a cup of coffee.",
"We will be back in 1/0 minutes.",
"Why don't you order a sandwich?",
"Don't panic, Just count to infinite.",
"Please wait, Your PC is not a superman!"
]

PERCENTAGE_GANANCIA = 0.35
PERCENTAGE_SOLIDARIO = 0.30
done = False

class BuenbitPrice:
  def __init__(self, price):
    self.price = str(price)

class DolarArg:
  def __init__(self, blue, oficial):
    self.blue = str(blue)
    self.oficial = str(oficial)
    self.solidario = str(oficial + (oficial * PERCENTAGE_GANANCIA) + (oficial * PERCENTAGE_SOLIDARIO))
    self.solidarioAfterReinbursment = str(oficial + (oficial * PERCENTAGE_SOLIDARIO))


def buenbitUsdPrice():
    buenbitData = requests.get('https://be.buenbit.com/api/market/tickers/').json()
    arsToDaiPrice = float(buenbitData["object"]["daiars"]["selling_price"])
    daiToUsdPrice = float(buenbitData["object"]["daiusd"]["purchase_price"])
    return BuenbitPrice((1 / daiToUsdPrice) * arsToDaiPrice)

def priceDolar():
    baseUrl = 'https://api-dolar-argentina.herokuapp.com/api/'
    oficial = float(requests.get(baseUrl + "dolaroficial").json()["venta"])
    blue = float(requests.get(baseUrl + "dolarblue").json()["venta"])
    return DolarArg(blue, oficial)

#here is the animation
def loading():
    currentMessage = random.choice(messages)
    for c in itertools.cycle(['___', '-__', '_-_', '__-', '___', '___', '___', ]):
        if done:
            break
        sys.stdout.write('\r'+ currentMessage + c)
        sys.stdout.flush()
        time.sleep(0.1)

def printPrices():
    global done
    done = False
    buenbitData = buenbitUsdPrice()
    dolarData = priceDolar()
    done = True
    os.system("clear")
    price = "Ars a usd buenbit:  " + buenbitData.price + "\n"
    price = price + "Dolar oficial: " + dolarData.oficial + "\n"
    price = price + "Dolar solidario: " + dolarData.solidario + "\n"
    price = price + "Dolar blue: " + dolarData.blue + "\n"
    price = price + "Dolar solidario con devolucion: " + dolarData.solidarioAfterReinbursment + "\n\n"
    for char in price:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.015)

os.system("clear")
threading.Thread(target=loading).start()
printPrices()


while True:
    done = False
    threading.Thread(target=loading).start()
    time.sleep(10)
    printPrices()

