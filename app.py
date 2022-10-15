import smtplib
import requests
import datetime
from lxml import html
import http.client
import os
import json

#############################################################################################
# collect api version

# token = os.environ("collect_api_token")


def wa_gas():
    token = "lol"
    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
        'content-type': "application/json",
        'authorization': token
    }

    conn.request("GET", "/gasPrice/stateUsaPrice?state=WA", headers=headers)

    res = conn.getresponse()
    data = res.read()

    d = data.decode("utf-8")
    d2 = json.loads(data)

    d3 = d2["result"]["cities"][10]["gasoline"]
    return f"Vancouver Average Regular:\n    ${str(d3)[:-1]}"


def get_stock():
    ticker = "NLY"
    api_key = os.environ.get('twelvedata_secretkey')
    url = f"https://api.twelvedata.com/quote?symbol={ticker}&apikey=oo"
    response = requests.get(url).json()
    price_close = f"${response['close'][:-3]}"
    previous_close = f"${response['previous_close'][:-3]}"
    change = f"{response['change'][:-3]}"
    percent_change = f"{response['percent_change'][:-3]}"
    volume = f"{response['volume']}"

    return f"Price Close: {price_close}\nPrevious Close: {previous_close}\nChange: {change}\nPercentage Change: {percent_change}\nVolume: {volume}"



month = str(datetime.datetime.now()).split(" ")[0].split("-")[1]
year = str(datetime.datetime.now()).split(" ")[0].split("-")[0]
day = str(datetime.datetime.now()).split(" ")[0].split("-")[2]

date = f"End of Day Alert: {month}/{day}/{year}"


def send_email():
    my_pass = "ooo"
    my_email = "cejvanniekirk098@gmail.com"
    receiver = "kirko190255@gmail.com" # TODO change to os after restart
    van = wa_gas()
    stock = get_stock()
    message = f"""End of Day Email Alert\n\nUpdates:\n\n----------------\n{van}\n----------------\n{stock}"""
    return message

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
    
        smtp.login(my_email, my_pass)
        subject = f"Daily Update: {month}-{day}-{year}"
        body = message
    
        msg = f"Subject: {subject}\n\n{body}"
    
        smtp.sendmail(my_email, receiver, msg)


send_email()



#
#
#
#



############################################################################################
# Web scraping version


# def get_costco_price():
#     url = "https://www.gasbuddy.com/station/131553"
#     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
#     r = requests.get(url, headers=headers)
#     tree = html.fromstring(r.content)
#     costco = tree.xpath('//*[@id="root"]/div/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[1]/span')
#
#     return f"Costco Gas\n\nRegular:\n{costco[0].text}"
#
#
# def get_arco_price():
#     url = "https://www.gasbuddy.com/station/73616"
#     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
#     r = requests.get(url, headers=headers)
#     tree = html.fromstring((r.content))
#     arco = tree.xpath('//*[@id="root"]/div/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[1]/span')
#
#     return f"ARCO Gas\n\nRegular:\n{arco[0].text}"
#
#
# def get_stock_info():
#     url = 'https://finance.yahoo.com/quote/NLY/'
#     xpath_stock_x = '//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[1]'
#     price_change_x = '//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[2]/span'
#     percentage_change_x = '//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[3]/span'
#     volume_x = '//*[@id="quote-summary"]/div[1]/table/tbody/tr[7]/td[2]/fin-streamer'
#     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
#     r = requests.get(url, headers=headers)
#     tree = html.fromstring(r.content)
#
#     stock_price = tree.xpath(xpath_stock_x)
#     price_change = tree.xpath(price_change_x)
#     percentage_change = tree.xpath(percentage_change_x)
#     volume = tree.xpath(volume_x)
#
#     return f"NLY End of Day Info:\n\nPrice: ${stock_price[0].text}\n{price_change[0].text} {percentage_change[0].text}\nVolume: {volume[0].text}\nTotal Stock Owned: 12.90\nWorth: {10.90 * float(stock_price[0].text)}"
#
#
# # ~~ functions ~~
#
# month = str(datetime.datetime.now()).split(" ")[0].split("-")[1]
# year = str(datetime.datetime.now()).split(" ")[0].split("-")[0]
# day = str(datetime.datetime.now()).split(" ")[0].split("-")[2]
#
# date = f"End of Day Alert: {month}/{day}/{year}"
#
#
# def send_email():
#     my_pass = "wspgulhstrmswxfx"
#     my_email = "cejvanniekirk098@gmail.com"
#     receiver = "kirko190255@gmail.com" # TODO change to os after restart
#     costco = get_costco_price()
#     arco = get_arco_price()
#     stock = get_stock_info()
#     message = f"""End of Day Email Alert\n\nUpdates:\n\n----------------\n{costco}\n\n----------------\n{arco}\n\n----------------\n{stock}"""
#
#     with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
#         smtp.ehlo()
#         smtp.starttls()
#         smtp.ehlo()
#
#         smtp.login(my_email, my_pass)
#         subject = f"Daily Update: {month}-{day}-{year}"
#         body = message
#
#         msg = f"Subject: {subject}\n\n{body}"
#
#         smtp.sendmail(my_email, receiver, msg)
#
#
# send_email()
#
