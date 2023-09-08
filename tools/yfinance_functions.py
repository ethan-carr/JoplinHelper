import yfinance as yf
import re

def get_pricedata(ticker,period="5d"):
    stock = yf.Ticker(str(ticker))
    data = str(stock.history(period=period, auto_adjust=False))
    data = data[data.index("\n")+1:]
    data = data[data.index("\n")+1:]
    
    arr = data.split('\n')
    fin = ""
    for ind in arr:
        ind = re.sub(r'\s+', ' ', ind)
        ind = ind.split(" ")
        ind = "- **"+ ind[0] + ":** " + ind[2] + " " + ind[3] + " " + ind[4] + " " + ind[5] + " " + ind[7]

        fin = ind + "\n" + fin
    
    #fin = fin + "Date  Open  High  Low  Close  Volume"
    return(fin)


def get_change(ticker):
    stock = yf.Ticker(str(ticker))
    data = str(stock.history(period="2d", auto_adjust=False))
    data = data[data.index("\n")+1:]
    data = data[data.index("\n")+1:]
    
    arr = data.split('\n')
    new_arr = []
    fin = ""
    for ind in arr:
        ind = re.sub(r'\s+', ' ', ind)
        new_arr.append(ind.split(" "))

    todays_date = new_arr[1][0]
    open_price = new_arr[1][2]
    close_price = new_arr[1][5]
    prev_close = new_arr[0][5]
    percentage_change = str(round((float(close_price) - float(prev_close)) * 100 / abs(float(prev_close)),3))

    return [todays_date, open_price, close_price, prev_close, percentage_change]

#get_change("PIRS")
