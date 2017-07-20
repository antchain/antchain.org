# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymongo
import json
import time
import os
import gettext
import re

# put your localpath here
localpath = 'var/www/antchain.org/web/'
zh_trans = gettext.translation('lang', localpath+'locale', languages=['zh_CN'])
en_trans = gettext.translation('lang', localpath+'locale', languages=['en_US'])

#from block import *
import block
import tx
import asset
import ads
import rank
import api

#DEFINE
BLOCK_PER_PAGE = 50
TX_PER_PAGE = 50
ADS_PER_PAGE = 50
ASSET_PER_PAGE = 20
ASSET_ADS_PER_PAGE = 50

def ENUM(**enums):
	return type('Enum', (), enums)

CoinState = ENUM( Unconfirmed=0, Confirmed=1<<0, Spent=1<<1, Vote=1<<2, Claimed=1<<3, Locked=1<<4, Frozen=1<<5, WatchOnly=1<<6 )

##################################################
###
### functions
###
##################################################
def GetLogo() :
	file_logo = open(localpath+'/logo.html')
	try:
		html_logo = file_logo.read()
	finally:
		file_logo.close()

	return html_logo


def GetLocalTime(times) :
	x = time.localtime(times)
	return time.strftime('%Y-%m-%d %H:%M:%S',x)

def GetLanguageByRequest() :
	supported_languages = ["zh_CN", "zh", "en"]
	lang = request.accept_languages.best_match(supported_languages)
	if lang == "zh_CN" or lang == "zh" :
		return "zh-CN"
	else :
		return "en"

def InstallLanguages() :
	lang = GetLanguageByRequest()
	if lang == "zh-CN" :
		zh_trans.install()
	else :
		en_trans.install()


def GetHeader(name) :
	InstallLanguages()

	html = '<html>\n'
	html = html + '<head>\n'
	html = html + '<meta charset="utf-8">\n'
	html = html + '<meta http-equiv="X-UA-Compatible" content="IE=edge">\n'
	html = html + '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
	html = html + '<title>'+ _("Antshares Blockchain Explorer") +'</title>\n'
	html = html + '<link rel="shortcut icon" href="/static/images/logo.png" media="screen" />\n'
	
	html = html + '<link rel="stylesheet" href="/static/css/fonts.css">\n'
	html = html + '<link rel="stylesheet" href="/static/css/normalize.css">'
	html = html + '<link rel="stylesheet" href="/static/css/milligram.min.css">'

	html = html + '<style type="text/css">\n'
	html = html + 'html,body,td,th{height: 100%;font-size:12px;font-family:"Roboto"}\n'
	html = html + 'body{}\n'
	html = html + '.column {text-align:left}\n'
	html = html + 'td {text-overflow:ellipsis; white-space:nowrap; overflow:hidden;}\n'
	html = html + 'a{text-decoration:none;}\n'
	html = html + '</style>\n'

	html = html + '<script>\n'
	html = html + '	var _hmt = _hmt || [];\n'
	html = html + '	(function() {\n'
	html = html + '	  var hm = document.createElement("script");\n'
	html = html + '	  hm.src = "https://hm.baidu.com/hm.js?8a4cd1b36cec648c82133995fa7f0f39";\n'
	html = html + '	  var s = document.getElementsByTagName("script")[0]; \n'
	html = html + '	  s.parentNode.insertBefore(hm, s);\n'
	html = html + '	})();\n'
	html = html + '</script>\n'

	html = html + '</head>\n'

	html = html + '<body>\n'
	html = html + '<div align="center">\n'
	html = html + '[ '+ _("Antshares Blockchain Explorer") +' antchain.org ]<br/>\n'

	if name == "index" :
		html = html + '<a href="/"><b>' + _("Index") + '</b></a>&emsp;&emsp;\n'
	else :
		html = html + '<a href="/">' + _("Index") + '</a>&emsp;&emsp;\n'

	if name == "block" :	
		html = html + '<a href="/block/"><b>' + _("Block") + '</b></a>&emsp;&emsp;\n'
	else :
		html = html + '<a href="/block/">' + _("Block") + '</a>&emsp;&emsp;\n'

	if name == "tx" :	
		html = html + '<a href="/tx/"><b>' + _("Transaction") + '</b></a>&emsp;&emsp;\n'
	else :
		html = html + '<a href="/tx/">' + _("Transaction") + '</a>&emsp;&emsp;\n'

	if name == "address" :
		html = html + '<a href="/address/"><b>' + _("Address") + '</b></a>&emsp;&emsp;\n'
	else :
		html = html + '<a href="/address/">' + _("Address") + '</a>&emsp;&emsp;\n'

	if name == "asset" :
		html = html + '<a href="/asset/"><b>' + _("Asset") + '</b></a>&emsp;&emsp;\n'
	else :
		html = html + '<a href="/asset/">' + _("Asset") + '</a>&emsp;&emsp;\n'

	if name == "rank" :
		html = html + '<a href="/rank/"><b>' + _("Rank") + '</b></a>&emsp;&emsp;\n'
	else :
		html = html + '<a href="/rank/">' + _("Rank") + '</a>&emsp;&emsp;\n'

	if name == "api" :
		html = html + '<a href="/api/"><b>' + "API" + '</b></a>&emsp;&emsp;\n'
	else :
		html = html + '<a href="/api/">' + "API" + '</a>&emsp;&emsp;\n'

	html = html + '<br/><br/>\n'
	html = html + '</div>\n'

	html = html + '<div class="container">\n'
	
	html = html + '<form action="/search" method="post">\n'
	html = html + '  <fieldset>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-30"></div>\n'
	html = html + '<div class="column column-30">\n'
	html = html + '    <input type="text" placeholder="' + _('height/address/hash/txid') + '" name="searchdata" id="searchdata">\n'
	html = html + '</div>\n'
	html = html + '<div class="column column-10"><input class="button" type="submit" value="'+ _('Search') +'"></div>\n'
	html = html + '<div class="column column-30"></div>\n'

	html = html + '  </fieldset>\n'
	html = html + '</form>\n'
	html = html + '<br/>\n'

	html = html + '</div>\n'
	html = html + '<div class="column column-30"></div>\n'
	html = html + '</div>\n'

	return html


def GetFooter() :
	html = "<br/><hr>\n"
	html = html + "<div align = 'center'>\n"
	html = html + "<br/>antchain.org (c) 2016-2017\n"
	html = html + "</div><br/>\n"

	html = html + "</body>\n"

	html = html + "</html>\n"

	return html


def GetAssetName(txid) :
	result = collection_txs.find_one({"txid":txid})
	asset = result['asset']

	return GetAssetNameByAsset(asset)

def GetAssetNameByAsset(asset) :
	lang = GetLanguageByRequest()
	for assetname in asset['name'] :
		if assetname['lang'] == lang :
			return assetname['name']

	return asset['name'][0]['name']

def GetAssetByTxid(txid) :
	result = collection_txs.find_one({"txid":txid})
	asset = result['asset']

	return asset

def GetAssetAmount(amount) :
	if amount == "-0.00000001" :
		amount = _("No limit")

	return 	str(amount)


##################################################
###
### import
###
##################################################
from flask import Flask
from flask import request
from werkzeug.routing import BaseConverter
class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]

app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter

client = pymongo.MongoClient("localhost", 27017)
db = client.antchain_main
collection_blocks = db.blocks
collection_txs = db.txs
collection_coins = db.coins
collection_ads = db.ads

@app.route("/")
def index():
	html = GetHeader("index")
	html = html + GetLogo()

	html = html + '<div name="block" align="center">'
	html = html + '<br/><br/>'
	html = html + '<h2>' + _("Block Information") + '</h2><a href="/block/">[' + _("More") + ']</a>'
	html = html + block.GetblockInternal(1,20)
	html = html + '</div>'

	html = html + '<div name="tx" align="center">'
	html = html + '<br/><br/>'
	html = html + '<h2>'+ _("Transaction Information") +'</h2><a href="/tx/">[' + _("More") + ']</a>'
	html = html + tx.GetTxInternal(None,1,20)
	html = html + '</div>'

	html = html + '<div name="address" align="center">'
	html = html + '<br/><br/>'
	html = html + '<h2>'+ _("Address Information") +'</h2><a href="/address/">[' + _("More") + ']</a>'
	html = html + ads.GetAddressInternal(None,1,20)
	html = html + '</div>'

	html = html + GetFooter()

	return html



##################################################
###
### search
###
##################################################
@app.route('/search', methods=['GET','POST'])
def Search():
	if request.method == 'POST':
		data = request.form['searchdata']

		# find address
		matchObj = re.match( '[A][a-zA-Z0-9]{33}', data)
		if matchObj:
			m = matchObj.group()
			result = collection_ads.find_one({"address":m})
			if result :
				html = '<meta http-equiv="refresh" content="0;url=/address/' + m + '"> '
				return html

		# find block hash or txid 
		matchObj = re.match( '[a-zA-Z0-9]{64}', data )
		if matchObj:
			m = matchObj.group()
			result = collection_txs.find_one({"txid":m})
			if result :
				html = '<meta http-equiv="refresh" content="0;url=/tx/' + m + '"> '
				return html

			result = collection_blocks.find_one({"hash":m})
			if result :
				html = '<meta http-equiv="refresh" content="0;url=/block/' + m + '"> '
				return html

		# find block height
		matchObj = re.match( '[0-9]{1,12}', data )
		if matchObj:
			m = matchObj.group()
			result = collection_blocks.find_one({"height":int(m)})
			if result :
				html = '<meta http-equiv="refresh" content="0;url=/block/' + str(int(m)) + '"> '
				return html

		# not found!
		html = GetHeader("index")

		html = html + '<div class="container">\n'
		html = html + '<div class="row">\n'
		html = html + data + ' Not Found.'
		html = html + '</div>\n'
		html = html + '</div>\n'

		html = html + GetFooter()

		return html

	else :
		html = GetHeader("index")
		html = html + GetFooter()

		return html


##################################################
###
### block
###
##################################################
@app.route('/block/')
def Getblock():
	return block.GetblockPage(1)

@app.route('/block/page/<int:page>')
def GetblockPages(page):
	return block.GetblockPage(page)

@app.route('/block/<blockhash>')
def GetblockByHash(blockhash):
	return block.GetblockByHashInternal(blockhash)

@app.route('/block/<int:block_height>')
def GetblockByHeight(block_height):
	return block.GetblockByHeightInternal(block_height)


##################################################
###
### tx
###
##################################################
@app.route('/tx/')
def GetTx():
	return tx.GetTxPage(None,1)

@app.route('/tx/page/<int:page>')
def GetTxPages(page):
	return tx.GetTxPage(None,page)

# TransactionType
@app.route('/tx/<regex("[a-zA-Z]{10,30}"):txtype>')
def GetTxByType(txtype):
	return tx.GetTxPage(txtype,1)

@app.route('/tx/<regex("[a-zA-Z]{10,30}"):txtype>/page/<int:page>')
def GetTxByTypePages(txtype,page):
	return tx.GetTxPage(txtype,page)

@app.route('/tx/<regex("[a-zA-Z0-9]{64}"):txid>')
def GetTxByHash(txid):
	return tx.GetTxByHashInternal(txid)


##################################################
###
### address
###
##################################################
@app.route('/address/')
def GetAds() :
	return ads.GetAddressPage(None,1)

@app.route('/address/page/<int:page>')
def GetAdsPages(page) :
	return ads.GetAddressPage(None,page)

@app.route('/address/<regex("[a-zA-Z0-9]{34}"):address>')
def GetAdsByAddress(address) :
	return ads.GetAdsByAddressPagesInternal(address,None,1)

@app.route('/address/<regex("[a-zA-Z0-9]{34}"):address>/page/<int:page>')
def GetAdsByAddressPages(address,page) :
	return ads.GetAdsByAddressPagesInternal(address,None,page)

@app.route('/address/<regex("[a-zA-Z0-9]{64}"):assetid>')
def GetAssetAds(assetid) :
	return ads.GetAddressPage(assetid,1)

@app.route('/address/<regex("[a-zA-Z0-9]{64}"):assetid>/page/<int:page>')
def GetAssetAdsPages(assetid,page) :
	return ads.GetAddressPage(assetid,page)

@app.route('/address/<regex("[a-zA-Z0-9]{34}"):address>/<regex("[a-zA-Z0-9]{64}"):assetid>')
def GetAdsAssetPages(address,assetid) :
	return ads.GetAdsByAddressPagesInternal(address,assetid,1)


##################################################
###
### asset
###
##################################################
@app.route('/asset/')
def GetAsset() :
	return asset.GetAssetPage(1)

@app.route('/asset/<assetid>')
def GetAssetByHash(assetid):
	return asset.GetAssetByHashPagesInternal(assetid,1)

@app.route('/asset/<assetid>/page/<int:page>')
def GetAssetByHashPages(assetid,page):
	return asset.GetAssetByHashPagesInternal(assetid,page)


##################################################
###
### rank
###
##################################################
@app.route('/rank/')
def GetRank() :
	return rank.GetRankByHashInternal("c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b",100)

@app.route('/rank/<assetid>')
def GetRankByHash(assetid) :
	return rank.GetRankByHashInternal(assetid,100)

##################################################
###
### api
###
##################################################
@app.route('/api/')
def GetApi() :
	return api.GetApi()

@app.route('/api/v1/address/get_value/<regex("[a-zA-Z0-9]{34}"):address>')
def Api_V1_Address_Get_Value(address) :
	return api.Api_V1_Address_Get_Value(address), {'content-type':'application/json'}

@app.route('/api/v1/block/get_current_height')
def Api_V1_Block_Get_Current_Height() :
	return api.Api_V1_Block_Get_Current_Height(), {'content-type':'application/json'}

@app.route('/api/v1/block/get_current_block')
def Api_V1_Block_Get_Current_Block() :
	return api.Api_V1_Block_Get_Current_Block(), {'content-type':'application/json'}

@app.route('/api/v1/block/get_block/<int:height>')
def Api_V1_Block_Get_Block_By_Height(height) :
	return api.Api_V1_Block_Get_Block_By_Height(height), {'content-type':'application/json'}

@app.route('/api/v1/block/get_block/<regex("[a-zA-Z0-9]{64}"):hash>')
def Api_V1_Block_Get_Block_By_Hash(hash) :
	return api.Api_V1_Block_Get_Block_By_Hash(hash), {'content-type':'application/json'}

@app.route('/api/v1/tx/get_tx/<regex("[a-zA-Z0-9]{64}"):txid>')
def Api_V1_Tx_Get_Tx(txid) :
	return api.Api_V1_Tx_Get_Tx(txid), {'content-type':'application/json'}


##################################################
###
### main
###
##################################################
if __name__ == "__main__":
    app.run()
