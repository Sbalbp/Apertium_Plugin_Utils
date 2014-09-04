#
# Apertium Plugin Utils.
#
# Copyright (C) 2014 Sergio Balbuena <sbalbp@gmail.com>.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

"""
:Synopsis: Acts as an interface with an Apertium-APY
"""

try:
	import urllib.parse as parse
except:
	import urllib as parse
try:
    import urllib.request as urllib2
except:
	import urllib2
try:
    import html.parser as HTMLParser
except:
	import HTMLParser
import sys
import json
import socket

timeout = 8

pyVersion = sys.version_info[0]

apyAddress = ['http://localhost:2737']

parser = HTMLParser.HTMLParser()

def checkAPY(address):
	"""
	Checks whether an APY server is running in the given address or not.

    :param address: Address to be checked.
    :type address: str
    :returns: True if there was a response from the server, False otherwise.
    """
	if(pyVersion >= 3):
		try:
			address.decode('utf-8')
		except:
			pass

	try:
		request = urllib2.urlopen(address+'/listPairs')
	except urllib2.URLError:
		return False
	except urllib2.HTTPError:
		return False
	except ValueError:
		return False

	return True

def getAPYListSize():
	"""
	Retrieves the length of the APY list.

    :returns: The number of APYs currently in the list.
    """
	return len(apyAddress)

def getAPYAddress(index=0):
	"""
	Retrieves an APY from the current APY list.

    :param index: Position of the APY to be retrieved from the list. 0 if omitted.
    :type index: int
    :returns: A string with the current APY address on success, or None otherwise.
    """
	if(len(apyAddress) <= index or index < 0):
		return None
	else:
		if(pyVersion >= 3):
			return apyAddress[index].encode('utf-8')
		else:
			return apyAddress[index]

def setAPYAddress(newAddress, newPort=None, order=None, force=False):
	"""
	Adds a new address to the APY addresses list.

    :param newAddress: New address for the APY.
    :type newAddress: str
    :param order: Position this address will take in the list. None (appends address) by default.
    :type order: int
    :param force: Forces the address to be set even if there was no response.
    :type force: boolean
    :returns: The new address list if it was changed, or None otherwise.
    """
	global apyAddress

	if(pyVersion >= 3):
		try:
			newAddress = newAddress.decode('utf-8')
		except:
			pass
		if(newPort is not None):
			try:
				newPort = newPort.decode('utf-8')
			except:
				pass

	if(newPort is not None):
		newAddress = newAddress+':'+newPort

	if(checkAPY(newAddress) or force):
		if(order == None):
			apyAddress.append(newAddress)
		else:
			apyAddress.insert(order, newAddress)

		return getAPYList()
	else:
		return None

def removeAPYAddress(index):
	"""
	Removes an APY from the APY list.

    :param index: Index of the address to remove in the list.
    :type index: int
    :returns: True on success or False otherwise.
    """
	global apyAddress

	if(index >= len(apyAddress)):
		return False
	else:
		apyAddress.pop(index)
		return True

def getAPYList():
	"""
	Retrieves the list of APY addresses.

    :returns: The list of APY addresses.
    """
	addrList = []

	for address in apyAddress:
		if(pyVersion >= 3):
			addrList.append(address.encode('utf-8'))
		else:
			addrList.append(address)

	return addrList

def setAPYList(newList):
	"""
	Sets a list of APY addresses as the address list.

    :param newList: List containing the addresses to be added.
    :returns: The actual number of APY addresses added.
    """
	global apyAddress

	apyAddress = []
	success = 0

	for address in newList:
		if(setAPYAddress(address, force=True) != None):
			success = success+1

	return success

def getAllPairs(index=-1):
	"""
	Retrieves a list with all the available language pairs.

    :param index: Optional integer indicating the position of the address in the list the request should be sent to. Defaults to -1. Used to keep the function from iterating through all the addresses.
    :type index: int
    :returns: A dictionary.

    	The dictionary has the following fields:

    	- **'ok'**: True if the call was successful, False otherwise

    	- **'errorMsg':** String with the cause of the error. Only present if **'ok'** is False

    	- **'result':** List with the language pairs. Only present if **'ok'** is True

    .. note::

       Each element of the result list is a list with two string elements: the source and the target languages of the pair, respectively.
    """
	if(index > -1 and index < len(apyAddress)):
		apyList = [apyAddress[index]]
		last = 0
	else:
		apyList = apyAddress
		last = len(apyAddress)-1

	for it,address in enumerate(apyList):
		pairs = []

		try:
			request = urllib2.urlopen(address+'/listPairs', timeout=timeout)
		except urllib2.URLError:
			if(it == last):
				return {'ok':False, 'errorMsg':'Error on connection'.encode('utf-8')}
			else:
				continue
		except urllib2.HTTPError:
			if(it == last):
				return {'ok':False, 'errorMsg':'Error on connection'.encode('utf-8')}
			else:
				continue
		except socket.timeout:
			if(it == last):
				return {'ok':False, 'errorMsg':'Request timed out'.encode('utf-8')}
			else:
				continue

		if(request.getcode() < 300):
			if(pyVersion >= 3):
				request = request.read().decode("utf-8")
				jsonObj = json.loads(request)
			else:
				jsonObj = json.load(request)

			for pair in jsonObj['responseData']:
				pairs.append([ pair['sourceLanguage'].encode("utf-8"), pair['targetLanguage'].encode("utf-8") ])

			return {'ok':True, 'result':pairs}

		else:
			if(it == last):
				return {'ok':False, 'errorMsg':('Response '+str(request.getcode())+' from APY').encode('utf-8')}
			else:
				continue

def getPairsBySource(source, index=-1):
	"""
	Retrieves a list with all the available language pairs that share a common source language.

    :param source: String with the source language that the returned pairs must share.
    :type source: str
    :param index: Optional integer indicating the position of the address in the list the request should be sent to. Defaults to -1. Used to keep the function from iterating through all the addresses.
    :type index: int
    :returns: A dictionary.

    	The dictionary has the following fields:

    	- **'ok'**: True if the call was successful, False otherwise

    	- **'errorMsg':** String with the cause of the error. Only present if **'ok'** is False

    	- **'result':** List with the language pairs. Only present if **'ok'** is True

    .. note::

       Each element of the result list is a list with two string elements: the source and the target languages of the pair, respectively.
    """
	if(index > -1 and index < len(apyAddress)):
		apyList = [apyAddress[index]]
		last = 0
	else:
		apyList = apyAddress
		last = len(apyAddress)-1

	for it,address in enumerate(apyList):
		pairs = []

		if(pyVersion >= 3):
			try:
				source = source.decode("utf-8")
			except:
				pass

		try:
			request = urllib2.urlopen(address+'/listPairs', timeout=timeout)
		except urllib2.URLError:
			if(it == last):
				return {'ok':False, 'errorMsg':'Error on connection'.encode('utf-8')}
			else:
				continue
		except urllib2.HTTPError:
			if(it == last):
				return {'ok':False, 'errorMsg':'Error on connection'.encode('utf-8')}
			else:
				continue
		except socket.timeout:
			if(it == last):
				return {'ok':False, 'errorMsg':'Request timed out'.encode('utf-8')}
			else:
				continue

		if(request.getcode() < 300):
			if(pyVersion >= 3):
				request = request.read().decode("utf-8")
				jsonObj = json.loads(request)
			else:
				jsonObj = json.load(request)

			for pair in jsonObj['responseData']:
				if(pair['sourceLanguage'] == source):
					pairs.append([ pair['sourceLanguage'].encode("utf-8"), pair['targetLanguage'].encode("utf-8") ])

			return {'ok':True, 'result':pairs}

		else:
			if(it == last):
				return {'ok':False, 'errorMsg':('Response '+str(request.getcode())+' from APY').encode('utf-8')}
			else:
				continue

def getPairsByTarget(target, index=-1):
	"""
	Retrieves a list with all the available language pairs that share a common source language.

    :param target: String with the target language that the returned pairs must share.
    :type target: str
    :param index: Optional integer indicating the position of the address in the list the request should be sent to. Defaults to -1. Used to keep the function from iterating through all the addresses.
    :type index: int
    :returns: A dictionary.

    	The dictionary has the following fields:

    	- **'ok'**: True if the call was successful, False otherwise

    	- **'errorMsg':** String with the cause of the error. Only present if **'ok'** is False

    	- **'result':** List with the language pairs. Only present if **'ok'** is True

    .. note::

       Each element of the result list is a list with two string elements: the source and the target languages of the pair, respectively.
    """
	if(index > -1 and index < len(apyAddress)):
		apyList = [apyAddress[index]]
		last = 0
	else:
		apyList = apyAddress
		last = len(apyAddress)-1

	for it,address in enumerate(apyList):
		pairs = []

		if(pyVersion >= 3):
			try:
				target = target.decode("utf-8")
			except:
				pass

		try:
			request = urllib2.urlopen(address+'/listPairs', timeout=timeout)
		except urllib2.URLError:
			if(it == last):
				return {'ok':False, 'errorMsg':'Error on connection'.encode('utf-8')}
			else:
				continue
		except urllib2.HTTPError:
			if(it == last):
				return {'ok':False, 'errorMsg':'Error on connection'.encode('utf-8')}
			else:
				continue
		except socket.timeout:
			if(it == last):
				return {'ok':False, 'errorMsg':'Request timed out'.encode('utf-8')}
			else:
				continue

		if(request.getcode() < 300):
			if(pyVersion >= 3):
				request = request.read().decode("utf-8")
				jsonObj = json.loads(request)
			else:
				jsonObj = json.load(request)

			for pair in jsonObj['responseData']:
				if(pair['targetLanguage'] == target):
					pairs.append([ pair['sourceLanguage'].encode("utf-8"), pair['targetLanguage'].encode("utf-8") ])

			return {'ok':True, 'result':pairs}

		else:
			if(it == last):
				return {'ok':False, 'errorMsg':('Response '+str(request.getcode())+' from APY').encode('utf-8')}
			else:
				continue

def pairExists(source, target, index=-1):
	"""
	Checks if a given language pair is available.

    :param source: String with the source language of the pair to be checked.
    :type source: str
    :param target: String with the target language of the pair to be checked.
    :type target: str
    :param index: Optional integer indicating the position of the address in the list the request should be sent to. Defaults to -1. Used to keep the function from iterating through all the addresses.
    :type index: int
    :returns: A dictionary.

    	The dictionary has the following fields:

    	- **'ok'**: True if the call was successful, False otherwise

    	- **'errorMsg':** String with the cause of the error. Only present if **'ok'** is False

    	- **'result':** True if the pair exists, False otherwise. Only present if **'ok'** is True
    """
	if(index > -1 and index < len(apyAddress)):
		apyList = [apyAddress[index]]
		last = 0
	else:
		apyList = apyAddress
		last = len(apyAddress)-1

	for it,address in enumerate(apyList):
		pairs = []

		if(pyVersion >= 3):
			try:
				source = source.decode('utf-8')
			except:
				pass
			try:
				target = target.decode('utf-8')
			except:
				pass

		try:
			request = urllib2.urlopen(address+'/listPairs', timeout=timeout)
		except urllib2.URLError:
			if(it == last):
				return {'ok':False, 'errorMsg':'Error on connection'.encode('utf-8')}
			else:
				continue
		except urllib2.HTTPError:
			if(it == last):
				return {'ok':False, 'errorMsg':'Error on connection'.encode('utf-8')}
			else:
				continue
		except socket.timeout:
			if(it == last):
				return {'ok':False, 'errorMsg':'Request timed out'.encode('utf-8')}
			else:
				continue

		if(request.getcode() < 300):
			if(pyVersion >= 3):
				request = request.read().decode("utf-8")
				jsonObj = json.loads(request)
			else:
				jsonObj = json.load(request)

			for pair in jsonObj['responseData']:
				if(pair['sourceLanguage'] == source and pair['targetLanguage'] == target):
					return {'ok':True, 'result':True}

			if(it == last):
				return {'ok':True, 'result':False}
			else:
				continue

		else:
			if(it == last):
				return {'ok':False, 'errorMsg':('Response '+str(request.getcode())+' from APY').encode('utf-8')}
			else:
				continue

def translate(text, source, target, index=-1):
	"""
	Translates a given text.

    :param text: String to be translated.
    :type text: str
    :param source: String with the language to translate the text from.
    :type source: str
    :param target: String with the language to translate the text to.
    :type target: str
    :param index: Optional integer indicating the position of the address in the list the request should be sent to. Defaults to -1. Used to keep the function from iterating through all the addresses.
    :type index: int
    :returns: A dictionary.

    	The dictionary has the following fields:

    	- **'ok'**: True if the call was successful, False otherwise

    	- **'errorMsg':** String with the cause of the error. Only present if **'ok'** is False

    	- **'result':** A string with the translated text. Only present if **'ok'** is True
    """
	if(index > -1 and index < len(apyAddress)):
		apyList = [apyAddress[index]]
		last = 0
	else:
		apyList = apyAddress
		last = len(apyAddress)-1

	for it,address in enumerate(apyList):
		result = pairExists(source, target, it)

		if(pyVersion >= 3):
			try:
				text = text.decode("utf-8")
			except:
				pass
			try:
				source = source.decode("utf-8")
			except:
				pass
			try:
				target = target.decode("utf-8")
			except:
				pass

		if(result['ok']):
			if(result['result']):

				try:
					request = urllib2.urlopen(address+'/translate?q='+parse.quote_plus(text)+'&langpair='+source+'|'+target, timeout=timeout)
				except urllib2.URLError:
					if(it == last):
						return {'ok':False, 'errorMsg':'Error on connection'.encode('utf-8')}
					else:
						continue
				except urllib2.HTTPError:
					if(it == last):
						return {'ok':False, 'errorMsg':'Error on connection'.encode('utf-8')}
					else:
						continue
				except socket.timeout:
					if(it == last):
						return {'ok':False, 'errorMsg':'Request timed out'.encode('utf-8')}
					else:
						continue

				if(request.getcode() < 300):
					if(pyVersion >= 3):
						request = request.read().decode("utf-8")
						jsonObj = json.loads(request)
					else:
						jsonObj = json.load(request)

					return {'ok':True, 'result':parser.unescape(jsonObj['responseData']['translatedText']).replace('%20',' ').encode('utf-8')}

				else:
					if(it == last):
						return {'ok':False, 'errorMsg':'Response '+str(request.getcode())+' from APY'}
					else:
						continue

			else:
				if(it == last):
					return {'ok':False, 'errorMsg':('Pair '+source+'-'+target+' does not exist').encode('utf-8')}
				else:
					continue
		else:
			if(it == last):
				return result
			else:
				continue
