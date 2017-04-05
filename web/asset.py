# -*- coding:utf-8 -*-

import web
import tx
import ads

antcoinid = "602c79718b16e442de58778e148d0b1084e3b2dffd5de6b7b16cee7969282de7"

def GetAssetIssuedAmount(assetid) :

	if assetid == antcoinid :
		return 0

	amout = 0
	results = web.collection_txs.find({"type":"IssueTransaction"}).sort("height",1)
	for result in results :
		vouts = result['vout']
		for vout in vouts :
			if vout['asset'] == assetid :
				amout = amout + int(vout['value'])

	return amout


def GetAssetInternal(page,listnum) :
	if page <= 0 :
		return 'page index begin: 1'

	start = (page-1) * listnum

	html = ''
	html = html + '<div class="container">\n'
	html = html + '<table width="80%" border="0" cellpadding="3" cellspacing="0" align="center">'
	html = html + '<tr align="left">'
	html = html + '<th>'+_('Asset Name')+'</th><th>'+_('Asset Type')+'</th><th>'+_('Asset Height')+'</th><th>'+_('Asset Precision')+'</th><th>'+_('Asset Issue')+'</th><th>'+_('Asset Amount')+'</th><th>'+_('Asset Time')+'</th>' + '<br/>'
	html = html + '</tr>'

	results = web.collection_txs.find({"type":"RegisterTransaction"}).sort("height",1)
	if results :
		for result in results :
			asset = result['asset']
			html = html + '<tr>'
			html = html + '<td>' + '<a href="/asset/' + result['txid'] + '">' + web.GetAssetNameByAsset(asset) + '</a></td>'
			html = html + '<td>' + asset['type'] + '</td>'
			html = html + '<td>' + str(result['height']) + '</td>'
			html = html + '<td>' + str(asset['precision']) + '</td>'
			html = html + '<td>' + str(GetAssetIssuedAmount(result['txid'])) + '</td>'
			html = html + '<td>' + web.GetAssetAmount(asset['amount']) + '</td>'
			html = html + '<td>' + web.GetLocalTime(result['time']) + '</td>'
			html = html + '</tr>'

	html = html + '</table>\n'
	html = html + '</div>\n'
	
	return html


def GetAssetPage(page) :
	html = web.GetHeader("asset")

	html = html + '<div name="asset" align="center">\n'
	html = html + '<br/><br/>\n'
	html = html + '<h2>' + _('Asset Information') + '</h2>\n'

	html = html + GetAssetInternal(page,web.ASSET_PER_PAGE)

	html = html + '</div>\n'

	html = html + web.GetFooter()
	
	return html

def GetAssetPagination(assetid,page,listnum) :
	html = ''
	html = html + '<div name="pages" align="center">\n'
	
	count = web.collection_ads.find({"asset":assetid}).count()
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

	html = html + '<a href="/asset/' + assetid + '/page/' + str(1) + '"><<</a> '
	for i in range(displaystart,displayend+1) :
		if i != page :
			html = html + '<a href="/asset/' + assetid + '/page/' + str(i) + '">' + str(i) + '</a> '
		else :
			html = html + str(i) + ' '	
	html = html + '<a href="/asset/' + assetid + '/page/' + str(pages) + '">>></a> '

	html = html + '<br/>\n'
	html = html + '</div>\n'

	return html


def GetAssetResultInternal(assetid,page,listnum) :
	html = ''
	
	Pagination = GetAssetPagination(assetid,page,listnum)

	html = html + Pagination
	html = html + ads.GetAddressInternal(assetid,page,listnum)
	html = html + '<br/>\n'
	html = html + Pagination

	return html


def GetAssetResult(tx_asset,page) :
	html = ''
	html = html + '<div class="container">\n'

	asset = tx_asset['asset']
	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Asset Name") +'</b></div><div class="column"><b>' + web.GetAssetNameByAsset(asset) + '</b></div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Asset ID") +'</b></div><div class="column"><a href="/tx/' + tx_asset['txid'] + '">' + tx_asset['txid'] + '</a></div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Asset Type") +'</b></div><div class="column">' + asset['type'] + '</div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Asset Precision") +'</b></div><div class="column">' + str(asset['precision']) + '</div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Asset Amount") +'</b></div><div class="column">' + str(asset['amount']) + '</div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Asset Issue") +'</b></div><div class="column">' + str(GetAssetIssuedAmount(tx_asset['txid'])) + '</div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Asset Issuer") +'</b></div><div class="column">' + asset['issuer'] + '</div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Asset Admin") +'</b></div><div class="column"><a href="/address/' + asset['admin'] + '">' + asset['admin'] + '</a></div>\n'
	html = html + '</div>\n'

	html = html + '</div>\n'

	'''
	html = html + '<hr/>\n'

	html = html + tx.GetTxResultInternal(tx_asset,None)

	html = html + '<hr/>\n'

	# antcoin not have IssueTransaction
	if tx_asset['txid'] != antcoinid :
		txid_set = set()
		results = web.collection_txs.find({"type":"IssueTransaction"}).sort("height",1)
		for result in results :
			vouts = result['vout']
			for vout in vouts :
				if vout['asset'] == tx_asset['txid'] :
					html = html + tx.GetTxResultInternal(result,None)
					html = html + '<hr/>\n'
					break
	'''

	html = html + GetAssetResultInternal(tx_asset['txid'],page,web.ASSET_ADS_PER_PAGE)

	return html


def GetAssetByHashPagesInternal(assetid,page) :
	html = web.GetHeader("asset")

	tx_asset = web.collection_txs.find_one({"txid":assetid})
	if tx_asset :
		html = html + GetAssetResult(tx_asset,page)
	else :
		html = html + _("ASSET Not Found!")

	html = html + web.GetFooter()

	return html