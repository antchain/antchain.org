#!/usr/bin/python

import pymongo
import urllib2
import json
import time
from decimal import Decimal
from sys import argv

import addressbuilder

def ENUM(**enums):
	return type('Enum', (), enums)

CoinState = ENUM( Unconfirmed=0, Confirmed=1<<0, Spent=1<<1, Vote=1<<2, Claimed=1<<3, Locked=1<<4, Frozen=1<<5, WatchOnly=1<<6 )

def ValidationBlock(block) :
	if block["hash"] is None:
		return False
	if block["size"] is None:
		return False
	if block["version"] is None:
		return False
	if block["previousblockhash"] is None:
		return False
	if block["merkleroot"] is None:
		return False
	if block["time"] is None:
		return False
	if block["height"] is None:
		return False
	if block["nonce"] is None:
		return False
	if block["nextminer"] is None:
		return False
	if block["script"]["stack"] is None:
		return False
	if block["script"]["redeem"] is None:
		return False

	return True

def ValidationTx(tx) :
	if tx["height"] is None:
		return False
	if tx["blockhash"] is None:
		return False
	if tx["time"] is None:
		return False
	if tx["txid"] is None:
		return False
	if tx["size"] is None:
		return False
	if tx["type"] is None:
		return False
	if tx["version"] is None:
		return False
	if tx["attributes"] is None:
		return False
	if tx["vin"] is None:
		return False
	if tx["vout"] is None:
		return False
	if tx["sys_fee"] is None:
		return False
	if tx["net_fee"] is None:
		return False
	if tx["scripts"] is None:
		return False

	return True

def SaveAds(ads) :
    # INSERT ADS
    result = collection_ads.insert_one(ads)
    if result:
        print "[ADS] Insert Address:", ads['address'], "Asset:", ads['asset']
    else:
		raise Exception("[ADS] Insert error!")


def GetPrecisionByAsset(assetid) :
    result = collection_txs.find_one({"txid": assetid})
    if result :
        return result['asset']['precision']
    else :
        raise Exception("[GetPrecisionByAsset] assetid can't find!")

def SaveAddress(coin,time) :
	value = Decimal("0")
	txid_set = set()
	txid_str = "["

	result = collection_ads.find_one({"asset": coin['asset'], "address": coin['address']})
	if result :
		# find one, 'value' 'txid' changes
		for txid in result['txid_list'] :
			txid_set.add(txid['txid'])

		# Check if spent
		n = GetPrecisionByAsset(coin['asset'])
		if n > 0 :
			strvalue = ('%.*f' % (n, result['value'])).rstrip('0')
		else :
			strvalue = str(result['value'])

		if int(coin['state']) & CoinState.Spent == CoinState.Spent:
			value = Decimal(strvalue) - Decimal(coin['value'])
			print "value = ", Decimal(strvalue), " - ", Decimal(coin['value']), " = ", str(value)

			if coin['spent_txid'] not in txid_set:
				txid_set.add(coin['spent_txid'])
				txid_str = txid_str + '{"txid":"' + coin['spent_txid'] + '","height":' + str(coin['height']) + '}'
		else:
			value = Decimal(strvalue) + Decimal(coin['value'])
			print "value = ", Decimal(strvalue), " + ", Decimal(coin['value']), " = ", str(value)

			if coin['txid'] not in txid_set:
				txid_set.add(coin['txid'])
				txid_str = txid_str + '{"txid":"' + coin['txid'] + '","height":' + str(coin['height']) + '}'

		# fill txid_list
		for txid in result['txid_list']:
			if len(txid_str) == 1 :
				txid_str = txid_str + '{"txid":"' + txid['txid'] + '","height":' + str(txid['height']) + '}'
			else :
				txid_str = txid_str + ',{"txid":"' + txid['txid'] + '","height":' + str(txid['height']) + '}'

		txid_str = txid_str + "]"

		if value.compare(Decimal("0")) == Decimal("0"):
			value = Decimal("0")

		if value.compare(Decimal("0")) == Decimal('-1'):
			raise Exception("[SaveAddress] value < 0")

		last_tx_time = time
		txid_array = json.loads(txid_str)

		# asset - address
		json_str = '{"value":%s, "last_tx_time":%d, "txid_list":%s}' % (value, last_tx_time, txid_str)
		sets = json.loads(json_str)
		result = collection_ads.update_one({"asset": coin['asset'], "address": coin['address']},{"$set":sets})

		if result.modified_count == 1 :
			print "[ADS] Update Address:", coin['address'], "Asset:", coin['asset']
		else :
			raise Exception("[ADS] Update Address error!")

		# address
		json_str = '{"last_tx_time":%d, "txid_list":%s}' % (last_tx_time, txid_str)
		sets = json.loads(json_str)
		result = collection_ads.update_one({"asset": "0", "address": coin['address']}, {"$set": sets})

		if result.modified_count == 1:
			print "[ADS] Update Address:", coin['address'], "Asset: 0"
		else:
			print "[ADS] Update Address:", coin['address'], "Asset: 0, No Changes."

	else :
		# not find, insert new one

		# Check if spent
		if int(coin['state']) & CoinState.Spent == CoinState.Spent:
			raise Exception("first coin tx couldn't be spent.")
		else:
			value = Decimal(coin['value'])

		first_tx_time = time
		last_tx_time = time

		# asset - address
		json_str = '{"asset":"%s", "address":"%s", "value":%s, "first_tx_time":%d, "last_tx_time":%d, "txid_list":[{"txid":"%s","height":%d}]}' % (coin['asset'], coin['address'], value, first_tx_time, last_tx_time, coin['txid'], coin['height'])
		ads = json.loads(json_str)
		SaveAds(ads)

		# address
		json_str = '{"asset":"0", "address":"%s", "value":0, "first_tx_time":%d, "last_tx_time":%d, "txid_list":[{"txid":"%s","height":%d}]}' % (coin['address'], first_tx_time, last_tx_time, coin['txid'], coin['height'])
		ads = json.loads(json_str)
		SaveAds(ads)


def GetBlockByHeight(height) :
	data = {"jsonrpc":"2.0", "method":"getblock", "params":[height,1], "id":5}
	headers = {'Content-Type': 'application/json'}
	request = urllib2.Request(url=urls,headers=headers,data=json.dumps(data))

	try :
		response = urllib2.urlopen(request)
	except :
		print "height:", height," urlopen error, retry."
		return None

	block = json.loads(response.read())
	return block['result']

def SaveBlocks(blockdata) :
	# INSERT BLOCK
	if not ValidationBlock(blockdata) :
		raise Exception("[BLOCKS] Validation ERROR!")

	result = collection_blocks.insert_one( blockdata )
	if result :
		print "[BLOCK] Insert Height:", blockdata['height'], "BlockHash:", blockdata['hash']
	else :
		raise Exception("[BLOCKS] Insert error!")

def SaveCoinsOutput(tx,vouts) :
	# PREPARE INSERT COINS
	vout_array = []
	for vout in vouts :
		vout['height'] = tx['height']
		vout['txid'] = tx['txid']
		vout['state'] = CoinState.Confirmed
		#del vout['high']
		#del vout['low']

		#save vout to ads
		SaveAddress(vout,tx['time'])

		vout_array.append(vout)
		#print "[COINS] Insert Output Prepare, Height:", vout['height'], "txid:", vout['txid'], "index:", vout['n']

	#INSERT COINS
	result = collection_coins.insert_many(vout_array)
	if result:
		print "[COINS] Insert output done, Height:", tx['height'], ", txid:", tx['txid'], "vout Num:", len(vouts)
	else:
		raise Exception("[COINS] Insert output error!")


def GetCoinsData(txid,n) :
	#print "GetCoinsData() txid:", txid, "n:", n
	result = list( collection_coins.find({"txid":txid,"n":n}) )
	if result :
		if len(result) == 1 :
			# delete key: _id and return
			del result[0]['_id']
			return result[0]
		else :
			raise Exception("GetCoinsData found not one index.")
	else :
		raise Exception("GetCoinsData not found Date.")

def SaveCoinsInput(tx,vins) :
	# PREPARE INSERT COINS
	#txtype = tx['type']
	vin_array = []
	for vin_ref in vins:
		print "vin_ref[txid]:", vin_ref['txid']
		print "vin_ref[vout]:", vin_ref['vout']
		vin = GetCoinsData(vin_ref['txid'],vin_ref['vout'])
		vin['height'] = tx['height']
		vin['state'] = vin['state'] | CoinState.Spent
		vin['spent_txid'] = tx['txid']

		# save vin to ads
		SaveAddress(vin,tx['time'])

		vin_array.append(vin)
		# print "[COINS] Insert Input Prepare, Height:", vin['height'], "txid:", vin['txid'], "index:", vin['n']

	# INSERT COINS
	result = collection_coins.insert_many(vin_array)
	if result:
		print "[COINS] Insert input done, Height:", tx['height'], ", txid:", tx['txid'], "vout Num:", len(vins)
	else:
		raise Exception("[COINS] Insert input error!")


def SaveTxs(blockdata,txs) :
	# PREPARE INSERT TXS
	tx_array = []
	for tx in txs:
		tx['height'] = blockdata['height']
		tx['blockhash'] = blockdata['hash']
		tx['time'] = blockdata['time']
		if not ValidationTx(tx):
			raise Exception("[TXS] Validation ERROR!")

		tx_array.append(tx)

		# if have input
		if len(tx['vin']) > 0:
			SaveCoinsInput(tx, tx['vin'])

		# if have output
		if len(tx['vout']) > 0 :
			SaveCoinsOutput(tx,tx['vout'])

		print "[TXS] Insert Prepare, Height:", tx['height'], "TxHash:", tx['txid']

	# INSERT TXS
	result = collection_txs.insert_many( tx_array )
	if result :
		print "[TXS] Insert done, Height:", tx['height'], ", Tx Num:", len(txs)
	else :
		raise Exception("[TXS] Insert error!")


def KeepCoinsToHeight(height) :
	result = collection_coins.delete_many({'height': {'$gt':height}})
	if result.deleted_count == 0 :
		print "[KeepCoinsToHeight] Height Result=0"
	elif result.deleted_count < 0 :
		raise Exception("KeepCoinsToHeight fault.")

	print "[KeepCoinsToHeight] Success, Height deleted_count:", result.deleted_count,"now height:", height


def KeepTxsToHeight(height) :
	result = collection_txs.delete_many({'height':{'$gt':height}})
	if result.deleted_count <=0 :
		raise Exception("KeepTxsToHeight fault.")

	print "[KeepTxsToHeight] Success, deleted_count:", result.deleted_count,"now height:", height

def KeepBlocksToHeight(height) :
	result = collection_blocks.delete_many({'height':{'$gt':height}})
	if result.deleted_count <=0 :
		raise Exception("KeepBlocksToHeight fault.")

	print "[KeepBlocksToHeight] Success, deleted_count:", result.deleted_count,"now height:", height


def GetSyncHeightFromDB() :
	# Find height in mongodb
	blocks_height = -1
	txs_height    = -1

	result = collection_blocks.find().sort("height",-1).limit(1)
	if result :
		for blockx in result:
			blocks_height = blockx['height']
			break

	result = collection_txs.find().sort("height",-1).limit(1)
	if result :
		for txx in result:
			txs_height = txx['height']
			break

	if txs_height < blocks_height :
		KeepCoinsToHeight(txs_height)
		KeepBlocksToHeight(txs_height)

	return txs_height + 1


def BuildIndex() :
	collection_blocks.ensure_index("height",unique=True)
	collection_blocks.ensure_index("hash", unique=True)

	collection_txs.ensure_index("txid", unique=True)
	collection_txs.ensure_index("height", unique=False)
	collection_txs.ensure_index("blockhash", unique=False)
	collection_txs.ensure_index("type", unique=False)

	collection_coins.ensure_index([("asset",1),("address",1)])
	collection_coins.ensure_index([("txid", 1), ("n", 1)])

	collection_ads.ensure_index([("asset", 1), ("address", 1)])
	print "Build Index Success."


def GetCurrentHeight() :
	data = {"jsonrpc": "2.0", "method": "getblockcount", "params": [0], "id": 5}
	headers = {'Content-Type': 'application/json'}
	request = urllib2.Request(url=urls, headers=headers, data=json.dumps(data))

	try:
		response = urllib2.urlopen(request)
	except:
		print "GetCurrentHeight() urlopen error, retry."
		return None

	rpcdata = json.loads(response.read())
	print "[GetCurrentHeight] Success, Current Height:", rpcdata['result']

	return rpcdata['result']


def RollbackToHeight(height) :
	KeepCoinsToHeight(height)
	KeepTxsToHeight(height)
	KeepBlocksToHeight(height)
	addressbuilder.RebuildAddress()

	print "RollbackToHeight: " + str(height) + ", Success."

#-----------------------------------------------
# MAIN START
#-----------------------------------------------
urls = 'http://seed3.antshares.org:10332'
client = pymongo.MongoClient("localhost", 27017)

db = client.antchain_main
collection_blocks	= db.blocks
collection_txs		= db.txs
collection_coins	= db.coins
collection_ads		= db.ads

# Get height
height = GetSyncHeightFromDB()
print "SYNC FROM HEIGHT:", height

if len(argv) > 1 :
	pyscript,height_argv = argv
	rollback_height = int(height_argv)
	if (rollback_height > 0) and (rollback_height < height) :
		inputstr = raw_input("Rollback to Height: "+height_argv+" ? (Y/N)")
		if inputstr == "Y" or inputstr == "y" :
			RollbackToHeight(rollback_height)
		else :
			print "Cancle rollback, halt."
	exit()

# Main loop to get block
while 1 :
	# Get Current Height
	current_height = None
	while ( current_height == None ) :
		current_height = GetCurrentHeight()

	# Continue if height equal
	while ( height < current_height ) :

		blockdata = None
		while (blockdata == None):
			blockdata = GetBlockByHeight(height)

		txs = blockdata['tx']
		blockdata['txnum'] = len(txs)
		del blockdata['tx']
		del blockdata['confirmations']

		SaveBlocks(blockdata)
		SaveTxs(blockdata, txs)

		height = height + 1
		#break

	#break
	time.sleep(15)
