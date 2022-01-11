# -*- coding: utf-8 -*-
import csv
from os import wait
import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
headless = False

exo = True
tradeit = True
lootfarm = True
swap = True


# intial setup
minDesiredPrice = 0
maxDesiredPrice = 999999

#names
csgoexoFinalNames = []
lootfarmFinalNames = []
swapggFinalNames = []
tradeitFinalNames = []

lootfarmSellNames = []
swapggSellNames = []

#buyprices
buycsgoexo = []
buylootfarm = []
buyswapgg = []
buytradeit = []

NamesWithMax = []
editedNames = []
maxCount = []

#sellprices
sellswapgg = []
selllootfarm = []
sellcsgoexo = []
selltradeit = []

options = webdriver.ChromeOptions()
if headless:
    options.headless = True
profile = webdriver.FirefoxProfile()
driver = webdriver.Chrome(executable_path=r'/home/max/Documents/PythonProjects/requestAixieBot/chromedriver_linux64/chromedriver', options=options)
driver.set_window_size(1920, 1080)

#grab all buy prices===============================================================================================================
#
if exo:
    driver.get("https://csgoexo.com/")
    time.sleep(11)
    driver.execute_script("window.scrollTo(0, 800);")

    # loops through the process until the min value reaches a certain value on CSGOEXO.com
    loop = True
    while loop:
        time.sleep(1)
        prices = driver.find_elements_by_class_name("csgo-item--price")  # grabs prices
        names = driver.find_elements_by_class_name("csgo-item--bg")  # grabs pic links with name in them

        # loops through all gathered prices and removes "$"
        for i in prices:
            if i.text == "Unavailable":
                names.pop(prices.index(i))
            else:
                priceVal = float(i.text.replace("$", ""))
                buycsgoexo.append(priceVal)
                sellcsgoexo.append(round(priceVal * .95, 4)) #append to sell prices

        # loops through all gathered name links
        for i in names:
            url = i.get_attribute("style")
            itemName = url.replace('background-image: url("https://items.csgoexo.com/', "")
            itemName = itemName.replace('-or-', " | ")
            itemName = itemName.replace('-%28', " ")
            itemName = itemName.replace('-', " ")
            itemName = itemName.replace('%29.png");', "")
            itemName = itemName.replace('stattraktm', "StatTrak")
            itemName = itemName.replace(" Doppler Phase 1", "")
            itemName = itemName.replace(" Doppler Phase 2", "")
            itemName = itemName.replace(" Doppler Phase 3", "")
            itemName = itemName.replace(" Doppler Phase 4", "")
            itemName = itemName.replace("factory new", "(factory new)")
            itemName = itemName.replace("minimal wear", "(minimal wear)")
            itemName = itemName.replace("field tested", "(field-tested)")
            itemName = itemName.replace("well worn", "(well-worn)")
            itemName = itemName.replace("battle scarred", "(battle-scarred)")

            csgoexoFinalNames.append(itemName.lower())

        time.sleep(1.5)
        lastPrice = str(round(float(buycsgoexo[len(buycsgoexo) - 1]) - 1))

        # sets max price to last min price taken
        priceBox = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div[2]/div[3]/input[2]")
        priceBox.click()
        actions = ActionChains(driver)
        actions.send_keys(Keys.ARROW_RIGHT)
        actions.send_keys(Keys.ARROW_RIGHT)
        actions.send_keys(Keys.ARROW_RIGHT)
        actions.send_keys(Keys.ARROW_RIGHT)
        actions.key_down(Keys.SHIFT)
        actions.send_keys(Keys.ARROW_LEFT)
        actions.send_keys(Keys.ARROW_LEFT)
        actions.send_keys(Keys.ARROW_LEFT)
        actions.send_keys(Keys.ARROW_LEFT)
        actions.send_keys(Keys.ARROW_LEFT)
        actions.send_keys(Keys.ARROW_LEFT)
        actions.key_up(Keys.SHIFT)
        actions.send_keys(lastPrice)
        actions.perform()
        time.sleep(1.5)

        # stops the scraping when the minimum item value is less than 20 dollars
        if round(float(lastPrice)) <= minDesiredPrice+1:
            loop = False

    print("done with exo")

last = 100000
offset = 0
while(last > minDesiredPrice + .1):
    url = str("https://tradeit.gg/api/v2/inventory/data?gameId=730&offset=" + str(offset) + "&limit=100&sortType=Price+-+high&minPrice=0&maxPrice=100000&fresh=true")
    driver.get(url)
    loop = True
    while(loop):
        try:
            driver.find_element_by_id("rawdata-tab").click()
            loop = False
        except:
            loop = True
    r = driver.find_element_by_class_name("data").text
    data = json.loads(r)

    itemsList = data['items']
    items = list(itemsList)

    prices = []
    for current in items:
        price = ((float(current["price"])) / 100)
        buytradeit.append(price)
        selltradeit.append(round(price * .93, 4))
        tradeitFinalNames.append(current["name"].lower().replace("stattrak™", "stattrak").replace("★ ", ""))
    last = buytradeit[len(buytradeit)-1] - .01
    offset = offset + 100
print("done with tradeit")

# lootfarm==============================================================================================================
if lootfarm:
    driver.get("https://loot.farm/")
    time.sleep(7)
    driver.execute_script("window.scrollTo(0, 500);")
    driver.find_element_by_id('moreSearchBack').click()
    # loops through process until it reaches the minimum value on tradeit.gg
    if maxDesiredPrice > 0:
        for x in range(9):
            driver.find_element_by_id('PriceHighFilter').send_keys(Keys.BACK_SPACE)
            driver.find_element_by_id('PriceHighFilter').send_keys(Keys.BACK_SPACE)
            time.sleep(.25)
        driver.find_element_by_id('PriceHighFilter').send_keys(maxDesiredPrice)

    count = 0
    loop = True
    while loop:
        time.sleep(2)
        items = driver.find_elements_by_class_name("itemblock")
        for i in items:
            price = float(i.get_attribute("data-p")) / 100
            buylootfarm.append(price)

        for i in items:
            name = i.get_attribute("data-name").lower()
            name = name.replace('(', "")
            name = name.replace(')', "")
            name = name.replace("★ ", "")
            name = name.replace("Battle-Scarred", "(Battle-Scarred)")
            name = name.replace("Well-Worn", "(Well-Worn)")
            name = name.replace("Field-Tested", "(Field-Tested)")
            name = name.replace("Minimal wear", "(Minimal Wear)")
            name = name.replace("factory new", "(Factory New)")
            name = name.replace("™", "")
            lootfarmFinalNames.append(name.lower())

        time.sleep(4)
        lastPrice = int((buylootfarm[len(buylootfarm) - 1]-.05))
        if float(lastPrice) < .15:
            loop = False

        # sets max price to last min price taken
        for x in range(0, 7):
            driver.find_element_by_id('PriceHighFilter').send_keys(Keys.BACK_SPACE)
            time.sleep(.5)
        driver.find_element_by_id('PriceHighFilter').send_keys(lastPrice)
#
# print("done with lootfarm")

# swapgg==============================================================================================================
if swap:
    r = requests.get('https://api.swap.gg/inventory/bot/730')

    resp = r.json()
    resp2 = (resp['result'])

    for item in resp2:
        name = (item['n'])
        price = (item['p'])
        name = name.replace("™", "")
        name = name.replace("★ ", "")
        buyswapgg.append(float(float(price) / 100))
        swapggFinalNames.append(name.lower())

#SELL PRICES==========================================================================================
#csgoexo.com in buy prices
#tradeit in buy prices

#lootfarm
prices = []
names = []

r = requests.get('https://loot.farm/fullprice.json')
resp = r.json()

for item in resp:
    prices.append(float(item['price']) / 100)
    names.append(item['name'])

targetNames = []
targetPrices = []
loops = len(prices)
for i in range(0, loops):
    targetNames.append(names[i])
    targetPrices.append(prices[i])

tempnames = []
counter = 0
for i in targetPrices:
    selllootfarm.append(round(i * .97, 4))
    tempnames.append(targetNames[counter])
    counter = counter + 1

for name in tempnames:
    # name = name.replace("(", "")
    # name = name.replace(")", "")
    # name = name.replace("★ ", "")
    # name = name.replace('StatTrak\\u2122', "StatTrak")
    # name = name.replace("Factory New", "(Factory New)")
    # name = name.replace("Minimal Wear", "(Minimal Wear)")
    # name = name.replace("Field-Tested", "(Field-Tested)")
    # name = name.replace("Well-Worn", "(Well-Worn)")
    # name = name.replace("Battle-Scarred", "(Battle-Scarred)")
    lootfarmSellNames.append(name.lower())

#swapgg
r = requests.get('https://api.swap.gg/prices/730')

resp = r.json()
resp2 = (resp['result'])

for item in resp2:
    name = (item['marketName'])
    price = (item['price'])
    price = round(item['price']['sides']['user'] * 1.03, 4)  # add the 3% bonus from name:  # if the price is in the desired parameters
    sellswapgg.append(round(float(price) / 100, 4))
    swapggSellNames.append(name.lower())

driver.close()



#PUT INTO CSV FILES========================================================================
def writefiles(file, prices, names):
    with open(file, mode="w+") as resultfile:
        result_writer = csv.writer(resultfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        counter = 0
        for i in prices:
            result_writer.writerow([names[counter], i])
            counter = counter + 1
#
writefiles('output/swapggbuy.csv', buyswapgg, swapggFinalNames)
writefiles('output/swapggsell.csv', sellswapgg, swapggSellNames)
#
writefiles('output/lootfarmbuy.csv', buylootfarm, lootfarmFinalNames)
writefiles('output/lootfarmsell.csv', selllootfarm, lootfarmSellNames)

writefiles('output/csgoexobuy.csv', buycsgoexo, csgoexoFinalNames)
writefiles('output/csgoexosell.csv', sellcsgoexo, csgoexoFinalNames)

writefiles('output/tradeitbuy.csv', buytradeit, tradeitFinalNames)
writefiles('output/tradeitsell.csv', selltradeit, tradeitFinalNames)