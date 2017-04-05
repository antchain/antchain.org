# -*- coding:utf-8 -*-

import math

import web

def GetRankByHashInternal(assetid,limitnum) :
	html = web.GetHeader("rank")

	html = html + '<div name="address" align="center">\n'
	html = html + '<br/><br/>\n'
	html = html + '<h2>'+ _("Rank") +'</h2>\n'


	html = html + '<div class="container">\n'

	count = web.collection_txs.find({"type":"RegisterTransaction"}).count()
	results = web.collection_txs.find({"type":"RegisterTransaction"}).sort("height",1)
	row = int(math.ceil(count / 4))

	r = 0
	for i in range(0, row+1) :
		html = html + '<div class="row">\n'
		html = html + '<div class="column column-20"></div>\n'
		
		for j in range(0,4) :
			if r >= count :
				html = html + '<div class="column column-15"></div>\n'
			elif assetid == results[r]['txid']:
				html = html + '<div class="column column-15"><a href="/rank/' + results[r]['txid'] + '"><b>[' + web.GetAssetNameByAsset(results[r]['asset']) + ']</b></a></div>\n'
			else :
				html = html + '<div class="column column-15"><a href="/rank/' + results[r]['txid'] + '">[' + web.GetAssetNameByAsset(results[r]['asset']) + ']</a></div>\n'
			r = r + 1

		html = html + '<div class="column column-20"></div>\n'
		html = html + '</div>\n'

	html = html + '</div>\n'

	html = html + '<br/>\n'

	if assetid != None :
		html = html + '<h4>- '+ web.GetAssetName(assetid) +' -</h4>\n'

	html = html + '<div class="container">\n'
	html = html + '<table width="80%" border="0" cellpadding="3" cellspacing="0" align="center">'
	html = html + '<tr align="left">'
	html = html + '<th>' + _('Rank') + '</th><th>' + _('Address') + '</th><th>' + _('Asset') + '</th><th>' + _('Value') + '</th><th>' + _('Transaction Counts') + '</th><th>' + _('Last Transaction Time') + '</th><th>' + _('First Transaction Time') + '</th>' + '<br/>'
	html = html + '</tr>'

	rank = 0
	#results = collection_ads.find({"asset":"c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b"}).sort("value",-1).limit(200)
	results = web.collection_ads.find({"asset":assetid}).sort("value",-1).limit(limitnum)
	if results :
		for result in results :
			rank = rank + 1
			html = html + '<tr>'
			html = html + '<td>' + str(rank) + '</td>'
			html = html + '<td>' + '<a href="/address/' + result['address'] + '">' + result['address'] + '</a></td>'
			html = html + '<td>' + web.GetAssetName(result['asset']) + '</td>'
			html = html + '<td>' + str(result['value']) + '</td>'
			html = html + '<td>' + str(len(result['txid_list'])) + '</td>'
			html = html + '<td>' + web.GetLocalTime(result['last_tx_time']) + '</td>'
			html = html + '<td>' + web.GetLocalTime(result['first_tx_time']) + '</td>'
			html = html + '</tr>'
			
	html = html + '</table>\n'
	html = html + '</div>\n'

	html = html + '</div>\n'

	html = html + web.GetFooter()

	return html