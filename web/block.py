# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import web
import tx

def GetTxsHtml(height) :
	html = ''
	txnum = web.collection_txs.find({"height":height}).count()
	if txnum > 0 :
		
		results = web.collection_txs.find({"height":height})
		for result in results :
			html = html + tx.GetTxResultInternal(result,None)
			html = html + "<br/>"

	return html

def GetBlockResult(result) :
	html = ''
	html = html + '<div class="container">\n'
	
	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Height") +'</b></div><div class="column"><b>' + str(result['height']) + '</b></div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Time") +'</b></div><div class="column">' + web.GetLocalTime(result['time']) + '</div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Hash") +'</b></div><div class="column"><b>' + result['hash'] + '</b></div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Previous Hash") +'</b></div><div class="column"><a href="/block/' + result['previousblockhash'] + '">' + result['previousblockhash'] + '</a></div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Merkleroot") +'</b></div><div class="column">' + result['merkleroot'] + '</div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Miner") +'</b></div><div class="column">' + result['nextminer'] + '</div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Size") +'</b></div><div class="column">' + str(result['size']) + ' Bytes</div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Version") +'</b></div><div class="column">' + str(result['version']) + '</div>\n'
	html = html + '</div>\n'

	html = html + '<div class="row">\n'
	html = html + '<div class="column column-10"><b>'+ _("Transaction Nums") +'</b></div><div class="column">' + str(result['txnum']) + '</div>\n'
	html = html + '</div>\n'
	
	html = html + '</div>\n'
	
	html = html + '<br/>\n'

	html = html + GetTxsHtml(result['height'])

	return html


def GetblockInternal(page,listnum) :
	if page <= 0 :
		return 'page index begin: 1'

	height = 0
	results = web.collection_blocks.find().sort("height",-1).limit(1)
	if results[0] :
		height =  results[0]['height']

	start = height-(page-1)*listnum

	if start < 0 :
		start = 0

	html = ''
	html = html + '<div class="container">\n'
	html = html + '<table width="80%" border="0" cellpadding="3" cellspacing="0" style="">\n'
	html = html + '<tr align="left">\n'
	html = html + '<th>'+ _("Height") +'</th><th>'+ _("Hash") +'</th><th>'+ _("Transaction Nums") +'</th><th>'+ _("Size") +'</th><th>'+ _("Time") +'</th>' + '<br/>\n'
	html = html + '</tr>\n'
	results = web.collection_blocks.find({"height":{"$lte":start}}).sort("height",-1).limit(listnum)
	for block in results :
		html = html + '<tr>\n'
		html = html + '<td>' + '<a href="/block/' + str(block['height']) + '">' + str(block['height']) + '</a>&emsp;&emsp;' + '</td>\n'
		html = html + '<td>' + '<a href="/block/' + block['hash'] + '">' + block['hash'] + '</a>&emsp;&emsp;</td>\n'
		html = html + '<td>' + str(block['txnum']) + '&emsp;&emsp;</td>\n'
		html = html + '<td>' + str(block['size']) + ' Bytes&emsp;&emsp;</td>\n'
		html = html + '<td>' + web.GetLocalTime(block['time']) + '&emsp;&emsp;</td>\n'
		html = html + '</tr>\n'
	html = html + '</table>\n'
	html = html + '</div>\n'

	return html



def GetBlockPagination(page) :
	html = ''
	html = html + '<div name="pages" align="center">\n'
	
	count = web.collection_blocks.find().count()
	pages = count / web.BLOCK_PER_PAGE
	if count % web.BLOCK_PER_PAGE != 0 :
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

	html = html + '<a href="/block/page/' + str(1) + '"><<</a> '
	for i in range(displaystart,displayend+1) :
		if i != page :
			html = html + '<a href="/block/page/' + str(i) + '">' + str(i) + '</a> '
		else :
			html = html + str(i) + ' '	
	html = html + '<a href="/block/page/' + str(pages) + '">>></a> '

	html = html + '<br/>\n'
	html = html + '</div>\n'

	return html


def GetblockPage(page) :
	html = web.GetHeader("block")

	html = html + '<div name="block" align="center">\n'
	html = html + '<br/><br/>\n'
	html = html + '<h2>'+ _("Block Information") +'</h2>\n'

	Pagination = GetBlockPagination(page)

	html = html + Pagination
	html = html + GetblockInternal(page,web.BLOCK_PER_PAGE)
	html = html + '<br/>\n'
	html = html + Pagination
	html = html + '</div>\n'

	html = html + web.GetFooter()

	return html


def GetblockByHashInternal(blockhash) :
	html = web.GetHeader("block")

	result = web.collection_blocks.find_one({"hash":blockhash})
	if result :
		html = html + GetBlockResult(result)
	else :
		html = html + _("Block Not Found!")

	html = html + web.GetFooter()

	return html


def GetblockByHeightInternal(block_height) :
	html = web.GetHeader("block")

	result = web.collection_blocks.find_one({"height":block_height})
	if result :
		html = html + GetBlockResult(result)
	else :
		html = html + _("Block Not Found!")

	html = html + web.GetFooter()

	return html	