from flask import *
import json
import csv
import os

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    return render_template('csTradeWebsite.html')

@app.route('/filtersubmit', methods=['GET', 'POST'])
def foo(): 
    params = request.get_json()
    From = params['from']
    to = params['to']
    min = params['min']
    max = params['max']

    if From == 'swap.gg':
        buyfile = 'output/swapggbuy.csv'
    if From == 'loot.farm':
        buyfile = 'output/lootfarmbuy.csv'
    if From == 'csgoexo.com':
        buyfile = 'output/csgoexobuy.csv'
    if From == 'tradeit.gg':
        buyfile = 'output/tradeitbuy.csv'
    if to == 'swap.gg':
        sellfile = 'output/swapggsell.csv'
    if to == 'loot.farm':
        sellfile = 'output/lootfarmsell.csv'
    if to == 'csgoexo.com':
        sellfile = 'output/csgoexosell.csv'
    if to == 'tradeit.gg':
        sellfile = 'output/tradeitsell.csv'

    buynames = []
    sellnames = []
    buyprices = []
    sellprices = []
    finaldata = []
 
    with open(buyfile, 'r') as f1:
        buyreader = csv.reader(f1, delimiter=",")
        for buyrow in buyreader:
            buynames.append(str(buyrow[0]))
            buyprices.append(float(buyrow[1]))

    with open(sellfile, 'r') as f1:
        sellreader = csv.reader(f1, delimiter=",")
        for sellrow in sellreader:
            sellnames.append(str(sellrow[0]))
            sellprices.append(float(sellrow[1]))

    names = []
    counter = 0
    for i in buynames:
        if i in sellnames:
            if i not in names:
                if float(buyprices[counter]) <= float(max) and float(buyprices[counter]) >= float(min):
                    pos = sellnames.index(i)
                    divided = round(sellprices[pos] / buyprices[counter], 5)
                    finaldata.append([i, buyprices[counter], sellprices[pos], divided])
                    names.append(i)
        counter = counter + 1

    jsondata = json.dumps(finaldata)
    return jsondata

if __name__ == '__main__':
    app.run()