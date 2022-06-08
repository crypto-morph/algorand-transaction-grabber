import requests
import sys
import codecs
from time import time

wallet="UGF55QR3K6RMEKFKA7TCXZXXWN6V5ZDP5VYYSN24ZQQNJ4SKRS4USWYVAI"

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

def lookupAsset(asset_id):
  global assets
  if (asset_id not in assets):
    url_asset_id = f'https://algoindexer.algoexplorerapi.io/v2/assets/{asset_id}'
    asset_id_info = requests.get(url_asset_id).json()
    asset_name = asset_id_info['asset']['params']['name']
    asset_ticker =asset_id_info['asset']['params']['unit-name']
    assets[asset_id] = asset_ticker
  else:
    asset_ticker = assets[asset_id]
  return(repr(asset_ticker))

def getTxn(next_id):
  if (next_id == 0):
   url= 'https://algoindexer.algoexplorerapi.io/v2/accounts/' + wallet + '/transactions'
  else:
   url= 'https://algoindexer.algoexplorerapi.io/v2/accounts/' + wallet + '/transactions?next=' + next_id  
  return requests.get(url).json()

def printTxn(data):
  data = data['transactions']
  for item in data:
    match item['tx-type']:
      case 'appl':
        try:
        #if(item.get('inner-txns')):
          uprint(str(item['round-time']) + "," + str(lookupAsset(item['inner-txns'][0]['asset-transfer-transaction']['asset-id'])) + "," + str(item['inner-txns'][0]['asset-transfer-transaction']['amount']) + "," + item['sender'] + "," + item['inner-txns'][0]['asset-transfer-transaction']['receiver'] + "," + item['tx-type'])
        except:
         True
         # print(",,,,APPL line failed to parse")
         #else:
         #print(item)
         #print(',,,,Application Create Transaction(appl)')
      case 'pay':
        uprint(str(item['round-time']) + "," + 'Algo,' + str(item['payment-transaction']['amount']) + "," + item['sender'] + "," + item['payment-transaction']['receiver'] + "," + item['tx-type'])
      case 'afrz':
        True
        #print(',,,,Asset Freeze Transaction(afrz)')
      case 'keyreg':
        True
        #print(',,,,Key Registration Transaction(keyreg)')
      case 'axfer':
        uprint(str(item['round-time']) + "," + str(lookupAsset(item['asset-transfer-transaction']['asset-id'])) + "," + str(item['asset-transfer-transaction']['amount']) + "," + item['sender'] + "," + item['asset-transfer-transaction']['receiver'] + "," + item['tx-type'])
      case 'acfg':
        uprint(str(item['round-time']) + ',,,,,Asset Configuration Transaction(acfg)')
      case 'pay':
        uprint(str(item['round-time']) + "," + str(lookupAsset(item['asset-transfer-transaction']['asset-id'])) + "," + str(item['asset-transfer-transaction']['amount']) + "," + item['sender'] + "," + item['asset-transfer-transaction']['receiver'] + "," + item['tx-type'])
      case _:
        uprint ("weird row")
        uprint (item)


assets = dict()

print ("round-time,asset-id, amount, sender, receiver, tx-type")

data = getTxn(0)
while (data['next-token']):  
  printTxn(data)
  data = getTxn(data['next-token'])
