#!/usr/bin/env python

import xchat
import operator
import time
import pickle
import os
import sys
import socket
import re
import math
import ssl

__module_name__ = "Idlerpg Playbot Script"
__module_version__ = "1.7"
__module_description__ = "Idlerpg Playbot Script"

if sys.version_info[0] >= 3:
	xchat.prnt("Python 3")
	import urllib.error
	import urllib.request
	import http.client
	python3 = True
if sys.version_info[0] < 3:
	xchat.prnt("Python 2")
	import urllib2
	import httplib
	python3 = False

# build hardcoded monster/creep lists, reverse
creeps = [	["Roach",       1500],   \
		["Spider",	2500],	\
		["Bat",         3500],  \
		["Wolf",        4500],  \
		["Goblin",	5500],	\
		["Shadow",	6500],	\
		["Lich",	7500],	\
		["Skeleton",	8500],	\
		["Ghost",       9500],	\
		["Phantom",     10500],  \
		["Troll",	12500],	\
		["Cyclop",      14500],  \
		["Mutant",	17500],	\
		["Ogre",        21500],  \
		["Phoenix",	25500],  \
		["Demon",       30500], \
		["Centaur",     35500], \
		["Werewolf",    40500], \
		["Giant",       9999999]  ]

monsters = [	["Blue_Dragon",	        8500],	\
		["Yellow_Dragon",       16000],  \
		["Green_Dragon",	26000],	\
		["Red_Dragon",	        36000], \
		["Black_Dragon",        41000], \
		["White_Dragon",        61000], \
		["Bronze_Dragon",       81000], \
		["Silver_Dragon",       101000], \
		["Gold_Dragon",         151000], \
		["Platinum_Dragon",     9999999]  ]

creeps.reverse()
monsters.reverse()

russweb = "http://russellb.x10.mx/"
gitweb = "https://github.com/RussellBeech/xchat-plugins"
gitweb2 = "https://raw.githubusercontent.com/RussellBeech/xchat-plugins/master/"
playerview = None 
playerview2 = None 
playerview3 = None 
playerview4 = None 
interval = 300
newlist = None
newlist2 = None
newlist3 = None
newlist4 = None
playerlist = None 
playerlist2 = None 
playerlist3 = None 
playerlist4 = None 
playerspage = None
playerspage2 = None
playerspage3 = None
playerspage4 = None
playerspagelist = None
mainhook = None
itemslists = None
currentversion = __module_version__
currentversion = float( currentversion )

CONFIG_FILE_LOCATION = xchat.get_info('xchatdir')+"/.playbotidlerpgquakemulti"
try:
	f = open(CONFIG_FILE_LOCATION,"rb")
	configList = pickle.load(f)
	f.close()
except:
	xchat.prnt("ConfigList Load Error - Using Default Settings")
	configList = []

# ZNC settings
ZNC = False # ZNC Server Mode - True = On, False = Off
ZNCServer = "*********" # ZNC Server Address
ZNCPort = "+8080" # ZNC Port Number - For SSL put + before and in " " "+8080"
ZNCUser = "***/***" # ZNC Username/Network
ZNCPass = "*********" # ZNC Password
ZNC2 = False # ZNC Server Mode - True = On, False = Off
ZNCServer2 = "*********" # ZNC Server Address
ZNCPort2 = "+8080" # ZNC Port Number - For SSL put + before and in " " "+8080"
ZNCUser2 = "***/***" # ZNC Username/Network
ZNCPass2 = "*********" # ZNC Password
ZNC3 = False # ZNC Server Mode - True = On, False = Off
ZNCServer3 = "*********" # ZNC Server Address
ZNCPort3 = "+8080" # ZNC Port Number - For SSL put + before and in " " "+8080"
ZNCUser3 = "***/***" # ZNC Username/Network
ZNCPass3 = "*********" # ZNC Password
ZNC4 = False # ZNC Server Mode - True = On, False = Off
ZNCServer4 = "*********" # ZNC Server Address
ZNCPort4 = "+8080" # ZNC Port Number - For SSL put + before and in " " "+8080"
ZNCUser4 = "***/***" # ZNC Username/Network
ZNCPass4 = "*********" # ZNC Password

# Changeable settings
servername = "irc.quakenet.org"
website = "https://quakeirpg.abandoned-irc.net"
setbuy = 15 # level to start buying items from
goldsave = 3100 # gold kept in hand
buylife = True
blackbuyspend = True
blackbuyspend14 = True
getgems = True
fightmode = True
channame = "#idlerpg"
setbotname = "IdleRPG"
creepattack = True # True = On, False = Off - Autocreep selection
setcreeptarget = "Werewolf" # Sets creep target. creepattack needs to be False to use
scrollssum = 3000 # Itemscore you start buying scrolls at
xpupgrade = True # Upgrade Items with XP
xpspend = 20 # Amount you use with xpget to upgrade items
bottextmode = True # True = on, False = off
errortextmode = True # True = on, False = off
intervaltext = True # True = on, False = off - Text displayed every interval
townworkswitch = True # True = Town/Work Area Switching, False = Town/Forest Area Switching
expbuy = False
slaysum = 1000 # minimum sum you start slaying without mana from

# declare stats as global
name = None
pswd = None
name2 = None
pswd2 = None
name3 = None
pswd3 = None
name4 = None
pswd4 = None
botname = setbotname
char1 = False
char2 = False
char3 = False
char4 = False
charcount = 0
private = True
chanmessage = True
chanmessagecount = 0
level = 0
mysum = 0
itemSum = 0
expertSum = 0
attackslaySum = 0
itemSum2 = 0
expertSum2 = 0
attackslaySum2 = 0
itemSum3 = 0
expertSum3 = 0
attackslaySum3 = 0
itemSum4 = 0
expertSum4 = 0
attackslaySum4 = 0
ufightcalc = 0
ufightcalc2 = 0
ufightcalc3 = 0
ufightcalc4 = 0
gold = 0
rank = 0
rank2 = 0
rank3 = 0
rank4 = 0

ttl = 0
atime = 0 # regentm
stime = 0 # slaytm

amulet = 0
charm = 0
helm = 0
boots = 0
gloves = 0
ring = 0
leggings = 0
shield = 0
tunic = 0
weapon = 0

fights = 0
scrolls = 0
exp = 0
mana = 0
stone1 = None
stone2 = None
stone3 = None
expert1 = None
expert2 = None
expert3 = None
expertitem1 = 0
expertitem2 = 0
expertitem3 = 0
expertitemb1 = 0
expertitemb2 = 0
expertitemb3 = 0
expertitemc1 = 0
expertitemc2 = 0
expertitemc3 = 0
expertitemd1 = 0
expertitemd2 = 0
expertitemd3 = 0
gems = 0
ability = None
xp = 0
life = 0
align = "n"
upgradelevel = 0

nickname = None
netname = None
nickname2 = None
netname2 = None
nickname3 = None
netname3 = None
nickname4 = None
netname4 = None
offline = None
offline2 = None
offline3 = None
offline4 = None
botcheck = None
botcheck2 = None
botcheck3 = None
botcheck4 = None
webworks = None 
gameactive = None
lottonum1 = None
lottonum2 = None
lottonum3 = None
location = None
locationtime = 0

game_chan = None
game_chan2 = None
game_chan3 = None
game_chan4 = None
botdisable1 = False
botdisable2 = False
botdisable3 = False
botdisable4 = False

for entry in configList:
	if(entry[0] == "blackbuyspend"):
		blackbuyspend = entry[1]
	if(entry[0] == "blackbuyspend14"):
		blackbuyspend14 = entry[1]
	if(entry[0] == "bottextmode"):
		bottextmode = entry[1]
	if(entry[0] == "buylife"):
		buylife = entry[1]
	if(entry[0] == "creepattack"):
		creepattack = entry[1]
	if(entry[0] == "errortextmode"):
		errortextmode = entry[1]
	if(entry[0] == "expbuy"):
		expbuy = entry[1]
	if(entry[0] == "fightmode"):
		fightmode = entry[1]
	if(entry[0] == "getgems"):
		getgems = entry[1]
	if(entry[0] == "goldsave"):
		goldsave = entry[1]
	if(entry[0] == "intervaltext"):
		intervaltext = entry[1]
	if(entry[0] == "scrollssum"):
		scrollssum = entry[1]
	if(entry[0] == "setbuy"):
		setbuy = entry[1]
	if(entry[0] == "setcreeptarget"):
		setcreeptarget = entry[1]
	if(entry[0] == "slaysum"):
		slaysum = entry[1]
	if(entry[0] == "townworkswitch"):
		townworkswitch = entry[1]
	if(entry[0] == "xpspend"):
		xpspend = entry[1]
	if(entry[0] == "xpupgrade"):
		xpupgrade = entry[1]
	if(entry[0] == "ZNC"):
		ZNC = entry[1]
	if(entry[0] == "ZNC2"):
		ZNC2 = entry[1]
	if(entry[0] == "ZNC3"):
		ZNC3 = entry[1]
	if(entry[0] == "ZNC4"):
		ZNC4 = entry[1]

# hook unload
def unloaded(userdata):
	xchat.prnt("Playbot Deactivated.")
xchat.hook_unload(unloaded)

# Announce activation
xchat.prnt("Playbot Activated.")

def versionchecker():
	global currentversion
	global python3
	global russweb
	global gitweb
	global gitweb2

	webversion = 0
	gitversion = 0
	newversion = 0
	try:
		if python3 is False:
			text = urllib2.urlopen(russweb + "playbotversionquake.txt")
		if python3 is True:
			text = urllib.request.urlopen(russweb + "playbotversionquake.txt")
		webversion = text.read()
		webversion = float( webversion )
		text.close()

	except:
		xchat.prnt( "Could not access {0}".format(russweb))

	try:
		if python3 is False:
			text2 = urllib2.urlopen(gitweb2 + "playbotversionquake.txt")
		if python3 is True:
			text2 = urllib.request.urlopen(gitweb2 + "playbotversionquake.txt")
		gitversion = text2.read()
		text2.close()
		if python3 is True:
			gitversion = gitversion.decode("UTF-8")
		gitversion = float( gitversion )

	except:
		xchat.prnt("Could not access {0}".format(gitweb2))

	xchat.prnt("Current version {0}".format(currentversion))
	xchat.prnt("Web version {0}".format(webversion))
	xchat.prnt("GitHub version {0}".format(gitversion))
	if webversion > gitversion:
		newversion = webversion
	if webversion < gitversion:
		newversion = gitversion
	if webversion == gitversion:
		newversion = gitversion
		
	if newversion > 0:
		if(currentversion == newversion):
			xchat.prnt("You have the current version of PlayBot")
		if(currentversion < newversion):
			xchat.prnt("You have an old version of PlayBot")
			xchat.prnt("You can download a new version from {0} or {1}".format(russweb, gitweb))
		if(currentversion > newversion):
			xchat.prnt("Give me, Give me")

def configwrite():
	global blackbuyspend
	global blackbuyspend14
	global buylife
	global creepattack
	global expbuy
	global fightmode
	global getgems
	global goldsave
	global intervaltext
	global scrollssum
	global setbuy
	global setcreeptarget
	global slaysum
	global townworkswitch
	global xpspend
	global xpupgrade
	global ZNC
	global ZNC2
	global ZNC3
	global ZNC4
	global bottextmode
	global errortextmode
	
	configList = []
	configList.append( ( "blackbuyspend", blackbuyspend ) )
	configList.append( ( "blackbuyspend14", blackbuyspend14 ) )
	configList.append( ( "bottextmode", bottextmode ) )
	configList.append( ( "buylife", buylife ) )
	configList.append( ( "creepattack", creepattack ) )
	configList.append( ( "errortextmode", errortextmode ) )
	configList.append( ( "expbuy", expbuy ) )
	configList.append( ( "fightmode", fightmode ) )
	configList.append( ( "getgems", getgems ) )
	configList.append( ( "goldsave", goldsave ) )
	configList.append( ( "intervaltext", intervaltext ) )
	configList.append( ( "scrollssum", scrollssum ) )
	configList.append( ( "setbuy", setbuy ) )
	configList.append( ( "setcreeptarget", setcreeptarget ) )
	configList.append( ( "slaysum", slaysum ) )
	configList.append( ( "townworkswitch", townworkswitch ) )
	configList.append( ( "xpspend", xpspend ) )
	configList.append( ( "xpupgrade", xpupgrade ) )
	configList.append( ( "ZNC", ZNC ) )
	configList.append( ( "ZNC2", ZNC2 ) )
	configList.append( ( "ZNC3", ZNC3 ) )
	configList.append( ( "ZNC4", ZNC4 ) )
	f = open(CONFIG_FILE_LOCATION,"wb")
	pickle.dump(configList,f)
	f.close()

def bottester(num):
	global game_chan
	global game_chan2
	global game_chan3
	global game_chan4
	global botname
	global char1
	global char2
	global char3
	global char4
	global botdisable1
	global botdisable2
	global botdisable3
	global botdisable4
	global setbotname
	
	botcount1 = 0
	botcount2 = 0
	botcount3 = 0
	botcount4 = 0
	botname = setbotname

	if num == 1 and char1 is True:

		userlist = game_chan.get_list("users")
		bottest = botname
		botentry = []

		for user in userlist:
			if bottest in user.nick and user.nick != bottest:
				botprefix = user.prefix
				if(botprefix == "@"):
					botentry.append(user.nick)
					botname10 = user.nick
		botcount1 = len(botentry)
		if botcount1 == 1:
			botname = botname10
		if botcount1 >= 2:
			botdisable1 = True
	if num == 2 and char2 is True:

		userlist = game_chan2.get_list("users")
		bottest = botname
		botentry = []
		
		for user in userlist:
			if bottest in user.nick and user.nick != bottest:
				botprefix = user.prefix
				if(botprefix == "@"):
					botentry.append(user.nick)
					botname10 = user.nick
		botcount2 = len(botentry)
		if botcount2 == 1:
			botname = botname10
		if botcount2 >= 2:
			botdisable2 = True

	if num == 3 and char3 is True:

		userlist = game_chan3.get_list("users")
		bottest = botname
		botentry = []
		
		for user in userlist:
			if bottest in user.nick and user.nick != bottest:
				botprefix = user.prefix
				if(botprefix == "@"):
					botentry.append(user.nick)
					botname10 = user.nick
		botcount3 = len(botentry)
		if botcount3 == 1:
			botname = botname10
		if botcount3 >= 2:
			botdisable3 = True

	if num == 4 and char4 is True:

		userlist = game_chan4.get_list("users")
		bottest = botname
		botentry = []
		
		for user in userlist:
			if bottest in user.nick and user.nick != bottest:
				botprefix = user.prefix
				if(botprefix == "@"):
					botentry.append(user.nick)
					botname10 = user.nick
		botcount4 = len(botentry)
		if botcount4 == 1:
			botname = botname10
		if botcount4 >= 2:
			botdisable4 = True

def usecommand(commanded, num):
	global game_chan
	global game_chan2
	global game_chan3
	global game_chan4
	global botname
	global channame
	global botdisable1
	global botdisable2
	global botdisable3
	global botdisable4
					
	if num == 1:
		bottester(1)
	if num == 2:
		bottester(2)
	if num == 3:
		bottester(3)
	if num == 4:
		bottester(4)

	if num == 1 and botdisable1 is False:
		try:
			game_chan.command( "msg {0} {1}".format(botname, commanded) )
		except AttributeError:
			xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame) )
	if num == 2 and botdisable2 is False:
		try:
			game_chan2.command( "msg {0} {1}".format(botname, commanded) )
		except AttributeError:
			xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame) )
	if num == 3 and botdisable3 is False:
		try:
			game_chan3.command( "msg {0} {1}".format(botname, commanded) )
		except AttributeError:
			xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame) )
	if num == 4 and botdisable4 is False:
		try:
			game_chan4.command( "msg {0} {1}".format(botname, commanded) )
		except AttributeError:
			xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame) )

xchat.prnt( "To start PlayBot use /login CharName Password" )

def login(word, word_eol, userdata):
	global name
	global pswd
	global name2
	global pswd2
	global name3
	global pswd3
	global name4
	global pswd4
	global setbuy
	global buylife
	global netname
	global nickname
	global netname2
	global nickname2
	global netname3
	global nickname3
	global netname4
	global nickname4
	global channame
	global gameactive
	global fightmode
	global charcount
	global game_chan
	global game_chan2
	global game_chan3
	global game_chan4
	global char1
	global char2
	global char3
	global char4
	global blackbuyspend
	global blackbuyspend14
	global getgems
	global scrollssum
	global xpupgrade
	global xpspend
	global intervaltext
	global townworkswitch
	global goldsave
	global creepattack
	global expbuy
	global playerspagelist
	global webworks
	global slaysum
	global bottextmode
	global errortextmode

	charcount += 1

	if charcount == 1:
		gameactive = True
		netname = xchat.get_info("network")
		nickname = xchat.get_info("nick")
		namecheck = False
		# find context
		game_chan = xchat.find_context(channel=channame)

		if "undernet" in netname and channame.lower() == "#irpg":
			xchat.prnt("The #irpg game on Undernet is not supported.  Expect your head to explode if you continue")
		if(game_chan is None):
			xchat.prnt("Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame))
			charcount = 0
		try:
			if(name is None or pswd is None):
				name = word[1]
				pswd = word[2]
		except IndexError:
			xchat.prnt( "LOGIN ERROR: To log in use /login CharName Password" )
			charcount = 0
		webdata()
		if(name is None or pswd is None):
			charcount = 0
			xchat.prnt("Login Failed")
		if charcount == 1:
			try:
				for entry in playerspagelist:
					if ">{0}<".format(name) in entry:
						namecheck = True
			except TypeError:
				webworks = False
			if(namecheck is False and webworks is True):
				xchat.prnt("LOGIN ERROR: {0} does not exist".format(name))
				charcount = 0

		if charcount == 0:
			gameactive = False
			name = None
			pswd = None
			return

		if charcount == 1:
			if(name != None and pswd != None):
				char1 = True
				usecommand("login {0} {1}".format(name, pswd), 1 )
	
	if charcount == 2:
		netname2 = xchat.get_info("network")
		nickname2 = xchat.get_info("nick")
		namecheck2 = False
		# find context
		game_chan2 = xchat.find_context(channel=channame)

		if "undernet" in netname2 and channame.lower() == "#irpg":
			xchat.prnt("The #irpg game on Undernet is not supported.  Expect your head to explode if you continue")
		if(game_chan2 is None):
			xchat.prnt("Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame))
			charcount = 1
		try:
			if(name2 is None or pswd2 is None):
				name2 = word[1]
				pswd2 = word[2]
		except IndexError:
			xchat.prnt( "LOGIN ERROR: To log in use /login CharName Password" )
			charcount = 1
		webdata()
		if(name2 is None or pswd2 is None):
			charcount = 1
			xchat.prnt("Login Failed")
		try:
			for entry in playerspagelist:
				if ">{0}<".format(name2) in entry:
					namecheck2 = True
		except TypeError:
			webworks = False
		if(namecheck2 is False and webworks is True):
			xchat.prnt("LOGIN ERROR: {0} does not exist".format(name2))
			charcount = 1
		if charcount == 2:
			if(nickname2 == nickname):
				charcount = 1
				xchat.prnt("Character {0} is already logged in".format(name))
			if(nickname2 != nickname):
				if name2 != name:
					char2 = True
					usecommand("login {0} {1}".format(name2, pswd2), 2 )
				if name2 == name:
					charcount = 1
					xchat.prnt("Character {0} is already logged in".format(name))
		if charcount == 1:
			char2 = False
			netname2 = None
			nickname2 = None
			game_chan2 = None
			name2 = None
			pswd2 = None
			return

	if charcount == 3:
		netname3 = xchat.get_info("network")
		nickname3 = xchat.get_info("nick")
		namecheck3 = False
		# find context
		game_chan3 = xchat.find_context(channel=channame)

		if "undernet" in netname3 and channame.lower() == "#irpg":
			xchat.prnt("The #irpg game on Undernet is not supported.  Expect your head to explode if you continue")
		if(game_chan3 is None):
			xchat.prnt("Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame))
			charcount = 2
		try:
			if(name3 is None or pswd3 is None):
				name3 = word[1]
				pswd3 = word[2]
		except IndexError:
			xchat.prnt( "LOGIN ERROR: To log in use /login CharName Password" )
			charcount = 2
		webdata()
		if(name3 is None or pswd3 is None):
			charcount = 2
			xchat.prnt("Login Failed")
		try:
			for entry in playerspagelist:
				if ">{0}<".format(name3) in entry:
					namecheck3 = True
		except TypeError:
			webworks = False
		if(namecheck3 is False and webworks is True):
			xchat.prnt("LOGIN ERROR: {0} does not exist".format(name3))
			charcount = 2
		if charcount == 3:
			if(nickname3 != nickname and name3 != name and nickname3 != nickname2 and name3 != name2):
				char3 = True
				usecommand("login {0} {1}".format(name3, pswd3), 3 )
			if(nickname3 == nickname or name3 == name):
				charcount = 2
				xchat.prnt("Character {0} is already logged in".format(name))
			if(nickname3 == nickname2 or name3 == name2):
				charcount = 2
				xchat.prnt("Character {0} is already logged in".format(name2))
		if charcount == 2:
			char3 = False
			netname3 = None
			nickname3 = None
			game_chan3 = None
			name3 = None
			pswd3 = None
			return

	if charcount == 4:
		netname4 = xchat.get_info("network")
		nickname4 = xchat.get_info("nick")
		namecheck4 = False
		# find context
		game_chan4 = xchat.find_context(channel=channame)

		if "undernet" in netname4 and channame.lower() == "#irpg":
			xchat.prnt("The #irpg game on Undernet is not supported.  Expect your head to explode if you continue")
		if(game_chan4 is None):
			xchat.prnt("Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame))
			charcount = 3
		try:
			if(name4 is None or pswd4 is None):
				name4 = word[1]
				pswd4 = word[2]
		except IndexError:
			xchat.prnt( "LOGIN ERROR: To log in use /login CharName Password" )
			charcount = 3
		webdata()
		if(name4 is None or pswd4 is None):
			charcount = 3
			xchat.prnt("Login Failed")
		try:
			for entry in playerspagelist:
				if ">{0}<".format(name4) in entry:
					namecheck4 = True
		except TypeError:
			webworks = False
		if(namecheck4 is False and webworks is True):
			xchat.prnt("LOGIN ERROR: {0} does not exist".format(name4))
			charcount = 3
		if charcount == 4:
			if(nickname4 != nickname and name4 != name and nickname4 != nickname2 and name4 != name2 and nickname4 != nickname3 and name4 != name3):
				char4 = True
				usecommand("login {0} {1}".format(name4, pswd4), 4 )
			if(nickname4 == nickname or name4 == name):
				charcount = 3
				xchat.prnt("Character {0} is already logged in".format(name))
			if(nickname4 == nickname2 or name4 == name2):
				charcount = 3
				xchat.prnt("Character {0} is already logged in".format(name2))
			if(nickname4 == nickname3 or name4 == name3):
				charcount = 3
				xchat.prnt("Character {0} is already logged in".format(name3))
		if charcount == 3:
			char4 = False
			netname4 = None
			nickname4 = None
			game_chan4 = None
			name4 = None
			pswd4 = None
			return

	if (charcount >= 1 and charcount <= 4):        
		time.sleep(3) # Needed
		usecommand("whoami", charcount)
		xchat.prnt("Player Character {0} has logged in".format(charcount))
	if charcount == 1:
		if blackbuyspend is True:
			xchat.prnt("BlackBuy Spend Mode Activated.  To turn it off use /blackbuyoff")
		if blackbuyspend is False:
			xchat.prnt("BlackBuy Spend Mode Deactivated.  To turn it off use /blackbuyon")
		if blackbuyspend14 is True:
			xchat.prnt("BlackBuy Spend 14 Mode Activated.  To turn it off use /blackbuy14off")
		if blackbuyspend14 is False:
			xchat.prnt("BlackBuy Spend 14 Mode Deactivated.  To turn it off use /blackbuy14on")
		if bottextmode is True:
			xchat.prnt("Bot Text Mode Activated.  To turn it off use /bottextoff")
		if buylife is True:
			xchat.prnt("Buy Life Mode Activated.  To turn it off use /buylifeoff")
		if buylife is False:
			xchat.prnt("Buy Life Mode Deactivated.  To turn it on use /buylifeon")
		if creepattack is True:
			xchat.prnt("CreepAttack Mode Activated.  To turn it off use /creepattackoff")
		if creepattack is False:
			xchat.prnt("CreepAttack Mode Deactivated.  To turn it on use /creepattackon")
		if errortextmode is True:
			xchat.prnt("Error Text Mode Activated.  To turn it off use /errortextoff")
		if expbuy is True:
			xchat.prnt("Experience Buying Mode Activated.  To turn it off use /expbuyoff")
		if expbuy is False:
			xchat.prnt("Experience Buying Mode Deactivated.  To turn it on use /expbuyon")
		if fightmode is True:
			xchat.prnt("Fighting Mode Activated.  To turn it off use /fightoff")
		if fightmode is False:
			xchat.prnt("Fighting Mode Deactivated.  To turn it on use /fighton")
		if getgems is True:
			xchat.prnt("GetGems Mode Activated.  To turn it off use /getgemsoff")
		if getgems is False:
			xchat.prnt("GetGems Mode Deactivated.  To turn it on use /getgemson")
		if intervaltext is True:
			xchat.prnt("Interval Text Mode Activated.  To turn it off use /intervaltextoff")
		if townworkswitch is True:
			xchat.prnt("Town/Work Switch Mode Activated.  To change to Town/Forest use /townforest")
		if townworkswitch is False:
			xchat.prnt("Town/Forest Switch Mode Activated.  To change to Town/Work use /townwork")
		if xpupgrade is True:
			xchat.prnt("XPUpgrade Mode Activated.  To turn it off use /xpupgradeoff")
		if xpupgrade is False:
			xchat.prnt("XPUpgrade Mode Deactivated.  To turn it on use /xpupgradeon")
		xchat.prnt("Current Goldsave: {0}.  If you want to change it use /setgoldsave number".format(goldsave))
		xchat.prnt("Current Item Buy Level: {0}.  If you want to change it use /setitembuy number".format(setbuy))
		xchat.prnt("Current Scrolls Buy ItemScore: {0}.  If you want to change it use /setscrolls number".format(scrollssum))
		xchat.prnt("Current SlaySum Minimum ItemScore: {0}.  If you want to change it use /setslaysum number".format(slaysum))
		xchat.prnt("Current XPSpend for xpget item upgrades: {0}.  If you want to change it use /setxpspend number".format(xpspend))
		xchat.prnt("")
		xchat.prnt("For a list of PlayBot commands use /helpplaybot")
		xchat.prnt("")
		versionchecker()
	if charcount >= 5:
		xchat.prnt("You can only play with 4 characters")
		charcount = 4

	# call main directly
	main(None)
	return xchat.EAT_ALL

# hook login command
xchat.hook_command("login", login, help="/login <charname> <password> - You can use this to login your character into the game")

def logoutchar(word, word_eol, userdata):
	global charcount
	global char1
	global char2
	global char3
	global char4
	global netname
	global netname2
	global netname3
	global netname4
	global game_chan
	global game_chan2
	global game_chan3
	global game_chan4
	global name
	global name2
	global name3
	global name4
	global pswd
	global pswd2
	global pswd3
	global pswd4
	global gameactive

	if charcount == 4:
		xchat.prnt("Character {0} Logged Out".format(name4))
		char4 = False
		netname4 = None
		game_chan4 = None
		name4 = None
		pswd4 = None
	if charcount == 3:
		xchat.prnt("Character {0} Logged Out".format(name3))
		char3 = False
		netname3 = None
		game_chan3 = None
		name3 = None
		pswd3 = None
	if charcount == 2:
		xchat.prnt("Character {0} Logged Out".format(name2))
		char2 = False
		netname2 = None
		game_chan2 = None
		name2 = None
		pswd2 = None
	if charcount == 1:
		xchat.prnt("Character {0} Logged Out".format(name))
		char1 = False
		netname = None
		game_chan = None
		name = None
		pswd = None
		gameactive = False
	if(charcount == 0):
		xchat.prnt("All Characters have already been Logged Out")
	if(charcount >= 1 and charcount <= 4):
		charcount -= 1
	return xchat.EAT_ALL

xchat.hook_command("logoutchar", logoutchar, help="/logoutchar - Logs out the last character from the PlayBot")

def setgoldsave(word, word_eol, userdata):
	global goldsave
	global gameactive

	if gameactive is True:
		try:
			goldsave = word[1]
			goldsave = int( goldsave )
		except IndexError:
			xchat.prnt("To change Item buy level use /setgoldsave number")
		xchat.prnt("Goldsave changed to {0}".format(goldsave))
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("setgoldsave", setgoldsave, help="/setgoldsave <number> - Sets how much gold you keep in hand")

def setitembuy(word, word_eol, userdata):
	global setbuy
	global gameactive

	if gameactive is True:
		try:
			setbuy = word[1]
			setbuy = int( setbuy )
		except IndexError:
			xchat.prnt("To change Item buy level use /setitembuy number")
		xchat.prnt("Item Buy Level changed to {0}".format(setbuy))
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("setitembuy", setitembuy, help="/setitembuy <number> - Sets at which level you will start buying items from")

def setscrolls(word, word_eol, userdata):
	global scrollssum
	global gameactive

	if gameactive is True:
		try:
			scrollssum = word[1]
			scrollssum = int( scrollssum )
		except IndexError:
			xchat.prnt("To change Itemscore at which you start buying scrolls use /setscrolls number")
		xchat.prnt("Scrolls Buy ItemScore changed to {0}".format(scrollssum))
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("setscrolls", setscrolls, help="/setscrolls <number> - Itemscore at which you start buying scrolls")

def setslaysum(word, word_eol, userdata):
	global slaysum
	global gameactive

	if gameactive is True:
		try:
			slaysum = word[1]
			slaysum = int( slaysum )
		except IndexError:
			xchat.prnt("To change SlaySum at which you start slaying dragons use /setslaysum number")
		xchat.prnt("SlaySum Minimum ItemScore changed to {0}".format(slaysum))
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("setslaysum", setslaysum, help="/setslaysum <number> - Itemscore at which you start slaying dragons")

def setxpspend(word, word_eol, userdata):
	global xpspend
	global gameactive

	if gameactive is True:
		try:
			testxpspend = word[1]
			testxpspend = int( testxpspend )
		except IndexError:
			xchat.prnt("To change how much you spend with xpget when upgrading items use /setxpspend number")
		if testxpspend >= 20:
			xpspend = testxpspend
			xchat.prnt("XPSpend for Item Upgrade changed to {0}".format(xpspend))
		if testxpspend < 20:
			xchat.prnt("XPSpend needs to be 20 or over")

		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("setxpspend", setxpspend, help="/setxpspend <number> - Sets how much you spend with xpget when upgrading items")

def expbuyoff(word, word_eol, userdata):
	global expbuy
	global gameactive
	
	if gameactive is True:
		expbuy = False
		xchat.prnt("Experience Buying Mode Deactivated.  To turn it on use /expbuyon")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("expbuyoff", expbuyoff, help="/expbuyoff - Turns Experience Buying off")

def expbuyon(word, word_eol, userdata):
	global expbuy
	global gameactive
	
	if gameactive is True:
		expbuy = True
		xchat.prnt("Experience Buying Mode Activated.  To turn it off use /expbuyoff")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("expbuyon", expbuyon, help="/expbuyon - Turns Experience Buying on")

def xpupgradeoff(word, word_eol, userdata):
	global xpupgrade
	global gameactive
	
	if gameactive is True:
		xpupgrade = False
		xchat.prnt("XPUpgrade Mode Deactivated.  To turn it on use /xpupgradeon")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("xpupgradeoff", xpupgradeoff, help="/xpupgradeoff - Turns XPUpgrade off")

def xpupgradeon(word, word_eol, userdata):
	global xpupgrade
	global gameactive

	if gameactive is True:
		xpupgrade = True
		xchat.prnt("XPUpgrade Mode Activated.  To turn if off use /xpupgradeoff")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("xpupgradeon", xpupgradeon, help="/xpupgradeon - Turns XPUpgrade on")

def zncoff(word, word_eol, userdata):
	global ZNC
	global ZNC2
	global ZNC3
	global ZNC4
	global gameactive
	
	if gameactive is True:
		try:
			testznc = word[1]
		except IndexError:
			xchat.prnt("To ZNC On use /zncon charnumber")
		try:
			if str.isdigit(testznc):
				num = int( testznc )
		except UnboundLocalError:
			return

		if num == 1:
			ZNC = False
			xchat.prnt("ZNC Mode Deactivated.  To turn it on use /zncon 1")
		if num == 2:
			ZNC2 = False
			xchat.prnt("ZNC2 Mode Deactivated.  To turn it on use /zncon 2")
		if num == 3:
			ZNC3 = False
			xchat.prnt("ZNC3 Mode Deactivated.  To turn it on use /zncon 3")
		if num == 4:
			ZNC4 = False
			xchat.prnt("ZNC4 Mode Deactivated.  To turn it on use /zncon 4")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("zncoff", zncoff, help="/zncoff - Turns ZNC off")

def zncon(word, word_eol, userdata):
	global ZNC
	global ZNC2
	global ZNC3
	global ZNC4
	global gameactive

	if gameactive is True:
		try:
			testznc = word[1]
		except IndexError:
			xchat.prnt("To ZNC On use /zncon charnumber")
		try:
			if str.isdigit(testznc):
				num = int( testznc )
		except UnboundLocalError:
			return

		if num == 1:
			ZNC = True
			xchat.prnt("ZNC Mode Activated.  To turn if off use /zncoff 1")
		if num == 2:
			ZNC2 = True
			xchat.prnt("ZNC2 Mode Activated.  To turn if off use /zncoff 2")
		if num == 3:
			ZNC3 = True
			xchat.prnt("ZNC3 Mode Activated.  To turn if off use /zncoff 3")
		if num == 4:
			ZNC4 = True
			xchat.prnt("ZNC4 Mode Activated.  To turn if off use /zncoff 4")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("zncon", zncon, help="/zncon - Turns ZNC on")

def creepattackoff(word, word_eol, userdata):
	global creepattack
	global gameactive

	if gameactive is True:
		creepattack = False
		xchat.prnt("CreepAttack Mode Deactivated.  To turn it on use /creepattackon")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("creepattackoff", creepattackoff, help="/creepattackoff - Turns CreepAttack mode off")

def creepattackon(word, word_eol, userdata):
	global creepattack
	global gameactive

	if gameactive is True:
		creepattack = True
		xchat.prnt("CreepAttack Mode Activated.  To turn it off use /creepattackoff")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("creepattackon", creepattackon, help="/creepattackon - Turns CreepAttack mode on")

def setcreep(word, word_eol, userdata):
	global setcreeptarget
	global creeps
	global gameactive

	if gameactive is True:
		try:
			testsetcreeptarget = word[1]
		except IndexError:
			xchat.prnt("To change creep use /setcreep creep")
		creepcheck = False
		for entry in creeps:
			if testsetcreeptarget == entry[0]:
				creepcheck = True
		if creepcheck is True:
			setcreeptarget = testsetcreeptarget
			xchat.prnt("Creep changed to {0}".format(setcreeptarget))
			configwrite()
		if creepcheck is False:
			xchat.prnt("Creep is not on the creep list")
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("setcreep", setcreep, help="/setcreep <creep> - Sets creep for manual creep selection")

def getgemsoff(word, word_eol, userdata):
	global getgems
	global gameactive

	if gameactive is True:
		getgems = False
		xchat.prnt("GetGems Mode Deactivated.  To turn it on use /getgemson")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("getgemsoff", getgemsoff, help="/getgemsoff - Turns GetGems mode off")

def getgemson(word, word_eol, userdata):
	global getgems
	global gameactive

	if gameactive is True:
		getgems = True
		xchat.prnt("GetGems Mode Activated.  To turn it off use /getgemsoff")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("getgemson", getgemson, help="/getgemson - Turns GetGems mode on")

def blackbuyoff(word, word_eol, userdata):
	global blackbuyspend
	global gameactive

	if gameactive is True:
		blackbuyspend = False
		xchat.prnt("BlackBuy Spend Mode Deactivated.  To turn it on use /blackbuyon")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("blackbuyoff", blackbuyoff, help="/blackbuyoff - Turns BlackBuy Spend mode off")

def blackbuyon(word, word_eol, userdata):
	global blackbuyspend
	global gameactive

	if gameactive is True:
		blackbuyspend = True
		xchat.prnt("BlackBuy Spend Mode Activated.  To turn if off use /blackbuyoff")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("blackbuyon", blackbuyon, help="/blackbuyon - Turns BlackBuy Spend mode on")

def blackbuy14off(word, word_eol, userdata):
	global blackbuyspend14
	global gameactive

	if gameactive is True:
		blackbuyspend14 = False
		xchat.prnt("BlackBuy Spend 14 Mode Deactivated.  To turn it on use /blackbuy14on")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("blackbuy14off", blackbuy14off, help="/blackbuy14off - Turns BlackBuy 14 Spend mode off")

def blackbuy14on(word, word_eol, userdata):
	global blackbuyspend14
	global gameactive

	if gameactive is True:
		blackbuyspend14 = True
		xchat.prnt("BlackBuy Spend 14 Mode Activated.  To turn if off use /blackbuy14off")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("blackbuy14on", blackbuy14on, help="/blackbuy14on - Turns BlackBuy 14 Spend mode on")

def buylifeoff(word, word_eol, userdata):
	global buylife
	global gameactive

	if gameactive is True:
		buylife = False
		xchat.prnt("Buy Life Mode Deactivated.  To turn it on use /buylifeon")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("buylifeoff", buylifeoff, help="/buylifeoff - Turns life buying off")

def buylifeon(word, word_eol, userdata):
	global buylife
	global gameactive

	if gameactive is True:
		buylife = True
		xchat.prnt("Buy Life Mode Activated.  To turn if off use /buylifeoff")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("buylifeon", buylifeon, help="/buylifeon - Turns life buying on")

def fightoff(word, word_eol, userdata):
	global fightmode
	global gameactive

	if gameactive is True:
		fightmode = False
		xchat.prnt("Fight Mode Deactivated.  To turn it on use /fighton")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("fightoff", fightoff, help="/fightoff - Turns Fighting off")

def fighton(word, word_eol, userdata):
	global fightmode
	global gameactive

	if gameactive is True:
		fightmode = True
		xchat.prnt("Fight Mode Activated.  To turn if off use /fightoff")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("fighton", fighton, help="/fighton - Turns Fighting on")

def bottextoff(word, word_eol, userdata):
	global bottextmode
	global gameactive

	if gameactive is True:
		bottextmode = False
		xchat.prnt("Bot Text Mode Deactivated.  To turn it back on use /bottexton")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("bottextoff", bottextoff, help="/bottextoff - Turns off Bot Text")

def bottexton(word, word_eol, userdata):
	global bottextmode
	global gameactive

	if gameactive is True:
		bottextmode = True
		xchat.prnt("Bot Text Mode Activated.  To turn it back off use /bottextoff")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("bottexton", bottexton, help="/bottexton - Turns on Bot Text")

def intervaltextoff(word, word_eol, userdata):
	global intervaltext
	global gameactive

	if gameactive is True:
		intervaltext = False
		xchat.prnt("Interval Text Mode Deactivated.  To turn it back on use /intervaltexton")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("intervaltextoff", intervaltextoff, help="/intervaltextoff - Turns off Interval Text")

def intervaltexton(word, word_eol, userdata):
	global intervaltext
	global gameactive

	if gameactive is True:
		intervaltext = True
		xchat.prnt("Interval Text Mode Activated.  To turn it back off use /intervaltextoff")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("intervaltexton", intervaltexton, help="/intervaltexton - Turns on Interval Text")

def errortextoff(word, word_eol, userdata):
	global errortextmode
	global gameactive

	if gameactive is True:
		errortextmode = False
		xchat.prnt("Error Text Mode Deactivated.  To turn it back on use /errortexton")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("errortextoff", errortextoff, help="/errortextoff - Turns off Error Text")

def errortexton(word, word_eol, userdata):
	global errortextmode
	global gameactive

	if gameactive is True:
		errortextmode = True
		xchat.prnt("Error Text Mode Activated.  To turn it back off use /errortextoff")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("errortexton", errortexton, help="/errortexton - Turns on Error Text")

def townwork(word, word_eol, userdata):
	global townworkswitch
	global gameactive

	if gameactive is True:
		townworkswitch = True
		xchat.prnt("Town/Work Switch Mode Activated.  To change to Town/Forest use /townforest")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("townwork", townwork, help="/townwork - Changes to Town/Work Switching")

def townforest(word, word_eol, userdata):
	global townworkswitch
	global gameactive

	if gameactive is True:
		townworkswitch = False
		xchat.prnt("Town/Forest Switch Mode Activated.  To change to Town/Work use /townwork")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("townforest", townforest, help="/townforest - Changes to Town/Forest Switching")

def versioncheck(word, word_eol, userdata):
	versionchecker()
	return xchat.EAT_ALL

xchat.hook_command("versioncheck", versioncheck, help="/versioncheck - To check if you have the latest version of PlayBot")

def helpplaybot(word, word_eol, userdata):
	xchat.prnt("PlayBot Commands List")
	xchat.prnt("")
	xchat.prnt("BlackBuy Spend Mode Off     - /blackbuyoff")
	xchat.prnt("BlackBuy Spend Mode On      - /blackbuyon")
	xchat.prnt("BlackBuy 14 Spend Mode Off  - /blackbuy14off")
	xchat.prnt("BlackBuy 14 Spend Mode On   - /blackbuy14on")
	xchat.prnt("Bot Text Mode Off           - /bottextoff")
	xchat.prnt("Bot Text Mode On            - /bottexton")
	xchat.prnt("Buy Life Mode Off           - /buylifeoff")
	xchat.prnt("Buy Life Mode On            - /buylifeon")
	xchat.prnt("CreepAttack Mode Off        - /creepattackoff")
	xchat.prnt("CreepAttack Mode On         - /creepattackon")
	xchat.prnt("Error Text Mode Off         - /errortextoff")
	xchat.prnt("Error Text Mode On          - /errortexton")
	xchat.prnt("Experince Buying Mode Off   - /expbuyoff")
	xchat.prnt("Experince Buying Mode On    - /expbuyon")
	xchat.prnt("Fighting Mode Off           - /fightoff")
	xchat.prnt("Fighting Mode On            - /fighton")
	xchat.prnt("GetGems Mode Off            - /getgemsoff")
	xchat.prnt("GetGems Mode On             - /getgemson")
	xchat.prnt("Interval Text Mode Off      - /intervaltextoff")
	xchat.prnt("Interval Text Mode On       - /intervaltexton")
	xchat.prnt("Log In Char                 - /login charname password")
	xchat.prnt("Log Out Char                - /logoutchar")
	xchat.prnt("PlayBot Commands List       - /helpplaybot")
	xchat.prnt("Player's Items              - /items")
	xchat.prnt("Player's Status             - /status")
	xchat.prnt("Set Creep Target            - /setcreep creep")
	xchat.prnt("Set Goldsave                - /setgoldsave number")
	xchat.prnt("Set Item Buy Level          - /setitembuy number")
	xchat.prnt("Set Scrolls Buy ItemScore   - /setscrolls number")
	xchat.prnt("Set SlaySum Min ItemScore   - /setslaysum number")
	xchat.prnt("Set XPSpend for upgrades    - /setxpspend number")
	xchat.prnt("Settings List               - /settings")
	xchat.prnt("Town/Forest Switch Mode     - /townforest")
	xchat.prnt("Town/Work Switch Mode       - /townwork")
	xchat.prnt("Version Checker             - /versioncheck")
	xchat.prnt("XPUpgrade Mode Off          - /xpupgradeoff")
	xchat.prnt("XPUpgrade Mode On           - /xpupgradeon")
	xchat.prnt("ZNC Mode Off                - /zncoff charnum")
	xchat.prnt("ZNC Mode On                 - /zncon charnum")
	xchat.prnt(" ")
	xchat.prnt("If you want more information about a command use /help <command> - ie /help settings")
	return xchat.EAT_ALL

xchat.hook_command("helpplaybot", helpplaybot, help="/helpplaybot - Gives a list of Playbot commands")

def settings(word, word_eol, userdata):
	global buylife
	global setbuy
	global char1
	global char2
	global char3
	global char4
	global name
	global name2
	global name3
	global name4
	global fightmode
	global ZNC
	global ZNC2
	global ZNC3
	global ZNC4
	global blackbuyspend
	global blackbuyspend14
	global getgems
	global creepattack
	global setcreeptarget
	global scrollssum
	global xpspend
	global xpupgrade
	global bottextmode
	global errortextmode
	global intervaltext
	global townworkswitch
	global goldsave
	global expbuy
	global slaysum
	
	xchat.prnt("Playbot Settings List")
	xchat.prnt("")
	if townworkswitch is True:
		xchat.prnt("Area Switch Mode - Town/Work")
	if townworkswitch is False:
		xchat.prnt("Area Switch Mode - Town/Forest")
	xchat.prnt("BlackBuy Spend Mode - {0}".format(blackbuyspend))
	xchat.prnt("BlackBuy 14 Spend Mode - {0}".format(blackbuyspend14))
	xchat.prnt("Bot Text Mode - {0}".format(bottextmode))
	xchat.prnt("Buy Life Mode - {0}".format(buylife))
	xchat.prnt("CreepAttack Mode - {0}".format(creepattack))
	xchat.prnt("Error Text Mode - {0}".format(errortextmode))
	xchat.prnt("Experience Buying Mode - {0}".format(expbuy))
	xchat.prnt("Fighting Mode - {0}".format(fightmode))
	xchat.prnt("GetGems Mode - {0}".format(getgems))
	xchat.prnt("Goldsave - {0}".format(goldsave))
	xchat.prnt("Interval Text Mode - {0}".format(intervaltext))
	xchat.prnt("Item Buy Level - {0}".format(setbuy))
	xchat.prnt("Player Character 1 - {0}, {1}".format(char1, name))
	xchat.prnt("Player Character 2 - {0}, {1}".format(char2, name2))
	xchat.prnt("Player Character 3 - {0}, {1}".format(char3, name3))
	xchat.prnt("Player Character 4 - {0}, {1}".format(char4, name4))
	xchat.prnt("Scrolls Buy ItemScore - {0}".format(scrollssum))
	xchat.prnt("Set Creep Target - {0}".format(setcreeptarget))
	xchat.prnt("SlaySum Minimum - {0}".format(slaysum))
	xchat.prnt("XPSpend Upgrade Amount - {0}".format(xpspend))
	xchat.prnt("XPUpgrade Mode - {0}".format(xpupgrade))
	xchat.prnt("ZNC Mode - {0}".format(ZNC))
	xchat.prnt("ZNC2 Mode - {0}".format(ZNC2))
	xchat.prnt("ZNC3 Mode - {0}".format(ZNC3))
	xchat.prnt("ZNC4 Mode - {0}".format(ZNC4))
	return xchat.EAT_ALL

xchat.hook_command("settings", settings, help="/settings - Gives a list of settings which you can change")

def newlister(num):
	global playerspagelist
	global newlist
	global newlist2
	global newlist3
	global newlist4
	global ability
	global python3
	global webworks
	global website
	global level
	global errortextmode
	
	test = []
	test2 = []
	test3 = []
	newlistererror = False

	if num == 1:
		newlist = []
	if num == 2:
		newlist2 = []
	if num == 3:
		newlist3 = []
	if num == 4:
		newlist4 = []
	getitems2(num)

	if webworks is True:
		testnum = 0
		for entry in playerspagelist:
			if "playerview.php" in entry:
				testnum += 1
				test = entry
				testadd = True
				if "offline" in test:
					testadd = False
				if testadd is True:
					test = re.sub(r'<.*?>', ' ', test)
					test = re.sub(r"&#039;", "'", test)
					test = test.split(" ")
					if testnum == 1:
						del test[0:14]
					test2.append(test)        

		for entry in test2:
			if(int(entry[8]) >= level):
				test3.append(entry)
		for player in test3:
			name_ = player[5]

			webworks2 = True
			weberror = False
			playerview20 = None
			playerlist20 = []

			# get raw player data from web, parse for relevant entry
			context = ssl._create_unverified_context()
			try:
				if python3 is False:
					text = urllib2.urlopen(website + "/playerview.php?player={0}".format(name_), context=context)
				if python3 is True:
					text = urllib.request.urlopen(website + "/playerview.php?player={0}".format(name_), context=context)
				playerview20 = text.read()
				text.close()
				if python3 is True:
					playerview20 = playerview20.decode("UTF-8")
			except:
				weberror = True
			if weberror is True:
				if errortextmode is True:
					xchat.prnt( "Could not access {0}".format(website))
				webworks2 = False

			# build list for player records
			if(playerview20 is None):
				if errortextmode is True:
					xchat.prnt( "Could not access {0}, unknown error.".format(website) )
				webworks2 = False
			else:
				playerlist20 = playerview20.split("\n")
				playerlist20 = playerlist20[:-1]

			amulettext = None
			bootstext = None
			charmtext = None
			glovestext = None
			helmtext = None
			leggingstext = None
			ringtext = None
			shieldtext = None
			tunictext = None
			weapontext = None
			amulet_ = None
			boots_ = None
			charm_ = None
			gloves_ = None
			helm_ = None
			leggings_ = None
			ring_ = None
			shield_ = None
			tunic_ = None
			weapon_ = None
			experttext1 = None
			experttext2 = None
			experttext3 = None
			expert1_ = None
			expert2_ = None
			expert3_ = None

			if webworks2 is True:
				for entry in playerlist20:
					if "amulet:" in entry:
						amulettext = entry
					if "boots:" in entry:
						bootstext = entry
					if "charm:" in entry:
						charmtext = entry
					if "gloves:" in entry:
						glovestext = entry
					if "helm:" in entry:
						helmtext = entry
					if "leggings:" in entry:
						leggingstext = entry
					if "ring:" in entry:
						ringtext = entry
					if "shield:" in entry:
						shieldtext = entry
					if "tunic:" in entry:
						tunictext = entry
					if "weapon:" in entry:
						weapontext = entry
					if "Expert 1:" in entry:
						experttext1 = entry
					if "Expert 2:" in entry:
						experttext2 = entry
					if "Expert 3:" in entry:
						experttext3 = entry
					
				try:
					amulettext = amulettext.split(" ")
					amuletsplit = amulettext[7]
					amulet_ = int(amuletsplit.strip("<br"))
					bootstext = bootstext.split(" ")
					bootssplit = bootstext[7]
					boots_ = int(bootssplit.strip("<br"))
					charmtext = charmtext.split(" ")
					charmsplit = charmtext[7]
					charm_ = int(charmsplit.strip("<br"))
					glovestext = glovestext.split(" ")
					glovessplit = glovestext[7]
					gloves_ = int(glovessplit.strip("<br"))
					helmtext = helmtext.split(" ")
					helmsplit = helmtext[7]
					helm_ = int(helmsplit.strip("<br"))
					leggingstext = leggingstext.split(" ")
					leggingssplit = leggingstext[7]
					leggings_ = int(leggingssplit.strip("<br"))
					ringtext = ringtext.split(" ")
					ringsplit = ringtext[7]
					ring_ = int(ringsplit.strip("<br"))
					shieldtext = shieldtext.split(" ")
					shieldsplit = shieldtext[7]
					shield_ = int(shieldsplit.strip("<br"))
					tunictext = tunictext.split(" ")
					tunicsplit = tunictext[7]
					tunic_ = int(tunicsplit.strip("<br"))
					weapontext = weapontext.split(" ")
					weaponsplit = weapontext[7]
					weapon_ = int(weaponsplit.strip("<br"))

					experttext1 = experttext1.split(" ")
					expertsplit1 = experttext1[8]
					expertsplitsplit1 = expertsplit1.split("<")
					expert1_ = expertsplitsplit1[0]
					experttext2 = experttext2.split(" ")
					expertsplit2 = experttext2[8]
					expertsplitsplit2 = expertsplit2.split("<")
					expert2_ = expertsplitsplit2[0]
					experttext3 = experttext3.split(" ")
					expertsplit3 = experttext3[8]
					expertsplitsplit3 = expertsplit3.split("<")
					expert3_ = expertsplitsplit3[0]
					expertcalcsum1 = 0
					expertcalcsum2 = 0
					expertcalcsum3 = 0
					if(expert1_ == "amulet"):
						expertcalcsum1 = amulet_ // 10
					if(expert1_ == "charm"):
						expertcalcsum1 = charm_ // 10
					if(expert1_ == "helm"):
						expertcalcsum1 = helm_ // 10
					if(expert1_ == "boots"):
						expertcalcsum1 = boots_ // 10
					if(expert1_ == "gloves"):
						expertcalcsum1 = gloves_ // 10
					if(expert1_ == "ring"):
						expertcalcsum1 = ring_ // 10
					if(expert1_ == "leggings"):
						expertcalcsum1 = leggings_ // 10
					if(expert1_ == "shield"):
						expertcalcsum1 = shield_ // 10
					if(expert1_ == "tunic"):
						expertcalcsum1 = tunic_ // 10
					if(expert1_ == "weapon"):
						expertcalcsum1 = weapon_ // 10

					if(expert2_ == "amulet"):
						expertcalcsum2 = amulet_ // 10
					if(expert2_ == "charm"):
						expertcalcsum2 = charm_ // 10
					if(expert2_ == "helm"):
						expertcalcsum2 = helm_ // 10
					if(expert2_ == "boots"):
						expertcalcsum2 = boots_ // 10
					if(expert2_ == "gloves"):
						expertcalcsum2 = gloves_ // 10
					if(expert2_ == "ring"):
						expertcalcsum2 = ring_ // 10
					if(expert2_ == "leggings"):
						expertcalcsum2 = leggings_ // 10
					if(expert2_ == "shield"):
						expertcalcsum2 = shield_ // 10
					if(expert2_ == "tunic"):
						expertcalcsum2 = tunic_ // 10
					if(expert2_ == "weapon"):
						expertcalcsum2 = weapon_ // 10

					if(expert3_ == "amulet"):
						expertcalcsum3 = amulet_ // 10
					if(expert3_ == "charm"):
						expertcalcsum3 = charm_ // 10
					if(expert3_ == "helm"):
						expertcalcsum3 = helm_ // 10
					if(expert3_ == "boots"):
						expertcalcsum3 = boots_ // 10
					if(expert3_ == "gloves"):
						expertcalcsum3 = gloves_ // 10
					if(expert3_ == "ring"):
						expertcalcsum3 = ring_ // 10
					if(expert3_ == "leggings"):
						expertcalcsum3 = leggings_ // 10
					if(expert3_ == "shield"):
						expertcalcsum3 = shield_ // 10
					if(expert3_ == "tunic"):
						expertcalcsum3 = tunic_ // 10
					if(expert3_ == "weapon"):
						expertcalcsum3 = weapon_ // 10
					expertcalcsumtotal = expertcalcsum1 + expertcalcsum2 + expertcalcsum3

					rank_ = int(player[2])
					level_ = int(player[8])
					sum_ = float(player[14])
					ulevel = int(player[16])
					ulevelcalc = ulevel * 100
					ability_ = player[20]
					abilityadj = 0
					if ability == "b":
						if ability_ == "w":
							abilityadj = math.floor((sum_ + expertcalcsumtotal) * 0.30)

					if ability == "p":
						if ability_ == "b":
							abilityadj = math.floor((sum_ + expertcalcsumtotal) * 0.30)
						
					if ability == "r":
						if ability_ == "p":
							abilityadj = math.floor((sum_ + expertcalcsumtotal) * 0.30)
						
					if ability == "w":
						if ability_ == "r":
							abilityadj = math.floor((sum_ + expertcalcsumtotal) * 0.30)
						
					life_ = float(player[28])
					lifecalc = life_ / 100
					adjSum = math.floor((sum_ + ulevelcalc + abilityadj + expertcalcsumtotal) * lifecalc)
					
					
					if num == 1:
								# name       sum   adjsum       level   life   ability   rank 
						newlist.append( ( player[5], sum_, int(adjSum), level_, life_, ability_, rank_ ) )
					if num == 2:
								 # name       sum   adjsum       level   life   ability   rank
						newlist2.append( ( player[5], sum_, int(adjSum), level_, life_, ability_, rank_ ) )
					if num == 3:
								 # name       sum   adjsum       level   life   ability   rank 
						newlist3.append( ( player[5], sum_, int(adjSum), level_, life_, ability_, rank_ ) )
					if num == 4:
								 # name       sum   adjsum       level   life   ability   rank 
						newlist4.append( ( player[5], sum_, int(adjSum), level_, life_, ability_, rank_ ) )
				except:
					newlistererror = True

	if newlistererror is True:
		webworks = False
		if errortextmode is True:
			xchat.prnt("Newlister Error")

	if num == 1:
		newlist.sort( key=operator.itemgetter(1), reverse=True )
		newlist.sort( key=operator.itemgetter(3) )
	if num == 2:
		newlist2.sort( key=operator.itemgetter(1), reverse=True )
		newlist2.sort( key=operator.itemgetter(3) )
	if num == 3:
		newlist3.sort( key=operator.itemgetter(1), reverse=True )
		newlist3.sort( key=operator.itemgetter(3) )
	if num == 4:
		newlist4.sort( key=operator.itemgetter(1), reverse=True )
		newlist4.sort( key=operator.itemgetter(3) )

def status(word, word_eol, userdata):
	global char1
	global char2
	global char3
	global char4
	global name
	global name2
	global name3
	global name4
	global botcheck
	global botcheck2
	global botcheck3
	global botcheck4
	global gameactive
	
	if gameactive is True:
		if char1 is True:
			if botcheck is True:
				xchat.prnt("{0}'s Status".format(name))
				xchat.prnt(" ")
				characterstats(1)
			if botcheck is False:
				xchat.prnt("Game Bot 1 not in channel")
		if char2 is True:
			if botcheck2 is True:
				xchat.prnt(" ")
				xchat.prnt("{0}'s Status".format(name2))
				xchat.prnt(" ")
				characterstats(2)
			if botcheck2 is False:
				xchat.prnt("Game Bot 2 not in channel")
		if char3 is True:
			if botcheck3 is True:
				xchat.prnt(" ")
				xchat.prnt("{0}'s Status".format(name3))
				xchat.prnt(" ")
				characterstats(3)
			if botcheck3 is False:
				xchat.prnt("Game Bot 3 not in channel")
		if char4 is True:
			if botcheck4 is True:
				xchat.prnt(" ")
				xchat.prnt("{0}'s Status".format(name4))
				xchat.prnt(" ")
				characterstats(4)
			if botcheck4 is False:
				xchat.prnt("Game Bot 4 not in channel")
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("status", status, help="/status - Gives a list of character stats")

def characterstats(num):
	global level
	global ttl
	global atime
	global stime
	global location
	global locationtime

	global fights
	global gold
	global gems
	global xp
	global mana
	global upgradelevel
	global expertSum
	global expertSum2
	global expertSum3
	global expertSum4
	global itemSum
	global attackslaySum
	global itemSum2
	global attackslaySum2
	global itemSum3
	global attackslaySum3
	global itemSum4
	global attackslaySum4
	global life
	global exp
	global scrolls
	global rank
	global rank2
	global rank3
	global rank4
	global lottonum1
	global lottonum2
	global lottonum3
	global align
	
	getitems2(num)

	if num == 1:
		itemSums = itemSum
		attackslaySums = attackslaySum
		expertSums = expertSum
		ranks = rank
	if num == 2:
		itemSums = itemSum2
		attackslaySums = attackslaySum2
		expertSums = expertSum2
		ranks = rank2
	if num == 3:
		itemSums = itemSum3
		attackslaySums = attackslaySum3
		expertSums = expertSum3
		ranks = rank3
	if num == 4:
		itemSums = itemSum4
		attackslaySums = attackslaySum4
		expertSums = expertSum4
		ranks = rank4
		
	xchat.prnt("Rank: {0}".format(ranks))
	xchat.prnt("Location: {0}  Time: {1} secs".format(location, locationtime))
	if align == "n":
		xchat.prnt("Alignment: Neutral")
	if align == "g":
		xchat.prnt("Alignment: Good")
	if align == "e":
		xchat.prnt("Alignment: Evil")
	xchat.prnt("Level: {0}".format(level))
	xchat.prnt("TTL: {0} secs".format(ttl))
	if(level >= 15):
		xchat.prnt("Attack Recovery: {0} secs".format(atime))
	if(level < 15):
		xchat.prnt("Creep Attacks Start at Level 15")
	if(level >= 30):
		xchat.prnt("Slay Recovery: {0} secs".format(stime))
	if(level < 30):
		xchat.prnt("Slaying Monsters Start at Level 30")
	xchat.prnt("Mana Potion: {0}".format(mana))
	if(level >= 25):
		xchat.prnt("Fights: {0} of 5".format(fights))
	if(level < 25):
		xchat.prnt("Fights Start at Level 25")
	xchat.prnt("Gold: {0}".format(gold))
	xchat.prnt("XP: {0}".format(xp))
	xchat.prnt("Gems: {0}".format(gems))
	xchat.prnt("Lotto1: {0}  Lotto2: {1}  Lotto3: {2}".format(lottonum1, lottonum2, lottonum3))
	xchat.prnt("Life: {0}".format(life))
	xchat.prnt("Scrolls: {0} of 5".format(scrolls))
	xchat.prnt("Exp Used: {0} of 5".format(exp))
	xchat.prnt("Upgrade Level: {0}".format(upgradelevel))
	xchat.prnt("Items Sum Score: {0}".format(itemSums))
	xchat.prnt("Expert Items Score: {0}".format(expertSums))
	xchat.prnt("Attack/SlaySum Item Score: {0}".format(int(attackslaySums)))

def items(word, word_eol, userdata):
	global char1
	global char2
	global char3
	global char4
	global name
	global name2
	global name3
	global name4
	global botcheck
	global botcheck2
	global botcheck3
	global botcheck4
	global gameactive

	if gameactive is True:
		if char1 is True:
			if botcheck is True:
				xchat.prnt("{0}'s Items List".format(name))
				xchat.prnt(" ")
				characteritems(1)
			if botcheck is False:
				xchat.prnt("Game Bot 1 not in channel")
		if char2 is True:
			if botcheck2 is True:
				xchat.prnt(" ")
				xchat.prnt("{0}'s Items List".format(name2))
				xchat.prnt(" ")
				characteritems(2)
			if botcheck2 is False:
				xchat.prnt("Game Bot 2 not in channel")
		if char3 is True:
			if botcheck3 is True:
				xchat.prnt(" ")
				xchat.prnt("{0}'s Items List".format(name3))
				xchat.prnt(" ")
				characteritems(3)
			if botcheck3 is False:
				xchat.prnt("Game Bot 3 not in channel")
		if char4 is True:
			if botcheck4 is True:
				xchat.prnt(" ")
				xchat.prnt("{0}'s Items List".format(name4))
				xchat.prnt(" ")
				characteritems(4)
			if botcheck4 is False:
				xchat.prnt("Game Bot 4 not in channel")
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("items", items, help="/items - Gives a list of character item scores")

def characteritems(num):
	global amulet
	global charm
	global helm
	global boots
	global gloves
	global ring
	global leggings
	global shield
	global tunic
	global weapon
	global itemSum
	global itemSum2
	global itemSum3
	global itemSum4
	global stone1
	global stone2
	global stone3
	global expert1
	global expert2
	global expert3
	global expertitem1
	global expertitem2
	global expertitem3
	global expertitemb1
	global expertitemb2
	global expertitemb3
	global expertitemc1
	global expertitemc2
	global expertitemc3
	global expertitemd1
	global expertitemd2
	global expertitemd3

	getitems2(num)

	if num == 1:
		itemSums = itemSum
		expertitems1 = expertitem1
		expertitems2 = expertitem2
		expertitems3 = expertitem3
	if num == 2:
		itemSums = itemSum2
		expertitems1 = expertitemb1
		expertitems2 = expertitemb2
		expertitems3 = expertitemb3
	if num == 3:
		itemSums = itemSum3
		expertitems1 = expertitemc1
		expertitems2 = expertitemc2
		expertitems3 = expertitemc3
	if num == 4:
		itemSums = itemSum4
		expertitems1 = expertitemd1
		expertitems2 = expertitemd2
		expertitems3 = expertitemd3

	xchat.prnt("Amulet: {0}".format(amulet))
	xchat.prnt("Charm: {0}".format(charm))
	xchat.prnt("Helm: {0}".format(helm))
	xchat.prnt("Boots: {0}".format(boots))
	xchat.prnt("Gloves: {0}".format(gloves))
	xchat.prnt("Ring: {0}".format(ring))
	xchat.prnt("Leggings: {0}".format(leggings))
	xchat.prnt("Shield: {0}".format(shield))
	xchat.prnt("Tunic: {0}".format(tunic))
	xchat.prnt("Weapon: {0}".format(weapon))
	xchat.prnt("Stones 1: {0}  2: {1}  3: {2}".format(stone1, stone2, stone3))
	xchat.prnt("Items Sum Score: {0}".format(itemSums))
	xchat.prnt("Expert Items 1: {0} {1}  2: {2} {3}  3: {4} {5}".format(expert1, expertitems1, expert2, expertitems2, expert3, expertitems3))

def hookmain():
	global mainhook
	global interval
	global gameactive
	global intervaltext

	# unhook if hooked previously with an old interval
	if(mainhook is not None):
		xchat.unhook(mainhook)
		mainhook = None

	# set main timer for (interval)
	if gameactive is True:
		mainhook = xchat.hook_timer(interval * 1000, main)  # hook_timer requires milliseconds
		if intervaltext is True:
			xchat.prnt("Checking timers every {0} minutes".format(interval // 60))

def on_message(word, word_eol, userdata):
	global chanmessage
	global name
	global name2
	global name3
	global name4
	global botname
	global netname
	global netname2
	global netname3
	global netname4
	global char1
	global char2
	global char3
	global char4
	global nickname
	global nickname2
	global nickname3
	global nickname4
	global life
	global level
	global buylife
	global gameactive
	global itemslists
	
	if gameactive is True:
		checknet = xchat.get_info("network")
		checknick = xchat.get_info("nick")
		if chanmessage is True:
			chanmessage = False
		    
		if char1 is True:
			if(checknet == netname and checknick == nickname):
				if itemslists != None:
					for entry in itemslists:
						if(entry[0] == 1 and entry[1] != None):
							level = entry[2]
							life = entry[3]
				lifebuy = False
				if botname in word[0] and "and been defeated in combat!" in word[1] and "is added to {0}'s clock".format(name) in word[1]:
					lifebuy = True
				if botname in word[0] and "has attacked a" in word[1] and "is added to {0}'s clock".format(name) in word[1]:
					lifebuy = True
				if botname in word[0] and "tried to slay a" in word[1] and "is added to {0}'s clock".format(name) in word[1]:
					lifebuy = True
				if botname in word[0] and "has challenged" in word[1] and "is added to {0}'s clock".format(name) in word[1]:
					lifebuy = True
				if botname in word[0] and "has challenged {0}".format(name) in word[1] and "and won!" in word[1]:
					lifebuy = True
				if botname in word[0] and "gold from {0}!".format(name) in word[1] and "XP and loses" in word[1]:
					lifebuy = True
				if lifebuy is True:
					if(level >= 15 and buylife is True and life >= 0):
						usecommand("buy life", 1)
						life = 100
		if char2 is True:
			if(checknet == netname2 and checknick == nickname2):
				life2 = 0
				level2 = 0
				if itemslists != None:
					for entry in itemslists:
						if(entry[0] == 2 and entry[1] != None):
							level2 = entry[2]
							life2 = entry[3]
				lifebuyb = False
				if botname in word[0] and "and been defeated in combat!" in word[1] and "is added to {0}'s clock".format(name2) in word[1]:
					lifebuyb = True
				if botname in word[0] and "has attacked a" in word[1] and "is added to {0}'s clock".format(name2) in word[1]:
					lifebuyb = True
				if botname in word[0] and "tried to slay a" in word[1] and "is added to {0}'s clock".format(name2) in word[1]:
					lifebuyb = True
				if botname in word[0] and "has challenged" in word[1] and "is added to {0}'s clock".format(name2) in word[1]:
					lifebuyb = True
				if botname in word[0] and "has challenged {0}".format(name2) in word[1] and "and won!" in word[1]:
					lifebuyb = True
				if botname in word[0] and "gold from {0}!".format(name2) in word[1] and "XP and loses" in word[1]:
					lifebuyb = True
				if lifebuyb is True:
					if(level2 >= 15 and buylife is True and life2 >= 0):
						usecommand("buy life", 2)
						life2 = 100
		if char3 is True:
			if(checknet == netname3 and checknick == nickname3):
				life3 = 0
				level3 = 0
				if itemslists != None:
					for entry in itemslists:
						if(entry[0] == 3 and entry[1] != None):
							level3 = entry[2]
							life3 = entry[3]
				lifebuyc = False
				if botname in word[0] and "and been defeated in combat!" in word[1] and "is added to {0}'s clock".format(name3) in word[1]:
					lifebuyc = True
				if botname in word[0] and "has attacked a" in word[1] and "is added to {0}'s clock".format(name3) in word[1]:
					lifebuyc = True
				if botname in word[0] and "tried to slay a" in word[1] and "is added to {0}'s clock".format(name3) in word[1]:
					lifebuyc = True
				if botname in word[0] and "has challenged" in word[1] and "is added to {0}'s clock".format(name3) in word[1]:
					lifebuyc = True
				if botname in word[0] and "has challenged {0}".format(name3) in word[1] and "and won!" in word[1]:
					lifebuyc = True
				if botname in word[0] and "gold from {0}!".format(name3) in word[1] and "XP and loses" in word[1]:
					lifebuyc = True
				if lifebuyc is True:
					if(level3 >= 15 and buylife is True and life3 >= 0):
						usecommand("buy life", 3)
						life3 = 100
		if char4 is True:
			if(checknet == netname4 and checknick == nickname4):
				life4 = 0
				level4 = 0
				if itemslists != None:
					for entry in itemslists:
						if(entry[0] == 4 and entry[1] != None):
							level4 = entry[2]
							life4 = entry[3]
				lifebuyd = False
				if botname in word[0] and "and been defeated in combat!" in word[1] and "is added to {0}'s clock".format(name4) in word[1]:
					lifebuyd = True
				if botname in word[0] and "has attacked a" in word[1] and "is added to {0}'s clock".format(name4) in word[1]:
					lifebuyd = True
				if botname in word[0] and "tried to slay a" in word[1] and "is added to {0}'s clock".format(name4) in word[1]:
					lifebuyd = True
				if botname in word[0] and "has challenged" in word[1] and "is added to {0}'s clock".format(name4) in word[1]:
					lifebuyd = True
				if botname in word[0] and "has challenged {0}".format(name4) in word[1] and "and won!" in word[1]:
					lifebuyd = True
				if botname in word[0] and "gold from {0}!".format(name4) in word[1] and "XP and loses" in word[1]:
					lifebuyd = True
				if lifebuyd is True:
					if(level4 >= 15 and buylife is True and life4 >= 0):
						usecommand("buy life", 4)
						life4 = 100

def private_cb(word, word_eol, userdata):
	global botname
	global netname
	global nickname
	global game_chan
	global name
	global pswd
	global netname2
	global nickname2
	global game_chan2
	global name2
	global pswd2
	global netname3
	global nickname3
	global game_chan3
	global name3
	global pswd3
	global netname4
	global nickname4
	global game_chan4
	global name4
	global pswd4
	global private
	global char1
	global char2
	global char3
	global char4

	global interval
	global gameactive
	
	if gameactive is True:
		checknet = xchat.get_info("network")
		checknick = xchat.get_info("nick")
		if char1 is True:
			nickname = game_chan.get_info("nick")
		if char2 is True:
			nickname2 = game_chan2.get_info("nick")
		if char3 is True:
			nickname3 = game_chan3.get_info("nick")
		if char4 is True:
			nickname4 = game_chan4.get_info("nick")
		if private is True:
			private = False
			
		if char1 is True:
			if(word[0] == botname and "You are not logged in." in word[1]):                
				if(checknet == netname and checknick == nickname):
					usecommand("login {0} {1}".format(name, pswd), 1)
					interval = 60
					hookmain()
		if char2 is True:
			if(word[0] == botname and "You are not logged in." in word[1]):                
				if(checknet == netname2 and checknick == nickname2):
					usecommand("login {0} {1}".format(name2, pswd2), 2)
					interval = 60
					hookmain()
		if char3 is True:
			if(word[0] == botname and "You are not logged in." in word[1]):                
				if(checknet == netname3 and checknick == nickname3):
					usecommand("login {0} {1}".format(name3, pswd3), 3)
					interval = 60
					hookmain()
		if char4 is True:
			if(word[0] == botname and "You are not logged in." in word[1]):                
				if(checknet == netname4 and checknick == nickname4):
					usecommand("login {0} {1}".format(name4, pswd4), 4)
					interval = 60
					hookmain()

def webdata():
	global playerlist
	global playerlist2
	global playerlist3
	global playerlist4
	global name
	global name2
	global name3
	global name4
	global webworks
	global playerview
	global playerview2
	global playerview3
	global playerview4
	global char1
	global char2
	global char3
	global char4
	global python3
	global playerspage
	global playerspagelist
	global website
	global errortextmode
	
	webworks = True
	weberror = False

	context = ssl._create_unverified_context()
	# get raw player data from web, parse for relevant entry
	if python3 is False:
		try:
			if char1 is True:
				text = urllib2.urlopen(website + "/playerview.php?player={0}".format(name), context=context)
				playerview = text.read()
				text.close()
			if char2 is True:
				textb = urllib2.urlopen(website + "/playerview.php?player={0}".format(name2), context=context)
				playerview2 = textb.read()
				textb.close()
			if char3 is True:
				textc = urllib2.urlopen(website + "/playerview.php?player={0}".format(name3), context=context)
				playerview3 = textc.read()
				textc.close()
			if char4 is True:
				textd = urllib2.urlopen(website + "/playerview.php?player={0}".format(name4), context=context)
				playerview4 = textd.read()
				textd.close()
			text2 = urllib2.urlopen(website + "/players.php", context=context)
			playerspage = text2.read()
			text2.close()
		except:
			weberror = True
	if python3 is True:
		try:
			if char1 is True:
				text = urllib.request.urlopen(website + "/playerview.php?player={0}".format(name), context=context)
				playerview = text.read()
				text.close()
				playerview = playerview.decode("UTF-8")
			if char2 is True:
				textb = urllib.request.urlopen(website + "/playerview.php?player={0}".format(name2), context=context)
				playerview2 = textb.read()
				textb.close()
				playerview2 = playerview2.decode("UTF-8")
			if char3 is True:
				textc = urllib.request.urlopen(website + "/playerview.php?player={0}".format(name3), context=context)
				playerview3 = textc.read()
				textc.close()
				playerview3 = playerview3.decode("UTF-8")
			if char4 is True:
				textd = urllib.request.urlopen(website + "/playerview.php?player={0}".format(name4), context=context)
				playerview4 = textd.read()
				textd.close()
				playerview4 = playerview4.decode("UTF-8")
			text2 = urllib.request.urlopen(website + "/players.php", context=context)
			playerspage = text2.read()
			text2.close()
			playerspage = playerspage.decode("UTF-8")
		except:
			weberror = True
	if weberror is True:
		if errortextmode is True:
			xchat.prnt( "Could not access {0}".format(website))
		webworks = False

	# build list for player records
	if char1 is True:
		if(playerview is None):
			if errortextmode is True:
				xchat.prnt( "Could not access {0}, unknown error.".format(website) )
			webworks = False
		else:
			playerlist = playerview.split("\n")
			playerlist = playerlist[:-1]
	if char2 is True:
		if(playerview2 is None):
			if errortextmode is True:
				xchat.prnt( "Could not access {0}, unknown error.".format(website) )
			webworks = False
		else:
			playerlist2 = playerview2.split("\n")
			playerlist2 = playerlist2[:-1]
	if char3 is True:
		if(playerview3 is None):
			if errortextmode is True:
				xchat.prnt( "Could not access {0}, unknown error.".format(website) )
			webworks = False
		else:
			playerlist3 = playerview3.split("\n")
			playerlist3 = playerlist3[:-1]
	if char4 is True:
		if(playerview4 is None):
			if errortextmode is True:
				xchat.prnt( "Could not access {0}, unknown error.".format(website) )
			webworks = False
		else:
			playerlist4 = playerview4.split("\n")
			playerlist4 = playerlist4[:-1]
	if(playerspage is None):
		if errortextmode is True:
			xchat.prnt( "Could not access {0}, unknown error.".format(website) )
		webworks = False
	else:
		playerspagelist = playerspage.split("\n")
		playerspagelist = playerspagelist[:-1]

def playerarea(num):
	global level
	global mysum
	global location
	global locationtime
	global townworkswitch
	
	getitems2(num)
	
	if townworkswitch is True:
		area = "work"
	if townworkswitch is False:
		area = "forest"

#	xchat.prnt("{0} {1} Time: {2} seconds".format(num, location, locationtime))
	if (level <= 25):
		mintime = (3 * 60 * 60)
	if (level > 25 and level <= 40):
		mintime = (6 * 60 * 60)
	if (level > 40 and level <= 50):
		mintime = (12 * 60 * 60)
	if (level > 50):
		mintime = (24 * 60 * 60)

	if locationtime == 0:
		usecommand("goto {0}".format(area), num)
		
	if(location == "In Town" and locationtime >= mintime and mysum < 6000 and mysum != 0):
		usecommand("goto {0}".format(area), num)
	if(location == "In Town" and mysum >= 6000):
		usecommand("goto {0}".format(area), num)
	if(location == "At Work" and locationtime >= mintime):
		usecommand("goto town", num)
	if(location == "In The Forest" and locationtime >= (24 * 60 * 60)):
		usecommand("goto town", num)
       
def itemsbuilder():
	global char1
	global char2
	global char3
	global char4
	global itemslists

	itemslists = []

	if char1 is True:
		itemslists.append( ( getvariables2(1) ) )
	if char2 is True:
		itemslists.append( ( getvariables2(2) ) )
	if char3 is True:
		itemslists.append( ( getvariables2(3) ) )
	if char4 is True:
		itemslists.append( ( getvariables2(4) ) )

def getvariables2(num):
	global playerlist
	global playerlist2
	global playerlist3
	global playerlist4
	global webworks
	global errortextmode

	if num == 1:
		playerlists = playerlist
	if num == 2:
		playerlists = playerlist2
	if num == 3:
		playerlists = playerlist3
	if num == 4:
		playerlists = playerlist4

	aligntext = None
	leveltext = None
	ttltext = None
	goldtext = None
	gemstext = None
	upgradetext = None
	abilitytext = None
	xptext = None
	exptext = None
	lifetext = None
	scrollstext = None
	manatext = None
	atimetext = None
	ctimetext = None
	
	amulettext = None
	bootstext = None
	charmtext = None
	glovestext = None
	helmtext = None
	leggingstext = None
	ringtext = None
	shieldtext = None
	tunictext = None
	weapontext = None

	sumtext = None
	experttext1 = None
	experttext2 = None
	experttext3 = None
	stonetext1 = None
	stonetext2 = None
	stonetext3 = None
	fightstext = None
	lottonumtext1 = None
	lottonumtext2 = None
	lottonumtext3 = None

	playeris = None
	worktext = None
	towntext = None
	foresttext = None
	location_ = None
	locationtime_ = 0
	atwork = False
	intown = False
	intheforest = False                       

	if playerlists != None:
		for entry in playerlists:
			if "Alignment:" in entry:
				aligntext = entry
			if "Level:" in entry:
				leveltext = entry
			if "Next level:" in entry:
				ttltext = entry
			if "Gold:" in entry:
				goldtext = entry
			if "Gems:" in entry:
				gemstext = entry
			if "Upgrade level:" in entry:
				upgradetext = entry
			if "Ability:" in entry:
				abilitytext = entry
			if "XP:" in entry:
				xptext = entry
			if "Exp Used:" in entry:
				exptext = entry
			if "Life:" in entry:
				lifetext = entry
			if "Scrolls Used:" in entry:
				scrollstext = entry
			if "Mana Potion:" in entry:
				manatext = entry
			if "Creep Attack in:" in entry:
				atimetext = entry
			if "Dragon Slay in:" in entry:
				stimetext = entry

			if "amulet:" in entry:
				amulettext = entry
			if "boots:" in entry:
				bootstext = entry
			if "charm:" in entry:
				charmtext = entry
			if "gloves:" in entry:
				glovestext = entry
			if "helm:" in entry:
				helmtext = entry
			if "leggings:" in entry:
				leggingstext = entry
			if "ring:" in entry:
				ringtext = entry
			if "shield:" in entry:
				shieldtext = entry
			if "tunic:" in entry:
				tunictext = entry
			if "weapon:" in entry:
				weapontext = entry

			if "Sum:" in entry:
				sumtext = entry
			if "Expert 1:" in entry:
				experttext1 = entry
			if "Expert 2:" in entry:
				experttext2 = entry
			if "Expert 3:" in entry:
				experttext3 = entry
			if "Stone 1:" in entry:
				stonetext1 = entry
			if "Stone 2:" in entry:
				stonetext2 = entry
			if "Stone 3:" in entry:
				stonetext3 = entry
			if "Manual FIGHT commands used (out of 5):" in entry:
				fightstext = entry
			if "Lotto Numbers 1:" in entry:
				lottonumtext1 = entry
			if "Lotto Numbers 2:" in entry:
				lottonumtext2 = entry
			if "Lotto Numbers 3:" in entry:
				lottonumtext3 = entry

			if "Player is:" in entry:
				playeris = entry
			if "Work Time:" in entry:
				worktext = entry
			if "Town Time:" in entry:
				towntext = entry
			if "Forest Time:" in entry:
				foresttext = entry

		try:
			try:
				if "Neutral" in aligntext:
					align_ = "n"
				if "Evil" in aligntext:
					align_ = "e"
				if "Good" in aligntext:
					align_ = "g"
			except TypeError:
				align_ = "n"
			leveltext = leveltext.split(" ")
			levelsplit = leveltext[7]
			level_ = int(levelsplit.strip("<br"))
			ttltext = ttltext.split(" ")
			daystext = int(ttltext[8])
			timetext = ttltext[10].strip("<br")
			ttl_ = timetosecs(daystext, timetext)
			goldtext = goldtext.split(" ")
			goldsplit = goldtext[7]
			gold_ = int(goldsplit.strip("<br"))
			gemstext = gemstext.split(" ")
			gemssplit = gemstext[7]
			gems_ = int(gemssplit.strip("<br"))
			upgradetext = upgradetext.split(" ")
			upgradesplit = upgradetext[8]
			upgradelevel_ = int(upgradesplit.strip("<br"))

			if "Barbarian" in abilitytext:
				ability_ = "b"
			if "Rogue" in abilitytext:
				ability_ = "r"
			if "Paladin" in abilitytext:
				ability_ = "p"
			if "Wizard" in abilitytext:
				ability_ = "w"

			xptext = xptext.split(" ")
			xpsplit = xptext[7]
			xp_ = int(xpsplit.strip("<br"))
			exptext = exptext.split(" ")
			expsplit = exptext[8]
			expsplit = expsplit.split("/")
			try:
				exp_ = int(expsplit[0])
			except:
				exp_ = 0
			lifetext = lifetext.split(" ")
			lifesplit = lifetext[7]
			life_ = int(lifesplit.strip("<br"))
			scrollstext = scrollstext.split(" ")
			scrollssplit = scrollstext[8]
			scrollssplit = scrollssplit.split("/")
			try:
				scrolls_ = int(scrollssplit[0])
			except ValueError:
				scrolls_ = 0
			manatext = manatext.split(" ")
			manasplit = manatext[8]
			manasplit = manasplit.split("/")
			mana_ = int(manasplit[0])

			try:
				atimetext = atimetext.split(" ")
				daystext = int(atimetext[9])
				timetext = atimetext[11].strip("<br")
				atime_ = timetosecs(daystext, timetext)
			except ValueError:
				atime_ = 0
			try:
				stimetext = stimetext.split(" ")
				daystext = int(stimetext[9])
				timetext = stimetext[11].strip("<br")
				stime_ = timetosecs(daystext, timetext)
			except ValueError:
				stime_ = 0

			amulettext = amulettext.split(" ")
			amuletsplit = amulettext[7]
			amulet_ = int(amuletsplit.strip("<br"))
			bootstext = bootstext.split(" ")
			bootssplit = bootstext[7]
			boots_ = int(bootssplit.strip("<br"))
			charmtext = charmtext.split(" ")
			charmsplit = charmtext[7]
			charm_ = int(charmsplit.strip("<br"))
			glovestext = glovestext.split(" ")
			glovessplit = glovestext[7]
			gloves_ = int(glovessplit.strip("<br"))
			helmtext = helmtext.split(" ")
			helmsplit = helmtext[7]
			helm_ = int(helmsplit.strip("<br"))
			leggingstext = leggingstext.split(" ")
			leggingssplit = leggingstext[7]
			leggings_ = int(leggingssplit.strip("<br"))
			ringtext = ringtext.split(" ")
			ringsplit = ringtext[7]
			ring_ = int(ringsplit.strip("<br"))
			shieldtext = shieldtext.split(" ")
			shieldsplit = shieldtext[7]
			shield_ = int(shieldsplit.strip("<br"))
			tunictext = tunictext.split(" ")
			tunicsplit = tunictext[7]
			tunic_ = int(tunicsplit.strip("<br"))
			weapontext = weapontext.split(" ")
			weaponsplit = weapontext[7]
			weapon_ = int(weaponsplit.strip("<br"))

			sumtext = sumtext.split(" ")
			sumsplit = sumtext[7]
			mysum_ = int(sumsplit.strip("<br"))
			experttext1 = experttext1.split(" ")
			expertsplit1 = experttext1[8]
			expertsplitsplit1 = expertsplit1.split("<")
			expert1_ = expertsplitsplit1[0]
			experttext2 = experttext2.split(" ")
			expertsplit2 = experttext2[8]
			expertsplitsplit2 = expertsplit2.split("<")
			expert2_ = expertsplitsplit2[0]
			experttext3 = experttext3.split(" ")
			expertsplit3 = experttext3[8]
			expertsplitsplit3 = expertsplit3.split("<")
			expert3_ = expertsplitsplit3[0]
			stonetext1 = stonetext1.split(" ")
			stonesplit1 = stonetext1[8]
			stonesplitsplit1 = stonesplit1.split("<")
			stone1_ = stonesplitsplit1[0]
			stonetext2 = stonetext2.split(" ")
			stonesplit2 = stonetext2[8]
			stonesplitsplit2 = stonesplit2.split("<")
			stone2_ = stonesplitsplit2[0]
			stonetext3 = stonetext3.split(" ")
			stonesplit3 = stonetext3[8]
			stonesplitsplit3 = stonesplit3.split("<")
			stone3_ = stonesplitsplit3[0]
			fightstext = fightstext.split(" ")
			fightssplit = fightstext[13]
			fights_ = int(fightssplit.strip("<br"))
			lottonumtext1 = re.sub(r'<.*?>', ' ', lottonumtext1)
			lottonumtext1 = lottonumtext1.split(" ")
			lottonumtext2 = re.sub(r'<.*?>', ' ', lottonumtext2)
			lottonumtext2 = lottonumtext2.split(" ")
			lottonumtext3 = re.sub(r'<.*?>', ' ', lottonumtext3)
			lottonumtext3 = lottonumtext3.split(" ")
			lottonum1_ = "{0} {1} and {2}".format(lottonumtext1[11], lottonumtext1[12], lottonumtext1[13])                        
			lottonum2_ = "{0} {1} and {2}".format(lottonumtext2[11], lottonumtext2[12], lottonumtext2[13])                        
			lottonum3_ = "{0} {1} and {2}".format(lottonumtext3[11], lottonumtext3[12], lottonumtext3[13])                        

			if "at work" in playeris:
				atwork = True
			if "in town" in playeris:
				intown = True
			if "in the forest" in playeris:
				intheforest = True
			if atwork is True:
				try:
					worktext = worktext.split(" ")
					workdays = int(worktext[8])
					worksplittime = worktext[10]
					worksplittime = worksplittime.strip("<br")
					locationtime_ = timetosecs(workdays, worksplittime)
					location_ = "At Work"
				except ValueError:
					locationtime_ = 0
					location_ = "At Work"
			if intown is True:
				try:
					towntext = towntext.split(" ")
					towndays = int(towntext[8])
					townsplittime = towntext[10]
					townsplittime = townsplittime.strip("<br")
					locationtime_ = timetosecs(towndays, townsplittime)
					location_ = "In Town"
				except ValueError:
					locationtime_ = 0
					location_ = "In Town"
			if intheforest is True:
				try:
					foresttext = foresttext.split(" ")
					forestdays = int(foresttext[8])
					forestsplittime = foresttext[10]
					forestsplittime = forestsplittime.strip("<br")
					locationtime_ = timetosecs(forestdays, forestsplittime)
					location_ = "In The Forest"
				except ValueError:
					locationtime_ = 0
					location_ = "In The Forest"
		except:
			webworks = False
			if errortextmode is True:
				xchat.prnt("{0} Variable Error".format(num))

		try:
				    # num  mysum   level   life   ability   ttl 
			itemslist = ( num, mysum_, level_, life_, ability_, ttl_, gold_, gems_, upgradelevel_, xp_, exp_, scrolls_, mana_, atime_, stime_, amulet_, boots_, charm_, gloves_, helm_, leggings_, ring_, shield_, tunic_, weapon_, expert1_, expert2_, expert3_, stone1_, stone2_, stone3_, fights_, align_, lottonum1_, lottonum2_, lottonum3_, location_, locationtime_ )
		except:
			itemslist = (num, None )
			
	return itemslist

def getitems2(num):
	global align
	global level
	global ttl
	global gold
	global gems
	global upgradelevel
	global ability
	global xp
	global exp
	global life
	global scrolls
	global mana
	global atime
	global stime

	global amulet
	global charm
	global helm
	global boots
	global gloves
	global ring
	global leggings
	global shield
	global tunic
	global weapon 

	global mysum
	global expert1
	global expert2
	global expert3
	global stone1
	global stone2
	global stone3
	global fights

	global itemslists
	global lottonum1
	global lottonum2
	global lottonum3
	global location
	global locationtime
	
#itemslists.append( ( player[5], mysum_, level_, life_, ability_, ttl_, gold_, gems_, upgradelevel_, xp_, exp_, scrolls_, mana_, atime_, stime_, amulet_, boots_, charm_, gloves_, helm_, leggings_, ring_, shield_, tunic_, weapon_, expert1_, expert2_, expert3_, stone1_, stone2_, stone3_, fights_, align_, lottonum1_, lottonum2_, lottonum3_, location_, locationtime_ ) )

	if itemslists != None:
		for entry in itemslists:
			if(entry[0] == num and entry[1] != None):
				mysum = entry[1]
				level = entry[2]
				life = entry[3]
				ability = entry[4]
				ttl = entry[5]
				gold = entry[6]
				gems = entry[7]
				upgradelevel = entry[8]
				xp = entry[9]
				exp = entry[10]
				scrolls = entry[11]
				mana = entry[12]
				atime = entry[13]
				stime = entry[14]
				amulet = entry[15]
				boots = entry[16]
				charm = entry[17]
				gloves = entry[18]
				helm = entry[19]
				leggings = entry[20]
				ring = entry[21]
				shield = entry[22]
				tunic = entry[23]
				weapon = entry[24]
				expert1 = entry[25]
				expert2 = entry[26]
				expert3 = entry[27]
				stone1 = entry[28]
				stone2 = entry[29]
				stone3 = entry[30]
				fights = entry[31]
				align = entry[32]
				lottonum1 = entry[33]
				lottonum2 = entry[34]
				lottonum3 = entry[35]
				location = entry[36]
				locationtime = entry[37]

def timetosecs(days,time):
	timesecs = 0
	splittime = time.split(":")
	hours = int(splittime[0])
	mins = int(splittime[1])
	secs = int(splittime[2])
	timesecs = ((days * 24 * 60 * 60) + (hours * 60 * 60) + (mins * 60) + secs)
	return timesecs

def main(userdata):
	global channame
	global botname
	global nickname
	global netname
	global nickname2
	global netname2
	global nickname3
	global netname3
	global nickname4
	global netname4
	global servername
	global game_chan
	global game_chan2
	global game_chan3
	global game_chan4
	global private
	global chanmessage
	global ZNC
	global ZNCServer
	global ZNCPort
	global ZNCUser
	global ZNCPass
	global ZNC2
	global ZNCServer2
	global ZNCPort2
	global ZNCUser2
	global ZNCPass2
	global ZNC3
	global ZNCServer3
	global ZNCPort3
	global ZNCUser3
	global ZNCPass3
	global ZNC4
	global ZNCServer4
	global ZNCPort4
	global ZNCUser4
	global ZNCPass4
	global botcheck
	global botcheck2
	global botcheck3
	global botcheck4
	global interval
	global webworks
	global rank
	global rank2
	global rank3
	global rank4
	global offline
	global offline2
	global offline3
	global offline4
	global playerspagelist
	global name
	global pswd
	global name2
	global pswd2
	global name3
	global pswd3
	global name4
	global pswd4
	global level
	global fights
	global char1
	global char2
	global char3
	global char4
	global chanmessagecount
	global life
	global intervaltext
	global itemslists
	global bottextmode
	global errortextmode
	global botdisable1
	global botdisable2
	global botdisable3
	global botdisable4
	
	if intervaltext is True:
		xchat.prnt( "INTERVAL {0}".format(time.asctime()) )
	if chanmessage is True:
		chanmessagecount += 1

	botcheck = False
	chancheck = True
	botcheck2 = False
	chancheck2 = True
	botcheck3 = False
	chancheck3 = True
	botcheck4 = False
	chancheck4 = True
	botdisable1 = False
	botdisable2 = False
	botdisable3 = False
	botdisable4 = False
	intervaldisable = False

	if char1 is True:
		bottester(1)
	if char2 is True:
		bottester(2)
	if char3 is True:
		bottester(3)
	if char4 is True:
		bottester(4)

	if char1 is True:
		if game_chan.get_info("channel").lower() != channame:
			chancheck = False
		if chancheck is False:
			if ZNC is True:
				game_chan.command( "quote PASS {0}:{1}".format(ZNCUser, ZNCPass) )
			game_chan.command( "join {0}".format(channame) )
			botcheck = False
		if chancheck is True:
			userlist = game_chan.get_list("users")
			for user in userlist:
				if botname in user.nick:
					botcheck = True
			if botcheck is False:
				 if errortextmode is True:
					 xchat.prnt( "1 Game Bot not in channel" )
	if char2 is True:
		if game_chan2.get_info("channel").lower() != channame:
			chancheck2 = False
		if chancheck2 is False:
			if ZNC2 is True:
				game_chan2.command( "quote PASS {0}:{1}".format(ZNCUser2, ZNCPass2) )
			game_chan2.command( "join {0}".format(channame) )
			botcheck2 = False
		if chancheck2 is True:
			userlist = game_chan2.get_list("users")
			for user in userlist:
				if botname in user.nick:
					botcheck2 = True
			if botcheck2 is False:
				 if errortextmode is True:
					 xchat.prnt( "2 Game Bot not in channel" )
	if char3 is True:
		if game_chan3.get_info("channel").lower() != channame:
			chancheck3 = False
		if chancheck3 is False:
			if ZNC3 is True:
				game_chan3.command( "quote PASS {0}:{1}".format(ZNCUser3, ZNCPass3) )
			game_chan3.command( "join {0}".format(channame) )
			botcheck3 = False
		if chancheck3 is True:
			userlist = game_chan3.get_list("users")
			for user in userlist:
				if botname in user.nick:
					botcheck3 = True
			if botcheck3 is False:
				 if errortextmode is True:
					 xchat.prnt( "3 Game Bot not in channel" )
	if char4 is True:
		if game_chan4.get_info("channel").lower() != channame:
			chancheck4 = False
		if chancheck4 is False:
			if ZNC4 is True:
				game_chan4.command( "quote PASS {0}:{1}".format(ZNCUser4, ZNCPass4) )
			game_chan4.command( "join {0}".format(channame) )
			botcheck4 = False
		if chancheck4 is True:
			userlist = game_chan4.get_list("users")
			for user in userlist:
				if botname in user.nick:
					botcheck4 = True
			if botcheck4 is False:
				 if errortextmode is True:
					 xchat.prnt( "4 Game Bot not in channel" )

	if private is True and chanmessagecount == 1:
		xchat.hook_print("Private Message", private_cb)
		xchat.hook_print("Private Message to Dialog", private_cb)
		
	if chanmessage is True and chanmessagecount == 1:
		xchat.hook_print("Channel Message", on_message)
		xchat.hook_print("Channel Msg Hilight", on_message)

	if botcheck is True or botcheck2 is True or botcheck3 is True or botcheck4 is True:
		webdata()
		if webworks is True:
			itemsbuilder()

	test = []
	offline = False
	offline2 = False
	offline3 = False
	offline4 = False
	rank = 0
	rank2 = 0
	rank3 = 0
	rank4 = 0
	if webworks is True:
		if char1 is True and botcheck is True:
			for entry in playerspagelist:
				if "playerview.php" in entry and name in entry:
					test = entry
			if "offline" in test:
				offline = True
			if offline is False:
				try:
					test = test.split('">')
					ranktext = test[1]
					ranktext = ranktext.split("</")
					rank = int(ranktext[0])
				except:
					offline = True
		if char2 is True and botcheck2 is True:
			for entry in playerspagelist:
				if "playerview.php" in entry and name2 in entry:
					test = entry
			if "offline" in test:
				offline2 = True
			if offline2 is False:
				try:
					test = test.split('">')
					ranktext = test[1]
					ranktext = ranktext.split("</")
					rank2 = int(ranktext[0])
				except:
					offline2 = True
		if char3 is True and botcheck3 is True:
			for entry in playerspagelist:
				if "playerview.php" in entry and name3 in entry:
					test = entry
			if "offline" in test:
				offline3 = True
			if offline3 is False:
				try:
					test = test.split('">')
					ranktext = test[1]
					ranktext = ranktext.split("</")
					rank3 = int(ranktext[0])
				except:
					offline3 = True
		if char4 is True and botcheck4 is True:
			for entry in playerspagelist:
				if "playerview.php" in entry and name4 in entry:
					test = entry
			if "offline" in test:
				offline4 = True
			if offline4 is False:
				try:
					test = test.split('">')
					ranktext = test[1]
					ranktext = ranktext.split("</")
					rank4 = int(ranktext[0])
				except:
					offline4 = True
	if char1 is True:
		if(webworks is True and offline is True):
			if errortextmode is True:
				xchat.prnt("1 Player Offline")
	if char2 is True:
		if(webworks is True and offline2 is True):
			if errortextmode is True:
				xchat.prnt("2 Player Offline")
	if char3 is True:
		if(webworks is True and offline3 is True):
			if errortextmode is True:
				xchat.prnt("3 Player Offline")
	if char4 is True:
		if(webworks is True and offline4 is True):
			if errortextmode is True:
				xchat.prnt("4 Player Offline")

	if char1 is True:
		nickname = game_chan.get_info("nick")
		netname = game_chan.get_info("network")
		if game_chan.get_info("server") is None:
			if errortextmode is True:
				xchat.prnt( "1 Not connected!" )
			if ZNC is False:
				game_chan.command( "server {0}".format(servername) )
			if ZNC is True:
				game_chan.command( "server {0} {1}".format(ZNCServer, ZNCPort) )
			interval = 45
			hookmain()
			intervaldisable = True

		if webworks is True and offline is True and botcheck is True:
			usecommand("login {0} {1}".format(name, pswd),1)
			interval = 45
			hookmain()
			intervaldisable = True
	if char2 is True:
		nickname2 = game_chan2.get_info("nick")
		netname2 = game_chan2.get_info("network")
		if game_chan2.get_info("server") is None:
			if errortextmode is True:
				xchat.prnt( "2 Not connected!" )
			if ZNC2 is False:
				game_chan2.command( "server {0}".format(servername) )
			if ZNC2 is True:
				game_chan2.command( "server {0} {1}".format(ZNCServer2, ZNCPort2) )
			interval = 45
			hookmain()
			intervaldisable = True

		if webworks is True and offline2 is True and botcheck2 is True:
			usecommand("login {0} {1}".format(name2, pswd2),2)
			interval = 45
			hookmain()
			intervaldisable = True
	if char3 is True:
		nickname3 = game_chan3.get_info("nick")
		netname3 = game_chan3.get_info("network")
		if game_chan3.get_info("server") is None:
			if errortextmode is True:
				xchat.prnt( "3 Not connected!" )
			if ZNC3 is False:
				game_chan3.command( "server {0}".format(servername) )
			if ZNC3 is True:
				game_chan3.command( "server {0} {1}".format(ZNCServer3, ZNCPort3) )
			interval = 45
			hookmain()
			intervaldisable = True

		if webworks is True and offline3 is True and botcheck3 is True:
			usecommand("login {0} {1}".format(name3, pswd3),3)
			interval = 45
			hookmain()
			intervaldisable = True
	if char4 is True:
		nickname4 = game_chan4.get_info("nick")
		netname4 = game_chan4.get_info("network")
		if game_chan4.get_info("server") is None:
			if errortextmode is True:
				xchat.prnt( "4 Not connected!" )
			if ZNC4 is False:
				game_chan4.command( "server {0}".format(servername) )
			if ZNC4 is True:
				game_chan4.command( "server {0} {1}".format(ZNCServer4, ZNCPort4) )
			interval = 45
			hookmain()
			intervaldisable = True

		if webworks is True and offline4 is True and botcheck4 is True:
			usecommand("login {0} {1}".format(name4, pswd4),4)
			interval = 45
			hookmain()
			intervaldisable = True

	if webworks is True and intervaldisable is False:
		intervalcalc()
	if webworks is False and intervaldisable is False:
		interval = 300
		hookmain()

	life2 = 0
	level2 = 0
	fights2 = 0
	life3 = 0
	level3 = 0
	fights3 = 0
	life4 = 0
	level4 = 0
	fights4 = 0
	
	if char1 is True:
		if itemslists != None:
			for entry in itemslists:
				if(entry[0] == 1 and entry[1] != None):
					level = entry[2]
					fights = entry[31]
					life = entry[3]
	if char2 is True:
		if itemslists != None:
			for entry in itemslists:
				if(entry[0] == 2 and entry[1] != None):
					level2 = entry[2]
					fights2 = entry[31]
					life2 = entry[3]
	if char3 is True:
		if itemslists != None:
			for entry in itemslists:
				if(entry[0] == 3 and entry[1] != None):
					level3 = entry[2]
					fights3 = entry[31]
					life3 = entry[3]
	if char4 is True:
		if itemslists != None:
			for entry in itemslists:
				if(entry[0] == 4 and entry[1] != None):
					level4 = entry[2]
					fights4 = entry[31]
					life4 = entry[3]

	if webworks is True:
		if char1 is True and offline is False and botcheck is True:
			playerarea(1)
			spendmoney(1)
			timercheck(1)
			if(level >= 25 and fights >= 0 and fights < 5 and life > 0):
				if bottextmode is True:
					xchat.prnt("1 Fights available")
			if(level >= 25 and fights >= 0 and fights < 5 and life > 10):
				newlister(1)
				fight_fight(1)
		if char2 is True and offline2 is False and botcheck2 is True:
			playerarea(2)
			spendmoney(2)
			timercheck(2)
			if(level2 >= 25 and fights2 >= 0 and fights2 < 5 and life2 > 0):
				if bottextmode is True:
					xchat.prnt("2 Fights available")
			if(level2 >= 25 and fights2 >= 0 and fights2 < 5 and life2 > 10):
				newlister(2)
				fight_fight(2)
		if char3 is True and offline3 is False and botcheck3 is True:
			playerarea(3)
			spendmoney(3)
			timercheck(3)
			if(level3 >= 25 and fights3 >= 0 and fights3 < 5 and life3 > 0):
				if bottextmode is True:
					xchat.prnt("3 Fights available")
			if(level3 >= 25 and fights3 >= 0 and fights3 < 5 and life3 > 10):
				newlister(3)
				fight_fight(3)
		if char4 is True and offline4 is False and botcheck4 is True:
			playerarea(4)
			spendmoney(4)
			timercheck(4)
			if(level4 >= 25 and fights4 >= 0 and fights4 < 5 and life4 > 0):
				if bottextmode is True:
					xchat.prnt("4 Fights available")
			if(level4 >= 25 and fights4 >= 0 and fights4 < 5 and life4 > 10):
				newlister(4)
				fight_fight(4)

	return True	# <- tells timer to repeat

def intervalcalc():
	global interval
	global level
	global fights
	global botcheck
	global offline
	global botcheck2
	global offline2
	global botcheck3
	global offline3
	global botcheck4
	global offline4
	global char1
	global char2
	global char3
	global char4
	global life
	global fightmode
	global itemslists
	
	sixty = 60
	onetwenty = 120
	interval = 5
	interval *= 60			# conv from min to sec
	intervallist = []
			
	level2 = 0
	fights2 = 0
	life2 = 0
	level3 = 0
	fights3 = 0
	life3 = 0
	level4 = 0
	fights4 = 0
	life4 = 0
	
	if char1 is True:
		if itemslists != None:
			for entry in itemslists:
				if(entry[0] == 1 and entry[1] != None):
					level = entry[2]
					fights = entry[31]
					life = entry[3]
	if char2 is True:
		if itemslists != None:
			for entry in itemslists:
				if(entry[0] == 2 and entry[1] != None):
					level2 = entry[2]
					fights2 = entry[31]
					life2 = entry[3]
	if char3 is True:
		if itemslists != None:
			for entry in itemslists:
				if(entry[0] == 3 and entry[1] != None):
					level3 = entry[2]
					fights3 = entry[31]
					life3 = entry[3]
	if char4 is True:
		if itemslists != None:
			for entry in itemslists:
				if(entry[0] == 4 and entry[1] != None):
					level4 = entry[2]
					fights4 = entry[31]
					life4 = entry[3]

	if char1 is True:                                       
		if botcheck is False or offline is True:
			intervallist.append( ( "interval", sixty ) )
		if botcheck is True and fightmode is True:
			if(level >= 25 and life > 10 and fightmode is True):
				if(fights >= 0 and fights < 5):
					intervallist.append( ( "interval", onetwenty ) )
	if char2 is True:
		if botcheck2 is False or offline2 is True:
			intervallist.append( ( "interval", sixty ) )
		if botcheck2 is True and fightmode is True:
			if(level2 >= 25 and life2 > 10 and fightmode is True):
				if(fights2 >= 0 and fights2 < 5):
					intervallist.append( ( "interval", onetwenty ) )
	if char3 is True:
		if botcheck3 is False or offline3 is True:
			intervallist.append( ( "interval", sixty ) )
		if botcheck3 is True and fightmode is True:
			if(level3 >= 25 and life3 > 10 and fightmode is True):
				if(fights3 >= 0 and fights3 < 5):
					intervallist.append( ( "interval", onetwenty ) )
	if char4 is True:
		if botcheck4 is False or offline4 is True:
			intervallist.append( ( "interval", sixty ) )
		if botcheck4 is True and fightmode is True:
			if(level4 >= 25 and life4 > 10 and fightmode is True):
				if(fights4 >= 0 and fights4 < 5):
					intervallist.append( ( "interval", onetwenty ) )

	intervallist.sort( key=operator.itemgetter(1), reverse=True )
	diff = 999999        
	for entry in intervallist:
		if(entry[1] < diff):
			interval = entry[1]

	hookmain()
	
def timercheck(num):
	global ttl
	global interval
	global atime
	global stime
	global level
	global attackslaySum
	global attackslaySum2
	global attackslaySum3
	global attackslaySum4
	global mana
	global gold
	global life
	global slaysum
	global bottextmode
	
	getitems2(num)

	if num == 1:
		attackslaySumlist = attackslaySum
	if num == 2:
		attackslaySumlist = attackslaySum2
	if num == 3:
		attackslaySumlist = attackslaySum3
	if num == 4:
		attackslaySumlist = attackslaySum4
		
	# make sure no times are negative
	if(atime < 0):
		atime = 0
	if(stime < 0):
		stime = 0

#	xchat.prnt("{0} atime {1}  stime {2}  ttl {3}".format(num, atime, stime, ttl))
	slaydisable = False
	
	if(ttl <= interval):
		timer = (ttl+10)*1000
		if bottextmode is True:
			xchat.prnt("Set lvlup {0} timer. Going off in {1} minutes.".format(num, timer // 60000))
		if num == 1:
			xchat.hook_timer(timer, lvlup)
		if num == 2:
			xchat.hook_timer(timer, lvlup2)
		if num == 3:
			xchat.hook_timer(timer, lvlup3)
		if num == 4:
			xchat.hook_timer(timer, lvlup4)
	
	# do checks for other actions.
	if(level >= 15 and atime <= interval and atime <= ttl and life > 10):
		timer = (atime+10)*1000
		if bottextmode is True:
			xchat.prnt("Set attack {0} timer. Going off in {1} minutes.".format(num, timer // 60000))
		slaydisable = True
		if num == 1:
			xchat.hook_timer(timer, attack)
		if num == 2:
			xchat.hook_timer(timer, attack2)
		if num == 3:
			xchat.hook_timer(timer, attack3)
		if num == 4:
			xchat.hook_timer(timer, attack4)

	if(level >= 30 and attackslaySumlist >= 1000 and stime <= interval and stime <= ttl and slaydisable is False and life > 10):
		if(mana == 0 and gold >= 1100 and attackslaySumlist < 150000):
			usecommand("buy mana", num)
			gold -= 1000
			mana = 1
		timer = (stime+10)*1000
		if mana == 0 and attackslaySumlist >= slaysum:
			if bottextmode is True:
				xchat.prnt("Set slay {0} timer. Going off in {1} minutes.".format(num, timer // 60000))
			if num == 1:
				xchat.hook_timer(timer, slay)
			if num == 2:
				xchat.hook_timer(timer, slay2)
			if num == 3:
				xchat.hook_timer(timer, slay3)
			if num == 4:
				xchat.hook_timer(timer, slay4)
		if mana == 1:
			if bottextmode is True:
				xchat.prnt("Set slay {0} timer. Going off in {1} minutes.".format(num, timer // 60000))
			mana = 0
			if num == 1:
				xchat.hook_timer(timer, slayb)
			if num == 2:
				xchat.hook_timer(timer, slayb2)
			if num == 3:
				xchat.hook_timer(timer, slayb3)
			if num == 4:
				xchat.hook_timer(timer, slayb4)
	
def expertcalc(item):
	expertcalcsum = 0
	if(item == "amulet"):
		expertcalcsum = amulet // 10
	if(item == "charm"):
		expertcalcsum = charm // 10
	if(item == "helm"):
		expertcalcsum = helm // 10
	if(item == "boots"):
		expertcalcsum = boots // 10
	if(item == "gloves"):
		expertcalcsum = gloves // 10
	if(item == "ring"):
		expertcalcsum = ring // 10
	if(item == "leggings"):
		expertcalcsum = leggings // 10
	if(item == "shield"):
		expertcalcsum = shield // 10
	if(item == "tunic"):
		expertcalcsum = tunic // 10
	if(item == "weapon"):
		expertcalcsum = weapon // 10
	return expertcalcsum
	
def spendmoney(num):
	global level
	global gold
	global gems
	global xp
	global life
	global buylife
	global setbuy
	global upgradelevel
	global expert1
	global expert2
	global expert3
	global itemSum
	global expertSum
	global attackslaySum
	global itemSum2
	global expertSum2
	global attackslaySum2
	global itemSum3
	global expertSum3
	global attackslaySum3
	global itemSum4
	global expertSum4
	global attackslaySum4
	global expertitem1
	global expertitem2
	global expertitem3
	global expertitemb1
	global expertitemb2
	global expertitemb3
	global expertitemc1
	global expertitemc2
	global expertitemc3
	global expertitemd1
	global expertitemd2
	global expertitemd3
	global align
	global mysum
	global blackbuyspend
	global blackbuyspend14
	global interval
	global scrolls
	global exp
	global getgems
	global goldsave
	global scrollssum
	global xpupgrade
	global xpspend
	global amulet
	global charm
	global helm
	global boots
	global gloves
	global ring
	global leggings
	global shield
	global tunic
	global weapon 
	global expbuy
	
	# level 15 >= buy - decide what to spend our gold on! :D
	# level 1 >= blackbuy - requires 15 gems per buy
	# level 1 >= get x gems - 150 gold per gem
	# xpget 20xp minimum
	# buy experience - 500 gold - 10% off TTL
	
	getitems2(num)

	lowestitem = worstitem(num)
#	xchat.prnt("{0} Worst item {1}".format(num, lowestitem))

	if(gold < 0):
		gold = 0
	
	lifediff = 100 - life
	lifebuy = 9999999999999999

	if(level >= 20):
		spendmulti = level // 5
	
	if(level >= 1 and level <= 19):
		lifebuy = lifediff * 3
	if(level >= 20):
		lifebuy = lifediff * spendmulti
	if(level >= 15  and buylife is True and life >= 0 and life < 100 and gold >= lifebuy):
		usecommand("buy life", num)
		gold -= lifebuy
		life = 100
	       
	gembuy = True
	if(level >= 35):
		if upgradelevel == 0 and gold < 600:
			gembuy = False
		if upgradelevel == 0 and gold >= 600:
			usecommand("buy upgrade", num)
			gold -= 500
			upgradelevel = 1
	if(level >= 40):
		if upgradelevel == 1 and gold < 1100:
			gembuy = False
		if upgradelevel == 1 and gold >= 1100:
			usecommand("buy upgrade", num)
			gold -= 1000
			upgradelevel = 2
	if(level >= 45):
		if upgradelevel == 2 and gold < 2100:
			gembuy = False
		if upgradelevel == 2 and gold >= 2100:
			usecommand("buy upgrade", num)
			gold -= 2000
			upgradelevel = 3
	if(level >= 50):
		if upgradelevel == 3 and gold < 4100:
			gembuy = False
		if upgradelevel == 3 and gold >= 4100:
			usecommand("buy upgrade", num)
			gold -= 4000
			upgradelevel = 4
	if(level >= 60):
		if upgradelevel == 4 and gold < 8100:
			gembuy = False
		if upgradelevel == 4 and gold >= 8100:
			usecommand("buy upgrade", num)
			gold -= 8000
			upgradelevel = 5

	if(gembuy is True and expbuy is True and exp < 5):
		expdiff = 5 - exp
		expcost = expdiff * 500
		if(gold >= (expcost + 1100)):
			for i in range(expdiff):
				usecommand("buy experience", num)
				gold -= 500
				exp += 1
		elif(gold >= 500 + 1100):
			golddiff = gold - 1100
			expcalc = golddiff // 500
			if expcalc >= 1:
				for i in range(expcalc):
					usecommand("buy experience", num)
					gold -= 500
					exp += 1

#	xchat.prnt("{0} goldsave: {1}  gembuy: {2}  level: {3}  upgradelevel: {4}  align: {5}".format(num, goldsave, gembuy, level, upgradelevel, align))
	
	if(level >= setbuy):
		buycost = level * 2 * 3
		buyitem = level * 2     
		buydiff = 19
		if(gold > buycost + 100):
			if(amulet < (buyitem - buydiff)):
				usecommand("buy amulet {0}".format(buyitem), num)
				gold -= buycost
				amulet = buyitem
		if(gold > buycost + 100):
			if(boots < (buyitem - buydiff)):
				usecommand("buy boots {0}".format(buyitem), num)
				gold -= buycost
				boots = buyitem
		if(gold > buycost + 100):
			if(charm < (buyitem - buydiff)):
				usecommand("buy charm {0}".format(buyitem), num)
				gold -= buycost
				charm = buyitem
		if(gold > buycost + 100):
			if(gloves < (buyitem - buydiff)):
				usecommand("buy gloves {0}".format(buyitem), num)
				gold -= buycost
				gloves = buyitem
		if(gold > buycost + 100):
			if(helm < (buyitem - buydiff)):
				usecommand("buy helm {0}".format(buyitem), num)
				gold -= buycost
				helm = buyitem
		if(gold > buycost + 100):
			if(leggings < (buyitem - buydiff)):
				usecommand("buy leggings {0}".format(buyitem), num)
				gold -= buycost
				leggings = buyitem
		if(gold > buycost + 100):
			if(ring < (buyitem - buydiff)):
				usecommand("buy ring {0}".format(buyitem), num)
				gold -= buycost
				ring = buyitem
		if(gold > buycost + 100):
			if(shield < (buyitem - buydiff)):
				usecommand("buy shield {0}".format(buyitem), num)
				gold -= buycost
				shield = buyitem
		if(gold > buycost + 100):
			if(tunic < (buyitem - buydiff)):
				usecommand("buy tunic {0}".format(buyitem), num)
				gold -= buycost
				tunic = buyitem
		if(gold > buycost + 100):
			if(weapon < (buyitem - buydiff)):
				usecommand("buy weapon {0}".format(buyitem), num)
				gold -= buycost
				weapon = buyitem

	if(level >= 25):
		if(gems < 15):
			if getgems is True and gembuy is True:
				gemdiff = 15 - gems
				gemcost = gemdiff * 150
				if gold > (goldsave + gemcost):
					usecommand("get {0} gems".format(gemdiff), num)
					gold -= gemcost
					gems += gemdiff
		if(gems >= 15):
			if getgems is True and gembuy is True:
				gemdiv = gems // 15
				gemdiv2 = gemdiv * 15
				gemdiv3 = gemdiv2 + 15
				gemdiff = gemdiv3 - gems
				gemcost = gemdiff * 150
				if gold > (goldsave + gemcost):
					usecommand("get {0} gems".format(gemdiff), num)
					gold -= gemcost
					gems += gemdiff
				
				moneycalc = gold - goldsave
				gemcalc = moneycalc // 150
				if(gemcalc >= 15):
					gems15 = gemcalc // 15
					if(gems15 >= 1):
						buymoney = gems15 * 150 * 15
						buygems = gems15 * 15
						usecommand("get {0} gems".format(buygems), num)
						gold -= buymoney
						gems += buygems

			blackbuydisable = False
			if(blackbuyspend14 is True):
				if(gems >= (15 * 14)):
					usecommand("blackbuy {0} 14".format(lowestitem[0]),num)
					gems -= (15 * 14) 
					if(gems >= 15):
						interval = 120
						hookmain()
						blackbuydisable = True

			if(blackbuyspend is True and blackbuydisable is False):
				if(gems >= 15):
					gemspend15 = gems // 15
					if(gemspend15 >= 1):
						usecommand("blackbuy {0} {1}".format(lowestitem[0], gemspend15), num)
						gems -= gemspend15 * 15 
						if(gems >= 15):
							interval = 120
							hookmain()

		if(xp >= 20 and mysum >= scrollssum and scrolls < 5):
			xpcalc = xp // 20
			scrollsdiff = 5 - scrolls
			scrollscost = scrollsdiff * 20
			if(xp >= scrollscost):
				for i in range(scrollsdiff):
					usecommand("xpget scroll",num)
					xp -= 20
					scrolls += 1
			elif(xp >= 20):
				xpcalc = xp // 20
				if xpcalc >= 1:
					for i in range(xpcalc):
						usecommand("xpget scroll",num)
						xp -= 20
						scrolls += 1
						
	if(level >= 25 and xpupgrade is True):
		if(xp >= xpspend):
			if(mysum < scrollssum):
				xpcalc = xp // xpspend
			if(mysum >= scrollssum):
				xpdiff = xp - 200
				xpcalc = xpdiff // xpspend                               
			if(xpcalc >= 1):
				if xpcalc > 5:
					xpcalc = 5
				for i in range(xpcalc):
					usecommand("xpget {0} {1}".format(lowestitem[0], xpspend), num)
					xp -= xpspend

	if num == 1:
		expertitem1 = expertcalc(expert1)
		expertitem2 = expertcalc(expert2)
		expertitem3 = expertcalc(expert3)
	if num == 2:
		expertitemb1 = expertcalc(expert1)
		expertitemb2 = expertcalc(expert2)
		expertitemb3 = expertcalc(expert3)
	if num == 3:
		expertitemc1 = expertcalc(expert1)
		expertitemc2 = expertcalc(expert2)
		expertitemc3 = expertcalc(expert3)
	if num == 4:
		expertitemd1 = expertcalc(expert1)
		expertitemd2 = expertcalc(expert2)
		expertitemd3 = expertcalc(expert3)
	   
	lifepercent = (float(life) / 100)
	if num == 1:
		itemSum = (amulet + charm + helm + boots + gloves + ring + leggings + shield + tunic + weapon)
		expertSum = expertitem1 + expertitem2 + expertitem3 
	if num == 2:
		itemSum2 = (amulet + charm + helm + boots + gloves + ring + leggings + shield + tunic + weapon)
		expertSum2 = expertitemb1 + expertitemb2 + expertitemb3 
	if num == 3:
		itemSum3 = (amulet + charm + helm + boots + gloves + ring + leggings + shield + tunic + weapon)
		expertSum3 = expertitemc1 + expertitemc2 + expertitemc3 
	if num == 4:
		itemSum4 = (amulet + charm + helm + boots + gloves + ring + leggings + shield + tunic + weapon)
		expertSum4 = expertitemd1 + expertitemd2 + expertitemd3 
	upgradeSum1 = upgradelevel * 100
	if num == 1:
		attackslaySum = (itemSum + expertSum + upgradeSum1) * lifepercent
	if num == 2:
		attackslaySum2 = (itemSum2 + expertSum2 + upgradeSum1) * lifepercent
	if num == 3:
		attackslaySum3 = (itemSum3 + expertSum3 + upgradeSum1) * lifepercent
	if num == 4:
		attackslaySum4 = (itemSum4 + expertSum4 + upgradeSum1) * lifepercent

def lvlup(userdata):
	lvlupmulti(1)

def lvlup2(userdata):
	lvlupmulti(2)

def lvlup3(userdata):
	lvlupmulti(3)

def lvlup4(userdata):
	lvlupmulti(4)

def lvlupmulti(num):
	global name
	global name2
	global name3
	global name4
	global level
	global interval
	global life
	global bottextmode

	getitems2(num)
	if num == 1:
		namelist = name
	if num == 2:
		namelist = name2
	if num == 3:
		namelist = name3
	if num == 4:
		namelist = name4

	interval = 60
	hookmain()

	level += 1

	if bottextmode is True:
		xchat.prnt("{0} has reached level {1}!".format(namelist, level))

	if(level >= 16 and life > 10):
		if num == 1:
			xchat.hook_timer(0, attack)
		if num == 2:
			xchat.hook_timer(0, attack2)
		if num == 3:
			xchat.hook_timer(0, attack3)
		if num == 4:
			xchat.hook_timer(0, attack4)

def fight_fight(num):
	global name
	global name2
	global name3
	global name4
	global level
	global ufightcalc
	global ufightcalc2
	global ufightcalc3
	global ufightcalc4
	global itemSum
	global expertSum
	global itemSum2
	global expertSum2
	global itemSum3
	global expertSum3
	global itemSum4
	global expertSum4
	global fights
	global rank
	global rank2
	global rank3
	global rank4
	global ability
	global upgradelevel
	global life
	global fightmode
	global bottextmode

	getitems2(num)

	if num == 1:
		ufight = testfight(1)
		namelist = name
		itemSumlist = itemSum
		expertSumlist = expertSum
		ranklist = rank
	if num == 2:
		ufight = testfight(2)
		namelist = name2
		itemSumlist = itemSum2
		expertSumlist = expertSum2
		ranklist = rank2
	if num == 3:
		ufight = testfight(3)
		namelist = name3
		itemSumlist = itemSum3
		expertSumlist = expertSum3
		ranklist = rank3
	if num == 4:
		ufight = testfight(4)
		namelist = name4
		itemSumlist = itemSum4
		expertSumlist = expertSum4
		ranklist = rank4
	
	upgradeSum1 = upgradelevel * 100
	fightSumTotal = itemSumlist + expertSumlist
	abilityadj = 0
	if ability == "b":
		if ufight[5] == "p":
			abilityadj = math.floor(fightSumTotal * 0.30)

	if ability == "p":
		if ufight[5] == "r":
			abilityadj = math.floor(fightSumTotal * 0.30)
		
	if ability == "r":
		if ufight[5] == "w":
			abilityadj = math.floor(fightSumTotal * 0.30)
		
	if ability == "w":
		if ufight[5] == "b":
			abilityadj = math.floor(fightSumTotal * 0.30)

	lifepercent = (float(life) / 100)
	fightAdj = (fightSumTotal + abilityadj + upgradeSum1) * lifepercent
	
	if num == 1:
		ufightcalc = fightAdj / ufight[2]
	if num == 2:
		ufightcalc2 = fightAdj / ufight[2]
	if num == 3:
		ufightcalc3 = fightAdj / ufight[2]
	if num == 4:
		ufightcalc4 = fightAdj / ufight[2]

	if(level >= 25):
		if num == 1:
			ufightcalclist = ufightcalc
		if num == 2:
			ufightcalclist = ufightcalc2
		if num == 3:
			ufightcalclist = ufightcalc3
		if num == 4:
			ufightcalclist = ufightcalc4
		if bottextmode is True:
			xchat.prnt("{0} Best fight for Rank {1}:  {2}  [{3}]  Opponent: Rank {4}:  {5}  [{6}], Odds {7}".format(num, ranklist, namelist, int(fightAdj), ufight[6], ufight[0], int(ufight[2]), ufightcalclist))
		if(ufightcalclist >= 0.9 and fightmode is True):
			usecommand("fight {0}".format( ufight[0] ),num)
			fights += 1

def testfight(num):
	global newlist
	global newlist2
	global newlist3
	global newlist4
	global level
	global name
	global name2
	global name3
	global name4
	global upgradelevel
	global itemSum
	global expertSum
	global itemSum2
	global expertSum2
	global itemSum3
	global expertSum3
	global itemSum4
	global expertSum4
	global ability
	global life

	getitems2(num)
	
	if num == 1:
		newlists = newlist
		namelist = name
		itemSumlist = itemSum
		expertSumlist = expertSum
	if num == 2:
		newlists = newlist2
		namelist = name2
		itemSumlist = itemSum2
		expertSumlist = expertSum2
	if num == 3:
		newlists = newlist3
		namelist = name3
		itemSumlist = itemSum3
		expertSumlist = expertSum3
	if num == 4:
		newlists = newlist4
		namelist = name4
		itemSumlist = itemSum4
		expertSumlist = expertSum4
		
	upgradeSum1 = upgradelevel * 100
	fightSumTotal = float(itemSumlist + expertSumlist)
	lifepercent = (float(life) / 100)
	test = []
	
	diff = 0
	best = ("Doctor Who?", 9999999999.0, 9999999999.0, 0, 0, "p", 0)
	newlists.sort( key=operator.itemgetter(2))
	if newlists != None:
		for entry in newlists:
			if(entry[3] >= level and entry[0] != namelist):
				abilityadj = 0
				if ability == "b":
					if entry[5] == "p":
						abilityadj = math.floor(fightSumTotal * 0.30)

				if ability == "p":
					if entry[5] == "r":
						abilityadj = math.floor(fightSumTotal * 0.30)
					
				if ability == "r":
					if entry[5] == "w":
						abilityadj = math.floor(fightSumTotal * 0.30)
					
				if ability == "w":
					if entry[5] == "b":
						abilityadj = math.floor(fightSumTotal * 0.30)

				fightAdj = (fightSumTotal + abilityadj + upgradeSum1) * lifepercent

				try:
					currdiff = fightAdj / entry[2]
				except ZeroDivisionError:
					currdiff = 0
				test.append( (entry, currdiff) )

		test.sort( key=operator.itemgetter(1))

		for entry in test:
			if entry[1] > diff:
				diff = entry[1]
				best = entry[0]

	return best

def attack(userdata):
	attackmulti(1)

def attack2(userdata):
	attackmulti(2)

def attack3(userdata):
	attackmulti(3)

def attack4(userdata):
	attackmulti(4)

def attackmulti(num):
	global creepattack
	global setcreeptarget
	
	if creepattack is True:
		creep = bestattack(num)
		if creep != "CreepList Error":
			usecommand("attack " + creep, num)
		if creep == "CreepList Error":
			xchat.prnt("{0}".format(creep))
	if creepattack is False:
		usecommand("attack " + setcreeptarget, num)
		
def slay(userdata):
	slaymulti(1, 1)

def slay2(userdata):
	slaymulti(2, 1)

def slay3(userdata):
	slaymulti(3, 1)

def slay4(userdata):
	slaymulti(4, 1)

def slayb(userdata):
	slaymulti(1, 2)

def slayb2(userdata):
	slaymulti(2, 2)

def slayb3(userdata):
	slaymulti(3, 2)

def slayb4(userdata):
	slaymulti(4, 2)

def slaymulti(num, num2):
	monster = bestslay(num, num2)
	if monster != "MonsterList Error":
		usecommand("slay " + monster, num)
	if monster == "MonsterList Error":
		xchat.prnt("{0}".format(monster))

def bestattack(num):
	global creeps
	global attackslaySum
	global attackslaySum2
	global attackslaySum3
	global attackslaySum4

	if num == 1:
		attackslaySumlist = attackslaySum
	if num == 2:
		attackslaySumlist = attackslaySum2
	if num == 3:
		attackslaySumlist = attackslaySum3
	if num == 4:
		attackslaySumlist = attackslaySum4
		
	good = "CreepList Error"
	for thing in creeps:
		if(attackslaySumlist <= thing[1]):
			good = thing[0]
	return good

def bestslay(num, num2):
	global monsters
	global attackslaySum
	global attackslaySum2
	global attackslaySum3
	global attackslaySum4

	if num == 1:
		attackslaySumlist = attackslaySum
	if num == 2:
		attackslaySumlist = attackslaySum2
	if num == 3:
		attackslaySumlist = attackslaySum3
	if num == 4:
		attackslaySumlist = attackslaySum4
		
	good = "MonsterList Error"
	if num2 == 1:
		multi = 1
	if num2 == 2:
		multi = 2
	for thing in monsters:
		if((attackslaySumlist * multi) <= thing[1]):
			good = thing[0]
	return good

def worstitem(num):
	global amulet
	global charm
	global helm
	global boots
	global gloves
	global ring
	global leggings
	global shield
	global tunic
	global weapon 

	itemlist = [	["amulet",	amulet],	\
			["charm",       charm],  \
			["helm",	helm],	\
			["boots",       boots],  \
			["gloves",	gloves],	\
			["ring",        ring],  \
			["leggings",	leggings],	\
			["shield",      shield],  \
			["tunic",	tunic],	\
			["weapon",	weapon]	]
	
	itemlist.sort( key=operator.itemgetter(1), reverse=True )
	good = itemlist
	diff = 999999
	for thing in itemlist:
		if(thing[1] < diff):
			good = thing
	return good
