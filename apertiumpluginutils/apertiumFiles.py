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
:Synopsis: Manages the files and dictionary used with the plugin

This module makes use of a dictionary to store the plugin preferences for the user.

The dictionary has the following fields:

- **'apyAddress'** : 'address to make requests to'
- **'incoming'** : { *user1, user2, ...., userN* }
- **'outgoing'**: { *user1, user2, ...., userN* }

The structure for each *userN*:

- **name** :

	**'source'** : *source_language_str*

	**'target'** : *target_language_str*
"""

import pickle
import sys
import os.path

dictionary = None

fileName = 'apertium_plugin_pairs_preferences.pkl'

def setFile(newFileName):
	"""
	Sets the name for the file where the dictionary will be stored.

    :param newFileName: The name of the file.
    :type newFileName: str
    """
	global fileName

	fileName = newFileName

def createDictionary():
	"""
	Creates a new empty dictionary and stores it in a file.

    .. note::

       If the file to store the dictionary in does not exist, it is created.
    """
	global dictionary

	dictionary = {'version':sys.version_info[0], 'apyAddress':['http://localhost:2737'.encode('utf-8')], 'incoming':{}, 'outgoing':{}}

	file1 = open(fileName, 'wb')

	pickle.dump(dictionary, file1)
	file1.close()

def read():
	"""
	Reads the dictionary from a file.

    .. note::

       If the file to store the dictionary in does not exist, a new file and a dictionary are created with :func:`createDictionary`.

    :returns: The dictionary.
    """
	global dictionary

	if(not os.path.isfile(fileName)):
		createDictionary()

	file1 = open(fileName, 'rb')

	dictionary = pickle.load(file1)
	file1.close()

	return dictionary

def save():
	"""
	Saves the current state of the dictionary to a file.
    """
	global dictionary

	file1 = open(fileName, 'wb')

	pickle.dump(dictionary, file1)
	file1.close()

def getKey(key):
	"""
	Retrieves the value pointed by a key in the dictionary.

    :param key: Entry in the dictionary to look for.
    :type key: str
    :returns: Value pointed by key if it exists, or None otherwise.
    """
	global dictionary

	if(dictionary is None):
		read()

	if(key in dictionary.keys()):
		if(isinstance(dictionary[key],str) and sys.version_info[0] >= 3):
			return dictionary[key].encode('utf-8')
		else:
			return dictionary[key]
	else:
		return None

def setKey(key, value):
	"""
	Sets the value pointed by a key in the dictionary.

    :param key: Entry in the dictionary to set.
    :type key: str
    :param value: Value to be assigned to the key.
    """
	global dictionary

	if(dictionary is None):
		read()

	dictionary[key] = value

def setLangPair(direction, user, source, target):
	"""
	Sets the language pair to be associated with an user in a direction.

    :param direction: String containing 'incoming' or 'outgoing'.
    :type direction: str
    :param user: User the language pair will be associated to.
    :type user: str
    :param source: Source language of the pair.
    :type direction: str
    :param target: Target language of the pair.
    :type direction: str
    :returns: True on success, or False otherwise.
    """
	global dictionary

	newDict = {}
	newDict['source'] = source
	newDict['target'] = target

	try:
		dictionary[direction][user]=newDict
		return True
	except:
		return False

def unsetLangPair(direction, user):
	"""
	Removes the language pair associated with an user in a direction.

    :param direction: String containing 'incoming' or 'outgoing'.
    :type direction: str
    :param user: User whose language pair binding is to be removed.
    :type user: str
    :returns: True on success, or False otherwise.
    """
	global dictionary

	if(direction in dictionary.keys() and user in dictionary[direction]):
		del dictionary[direction][user]
		return True
	else:
		return False

def getDictionary():
	"""
	Retrieves the current dictionary.

    :param key: Entry in the dictionary to set.
    :type key: str
    :returns: The dictionary.
    """
	global dictionary

	if(dictionary is None):
		read()

	return dictionary

def setDictionary(newDictionary):
	"""
	Overrides the current dictionary with a new one.

    :param newDictionary: Dictionary to replace the old one with.
    """
	global dictionary

	dictionary = newDictionary
