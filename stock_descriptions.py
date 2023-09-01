from tools import marketaux_functions as marketaux
from tools import openai_functions as openai
from tools import yfinance_functions as yfinance
from tools import joplin_functions as joplin


notebook_name = "Individual Stocks"



def getTicker(full_name):
    return full_name[:str(full_name).index(" ")]




def create_stock_description(full_name):
    ticker = getTicker(full_name)

    #| # TCKR | Stock Name Inc.
    data = '# ' + str(full_name) + "\n\n" 

    #| Sector | Industry | Country | Exchange

    #| ### Overview
    #| OpenAI Generated Overview.

    #| ### Resources
    #| - Finviz, Yahoo finance, Tradingview, EarningsWhisper, etc.
    opening_prompt = 'I am making a journal entry for some stocks that look interesting to me, I need for you to fill in the template with the relevant information about the stock. I will give you an example for the input "IONQ | IonQ, Inc.":\nTechnology | Semiconductors | USA | NYSE\n\n### Overview\n\nIonQ, Inc. is a technology company focused on quantum computing. The company develops and manufactures quantum computers that leverage the principles of quantum mechanics to perform complex calculations. IonQ aims to advance the field of quantum computing by providing powerful and scalable quantum hardware for various applications, including optimization, cryptography, and material science. The company is headquartered in College Park, Maryland.\n\n### Resources\n- [Finviz](https://finviz.com/quote.ashx?t=IONQ)\n- [Yahoo Finance](https://finance.yahoo.com/quote/IONQ/?p=IONQ)\n- [Google News](https://news.google.com/search?q=IONQ&hl=en-US&gl=US&ceid=US%3Aen)\n- [Stock Analysis](https://stockanalysis.com/stocks/ionq/)\n- [MarketWatch](https://www.marketwatch.com/investing/stock/ionq)\n- [TradingView](https://www.tradingview.com/chart/?symbol=IONQ)\n- [EarningsWhisper](https://www.earningswhispers.com/stocks/IONQ)\n- [StockTwits](https://stocktwits.com/symbol/IONQ)\n\n End example prompt, now Generate for the stock "'+str(full_name)+'"'
    
    output = openai.send_gptprompt(opening_prompt,tokens=2500)

    #| ## News / Catalysts
    data = data + output + "\n\n## News / Catalysts\n"

    # Adding in the news/catalysts
    news = marketaux.get_news(ticker=ticker)
    data = data + news + "\n\n"
    
    # Yada Yada this is where my analysis needs to go, maybe get some of this automated, is there a tradingview api?
    
    #| ## Comments

    #| # Analysis

    #| ## Technical Analysis
    #| - Moving Averages, RSI, etc.

    #| ## Risk Management + Trading Plan
    #| - Risk Percent, Entry Point, etc.
    data = data + "## Comments\n" + "(leave blank)\n\n" + "# Analysis\n\n" + "## Technical Analysis\n"+ "- Moving Averages: (include relevant MA values)\n"+ "- RSI: (current value)\n"+ "- Chart Patterns: (mention any relevant patterns)\n"+ '- Trading Volume: (analyze recent volume trends)\n'+ "- Support: (identify key support levels)\n"+ "- Resistance: (identify key resistance levels)\n\n\n\n"+ "## Risk Management + Trading Plan\n"+ "- Risk Percentage: (how much you're willing to risk per trade)\n"+ "- Entry Point: (your planned entry price)\n"+ "- Stop-Loss: (your determined stop-loss level)\n"+ "- Trading Timeframe: (daily, weekly, etc.)\n"+ "- Market Trend: (bullish, bearish, sideways)\n"+ "- Profit Target: (your target price for taking profits)\n"+ "- Rationale: (explain the reasons behind your trade decisions)\n\n\n\n"

    #| ## Price Action
    #| Inserting price action of recent
    data = data + "## Price Action\n"
    data = data + yfinance.get_pricedata(ticker=ticker) + "\n\n"

    #| ## Comments
    data = data + "## Comments\n\n"

    # Adding the full note to Joplin.
    notebook_id = joplin.get_notebook(name=notebook_name)
    joplin.api.add_note(title=str(full_name),body=data, parent_id=notebook_id)

    print(data)
    return data

#create_stock_description("EYPT | EyePoint Pharmaceuticals, Inc.")




def update_stock_description(full_name,header,data,overwrite=False):
    note_id=joplin.get_note(name=full_name)
    notedata = joplin.api.get_note(id_=note_id,fields="body, title")
    body = notedata.body
    
    # Check make sure the heading exists
    if header not in body:
        print("The header is not contained in the body!")
        return "The header is not contained in the body!"
    
    post = body[body.index(header)+len(header):]
    pre = body[:body.index(header)+len(header)]

    if overwrite==True:
        # Do overwrite of section
        
        return data
    elif overwrite==False:
        # Do append
        new_dat =  pre + data + post
        print(new_dat)
        joplin.api.modify_note(id_=note_id,body=new_dat)
        return data
    else:
        # Error the mode is incorrect
        print("Only do mode='w' or 'a' for write or append")
        return "Only do mode='w' or 'a' for write or append"

#update_stock_description("testarticle","## Header 1\n","HEllo",False)



def update_news(full_name):
    ticker = getTicker(full_name=full_name)
    news = marketaux.get_news(ticker=ticker,daysprior=1)
    
    if "No news found on" in news:
        print("No news!")
        return "No news!"
    
    update_stock_description(full_name,header="## News / Catalysts\n",data=news,overwrite=False)

#update_news("EYPT | EyePoint Pharmaceuticals, Inc.")



def update_price(full_name):
    ticker = getTicker(full_name=full_name)
    price = yfinance.get_pricedata(ticker=ticker,period="1d")

    update_stock_description(full_name,header="## Price Action\n",data=price,overwrite=False)

#update_price("EYPT | EyePoint Pharmaceuticals, Inc.")




