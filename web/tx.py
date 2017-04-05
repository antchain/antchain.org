# -*- coding:utf-8 -*-

import math

import web

def GetMinerTransactionResult(result) :
	html = ''
	html = html + '<div class="container">\n'
	
	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("MinerTransaction") +'</b></div>\n'
	html = html + '<div class="column"><a href="/tx/'+ result['txid'] + '">' + result['txid'] + '</a></div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10">'+ _("Time") +'</div>\n'
	html = html + '<div class="column">' + web.GetLocalTime(result['time']) + '</div>\n'
	html = html + '<div class="column column-offset-50">'+ _("System Fee") + ' ' + result['sys_fee'] + ' ' + _("ANC") + '</div>\n'
	html = html + '</div>\n'

	html = html + '</div>\n'

	return html


def GetCoinByTxVin(vin) :
	result = web.collection_coins.find_one({"txid":vin['txid'],"n":vin['vout']})
	return result


def GetCoinByTxVout(txid,vout) :
	results = web.collection_coins.find({"txid":txid,"n":vout['n']}).sort("height",-1)

	if results[0]['state'] & web.CoinState.Spent == web.CoinState.Spent :
		return results[0]
	else :
		return None

def GetCoinsByTransactionResult(result,address,lens) :
	html = ''

	for i in range(0,lens) :
		html = html + '<div class="row">\n'
		if len(result['vin']) > i :
			coinResult = GetCoinByTxVin(result['vin'][i])
			html = html + '<div class="column column-10"><a href="/tx/' + coinResult['txid'] + '"><-</a></div>\n'
			if coinResult['address'] == address :
				html = html + '<div class="column column-25"><a href="/address/' + coinResult['address'] + '"><b>' + coinResult['address'] + '</b></a></div><div class="column column-15">-' + str(coinResult['value']) + ' ' + web.GetAssetName(coinResult['asset']) + '</div>'
			else :
				html = html + '<div class="column column-25"><a href="/address/' + coinResult['address'] + '">' + coinResult['address'] + '</a></div><div class="column column-15">-' + str(coinResult['value']) + ' ' + web.GetAssetName(coinResult['asset']) + '</div>'
		else :
			html = html + '<div class="column column-10"></div>\n'
			html = html + '<div class="column column-25"></div><div class="column column-15"></div>\n'

		if len(result['vout']) > i :
			if result['vout'][i]['address'] == address :
				html = html + '<div class="column column-25"><a href="/address/' + result['vout'][i]['address'] + '"><b>' + result['vout'][i]['address'] + '</b></a></div><div class="column column-15">+'+  str(result['vout'][i]['value']) + ' ' + web.GetAssetName(result['vout'][i]['asset']) + '</div>\n'
			else :
				html = html + '<div class="column column-25"><a href="/address/' + result['vout'][i]['address'] + '">' + result['vout'][i]['address'] + '</a></div><div class="column column-15">+'+  str(result['vout'][i]['value']) + ' ' + web.GetAssetName(result['vout'][i]['asset']) + '</div>\n'

			coinResult = GetCoinByTxVout(result['txid'],result['vout'][i])
			if coinResult != None :
				html = html + '<div class="column column-10"><a href="/tx/'+ coinResult['spent_txid'] + '">-></a></div>\n'
			else :
				html = html + '<div class="column column-10"></div>\n'
		else :
			html = html + '<div class="column column-25"></div><div class="column column-15"></div>\n'
			html = html + '<div class="column column-10"></div>\n'
		html = html + '</div>\n'

	return html


def GetContractTransactionResult(result,address) :
	html = ''
	html = html + '<br/>\n'

	lens = 0
	len_in = len(result['vin'])
	len_out = len(result['vout'])
	if len_in > len_out :
		lens = len_in
	else :
		lens = len_out

	html = html + '<div class="container">\n'
	
	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("ContractTransaction") + '</b></div>\n'
	html = html + '<div class="column"><a href="/tx/'+ result['txid'] + '">' + result['txid'] + '</a></div>\n'
	html = html + '</div>\n'

	#html = html + '<div class="row">\n'
	#html = html + '<table style="padding-left:1em;padding-right:1em;" width="80%" border="0" cellpadding="3" cellspacing="0">\n'

	html = html + GetCoinsByTransactionResult(result,address,lens)

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10">'+ _("Time") + '</div>\n'
	html = html + '<div class="column">' + web.GetLocalTime(result['time']) + '</div>\n'
	html = html + '<div class="column column-offset-50">'+ _("System Fee") + ' ' + result['sys_fee'] + ' ' + _("ANC") + '</div>\n'
	html = html + '</div>\n'

	#html = html + '</table>\n'
	#html = html + '</div>\n'

	html = html + '</div>\n'

	return html

def GetClaimTransactionResult(result,address) :
	html = ''
	html = html + '<div class="container">\n'

	lens = len(result['vout'])
	
	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("ClaimTransaction") +'</b></div>\n'
	html = html + '<div class="column"><a href="/tx/'+ result['txid'] + '">' + result['txid'] + '</a></div>\n'
	html = html + '</div>\n'

	html = html + GetCoinsByTransactionResult(result,address,lens)

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10">'+ _("Time") +'</div>\n'
	html = html + '<div class="column">' + web.GetLocalTime(result['time']) + '</div>\n'
	html = html + '<div class="column column-offset-50">'+ _("System Fee") + ' ' + result['sys_fee'] + ' ' + _("ANC") + '</div>\n'
	html = html + '</div>\n'

	html = html + '</div>\n'

	return html


def GetRegisterTransactionResult(result,address) :
	html = ''
	html = html + '<div class="container">\n'

	lens = 0
	len_in = len(result['vin'])
	len_out = len(result['vout'])
	if len_in > len_out :
		lens = len_in
	else :
		lens = len_out
	
	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("RegisterTransaction") +'</b></div>\n'
	html = html + '<div class="column"><a href="/tx/'+ result['txid'] + '">' + result['txid'] + '</a></div>\n'
	html = html + '</div>\n'
	
	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10">'+ _("Asset Name") +'</div>\n'
	html = html + '<div class="column"><a href="/asset/'+ result['txid'] + '">' + web.GetAssetNameByAsset(result['asset']) + '</a></div>\n'
	html = html + '</div>\n'
	
	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10">'+ _("Asset Type") +'</div>\n'
	html = html + '<div class="column">' + result['asset']['type'] + '</div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10">'+ _("Asset Amount") +'</div>\n'
	html = html + '<div class="column">' + web.GetAssetAmount(result['asset']['amount']) + '</div>\n'
	html = html + '</div>\n'
	
	html = html + GetCoinsByTransactionResult(result,address,lens)
	
	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10">'+ _("Time") +'</div>\n'
	html = html + '<div class="column">' + web.GetLocalTime(result['time']) + '</div>\n'
	html = html + '<div class="column column-offset-50">'+ _("System Fee") + ' ' + result['sys_fee'] + ' ' + _("ANC") + '</div>\n'
	html = html + '</div>\n'

	html = html + '</div>\n'

	return html

def GetIssueTransactionResult(result,address) :
	html = ''
	html = html + '<div class="container">\n'

	lens = len(result['vout'])
	
	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("IssueTransaction") +'</b></div>\n'
	html = html + '<div class="column"><a href="/tx/'+ result['txid'] + '">' + result['txid'] + '</a></div>\n'
	html = html + '</div>\n'
	
	asset = web.GetAssetByTxid(result['vout'][0]['asset'])

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10">'+ _("Asset Name") +'</div>\n'
	html = html + '<div class="column"><a href="/asset/'+ result['txid'] + '">' + web.GetAssetNameByAsset(asset) + '</a></div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10">'+ _("Asset Type") +'</div>\n'
	html = html + '<div class="column">' + asset['type'] + '</div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10">'+ _("Asset Amount") +'</div>\n'
	html = html + '<div class="column">' + web.GetAssetAmount(asset['amount']) + '</div>\n'
	html = html + '</div>\n'
	
	html = html + GetCoinsByTransactionResult(result,address,lens)
	
	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10">'+ _("Time") +'</div>\n'
	html = html + '<div class="column">' + web.GetLocalTime(result['time']) + '</div>\n'
	html = html + '<div class="column column-offset-50">'+ _("System Fee") + ' ' + result['sys_fee'] + ' ' + _("ANC") + '</div>\n'
	html = html + '</div>\n'

	html = html + '</div>\n'

	return html

def GetEnrollmentTransactionResult(result,address) :
	html = ''
	html = html + '<div class="container">\n'

	lens = 0
	len_in = len(result['vin'])
	len_out = len(result['vout'])
	if len_in > len_out :
		lens = len_in
	else :
		lens = len_out
	
	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("EnrollmentTransaction") +'</b></div>\n'
	html = html + '<div class="column"><a href="/tx/'+ result['txid'] + '">' + result['txid'] + '</a></div>\n'
	html = html + '</div>\n'
	
	html = html + GetCoinsByTransactionResult(result,address,lens)
	
	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10">'+ _("Time") +'</div>\n'
	html = html + '<div class="column">' + web.GetLocalTime(result['time']) + '</div>\n'
	html = html + '<div class="column column-offset-50">'+ _("System Fee") + ' ' + result['sys_fee'] + ' ' + _("ANC") + '</div>\n'
	html = html + '</div>\n'

	html = html + '</div>\n'

	return html


def GetTxResultInternal(result,address) :
	html = ''
	if result['type'] == 'MinerTransaction' :
		html = html + GetMinerTransactionResult(result)
	elif result['type'] == 'ContractTransaction' :
		html = html + GetContractTransactionResult(result,address)
	elif result['type'] == 'ClaimTransaction' :
		html = html + GetClaimTransactionResult(result,address)
	elif result['type'] == 'RegisterTransaction' :
		html = html + GetRegisterTransactionResult(result,address)
	elif result['type'] == 'IssueTransaction' :
		html = html + GetIssueTransactionResult(result,address)
	elif result['type'] == 'EnrollmentTransaction' :
		html = html + GetEnrollmentTransactionResult(result,address)
	return html

def GetTxResult(result) :
	html = ''
	html = html + '<div class="container">\n'
	
	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Txid") +'</b></div><div class="column"><b>' + result['txid'] + '</b></div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Type") +'</b></div><div class="column"><a href="/tx/' + result['type'] + '">' + _(result['type']) + '</a></div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Time") +'</b></div><div class="column">' + web.GetLocalTime(result['time']) + '</div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Fee") +'</b></div><div class="column">' + result['sys_fee'] + ' ' + _("ANC") + '</div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("TxSize") +'</b></div><div class="column">' + str(result['size']) + ' Bytes</div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("TxVersion") +'</b></div><div class="column">' + str(result['version']) + '</div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("From Height") +'</b></div><div class="column"><a href="/block/' + str(result['height']) + '">' + str(result['height']) + '</a></div>\n'
	html = html + '</div>\n'

	html = html + '</div>\n'
	
	html = html + '<br/>\n'

	html = html + GetTxResultInternal(result,None)

	return html


def GetTxByHashInternal(txid) :
	html = web.GetHeader("tx")

	result = web.collection_txs.find_one({"txid":txid})
	if result :
		html = html + GetTxResult(result)
	else :
		html = html + _("Transaction Not Found!")

	html = html + web.GetFooter()

	return html


def GetTxInternal(txtype,page,listnum) :
	if page <= 0 :
		return 'page index begin: 1'

	start = (page-1)*listnum

	html = ''
	html = html + '<div class="container">\n'
	html = html + '<table width="80%" border="0" cellpadding="3" cellspacing="0">\n'
	html = html + '<tr align="left">\n'
	html = html + '<th>'+ _("Type") +'</th><th>'+ _("Txid") +'</th><th>'+ _("Height") +'</th><th>'+ _("In/Out") +'</th><th>'+ _("System Fee") +'</th><th>'+ _("Size") +'</th><th>'+ _("Time") +'</th>' + '<br/>\n'
	html = html + '</tr>\n'

	if txtype == None :
		results = web.collection_txs.find({"type":{"$ne":"MinerTransaction"}}).sort("height",-1).limit(listnum).skip(start)
	else :
		results = web.collection_txs.find({"type":txtype}).sort("height",-1).limit(listnum).skip(start)

	for tx in results :
		html = html + '<tr>\n'
		html = html + '<td>' + '<a href="/tx/' + tx['type'] + '">' + _(tx['type']) + '</a>&emsp;</td>\n'
		html = html + '<td>' + '<a href="/tx/' + tx['txid'] + '">' + tx['txid'] + '</a>&emsp;</td>\n'
		html = html + '<td>' + '<a href="/block/' + str(tx['height']) + '">' + str(tx['height']) + '</a>&emsp;' + '</td>\n'
		html = html + '<td>' + str(len(tx['vin'])) + '/' + str(len(tx['vout'])) + '&emsp;</td>\n'
		html = html + '<td>' + str(tx['size']) + ' Bytes&emsp;</td>\n'
		html = html + '<td>' + str(tx['size']) + ' Bytes&emsp;</td>\n'
		html = html + '<td>' + web.GetLocalTime(tx['time']) + '&emsp;</td>\n'
		html = html + '</tr>\n'
	html = html + '</table>\n'
	html = html + '</div>\n'

	return html


def GetTxPagination(txtype,page) :
	html = ''
	html = html + '<div name="pages" align="center">\n'
	
	if txtype == None :
		count = web.collection_txs.find({"type":{"$ne":"MinerTransaction"}}).count()
	else :
		count = web.collection_txs.find({"type":txtype}).count()

	if count == 0 :
		return ''

	pages = count / web.TX_PER_PAGE
	if count % web.TX_PER_PAGE != 0 :
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

	if txtype == None :
		html = html + '<a href="/tx/page/' + str(1) + '"><<</a> '
		for i in range(displaystart,displayend+1) :
			if i != page :
				html = html + '<a href="/tx/page/' + str(i) + '">' + str(i) + '</a> '
			else :
				html = html + str(i) + ' '	
		html = html + '<a href="/tx/page/' + str(pages) + '">>></a> '
	else :
		html = html + '<a href="/tx/' + txtype + '/page/' + str(1) + '"><<</a> '
		for i in range(displaystart,displayend+1) :
			if i != page :
				html = html + '<a href="/tx/' + txtype + '/page/' + str(i) + '">' + str(i) + '</a> '
			else :
				html = html + str(i) + ' '	
		html = html + '<a href="/tx/' + txtype + '/page/' + str(pages) + '">>></a> '


	html = html + '<br/>\n'
	html = html + '</div>\n'

	return html



def GetTxPage(txtype,page) :
	html = web.GetHeader("tx")

	html = html + '<div name="tx" align="center">\n'
	html = html + '<br/><br/>\n'
	html = html + '<h2>'+ _("Transaction Information") +'</h2>\n'

	html = html + '<div class="container">\n'

	results = web.collection_txs.find({"type":{"$ne":"MinerTransaction"}}).distinct("type")
	count = len(results)
	row = int(math.ceil(count / 4))

	r = 0
	for i in range(0, row+1) :
		html = html + '<div class="row">\n'
		html = html + '<div class="column column-20"></div>\n'
		
		for j in range(0,4) :
			if i==0 and j==0 :
				if txtype == None :
					html = html + '<div class="column column-15"><a href="/tx"><b>[' + _('All Transaction') + ']</b></a></div>\n'
				else :
					html = html + '<div class="column column-15"><a href="/tx">[' + _('All Transaction') + ']</a></div>\n'
				continue

			if r >= count or results[r] == "MinerTransaction":
				html = html + '<div class="column column-15"></div>\n'
			elif txtype == results[r] :
				html = html + '<div class="column column-15"><a href="/tx/' + results[r] + '"><b>[' + _(results[r]) + ']</b></a></div>\n'
			else :
				html = html + '<div class="column column-15"><a href="/tx/' + results[r] + '">[' + _(results[r]) + ']</a></div>\n'
			r = r + 1

		html = html + '<div class="column column-20"></div>\n'
		html = html + '</div>\n'

	html = html + '</div>\n'

	html = html + '<br/>\n'
	html = html + '<br/>\n'

	if txtype != None :
		html = html + '<h4>- '+ _(txtype) +' -</h4>\n'

	Pagination = GetTxPagination(txtype,page)

	html = html + Pagination
	html = html + GetTxInternal(txtype,page,web.BLOCK_PER_PAGE)
	html = html + '<br/>\n'
	html = html + Pagination
	html = html + '</div>\n'

	html = html + web.GetFooter()

	return html

