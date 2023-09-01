from tools import marketaux_functions as marketaux
from tools import openai_functions as openai
from tools import yfinance_functions as yfinance
from tools import joplin_functions as joplin
from datetime import datetime, timedelta
from time import sleep

import stock_descriptions


notebook_name = "Individual Stocks"
subnotebook_name = "Journal"



def getTicker(full_name):
    return full_name[:str(full_name).index(" ")]



def update_daily_journal(full_name,header,data,overwrite=False):
    note_id=joplin.get_note(name=full_name)
    notedata = joplin.api.get_note(id_=note_id,fields="body, title")
    body = notedata.body

    # Check make sure the heading exists
    if header not in body:
        print("The header is not contained in the body!" + str(header))
        return "The header is not contained in the body!"

    post = body[body.index(header)+len(header):]
    pre = body[:body.index(header)+len(header)]

    if overwrite==True:
        
        # Do overwrite of section
        new_dat =  pre + data + post[post.index("##")-2:]
        joplin.api.modify_note(id_=note_id,body=new_dat)
        return data

    elif overwrite==False:
        # Do append
        new_dat =  pre + data + post
        joplin.api.modify_note(id_=note_id,body=new_dat)
        return data
    
    else:
        # Error the mode is incorrect
        print("Only do mode='w' or 'a' for write or append")
        return "Only do mode='w' or 'a' for write or append"

#update_daily_journal(str(datetime.today().strftime("%A %m/%d/%Y")),"## Watching\n","HEllo",False)
#update_daily_journal("testarticle","## Header 1\n","HEllo This is a new test!",True)



def load_previous(source):
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%A %m/%d/%Y")

    try:
        note_id=joplin.get_note(name=yesterday)
    except:
        print("Note does not exist from yesterday!")
        return False
    
    notedata = joplin.api.get_note(id_=note_id,fields="body, title")
    body = notedata.body
    
    # Check make sure the heading exists
    if source not in body:
        print("The header is not contained in the body!")
        return "The header is not contained in the body!"
    
    post = body[body.index(source)+len(source):]
    post = post[:post.index("##")-1]

    return post
    


def load_todays(source):
    formatted_date = datetime.today().strftime("%A %m/%d/%Y")

    try:
        note_id=joplin.get_note(name=formatted_date)
    except:
        print("Note does not exist from yesterday!")
        return False
    
    notedata = joplin.api.get_note(id_=note_id,fields="body, title")
    body = notedata.body
    
    # Check make sure the heading exists
    if source not in body:
        print("The header is not contained in the body!")
        return "The header is not contained in the body!"
    
    post = body[body.index(source)+len(source):]
    post = post[:post.index("##")-1]

    return post
    


def update_portfolio():
    # Load in Paper portfolio from yesteday
    portfolio = load_todays("### Paper\n")

    lines = portfolio.split('\n')

    for i in range(len(lines)):
        line = lines[i]

        if str("https://www.tradingview.com/chart") in str(line):

            # We have the top line
            full_name = line[str(line).index("[")+1:str(line).index("]")]
            ticker = getTicker(full_name=full_name)

            line = line[str(line).index(")")+4:]
            line = line.split(" ")

            qty = line[1]
            price_bought = str(line[3])[1:]
            date_bought = line[4]

            # The most recent logged
            formatted_date = datetime.today().strftime("%Y-%m-%d")
            recent = str(lines[i+1])[3:13]
            print("RECENT::" + recent)
            if(str(formatted_date) != str(recent)):
                # [todays_date, open_price, close_price, prev_close, percentage_change]
                print("WE DIFF")
                price_changes = yfinance.get_change(ticker=ticker)
                total_gain = round((float(price_changes[2]) - float(price_bought))*100 / abs(float(price_bought)),3)
                data = "\t- " + str(price_changes[0]) + ": OPEN $" + str(price_changes[1]) + ", CLOSE $" + str(price_changes[2]) + " change " + str(price_changes[4]) + "% on day ("+str(total_gain)+"% TGain)"     
                lines.insert(i+1,data)
            else:
                print("ALL DA SAME")
                a= 1

    remake = ""
    for line in lines:
        remake = remake + line + "\n"

    update_daily_journal(str(datetime.today().strftime("%A %m/%d/%Y")), "### Paper\n", remake, overwrite=True)

    # Also update Real

    # Load in Paper portfolio from yesteday
    portfolio = load_todays("### TD Ameritrade\n")

    lines = portfolio.split('\n')

    for i in range(len(lines)):
        line = lines[i]

        if str("https://www.tradingview.com/chart") in str(line):

            # We have the top line
            full_name = line[str(line).index("[")+1:str(line).index("]")]
            ticker = getTicker(full_name=full_name)

            line = line[str(line).index(")")+4:]
            line = line.split(" ")

            qty = line[1]
            price_bought = str(line[3])[1:]
            date_bought = line[4]

            # The most recent logged
            formatted_date = datetime.today().strftime("%Y-%m-%d")
            recent = str(lines[i+1])[3:13]
            print("RECENT::" + recent)
            if(str(formatted_date) != str(recent)):
                # [todays_date, open_price, close_price, prev_close, percentage_change]
                print("WE DIFF")
                price_changes = yfinance.get_change(ticker=ticker)
                total_gain = round((float(price_changes[2]) - float(price_bought))*100 / abs(float(price_bought)),3)
                data = "\t- " + str(price_changes[0]) + ": OPEN $" + str(price_changes[1]) + ", CLOSE $" + str(price_changes[2]) + " change " + str(price_changes[4]) + "% on day ("+str(total_gain)+"% TGain)"     
                lines.insert(i+1,data)
            else:
                print("ALL DA SAME")
                a= 1

    remake = ""
    for line in lines:
        remake = remake + line + "\n"

    update_daily_journal(str(datetime.today().strftime("%A %m/%d/%Y")), "### TD Ameritrade\n", remake, overwrite=True)

    return "Portfolio updated! " +str(datetime.today().strftime("%H:%M:%S"))

#update_portfolio()



def add_to_portfolio(full_name,account,date,price,shares):
    port = load_todays("### "+str(account)+"\n")
    if(str(full_name) in str(port)):
        # Add in another way?
        return "Already in portfolio!"
    
    ticker = getTicker(full_name=full_name)
    data = "- **["+str(full_name)+"](https://www.tradingview.com/chart/Z6kzaPjp/?symbol="+str(ticker)+")** Purchased " + str(shares) + " @ $" + str(price) + " " + str(date) + " ("+str(account)[str(account).index(" ")+1:str(account).index("\n")]+")\n"

    # [todays_date, open_price, close_price, prev_close, percentage_change]
    price_changes = yfinance.get_change(ticker=ticker)
    total_gain = round((float(price_changes[2]) - float(price))*100 / abs(float(price)),3)
    data = data + "\t- " + str(price_changes[0]) + ": OPEN $" + str(price_changes[1]) + ", CLOSE $" + str(price_changes[2]) + " change " + str(price_changes[4]) + "% on day ("+str(total_gain)+"% TGain)\n"     
    
    update_daily_journal(str(datetime.today().strftime("%A %m/%d/%Y")), account, data=data, overwrite=False)

    return True

#add_to_portfolio("AAOI | Applied Optoelectronics, Inc.", "### Paper\n","08/28/2023","12.99","1000")



def create_daily_journal():

    notename_date = datetime.today().strftime("%A %m/%d/%Y")
    # Check if the file exists first before making a new one!!
    if(joplin.get_note(notename_date) != "NO SUCH NOTES!"):
        print("Daily journal already exists!")
        return "Daily journal already exists!"


    #| # Wednesday 08/30/2023
    #| **Tracker:** [finviz](tracker)

    #| ## Todo's

    #| ## Watching
    formatted_date = datetime.today().strftime("# %A %m/%d/%Y")
    data = formatted_date + "\n**Tracker:** [finviz](totallythelink)\n\n***\n## Todo's\n\n\n***\n## Watching\n\n### NEW WATCHING!\n"

    # Can add in new watching now:

    data = data + "\n### OLD WATCHING!\n"

    data = data + "\n## Buying\n\n### NEW BUYING!\n"

    # Add in buy data

    data = data + "\n## Selling\n"

    # Add in sell data

    data = data + "\n## Portfolio\n\n### Paper\n"

    # Add in paper trading account from yesterday?
    # Add in buys

    data = data + "\n### TD Ameritrade\n"

    # Add in actual trading account from yesterday?

    data = data + "\n\n***\n## Notes\n\n"

    # Adding the full note to Joplin.
    notebook_id = joplin.get_notebook(name=subnotebook_name)
    joplin.api.add_note(title=str(datetime.today().strftime("%A %m/%d/%Y")),body=data, parent_id=notebook_id)

    # Load in old watching stuff from yesterday?
    update_daily_journal(str(datetime.today().strftime("%A %m/%d/%Y")), "### OLD WATCHING!\n", load_previous("### OLD WATCHING!\n"), overwrite=False)
    update_daily_journal(str(datetime.today().strftime("%A %m/%d/%Y")), "### OLD WATCHING!\n", load_previous("### NEW WATCHING!\n"), overwrite=False)

    # Load in old portfolio

    return "Created daily journal document!"

#print(create_daily_journal())



def add_to_todo(task):
    daily_name = str(datetime.today().strftime("%A %m/%d/%Y"))
    update_daily_journal(full_name=daily_name,header="## Todo's\n",data="- [ ] " + str(task) + "\n",overwrite=False)

#add_to_todo("Finish Screening")



def add_to_watching(full_name):
    daily_name = str(datetime.today().strftime("%A %m/%d/%Y"))
    note_id=joplin.get_note(name=full_name)
    ticker = getTicker(full_name=full_name)

    data = "- **" + ticker + ":** "

    if(str(full_name) in str(load_todays("### OLD WATCHING!\n"))):
        print("Already in there!")
        return("Already in there!")

    # openAI shits
    opening_prompt = 'I need to write out small descriptions for a bunch of stocks. I will provide a ticker, please write a description of the stock.  For example an input of "IONQ | IonQ, Inc.": a technology company focused on quantum computing. The company develops and manufactures quantum computers that leverage the principles of quantum mechanics to perform complex calculations. End of example. Please do for ' + full_name

    output = openai.send_gptprompt(opening_prompt,tokens=500)
    #print(output)
    data = data + output

    data = data + "\n\t- **Comments post market close:** Add comment\n\t- ["+full_name+"](:/"+note_id+")\n\t- [TradingView](https://www.tradingview.com/chart/Z6kzaPjp/?symbol="+ticker+")\n"

    # Adds an individual file if it doesn't already exist.
    if(str(note_id) == str("NO SUCH NOTES!")):
        stock_descriptions.create_stock_description(full_name=full_name)
    else:
        print("Exists!")    

    update_daily_journal(full_name=daily_name,header="### NEW WATCHING!\n",data=data,overwrite=False)

    add_to_todo("Finish Analyzing " + str(ticker) + " for " + daily_name)

    return "Added " + str(ticker) + " to Watchlist!"

#add_to_watching("DNA | Ginkgo Bioworks Holdings, Inc.")
#add_to_watching("APLE | Apple Hospitality REIT, Inc.")

#print(joplin.get_note(name="APLE | Apple Hospitality REIT, Inc."))

def add_to_buying(full_name, date, price, shares, account):
    daily_name = str(datetime.today().strftime("%A %m/%d/%Y"))

    note_id=joplin.get_note(name=full_name)
    ticker = getTicker(full_name=full_name)

    if account not in ["Paper", "TD Ameritrade"]:
        print("Not correct input type! Only Paper or TD Ameritrade")
        return "Not correct input type!"

    data = "- **" + str(ticker) + ":** Purchased " + str(shares) + " at $" + str(price) + " on " + str(date) + " ("+str(account)+")\n\t- **Comments:** Add comment\n\t- TradingView Chart\n\t- Stop loss: \n\t- End Goal: \n\t- Time Frame: \n\t- Willing to take: \n\t- [TradingView](https://www.tradingview.com/chart/Z6kzaPjp/?symbol="+str(ticker)+")\n\t- ["+str(full_name)+"](:/"+str(note_id)+")\n"

    # Update journal with the new data
    update_daily_journal(full_name=daily_name,header="### NEW BUYING!\n",data=data,overwrite=False)
    print("Hmm.")
    # Add it to the portfolio section as well
    add_to_portfolio(full_name=full_name, account="### "+str(account)+"\n",date=date,price=price,shares=shares)

    # Add it to a new trade file as well

    return "Adding bought " + str(ticker) + " shares!"

#add_to_buying("VRRM | Verra Mobility Corporation","08/29/2023",17.67,300)



def add_to_sell(full_name, date, price, shares,account):
    daily_name = str(datetime.today().strftime("%A %m/%d/%Y"))

    if account not in ["Paper", "TD Ameritrade"]:
        print("Not correct input type! Only Paper or TD Ameritrade")
        return "Not correct input type!"
    
    ticker = getTicker(full_name=full_name)

    purchased = ""
    prev_portfolio = load_previous("### " + str(account) + "\n")
    #print(prev_portfolio)
    prev_portfolio = prev_portfolio.split("\n")
    for line in prev_portfolio:
        #print(line)
        if str(full_name) in str(line):
            line = line[line.index(")")+4:]
            line = line.split(" ")
            purchased = line[3][1:]
    
    percentage_gain = round((float(price) - float(purchased))*100 / abs(float(purchased)),3)
    money_gain = round((float(price) - float(purchased))*float(shares),2)
  
    selldata = "- **" +str(full_name) + "** Sold " + str(shares) + " shares at $" + str(price) + " on " + str(date) + " ("+str(account)+")\n\t- **Comments:** Add Comments\n\t- TradingView Chart\n\t- Gain: $"+str(money_gain)+" ("+str(percentage_gain)+"%)\n"

    portfolio_data = "\t\t- SOLD! " + str(shares) + " shares @ $" + str(price) + " for a $" + str(money_gain) + " return! ("+str(percentage_gain)+"%)"
    
    # Update journal with the new data
    update_daily_journal(full_name=daily_name,header="## Selling\n",data=selldata,overwrite=False)

    # Update portfolio
    todays_port = load_todays("### " + str(account) + "\n")
    todays_port = todays_port.split('\n')
    for i in range(len(todays_port)):
        line = todays_port[i]
        if str(full_name) in str(line):
            todays_port.insert(i+2,portfolio_data)

    remake = ""
    for line in todays_port:
        remake = remake + line + "\n"

    update_daily_journal(full_name=daily_name,header="## "+str(account)+"\n",data=remake,overwrite=True)

    return True

#add_to_sell("AAOI | Applied Optoelectronics, Inc.","2023-08-30","15.03","100","Paper")