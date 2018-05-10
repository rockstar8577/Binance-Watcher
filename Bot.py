# import the library
import multiprocessing
import time
from appJar import gui
from binance.client import Client

class Ticker:
    def __init__(self, symbol="", priceUSDT=0.0, priceBTC=0.0, priceETH=0.0):
        self.symbol = symbol
        self.priceUSDT = priceUSDT
        self.priceBTC = priceBTC
        self.priceETH = priceETH
        
    def printTicker(self):
        print(self.symbol)
        print(self.priceUSDT)
        print(self.priceBTC)
        print(self.priceETH)

    def setTicker(self, newTicker):
        self.symbol = newTicker.symbol
        self.priceUSDT = newTicker.priceUSDT
        self.priceBTC = newTicker.priceBTC
        self.priceETH = newTicker.priceETH

    def toList(self):
        return [self.symbol, self.priceUSDT, self.priceBTC, self.priceETH]
    
    

# setup api
api_key = ""
api_secret = ""
client = Client(api_key, api_secret)


# functions/events
def quitProgram(button):
    if button == "Quit":
        app.stop()
    #else:


def updateLabel(self):
    #num = getPrice()
    app.setLabel("BTCUSDT_Price", num)

def updatePrice():
    while(True):
        global tickerList
        
        for ticker in tickerList:
            ticker.setTicker(getTickerPrices(ticker.symbol))

        if app.getTableRowCount("symbolTable") > 0:
            app.deleteAllTableRows("symbolTable")

        for ticker in tickerList:
            app.addTableRow("symbolTable", ticker.toList())
            #app.queueFunction(app.addTableRow("symbolTable", ticker.toList()))
        
        time.sleep(0.1)

def addTicker(btn):
    global tickerList
    global currentSymbol
    currentSymbol = app.getEntry("entryTicker")
    if btn == "Add":
        tickerList.append(getTickerPrices(currentSymbol))

def getTickerPrices(ticker):
    try:
        BTC = 0.0
        ETH = 0.0
        USDT = 0.0
        if ticker != "USDT":
            USDT = client.get_symbol_ticker(symbol=currentSymbol+"USDT")["price"]
        if ticker != "BTC":
            BTC = client.get_symbol_ticker(symbol=currentSymbol+"BTC")["price"]
            if ticker != "ETH":
                ETH = client.get_symbol_ticker(symbol=currentSymbol+"ETH")["price"]
        
        return Ticker(ticker, USDT, BTC, ETH)
    except:
        print("Error adding ticker")

#globals
tickerList = []
update = True
currentSymbol = ""


# create a GUI variable called app
app = gui("Login Window", "800x600")
app.setFont(18)


# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "Crypto", colspan=2)

row = app.getRow()
app.addEntry("entryTicker", colspan=2)


row = app.getRow()
tableHeader = [["Symbol", "USDT", "BTC", "ETH"]]
app.addTable("symbolTable", tableHeader, row, colspan=2)


# link the buttons to the function called press
row = app.getRow()
app.addButtons(["Add"], addTicker, row, 0)
app.addButtons(["Quit"], quitProgram, row, 1)


app.setFocus("entryTicker")

# start the GUI
app.thread(updatePrice)
app.go()

#app.setPollTime(1)
