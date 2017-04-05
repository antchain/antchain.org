# -*- coding:utf-8 -*-

import math

import web
import tx

def GetAdsPagination(assetid,page) :
	html = ''
	html = html + '<div name="pages" align="center">\n'
	
	if assetid != None :
		count = web.collection_ads.find({"asset":assetid}).count()
	else :
		count = web.collection_ads.find({"asset":{"$ne":"0"}}).count()

	if count == 0 :
		return ''

	pages = count / web.ADS_PER_PAGE
	if count % web.ADS_PER_PAGE != 0 :
		pages = pages + 1

	if page <= 4 :
		displaystart = 1
	else :
		if page - 4 > 1 :
			displaystart = page - 4
		else :
			displaystart = 1
	
	if page >= pages - 4 and pages > 9 :
		displaystart = pages - 9
		displayend = pages
	else :
		if pages <= 9 :
			displayend = pages
		else :
			displayend = displaystart + 9

	if assetid != None :
		html = html + '<a href="/address/' + assetid + '/page/' + str(1) + '"><<</a> '
	else :
		html = html + '<a href="/address/page/' + str(1) + '"><<</a> '
	for i in range(displaystart,displayend+1) :
		if i != page :
			if assetid != None :
				html = html + '<a href="/address/' + assetid + '/page/' + str(i) + '">' + str(i) + '</a> '
			else :
				html = html + '<a href="/address/page/' + str(i) + '">' + str(i) + '</a> '
		else :
			html = html + str(i) + ' '

	if assetid != None :
		html = html + '<a href="/address/' + assetid + '/page/' + str(pages) + '">>></a> '
	else :
		html = html + '<a href="/address/page/' + str(pages) + '">>></a> '

	html = html + '<br/>\n'
	html = html + '</div>\n'

	return html


def GetAddressInternal(assetid,page,listnum) :
	if page <= 0 :
		return 'page index begin: 1'

	start = (page-1) * listnum

	html = ''
	html = html + '<div class="container">\n'
	html = html + '<table width="80%" border="0" cellpadding="3" cellspacing="0" align="center">'
	html = html + '<tr align="left">'
	html = html + '<th>'+ _("Address") +'</th><th>'+ _("AdsAsset") +'</th><th>'+ _("Value") +'</th><th>'+ _("Transaction Counts") +'</th><th>'+ _("Last Transaction Time") +'</th><th>'+ _("First Transaction Time") +'</th>' + '<br/>'
	html = html + '</tr>'

	if assetid != None :
		results = web.collection_ads.find({"asset":assetid}).sort("last_tx_time",-1).limit(listnum).skip(start)
	else :
		results = web.collection_ads.find({"asset":{"$ne":"0"}}).sort("last_tx_time",-1).limit(listnum).skip(start)

	if results :
		for result in results :
			html = html + '<tr>'
			html = html + '<td>' + '<a href="/address/' + result['address'] + '">' + result['address'] + '</a></td>'
			html = html + '<td>' + web.GetAssetName(result['asset']) + '</td>'
			html = html + '<td>' + str(result['value']) + '</td>'
			html = html + '<td>' + str(len(result['txid_list'])) + '</td>'
			html = html + '<td>' + web.GetLocalTime(result['last_tx_time']) + '</td>'
			html = html + '<td>' + web.GetLocalTime(result['first_tx_time']) + '</td>'
			html = html + '</tr>'
			
	html = html + '</table>\n'
	html = html + '</div>\n'

	return html

def GetAddressPage(assetid,page) :
	html = web.GetHeader("address")

	html = html + '<div name="address" align="center">\n'
	html = html + '<br/><br/>\n'
	html = html + '<h2>'+ _("Address Information") +'</h2>\n'

	html = html + '<div class="container">\n'

	count = web.collection_txs.find({"type":"RegisterTransaction"}).count()
	results = web.collection_txs.find({"type":"RegisterTransaction"}).sort("height",1)
	row = int(math.ceil(count / 4))

	r = 0
	for i in range(0, row+1) :
		html = html + '<div class="row">\n'
		html = html + '<div class="column column-20"></div>\n'
		
		for j in range(0,4) :
			if i==0 and j==0 :
				if assetid == None :
					html = html + '<div class="column column-15"><a href="/address/"><b>[' + _('All Asset') + ']</b></a></div>\n'
				else :
					html = html + '<div class="column column-15"><a href="/address/">[' + _('All Asset') + ']</a></div>\n'
				continue

			if r >= count :
				html = html + '<div class="column column-15"></div>\n'
			elif assetid == results[r]['txid']:
				html = html + '<div class="column column-15"><a href="/address/' + results[r]['txid'] + '"><b>[' + web.GetAssetNameByAsset(results[r]['asset']) + ']</b></a></div>\n'
			else :
				html = html + '<div class="column column-15"><a href="/address/' + results[r]['txid'] + '">[' + web.GetAssetNameByAsset(results[r]['asset']) + ']</a></div>\n'
			r = r + 1

		html = html + '<div class="column column-20"></div>\n'
		html = html + '</div>\n'

	html = html + '</div>\n'

	html = html + '<br/>\n'

	if assetid != None :
		html = html + '<h4>- '+ web.GetAssetName(assetid) +' -</h4>\n'

	Pagination = GetAdsPagination(assetid,page)

	html = html + Pagination
	html = html + GetAddressInternal(assetid,page,web.ADS_PER_PAGE)
	html = html + '<br/>\n'
	html = html + Pagination
	html = html + '</div>\n'

	html = html + web.GetFooter()

	return html


def GetAddressPagination(address_all,page,listnum) :
	html = ''
	html = html + '<div name="pages" align="center">\n'
	
	count = len(address_all['txid_list'])
	pages = count / listnum
	if count % listnum != 0 :
		pages = pages + 1

	if page <= 4 :
		displaystart = 1
	else :
		if page - 4 > 1 :
			displaystart = page - 4
		else :
			displaystart = 1
	
	if page >= pages - 4 and pages > 9 :
		displaystart = pages - 9
		displayend = pages
	else :
		if pages <= 9 :
			displayend = pages
		else :
			displayend = displaystart + 9

	ads = address_all['address']
	html = html + '<a href="/address/' + ads + '/page/' + str(1) + '"><<</a> '
	for i in range(displaystart,displayend+1) :
		if i != page :
			html = html + '<a href="/address/' + ads + '/page/' + str(i) + '">' + str(i) + '</a> '
		else :
			html = html + str(i) + ' '	
	html = html + '<a href="/address/' + ads + '/page/' + str(pages) + '">>></a> '

	html = html + '<br/>\n'
	html = html + '</div>\n'

	return html


def GetAddressResultInternal(address_all,page,listnum) :
	html = ''

	nstart = (page-1) * listnum
	i = -1
	for txid in address_all['txid_list'] :
		i = i + 1
		if i < nstart :
			continue
		if i >= (nstart + listnum) :
			break

		tx_result = web.collection_txs.find_one({"txid":txid['txid']})
		html = html + tx.GetTxResultInternal(tx_result,address_all['address'])
		html = html + '<hr/>\n'

	return html


def GetAddressResult(asset_address,address_all,page) :
	html = ''
	html = html + '<div class="container">\n'

	address = asset_address[0]['address']
	html = html + '<div class="row">\n'
	html = html + '<div class="column column-15"><b>'+ _("Address") +'</b></div><div class="column"><b>' + address + '</b></div>\n'
	html = html + '</div>\n'

	ncount = 0
	results = {}
	for result in asset_address :
		html = html + '<div class="row">\n'
		html = html + '<div class="column column-15"><b>'+ _("Asset") +'</b></div><div class="column">' + str(result['value']) + ' <b>' + web.GetAssetName(result['asset']) + '</b></div>\n'
		html = html + '</div>\n'
		results[ncount] = result
		ncount = ncount + 1

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-15"><b>'+ _("First Transaction Time") +'</b></div><div class="column">' + web.GetLocalTime(address_all['first_tx_time']) + '</div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-15"><b>'+ _("Last Transaction Time") +'</b></div><div class="column">' + web.GetLocalTime(address_all['last_tx_time']) + '</div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-15"><b>'+ _("Transaction Nums") +'</b></div><div class="column">' + str(len(address_all['txid_list'])) + '</div>\n'
	html = html + '</div>\n'

	html = html + '</div>\n'

	html = html + '<hr/>\n'

	#########################################################################
	# list all asset

	html = html + '<div class="container">\n'

	row = int(math.ceil(ncount / 4))

	r = 0
	for i in range(0, row+1) :
		html = html + '<div class="row">\n'
		html = html + '<div class="column column-20"></div>\n'
		
		for j in range(0,4) :
			if i==0 and j==0 :
				if address_all['asset'] == "0" :
					html = html + '<div class="column column-15"><a href="/address/' + address_all['address'] + '"><b>[' + _('All Asset') + ']</b></a></div>\n'
				else :
					html = html + '<div class="column column-15"><a href="/address/' + address_all['address'] + '">[' + _('All Asset') + ']</a></div>\n'
				continue

			if r >= ncount :
				html = html + '<div class="column column-15"></div>\n'
			elif address_all['asset'] == results[r]['asset']:
				html = html + '<div class="column column-15"><a href="/address/' + address_all['address'] + '/' + results[r]['asset'] + '"><b>[' + web.GetAssetName(results[r]['asset']) + ']</b></a></div>\n'
			else :
				html = html + '<div class="column column-15"><a href="/address/' + address_all['address'] + '/' + results[r]['asset'] + '">[' + web.GetAssetName(results[r]['asset']) + ']</a></div>\n'
			r = r + 1

		html = html + '<div class="column column-20"></div>\n'
		html = html + '</div>\n'

	html = html + '</div>\n'

	html = html + '<hr/>\n'

	#########################################################################

	Pagination = GetAddressPagination(address_all,page,web.ADS_PER_PAGE)

	html = html + Pagination
	html = html + GetAddressResultInternal(address_all,page,web.ADS_PER_PAGE)
	html = html + '<br/>\n'
	html = html + Pagination
	
	return html


def GetAdsByAddressPagesInternal(address,assetid,page) :
	html = web.GetHeader("address")

	#asset = "c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b"
	if assetid == None :
		asset_adddress = web.collection_ads.find({"asset":{"$ne":"0"},"address":address}).sort("first_tx_time",1)
		address_all = web.collection_ads.find_one({"asset":"0","address":address})
		if asset_adddress and address_all:
			html = html + GetAddressResult(asset_adddress,address_all,page)
		else :
			html = html + _("Address Not Found!")
	else :
		asset_adddress = web.collection_ads.find({"asset":{"$ne":"0"},"address":address}).sort("first_tx_time",1)
		address_all = web.collection_ads.find_one({"asset":assetid,"address":address})
		if asset_adddress and address_all:
			html = html + GetAddressResult(asset_adddress,address_all,page)
		else :
			html = html + _("Asset or Address Not Found!")

	html = html + web.GetFooter()

	return html