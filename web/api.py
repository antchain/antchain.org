# -*- coding:utf-8 -*-

import web
import json

def GetApi() :
	html = web.GetHeader("api")

	html = html + '<div name="asset" align="center">\n'
	html = html + '<br/><br/>\n'
	html = html + '<h2>' + _('API Interface') + '</h2>\n'

	html = html + '<div class="container">\n'

	html = html + '<table width="80%" border="0" cellpadding="3" cellspacing="0" align="center">\n'
	html = html + '<tr align="left">\n'
	html = html + '<th>' + _('Interface Name') + '</th><th>' + _('Call Address') + '</th><th>' + _('Parameter') + '</th><th>' + _('Example') + '</th>\n'
	html = html + '</tr>'

	html = html + '<tr>'
	html = html + '<td>' + _('Get address value') + '</a></td>'
	html = html + '<td>/api/v1/address/get_value/<b>{address}</b></td>'
	html = html + '<td>address</td>'
	html = html + '<td><a href="/api/v1/address/get_value/AQVh2pG732YvtNaxEGkQUei3YA4cvo7d2i">' + _('Example') + '</a></td>'
	html = html + '</tr>'

	html = html + '<tr>'
	html = html + '<td>' + _('Get current block height') + '</a></td>'
	html = html + '<td>/api/v1/block/get_current_height</td>'
	html = html + '<td>' + _('None') + '</td>'
	html = html + '<td><a href="/api/v1/block/get_current_height">' + _('Example') + '</a></td>'
	html = html + '</tr>'

	html = html + '<tr>'
	html = html + '<td>' + _('Get current block') + '</a></td>'
	html = html + '<td>/api/v1/block/get_current_block</td>'
	html = html + '<td>' + _('None') + '</td>'
	html = html + '<td><a href="/api/v1/block/get_current_block">' + _('Example') + '</a></td>'
	html = html + '</tr>'

	html = html + '<tr>'
	html = html + '<td>' + _('Get block by height') + '</a></td>'
	html = html + '<td>/api/v1/block/get_block/<b>{height}</b></td>'
	html = html + '<td>height</td>'
	html = html + '<td><a href="/api/v1/block/get_block/0">' + _('Example') + '</a></td>'
	html = html + '</tr>'

	html = html + '<tr>'
	html = html + '<td>' + _('Get block by hash') + '</a></td>'
	html = html + '<td>/api/v1/block/get_block/<b>{blockhash}</b></td>'
	html = html + '<td>blockhash</td>'
	html = html + '<td><a href="/api/v1/block/get_block/d42561e3d30e15be6400b6df2f328e02d2bf6354c41dce433bc57687c82144bf">' + _('Example') + '</a></td>'
	html = html + '</tr>'

	html = html + '<tr>'
	html = html + '<td>' + _('Get transaction by txid') + '</a></td>'
	html = html + '<td>/api/v1/tx/get_tx/<b>{txid}</b></td>'
	html = html + '<td>txid</td>'
	html = html + '<td><a href="/api/v1/tx/get_tx/3631f66024ca6f5b033d7e0809eb993443374830025af904fb51b0334f127cda">' + _('Example') + '</a></td>'
	html = html + '</tr>'

	html = html + '</table>\n'

	html = html + '</div>\n'

	html = html + '</div>\n'

	html = html + web.GetFooter()

	return html

def Api_V1_Address_Get_Value(address) :
	data = {}
	data['address'] = address

	assetarray = []

	asset_address = web.collection_ads.find({"asset":{"$ne":"0"},"address":address}).sort("first_tx_time",1)
	for result in asset_address :
		asset = {}
		asset['name'] = web.GetAssetName(result['asset'])
		asset['assetid'] = result['asset']
		asset['value'] = str(result['value'])
		assetarray.append(asset)

	data['asset'] = assetarray

	json_str = json.dumps(data)

	return json_str

def Api_V1_Block_Get_Current_Height() :
	data = {}

	block = web.collection_blocks.find().sort("height",-1).limit(1)

	data['height'] = block[0]['height']

	json_str = json.dumps(data)

	return json_str

def Api_V1_Block_Get_Current_Block() :
	return ''

def Api_V1_Block_Get_Block() :
	return ''

def Api_V1_Block_Get_Block(height,hash) :
	return ''

def Api_V1_Tx_Get_Tx(txid) :
	return ''