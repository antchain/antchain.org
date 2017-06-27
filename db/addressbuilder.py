#!/usr/bin/python

import pymongo
import json
from decimal import Decimal

def ENUM(**enums):
	return type('Enum', (), enums)

CoinState = ENUM( Unconfirmed=0, Confirmed=1<<0, Spent=1<<1, Vote=1<<2, Claimed=1<<3, Locked=1<<4, Frozen=1<<5, WatchOnly=1<<6 )

def GetTimeByBlockHeight(height) :
    result = collection_blocks.find_one({"height":height})
    return result['time']

def GetHeightByTxid(txid) :
    result = collection_txs.find_one({"txid": txid})
    if result == None :
        print "txid is None: " + txid
    return result['height']

def SaveAds(ads) :
    # INSERT ADS
    result = collection_ads.insert_one(ads)
    if result:
        print "[ADS] Insert Address:", ads['address'], "Asset:", ads['asset']
    else:
        print "[ADS] Insert error!"

def SaveAssetAddress(asset,address) :
    #print "Asset:", asset,"Address:", address
    i = 0
    value = Decimal("0")
    txid_set = set()
    txid_list = []

    results = collection_coins.find({"asset":asset,"address":address}).sort("height",-1)
    for result in results :
        #print "coinsHeight: " + str(result['height'])
        if i == 0 :
            first_tx_time = GetTimeByBlockHeight( result['height'] )

        # Check if spent
        if int(result['state']) & CoinState.Spent == CoinState.Spent :
            value = Decimal(value) - Decimal(result['value'])
            print "value -", Decimal(result['value']), "value:", value

            if result['spent_txid'] not in txid_set:
                txid_set.add(result['spent_txid'])
                txid_list.append( {'txid':result['spent_txid'],'height':str(GetHeightByTxid(result['spent_txid']))} )
        else :
            value = Decimal(value) + Decimal(result['value'])
            print "value +", Decimal(result['value']), "value:", value

            if result['txid'] not in txid_set:
                txid_set.add(result['txid'])
                txid_list.append( {'txid':result['txid'],'height':str(result['height'])} )

        i = i + 1

    if value.compare(Decimal("0")) == Decimal("0") :
        value = Decimal("0")

    if value.compare(Decimal("0")) == Decimal('-1'):
        raise Exception("[SaveAddress] value < 0")

    last_tx_time = GetTimeByBlockHeight(result['height'])

    ads_dict = {}
    ads_dict['asset'] = asset
    ads_dict['address'] = address
    ads_dict['value'] = str(value)
    ads_dict['first_tx_time'] = first_tx_time
    ads_dict['last_tx_time'] = last_tx_time
    ads_dict['txid_list'] = txid_list

    SaveAds(ads_dict)


def SaveAddress(address) :
    i = 0
    txid_set = set()
    txid_list = []

    results = collection_coins.find({"address": address}).sort("height", -1)
    for result in results:
        if i == 0:
            first_tx_time = GetTimeByBlockHeight(result['height'])

        # Check if spent
        if int(result['state']) & CoinState.Spent == CoinState.Spent:
            if result['spent_txid'] not in txid_set:
                txid_set.add(result['spent_txid'])
                txid_list.append( {'txid':result['spent_txid'],'height':str(GetHeightByTxid(result['spent_txid']))} )
        else:
            if result['txid'] not in txid_set:
                txid_set.add(result['txid'])
                txid_list.append( {'txid':result['txid'],'height':str(result['height'])} )

        i = i + 1

    last_tx_time = GetTimeByBlockHeight(result['height'])

    ads_dict = {}
    ads_dict['asset'] = "0"
    ads_dict['address'] = address
    ads_dict['value'] = "0"
    ads_dict['first_tx_time'] = first_tx_time
    ads_dict['last_tx_time'] = last_tx_time
    ads_dict['txid_list'] = txid_list

    SaveAds(ads_dict)


def RebuildAddress() :
    # Clear address collection first
    collection_ads.remove({})

    asset_results = collection_coins.distinct("asset")
    for asset in asset_results:
        address_asset_results = collection_coins.distinct("address", {"asset": asset})
        for address in address_asset_results:
            SaveAssetAddress(asset, address)

    address_results = collection_coins.distinct("address")
    for address in address_results:
        SaveAddress(address)

#-----------------------------------------------
# MAIN START
#-----------------------------------------------

client = pymongo.MongoClient("localhost", 27017)
db = client.antchain_main
collection_blocks = db.blocks
collection_txs    = db.txs
collection_coins  = db.coins
collection_ads    = db.ads

#RebuildAddress()
