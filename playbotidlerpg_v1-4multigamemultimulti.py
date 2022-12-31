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
__module_version__ = "1.4"
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
		["Spider",	2000],	\
		["Bat",         3000],  \
		["Wolf",        4000],  \
		["Goblin",	5000],	\
		["Shadow",	6000],	\
		["Lich",	7000],	\
		["Skeleton",	8000],	\
		["Ghost",       9000],	\
		["Phantom",     10000],  \
		["Troll",	12000],	\
		["Cyclop",      14000],  \
		["Mutant",	17000],	\
		["Ogre",        21000],  \
		["Phoenix",	25000],  \
		["Wraith",      30000],  \
		["Vampire",     35000],  \
		["Bigfoot",     40000],  \
		["Chimera",     45000],  \
		["Witch",       50000], \
		["Imp",         55000], \
		["Hag",         60000], \
		["Kraken",      65000], \
		["Wyvern",      70000], \
		["Grendel",     75000], \
		["Banshee",     80000], \
		["Leprechaun",  85000], \
		["Mummy",       90000], \
		["Sphinx",      95000], \
		["Krampus",     100000], \
		["Griffin",     105000], \
		["Harpy",       110000], \
		["Hydra",       115000], \
		["Demon",       125000], \
		["Centaur",     150000], \
		["Werewolf",    250000], \
		["Giant",       2000000], \
		["Satan",       9999999]  ]

monsters = [	["Blue_Dragon",	        7500],	\
		["Yellow_Dragon",       15000],  \
		["Green_Dragon",	25000],	\
		["Red_Dragon",	        35000], \
		["Black_Dragon",        40000], \
		["White_Dragon",        60000], \
		["Bronze_Dragon",       80000], \
		["Silver_Dragon",       100000], \
		["Gold_Dragon",         350000], \
		["Platinum_Dragon",     6000000], \
		["Diamond_Dragon",      9999999]  ]

creeps.reverse()
monsters.reverse()

#               Network                 Website                                 Server                          FightLL ChanName        BotName                         GameID
gamelist = [    ["abandoned-irc",       "http://irpg.abandoned-irc.net",        "irc.abandoned-irc.net",        True,   "#zw-idlerpg",  "IdleRPG",                      1],  \
		["dalnet",              "https://tilde.green/~hellspawn",       "irc.dal.net",                  True,   "#irpg",        "DAL-IRPG",                     2], \
		["efnet",               "http://idle.rpgsystems.org",           "irc.efnet.net",                True,   "#idlerpg",     "IdleRPG",                      3], \
		["technet",             "http://evilnet.idleirpg.site",         "irc.technet.chat",             True,   "#idlerpg",     "IdleRPG/IRC-nERDs",            4],  \
		["irc-nerds",           "http://evilnet.idleirpg.site",         "irc.irc-nerds.net",            True,   "#idlerpg",     "IdleRPG",                      4],  \
		["twistednet",          "http://idlerpg.twistednet.org",        "irc.twistednet.org",           False,  "#idlerpg",     "IdleRPG",                      5]   ]

russweb = "https://russellb.000webhostapp.com/"
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
playerspagelist2 = None
playerspagelist3 = None
playerspagelist4 = None
mainhook = None
itemslist = None
currentversion = __module_version__
currentversion = float( currentversion )

CONFIG_FILE_LOCATION = xchat.get_info('xchatdir')+"/.playbotidlerpgmultigamemultimulti"
try:
	f = open(CONFIG_FILE_LOCATION,"rb")
	configList = pickle.load(f)
	f.close()
except:
	xchat.prnt("ConfigList Load Error - Using Default Settings")
	configList = []

# ZNC settings
ZNC = False # ZNC Server Mode - True = On, False = Off
ZNCServer = "*******" # ZNC Server Address
ZNCPort = "+8080" # ZNC Port Number - For SSL put + before and in " " "+8080"
ZNCUser = "***/***" # ZNC Username/Network
ZNCPass = "*******" # ZNC Password
ZNC2 = False # ZNC Server Mode - True = On, False = Off
ZNCServer2 = "*******" # ZNC Server Address
ZNCPort2 = "+8080" # ZNC Port Number - For SSL put + before and in " " "+8080"
ZNCUser2 = "***/***" # ZNC Username/Network
ZNCPass2 = "*******" # ZNC Password
ZNC3 = False # ZNC Server Mode - True = On, False = Off
ZNCServer3 = "*******" # ZNC Server Address
ZNCPort3 = "+8080" # ZNC Port Number - For SSL put + before and in " " "+8080"
ZNCUser3 = "***/***" # ZNC Username/Network
ZNCPass3 = "*******" # ZNC Password
ZNC4 = False # ZNC Server Mode - True = On, False = Off
ZNCServer4 = "*******" # ZNC Server Address
ZNCPort4 = "+8080" # ZNC Port Number - For SSL put + before and in " " "+8080"
ZNCUser4 = "***/***" # ZNC Username/Network
ZNCPass4 = "*******" # ZNC Password

# Changeable settings
setbuy = 15 # level to start buying items from
goldsave = 3100 # gold kept in hand
buylife = True
blackbuyspend = True
blackbuyspend14 = True
getgems = True
fightmode = True
creepattack = True # True = On, False = Off - Autocreep selection
setcreeptarget = "Werewolf" # Sets creep target. creepattack needs to be False to use
scrollssum = 3000 # item score you start buying scrolls
xpupgrade = True # Upgrade Items with XP
xpspend = 20 # Amount you use with xpget to upgrade items
intervaltext = True # True = on, False = off - Text displayed every interval
townworkswitch = True # True = Town/Work Area Switching, False = Town/Forest Area Switching
buyluck = False
buypower = False
expbuy = False
slaysum = 1000 # minimum sum you start slaying without mana from

# declare stats as global
fightlevellimit = None
fightlevellimit2 = None
fightlevellimit3 = None
fightlevellimit4 = None
channame = None
botname = None
channame2 = None
botname2 = None
channame3 = None
botname3 = None
channame4 = None
botname4 = None
servername = None
website = None
servername2 = None
website2 = None
servername3 = None
website3 = None
servername4 = None
website4 = None
gameid = 0
gameid2 = 0
gameid3 = 0
gameid4 = 0
name = None
pswd = None
name2 = None
pswd2 = None
name3 = None
pswd3 = None
name4 = None
pswd4 = None
char1 = False
char2 = False
char3 = False
char4 = False
charcount = 0
private = True
chanmessage = True
chanmessagecount = 0
level = 0
level2 = 0
level3 = 0
level4 = 0
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
fights2 = 0
fights3 = 0
fights4 = 0
scrolls = 0
exp = 0
luck = 0
powerpots = 0
mana = 0
stone1 = None
stone2 = None
stone3 = None
stoneb1 = None
stoneb2 = None
stoneb3 = None
stonec1 = None
stonec2 = None
stonec3 = None
stoned1 = None
stoned2 = None
stoned3 = None
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
life2 = 0
life3 = 0
life4 = 0
align = "n"
upgradelevel = 0
eatused = 0

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
webworksB = None 
webworksC = None 
webworksD = None 
gameactive = None
lottonuma1 = None
lottonuma2 = None
lottonuma3 = None
lottonumb1 = None
lottonumb2 = None
lottonumb3 = None
lottonumc1 = None
lottonumc2 = None
lottonumc3 = None
lottonumd1 = None
lottonumd2 = None
lottonumd3 = None
location = None
locationtime = 0
location2 = None
locationtime2 = 0
location3 = None
locationtime3 = 0
location4 = None
locationtime4 = 0

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
	if(entry[0] == "buylife"):
		buylife = entry[1]
	if(entry[0] == "buyluck"):
		buyluck = entry[1]
	if(entry[0] == "buypower"):
		buypower = entry[1]
	if(entry[0] == "creepattack"):
		creepattack = entry[1]
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

	webversion = None
	try:
		if python3 is False:
			text = urllib2.urlopen(russweb + "playbotversionmultigame.txt")
		if python3 is True:
			text = urllib.request.urlopen(russweb + "playbotversionmultigame.txt")
		webversion = text.read()
		webversion = float( webversion )
		text.close()

	except:
		xchat.prnt( "Could not access {0}".format(russweb))

	xchat.prnt("Current version {0}".format(currentversion))
	xchat.prnt("Web version {0}".format(webversion))
	if webversion != None:
		if(currentversion == webversion):
			xchat.prnt("You have the current version of PlayBot")
		if(currentversion < webversion):
			xchat.prnt("You have an old version of PlayBot")
			xchat.prnt("You can download a new version from {0}".format(russweb))
		if(currentversion > webversion):
			xchat.prnt("Give me, Give me")

def configwrite():
	global blackbuyspend
	global blackbuyspend14
	global buylife
	global buyluck
	global buypower
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
	
	configList = []
	configList.append( ( "blackbuyspend", blackbuyspend ) )
	configList.append( ( "blackbuyspend14", blackbuyspend14 ) )
	configList.append( ( "buylife", buylife ) )
	configList.append( ( "buyluck", buyluck ) )
	configList.append( ( "buypower", buypower ) )
	configList.append( ( "creepattack", creepattack ) )
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
	global botname2
	global botname3
	global botname4
	global netname
	global netname2
	global netname3
	global netname4
	global char1
	global char2
	global char3
	global char4
	global botdisable1
	global botdisable2
	global botdisable3
	global botdisable4
	
	botcount1 = 0
	botcount2 = 0
	botcount3 = 0
	botcount4 = 0

	if num == 1 and char1 is True:
		for entry in gamelist:
			if entry[0] in netname.lower():
				botname = entry[5]
		bottest = botname
		botentry = []

		try:
			userlist = game_chan.get_list("users")

			for user in userlist:
				if bottest in user.nick and user.nick != bottest:
					botprefix = user.prefix
					if(botprefix == "@"):
						botentry.append(user.nick)
						botname10 = user.nick
		except AttributeError:
			xchat.prnt( "AttributeError" )

		botcount1 = len(botentry)
		if botcount1 == 1:
			botname = botname10
		if botcount1 >= 2:
			botdisable1 = True
	if num == 2 and char2 is True:
		for entry in gamelist:
			if entry[0] in netname2.lower():
				botname2 = entry[5]
		bottest = botname2
		botentry = []

		try:
			userlist = game_chan2.get_list("users")

			for user in userlist:
				if bottest in user.nick and user.nick != bottest:
					botprefix = user.prefix
					if(botprefix == "@"):
						botentry.append(user.nick)
						botname10 = user.nick
		except AttributeError:
			xchat.prnt( "AttributeError" )

		botcount2 = len(botentry)
		if botcount2 == 1:
			botname2 = botname10
		if botcount2 >= 2:
			botdisable2 = True
	if num == 3 and char3 is True:
		for entry in gamelist:
			if entry[0] in netname3.lower():
				botname3 = entry[5]
		bottest = botname3
		botentry = []

		try:
			userlist = game_chan3.get_list("users")

			for user in userlist:
				if bottest in user.nick and user.nick != bottest:
					botprefix = user.prefix
					if(botprefix == "@"):
						botentry.append(user.nick)
						botname10 = user.nick
		except AttributeError:
			xchat.prnt( "AttributeError" )

		botcount3 = len(botentry)
		if botcount3 == 1:
			botname3 = botname10
		if botcount3 >= 2:
			botdisable3 = True
	if num == 4 and char4 is True:
		for entry in gamelist:
			if entry[0] in netname4.lower():
				botname4 = entry[5]
		bottest = botname4
		botentry = []

		try:
			userlist = game_chan4.get_list("users")

			for user in userlist:
				if bottest in user.nick and user.nick != bottest:
					botprefix = user.prefix
					if(botprefix == "@"):
						botentry.append(user.nick)
						botname10 = user.nick
		except AttributeError:
			xchat.prnt( "AttributeError" )

		botcount4 = len(botentry)
		if botcount4 == 1:
			botname4 = botname10
		if botcount4 >= 2:
			botdisable4 = True

def usecommand(commanded, num):
	global game_chan
	global game_chan2
	global game_chan3
	global game_chan4
	global botname
	global botname2
	global botname3
	global botname4
	global channame
	global channame2
	global channame3
	global channame4
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

	if(num == 1 and botdisable1 is False):
		try:
			game_chan.command( "msg {0} {1}".format(botname, commanded) )
		except AttributeError:
			raise NameError( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame) )
	if(num == 2 and botdisable2 is False):
		try:
			game_chan2.command( "msg {0} {1}".format(botname2, commanded) )
		except AttributeError:
			raise NameError( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame2) )
	if(num == 3 and botdisable3 is False):
		try:
			game_chan3.command( "msg {0} {1}".format(botname3, commanded) )
		except AttributeError:
			raise NameError( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame3) )
	if(num == 4 and botdisable4 is False):
		try:
			game_chan4.command( "msg {0} {1}".format(botname4, commanded) )
		except AttributeError:
			raise NameError( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame4) )

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
	global channame2
	global channame3
	global channame4
	global game_chan
	global game_chan2
	global game_chan3
	global game_chan4
	global gameactive
	global fightmode
	global char1
	global char2
	global char3
	global char4
	global charcount
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
	global gamelist
	global website
	global servername
	global fightlevellimit
	global botname
	global website2
	global servername2
	global fightlevellimit2
	global botname2
	global website3
	global servername3
	global fightlevellimit3
	global botname3
	global website4
	global servername4
	global fightlevellimit4
	global botname4
	global buyluck
	global buypower
	global expbuy
	global gameid
	global gameid2
	global gameid3
	global gameid4
	global playerspagelist
	global playerspagelist2
	global playerspagelist3
	global playerspagelist4
	global webworks
	global webworksB
	global webworksC
	global webworksD
	global slaysum
	
	charcount += 1

	netlist = []
	for entry in gamelist:
		netlist.append( ( entry[0] ) )
	if charcount == 1:
		netcheck = False
		gameactive = True
		netname = xchat.get_info("network")
		nickname = xchat.get_info("nick")
		namecheck = False

		for entry in gamelist:
			if entry[0] in netname.lower():
				website = entry[1]
				servername = entry[2]
				fightlevellimit = entry[3]
				channame = entry[4]
				botname = entry[5]
				gameid = entry[6]
				netcheck = True
				
		# find context
		game_chan = xchat.find_context(channel=channame)

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
		if netcheck is True:
			webdata2(1)
		if netcheck is False:
			xchat.prnt("Networks supported: {0}".format(netlist))
			if "quakenet" in netname.lower():
				xchat.prnt("You need to use the QuakeNet version of PlayBot")
		if(name is None or pswd is None or netcheck is False):
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
		netcheck = False
		netname2 = xchat.get_info("network")
		nickname2 = xchat.get_info("nick")
		namecheck2 = False

		for entry in gamelist:
			if entry[0] in netname2.lower():
				website2 = entry[1]
				servername2 = entry[2]
				fightlevellimit2 = entry[3]
				channame2 = entry[4]
				botname2 = entry[5]
				gameid2 = entry[6]
				netcheck = True

		# find context
		game_chan2 = xchat.find_context(channel=channame2)

		if(game_chan2 is None):
			xchat.prnt("Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame2))
			charcount = 1
		try:
			if(name2 is None or pswd2 is None):
				name2 = word[1]
				pswd2 = word[2]
		except IndexError:
			xchat.prnt( "LOGIN ERROR: To log in use /login CharName Password" )
			charcount = 1
		if netcheck is True:
			webdata2(2)
		if netcheck is False:
			xchat.prnt("Networks supported: {0}".format(netlist))
			if "quakenet" in netname2.lower():
				xchat.prnt("You need to use the QuakeNet version of PlayBot")
		if(name2 is None or pswd2 is None or netcheck is False):
			charcount = 1
			xchat.prnt("Login Failed")
		if charcount == 2:
			try:
				for entry in playerspagelist2:
					if ">{0}<".format(name2) in entry:
						namecheck2 = True
			except TypeError:
				webworksB = False
			if(namecheck2 is False and webworksB is True):
				xchat.prnt("LOGIN ERROR: {0} does not exist".format(name2))
				charcount = 1
			if charcount == 2:
				if gameid2 != gameid:
					char2 = True
					usecommand("login {0} {1}".format(name2, pswd2), 2 )
				if gameid2 == gameid:
					if nickname2 == nickname:
						charcount = 1
						xchat.prnt("Character {0} is already logged in".format(name))
					if nickname2 != nickname:                                        
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
			gameid2 = 0
			return

	if charcount == 3:
		netcheck = False
		netname3 = xchat.get_info("network")
		nickname3 = xchat.get_info("nick")
		namecheck3 = False

		for entry in gamelist:
			if entry[0] in netname3.lower():
				website3 = entry[1]
				servername3 = entry[2]
				fightlevellimit3 = entry[3]
				channame3 = entry[4]
				botname3 = entry[5]
				gameid3 = entry[6]
				netcheck = True

		# find context
		game_chan3 = xchat.find_context(channel=channame3)

		if(game_chan3 is None):
			xchat.prnt("Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame3))
			charcount = 2
		try:
			if(name3 is None or pswd3 is None):
				name3 = word[1]
				pswd3 = word[2]
		except IndexError:
			xchat.prnt( "LOGIN ERROR: To log in use /login CharName Password" )
			charcount = 2
		if netcheck is True:
			webdata2(3)
		if netcheck is False:
			xchat.prnt("Networks supported: {0}".format(netlist))
			if "quakenet" in netname3.lower():
				xchat.prnt("You need to use the QuakeNet version of PlayBot")
		if(name3 is None or pswd3 is None or netcheck is False):
			charcount = 2
			xchat.prnt("Login Failed")
		if charcount == 3:
			try:
				for entry in playerspagelist3:
					if ">{0}<".format(name3) in entry:
						namecheck3 = True
			except TypeError:
				webworksC = False
			if(namecheck3 is False and webworksC is True):
				xchat.prnt("LOGIN ERROR: {0} does not exist".format(name3))
				charcount = 2
			if charcount == 3:
				if gameid3 != gameid and gameid3 != gameid2: 
					char3 = True
					usecommand("login {0} {1}".format(name3, pswd3), 3 )
				if gameid3 == gameid:
					if nickname3 == nickname or name3 == name:
						charcount = 2
						xchat.prnt("Character {0} is already logged in".format(name))
					if nickname3 != nickname and name3 != name:
						char3 = True
						usecommand("login {0} {1}".format(name3, pswd3), 3 )
				if gameid3 == gameid2:
					if nickname3 == nickname2 or name3 == name2:
						charcount = 2
						xchat.prnt("Character {0} is already logged in".format(name2))
					if nickname3 != nickname2 and name3 != name2:
						char3 = True
						usecommand("login {0} {1}".format(name3, pswd3), 3 )
					
		if charcount == 2:
			char3 = False
			netname3 = None
			nickname3 = None
			game_chan3 = None
			name3 = None
			pswd3 = None
			gameid3 = 0
			return

	if charcount == 4:
		netcheck = False
		netname4 = xchat.get_info("network")
		nickname4 = xchat.get_info("nick")
		namecheck4 = False

		for entry in gamelist:
			if entry[0] in netname4.lower():
				website4 = entry[1]
				servername4 = entry[2]
				fightlevellimit4 = entry[3]
				channame4 = entry[4]
				botname4 = entry[5]
				gameid4 = entry[6]
				netcheck = True

		# find context
		game_chan4 = xchat.find_context(channel=channame4)

		if(game_chan4 is None):
			xchat.prnt("Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame4))
			charcount = 3
		try:
			if(name4 is None or pswd4 is None):
				name4 = word[1]
				pswd4 = word[2]
		except IndexError:
			xchat.prnt( "LOGIN ERROR: To log in use /login CharName Password" )
			charcount = 3
		if netcheck is True:
			webdata2(4)
		if netcheck is False:
			xchat.prnt("Networks supported: {0}".format(netlist))
			if "quakenet" in netname4.lower():
				xchat.prnt("You need to use the QuakeNet version of PlayBot")
		if(name4 is None or pswd4 is None or netcheck is False):
			charcount = 3
			xchat.prnt("Login Failed")
		if charcount == 4:
			try:
				for entry in playerspagelist4:
					if ">{0}<".format(name4) in entry:
						namecheck4 = True
			except TypeError:
				webworksD = False
			if(namecheck4 is False and webworksD is True):
				xchat.prnt("LOGIN ERROR: {0} does not exist".format(name4))
				charcount = 3
			if charcount == 4:
				if gameid4 != gameid and gameid4 != gameid2 and gameid4 != gameid3: 
					char4 = True
					usecommand("login {0} {1}".format(name4, pswd4), 4 )
				if gameid4 == gameid:
					if nickname4 == nickname or name4 == name:
						charcount = 3
						xchat.prnt("Character {0} is already logged in".format(name))
					if nickname4 != nickname and name4 != name:
						char4 = True
						usecommand("login {0} {1}".format(name4, pswd4), 4 )
				if gameid4 == gameid2:
					if nickname4 == nickname2 or name4 == name2:
						charcount = 3
						xchat.prnt("Character {0} is already logged in".format(name2))
					if nickname4 != nickname2 and name4 != name2:
						char4 = True
						usecommand("login {0} {1}".format(name4, pswd4), 4 )
				if gameid4 == gameid3:
					if nickname4 == nickname3 or name4 == name3:
						charcount = 3
						xchat.prnt("Character {0} is already logged in".format(name3))
					if nickname4 != nickname3 and name4 != name3:
						char4 = True
						usecommand("login {0} {1}".format(name4, pswd4), 4 )
		if charcount == 3:
			char4 = False
			netname4 = None
			nickname4 = None
			game_chan4 = None
			name4 = None
			pswd4 = None
			gameid4 = 0
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
		if buylife is True:
			xchat.prnt("Buy Life Mode Activated.  To turn it off use /buylifeoff")
		if buylife is False:
			xchat.prnt("Buy Life Mode Deactivated.  To turn it on use /buylifeon")
		if buyluck is True:
			xchat.prnt("Buy Luck Potion Mode Activated.  To turn it off use /buyluckoff")
		if buyluck is False:
			xchat.prnt("Buy Luck Potion Mode Deactivated.  To turn it on use /buyluckon")
		if buypower is True:
			xchat.prnt("Buy Power Potion Mode Activated.  To turn it off use /buypoweroff")
		if buypower is False:
			xchat.prnt("Buy Power Potion Mode Deactivated.  To turn it on use /buypoweron")
		if creepattack is True:
			xchat.prnt("CreepAttack Mode Activated.  To turn it off use /creepattackoff")
		if creepattack is False:
			xchat.prnt("CreepAttack Mode Deactivated.  To turn it on use /creepattackon")
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
		xchat.prnt("Current Scroll Buy ItemScore: {0}.  If you want to change it use /setscrolls number".format(scrollssum))
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

def buyluckoff(word, word_eol, userdata):
	global buyluck
	buyluck = False
	xchat.prnt("Buy Luck Power Mode Deactivated.  To turn it on use /buyluckon")
	configwrite()
	return xchat.EAT_ALL

xchat.hook_command("buyluckoff", buyluckoff, help="/buyluckoff - Turns buying luck off")

def buyluckon(word, word_eol, userdata):
	global buyluck
	buyluck = True
	xchat.prnt("Buy Luck Power Mode Activated.  To turn if off use /buyluckoff")
	configwrite()
	return xchat.EAT_ALL

xchat.hook_command("buyluckon", buyluckon, help="/buyluckon - Turns buying luck on")

def buypoweroff(word, word_eol, userdata):
	global buypower
	buypower = False
	xchat.prnt("Buy Power Potion Mode Deactivated.  To turn it on use /buypoweron")
	configwrite()
	return xchat.EAT_ALL

xchat.hook_command("buypoweroff", buypoweroff, help="/buypoweroff - Turns buying power potion off")

def buypoweron(word, word_eol, userdata):
	global buypower
	buypower = True
	xchat.prnt("Buy Power Potion Mode Activated.  To turn if off use /buypoweroff")
	configwrite()
	return xchat.EAT_ALL

xchat.hook_command("buypoweron", buypoweron, help="/buypoweron - Turns buying power potion on")

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
	xchat.prnt("Buy Life Mode Off           - /buylifeoff")
	xchat.prnt("Buy Life Mode On            - /buylifeon")
	xchat.prnt("Buy Luck Potion Mode Off    - /buyluckoff")
	xchat.prnt("Buy Luck Potion Mode On     - /buyluckon")
	xchat.prnt("Buy Power Potion Mode Off   - /buyluckoff")
	xchat.prnt("Buy Power Potion Mode On    - /buyluckon")
	xchat.prnt("CreepAttack Mode Off        - /creepattackoff")
	xchat.prnt("CreepAttack Mode On         - /creepattackon")
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
	xchat.prnt("Set Scroll Buy ItemScore    - /setscrolls number")
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
	global buyluck
	global buypower
	global setbuy
	global char1
	global char2
	global char3
	global char4
	global name
	global name2
	global name3
	global name4
	global gameactive
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
	global intervaltext
	global townworkswitch
	global goldsave
	global netname
	global netname2
	global netname3
	global netname4
	global expbuy
	global slaysum
	
	if gameactive is True:
		xchat.prnt("Playbot Settings List")
		xchat.prnt("")
		if townworkswitch is True:
			xchat.prnt("Area Switch Mode - Town/Work")
		if townworkswitch is False:
			xchat.prnt("Area Switch Mode - Town/Forest")
		xchat.prnt("BlackBuy Spend Mode - {0}".format(blackbuyspend))
		xchat.prnt("BlackBuy 14 Spend Mode - {0}".format(blackbuyspend14))
		xchat.prnt("Buy Life Mode - {0}".format(buylife))
		xchat.prnt("Buy Luck Mode - {0}".format(buyluck))
		xchat.prnt("Buy Power Potion Mode - {0}".format(buypower))
		xchat.prnt("CreepAttack Mode - {0}".format(creepattack))
		xchat.prnt("Experience Buying Mode - {0}".format(expbuy))
		xchat.prnt("Fighting Mode - {0}".format(fightmode))
		xchat.prnt("GetGems Mode - {0}".format(getgems))
		xchat.prnt("Goldsave - {0}".format(goldsave))
		xchat.prnt("Interval Text Mode - {0}".format(intervaltext))
		xchat.prnt("Item Buy Level - {0}".format(setbuy))
		xchat.prnt("Player Character 1 - {0}, {1}.  Network {2}".format(char1, name, netname))
		xchat.prnt("Player Character 2 - {0}, {1}.  Network {2}".format(char2, name2, netname2))
		xchat.prnt("Player Character 3 - {0}, {1}.  Network {2}".format(char3, name3, netname3))
		xchat.prnt("Player Character 4 - {0}, {1}.  Network {2}".format(char4, name4, netname4))
		xchat.prnt("Scrolls Buy ItemScore - {0}".format(scrollssum))
		xchat.prnt("Set Creep Target - {0}".format(setcreeptarget))
		xchat.prnt("SlaySum Minimum - {0}".format(slaysum))
		xchat.prnt("XPSpend Upgrade Amount - {0}".format(xpspend))
		xchat.prnt("XPUpgrade Mode - {0}".format(xpupgrade))
		xchat.prnt("ZNC Mode - {0}".format(ZNC))
		xchat.prnt("ZNC2 Mode - {0}".format(ZNC2))
		xchat.prnt("ZNC3 Mode - {0}".format(ZNC3))
		xchat.prnt("ZNC4 Mode - {0}".format(ZNC4))
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("settings", settings, help="/settings - Gives a list of settings which you can change")

def newlister(num):
	global playerspagelist
	global playerspagelist2
	global playerspagelist3
	global playerspagelist4
	global newlist
	global newlist2
	global newlist3
	global newlist4
	global ability
	global python3
	global webworks
	global webworksB
	global webworksC
	global webworksD
	global charcount
	global website
	global website2
	global website3
	global website4
	global level
	global fightlevellimit
	global fightlevellimit2
	global fightlevellimit3
	global fightlevellimit4
	global netname
	global netname2
	global netname3
	global netname4
	
	test = []
	test2 = []
	test3 = []
	newlistererror = False

	if num == 1:
		newlist = []
		webworkslist = webworks
		playerspagelists = playerspagelist
		websites = website
		fightlevellimits = fightlevellimit
		netnames = netname
	if num == 2:
		newlist2 = []
		webworkslist = webworksB
		playerspagelists = playerspagelist2
		websites = website2
		fightlevellimits = fightlevellimit2
		netnames = netname2
	if num == 3:
		newlist3 = []
		webworkslist = webworksC
		playerspagelists = playerspagelist3
		websites = website3
		fightlevellimits = fightlevellimit3
		netnames = netname3
	if num == 4:
		newlist4 = []
		webworkslist = webworksD
		playerspagelists = playerspagelist4
		websites = website4
		fightlevellimits = fightlevellimit4
		netnames = netname4
	if charcount >= 2:
		getitems(num)

	if webworkslist is True:
		testnum = 0
		for entry in playerspagelists:
			if "playerview.php" in entry:
				testnum += 1
				test = entry
				testadd = True
				if "offline" in test:
					testadd = False
				if testadd is True:
					test = re.sub(r'<.*?>', ' ', test)
					test = test.split(" ")
					if testnum == 1:
						del test[0:14]
					test2.append(test)        

		if fightlevellimits is True:
			for entry in test2:
				if(int(entry[8]) >= level):
					test3.append(entry)
		if fightlevellimits is False:
			test3 = test2
		for player in test3:
			name_ = player[5]

			webworks2 = True
			weberror = False
			playerview20 = None
			playerlist20 = []

			# get raw player data from web, parse for relevant entry
			try:
				if "dalnet" in netnames.lower():
					context = ssl._create_unverified_context()
					if python3 is False:
						text = urllib2.urlopen(websites + "/playerview.php?player={0}".format(name_), context=context)
					if python3 is True:
						text = urllib.request.urlopen(websites + "/playerview.php?player={0}".format(name_), context=context)
				else:
					if python3 is False:
						text = urllib2.urlopen(websites + "/playerview.php?player={0}".format(name_))
					if python3 is True:
						text = urllib.request.urlopen(websites + "/playerview.php?player={0}".format(name_))
				playerview20 = text.read()
				text.close()
				if python3 is True:
					playerview20 = playerview20.decode("UTF-8")
			except:
				weberror = True
			if weberror is True:
				xchat.prnt( "Could not access {0}".format(websites))
				webworks2 = False

			# build list for player records
			if(playerview20 is None):
				xchat.prnt( "Could not access {0}, unknown error.".format(websites) )
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
		if num == 1:
			webworks = False
			xchat.prnt("Newlister Error 1")
		if num == 2:
			webworksB = False
			xchat.prnt("Newlister Error 2")
		if num == 3:
			webworksC = False
			xchat.prnt("Newlister Error 3")
		if num == 4:
			webworksD = False
			xchat.prnt("Newlister Error 4")

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
	global charcount
	
	global level
	global ttl
	global atime
	global stime
	global location
	global locationtime
	global location2
	global locationtime2
	global location3
	global locationtime3
	global location4
	global locationtime4

	global powerpots
	global fights
	global gold
	global gems
	global xp
	global mana
	global luck
	global upgradelevel
	global expertSum1
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
	global lottonuma1
	global lottonuma2
	global lottonuma3
	global lottonumb1
	global lottonumb2
	global lottonumb3
	global lottonumc1
	global lottonumc2
	global lottonumc3
	global lottonumd1
	global lottonumd2
	global lottonumd3
	global align
	global eatused
	
	if charcount >= 2:
		getitems(num)

	if num == 1:
		itemSums = itemSum
		attackslaySums = attackslaySum
		expertSums = expertSum
		ranks = rank
		locations = location
		locationtimes = locationtime
		lottonums1 = lottonuma1
		lottonums2 = lottonuma2
		lottonums3 = lottonuma3
	if num == 2:
		itemSums = itemSum2
		attackslaySums = attackslaySum2
		expertSums = expertSum2
		ranks = rank2
		locations = location2
		locationtimes = locationtime2
		lottonums1 = lottonumb1
		lottonums2 = lottonumb2
		lottonums3 = lottonumb3
	if num == 3:
		itemSums = itemSum3
		attackslaySums = attackslaySum3
		expertSums = expertSum3
		ranks = rank3
		locations = location3
		locationtimes = locationtime3
		lottonums1 = lottonumc1
		lottonums2 = lottonumc2
		lottonums3 = lottonumc3
	if num == 4:
		itemSums = itemSum4
		attackslaySums = attackslaySum4
		expertSums = expertSum4
		ranks = rank4
		locations = location4
		locationtimes = locationtime4
		lottonums1 = lottonumd1
		lottonums2 = lottonumd2
		lottonums3 = lottonumd3
		
	xchat.prnt("Rank: {0}".format(ranks))
	xchat.prnt("Location: {0}  Time: {1} secs".format(locations, locationtimes))
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
	xchat.prnt("Power Potions: {0}".format(powerpots))
	xchat.prnt("Luck Potion: {0}".format(luck))
	if(level >= 25):
		xchat.prnt("Fights: {0} of 5".format(fights))
	if(level < 25):
		xchat.prnt("Fights Start at Level 25")
	xchat.prnt("Gold: {0}".format(gold))
	xchat.prnt("XP: {0}".format(xp))
	xchat.prnt("Gems: {0}".format(gems))
	xchat.prnt("Lotto1: {0}  Lotto2: {1}  Lotto3: {2}".format(lottonums1, lottonums2, lottonums3))
	xchat.prnt("Life: {0}".format(life))
	xchat.prnt("Scrolls: {0} of 5".format(scrolls))
	xchat.prnt("Exp Used: {0} of 5".format(exp))
	xchat.prnt("Eat Used: {0} of 200".format(eatused))
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
	global charcount
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

	if charcount >= 2:
		getitems(num)

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
	xchat.prnt("Boots: {0}".format(boots))
	xchat.prnt("Charm: {0}".format(charm))
	xchat.prnt("Gloves: {0}".format(gloves))
	xchat.prnt("Helm: {0}".format(helm))
	xchat.prnt("Leggings: {0}".format(leggings))
	xchat.prnt("Ring: {0}".format(ring))
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
	global botname2
	global botname3
	global botname4
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
	global life2
	global life3
	global life4
	global level
	global level2
	global level3
	global level4
	global buylife
	global gameactive
	
	if gameactive is True:
		checknet = xchat.get_info("network")
		checknick = xchat.get_info("nick")
		if chanmessage is True:
			chanmessage = False
		    
		if char1 is True:
			if(checknet == netname and checknick == nickname):
				lifebuy = False
				if botname in word[0] and "has challenged" in word[1] and "is added to {0} clock".format(name) in word[1]: #rand challenge
					lifebuy = True
				if botname in word[0] and "has attacked a" in word[1] and "is added to {0} clock".format(name) in word[1]: #attack
					lifebuy = True
				if botname in word[0] and "tried to slay a" in word[1] and "is added to {0} clock".format(name) in word[1]: #slay
					lifebuy = True
				if botname in word[0] and "has been set upon by some" in word[1] and "is added to {0}'s clock".format(name) in word[1]: #rand creep
					lifebuy = True
				if botname in word[0] and "fights a random" in word[1] and "is added to {0} clock".format(name) in word[1]: #rand god
					lifebuy = True
				if botname in word[0] and "{0}".format(name) in word[1] and "have hunted down a bunch of" in word[1] and "but they beat them badly!" in word[1]: #team hunt
					lifebuy = True
				if botname in word[0] and "from {0}!".format(name) in word[1] and "XP and loses" in word[1]: #tourney
					lifebuy = True
				if lifebuy is True:
					if(level >= 15 and buylife is True and life >= 0):
						usecommand("buy life", 1)
						life = 100
		if char2 is True:
			if(checknet == netname2 and checknick == nickname2):
				lifebuyb = False
				if botname2 in word[0] and "has challenged" in word[1] and "is added to {0} clock".format(name2) in word[1]:
					lifebuyb = True
				if botname2 in word[0] and "has attacked a" in word[1] and "is added to {0} clock".format(name2) in word[1]:
					lifebuyb = True
				if botname2 in word[0] and "tried to slay a" in word[1] and "is added to {0} clock".format(name2) in word[1]:
					lifebuyb = True
				if botname2 in word[0] and "has been set upon by some" in word[1] and "is added to {0}'s clock".format(name2) in word[1]: #rand creep
					lifebuyb = True
				if botname2 in word[0] and "fights a random" in word[1] and "is added to {0} clock".format(name2) in word[1]: #rand god
					lifebuyb = True
				if botname2 in word[0] and "{0}".format(name2) in word[1] and "have hunted down a bunch of" in word[1] and "but they beat them badly!" in word[1]: #team hunt
					lifebuyb = True
				if botname2 in word[0] and "from {0}!".format(name2) in word[1] and "XP and loses" in word[1]:
					lifebuyb = True
				if lifebuyb is True:
					if(level2 >= 15 and buylife is True and life2 >= 0):
						usecommand("buy life", 2)
						life2 = 100
		if char3 is True:
			if(checknet == netname3 and checknick == nickname3):
				lifebuyc = False
				if botname3 in word[0] and "has challenged" in word[1] and "is added to {0} clock".format(name3) in word[1]:
					lifebuyc = True
				if botname3 in word[0] and "has attacked a" in word[1] and "is added to {0} clock".format(name3) in word[1]:
					lifebuyc = True
				if botname3 in word[0] and "tried to slay a" in word[1] and "is added to {0} clock".format(name3) in word[1]:
					lifebuyc = True
				if botname3 in word[0] and "has been set upon by some" in word[1] and "is added to {0}'s clock".format(name3) in word[1]: #rand creep
					lifebuyc = True
				if botname3 in word[0] and "fights a random" in word[1] and "is added to {0} clock".format(name3) in word[1]: #rand god
					lifebuyc = True
				if botname3 in word[0] and "{0}".format(name3) in word[1] and "have hunted down a bunch of" in word[1] and "but they beat them badly!" in word[1]: #team hunt
					lifebuyc = True
				if botname3 in word[0] and "from {0}!".format(name3) in word[1] and "XP and loses" in word[1]:
					lifebuyc = True
				if lifebuyc is True:
					if(level3 >= 15 and buylife is True and life3 >= 0):
						usecommand("buy life", 3)
						life3 = 100
		if char4 is True:
			if(checknet == netname4 and checknick == nickname4):
				lifebuyd = False
				if botname4 in word[0] and "has challenged" in word[1] and "is added to {0} clock".format(name4) in word[1]:
					lifebuyd = True
				if botname4 in word[0] and "has attacked a" in word[1] and "is added to {0} clock".format(name4) in word[1]:
					lifebuyd = True
				if botname4 in word[0] and "tried to slay a" in word[1] and "is added to {0} clock".format(name4) in word[1]:
					lifebuyd = True
				if botname4 in word[0] and "has been set upon by some" in word[1] and "is added to {0}'s clock".format(name4) in word[1]: #rand creep
					lifebuyd = True
				if botname4 in word[0] and "fights a random" in word[1] and "is added to {0} clock".format(name4) in word[1]: #rand god
					lifebuyd = True
				if botname4 in word[0] and "{0}".format(name4) in word[1] and "have hunted down a bunch of" in word[1] and "but they beat them badly!" in word[1]: #team hunt
					lifebuyd = True
				if botname4 in word[0] and "from {0}!".format(name4) in word[1] and "XP and loses" in word[1]:
					lifebuyd = True
				if lifebuyd is True:
					if(level4 >= 15 and buylife is True and life4 >= 0):
						usecommand("buy life", 4)
						life4 = 100

def private_cb(word, word_eol, userdata):
	global botname
	global botname2
	global botname3
	global botname4
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
			if(word[0] == botname2 and "You are not logged in." in word[1]):                
				if(checknet == netname2 and checknick == nickname2):
					usecommand("login {0} {1}".format(name2, pswd2), 2)
					interval = 60
					hookmain()
		if char3 is True:
			if(word[0] == botname3 and "You are not logged in." in word[1]):                
				if(checknet == netname3 and checknick == nickname3):
					usecommand("login {0} {1}".format(name3, pswd3), 3)
					interval = 60
					hookmain()
		if char4 is True:
			if(word[0] == botname4 and "You are not logged in." in word[1]):                
				if(checknet == netname4 and checknick == nickname4):
					usecommand("login {0} {1}".format(name4, pswd4), 4)
					interval = 60
					hookmain()

def webdata2(num):
	global playerlist
	global playerlist2
	global playerlist3
	global playerlist4
	global name
	global name2
	global name3
	global name4
	global webworks
	global webworksB
	global webworksC
	global webworksD
	global playerview
	global playerview2
	global playerview3
	global playerview4
	global python3
	global playerspage
	global playerspagelist
	global website
	global playerspage2
	global playerspagelist2
	global website2
	global playerspage3
	global playerspagelist3
	global website3
	global playerspage4
	global playerspagelist4
	global website4
	global netname
	global netname2
	global netname3
	global netname4
	
	webworks = True
	webworksB = True
	webworksC = True
	webworksD = True
	weberror = False
	context = ssl._create_unverified_context()

	if num == 1:
		websites = website
		names = name
		netnames = netname
	if num == 2:
		websites = website2
		names = name2
		netnames = netname2
	if num == 3:
		websites = website3
		names = name3
		netnames = netname3
	if num == 4:
		websites = website4
		names = name4
		netnames = netname4
	# get raw player data from web, parse for relevant entry
	if python3 is False:
		try:
			if "dalnet" in netnames.lower():
				text = urllib2.urlopen(websites + "/playerview.php?player={0}".format(names), context=context)
			else:
				text = urllib2.urlopen(websites + "/playerview.php?player={0}".format(names))
			if num == 1:
				playerview = text.read()
			if num == 2:
				playerview2 = text.read()
			if num == 3:
				playerview3 = text.read()
			if num == 4:
				playerview4 = text.read()
			text.close()
			if "dalnet" in netnames.lower():
				text2 = urllib2.urlopen(websites + "/players.php", context=context)
			else:
				text2 = urllib2.urlopen(websites + "/players.php")
			if num == 1:
				playerspage = text2.read()
			if num == 2:
				playerspage2 = text2.read()
			if num == 3:
				playerspage3 = text2.read()
			if num == 4:
				playerspage4 = text2.read()
			text2.close()
		except:
			weberror = True
	if python3 is True:
		try:
			if "dalnet" in netnames.lower():
				text = urllib.request.urlopen(websites + "/playerview.php?player={0}".format(names), context=context)
			else:
				text = urllib.request.urlopen(websites + "/playerview.php?player={0}".format(names))
			if num == 1:
				playerview = text.read()
				text.close()
				playerview = playerview.decode("UTF-8")
				if "dalnet" in netnames.lower():
					text2 = urllib.request.urlopen(websites + "/players.php", context=context)
				else:
					text2 = urllib.request.urlopen(websites + "/players.php")
				playerspage = text2.read()
				text2.close()
				playerspage = playerspage.decode("UTF-8")
			if num == 2:
				playerview2 = text.read()
				text.close()
				playerview2 = playerview2.decode("UTF-8")
				if "dalnet" in netnames.lower():
					text2 = urllib.request.urlopen(websites + "/players.php", context=context)
				else:
					text2 = urllib.request.urlopen(websites + "/players.php")
				playerspage2 = text2.read()
				text2.close()
				playerspage2 = playerspage2.decode("UTF-8")
			if num == 3:
				playerview3 = text.read()
				text.close()
				playerview3 = playerview3.decode("UTF-8")
				if "dalnet" in netnames.lower():
					text2 = urllib.request.urlopen(websites + "/players.php", context=context)
				else:
					text2 = urllib.request.urlopen(websites + "/players.php")
				playerspage3 = text2.read()
				text2.close()
				playerspage3 = playerspage3.decode("UTF-8")
			if num == 4:
				playerview4 = text.read()
				text.close()
				playerview4 = playerview4.decode("UTF-8")
				if "dalnet" in netnames.lower():
					text2 = urllib.request.urlopen(websites + "/players.php", context=context)
				else:
					text2 = urllib.request.urlopen(websites + "/players.php")
				playerspage4 = text2.read()
				text2.close()
				playerspage4 = playerspage4.decode("UTF-8")
		except:
			weberror = True

	if weberror is True:
		xchat.prnt( "Could not access {0}".format(websites))
		if num == 1:
			webworks = False
		if num == 2:
			webworksB = False
		if num == 3:
			webworksC = False
		if num == 4:
			webworksD = False

	# build list for player records
	if num == 1:
		if(playerview is None):
			xchat.prnt( "Could not access {0}, unknown error.".format(website) )
			webworks = False
		else:
			playerlist = playerview.split("\n")
			playerlist = playerlist[:-1]
		if(playerspage is None):
			xchat.prnt( "Could not access {0}, unknown error.".format(website) )
			webworks = False
		else:
			playerspagelist = playerspage.split("\n")
			playerspagelist = playerspagelist[:-1]
	if num == 2:
		if(playerview2 is None):
			xchat.prnt( "Could not access {0}, unknown error.".format(website2) )
			webworksB = False
		else:
			playerlist2 = playerview2.split("\n")
			playerlist2 = playerlist2[:-1]
		if(playerspage2 is None):
			xchat.prnt( "Could not access {0}, unknown error.".format(website2) )
			webworksB = False
		else:
			playerspagelist2 = playerspage2.split("\n")
			playerspagelist2 = playerspagelist2[:-1]
	if num == 3:
		if(playerview3 is None):
			xchat.prnt( "Could not access {0}, unknown error.".format(website3) )
			webworksC = False
		else:
			playerlist3 = playerview3.split("\n")
			playerlist3 = playerlist3[:-1]
		if(playerspage3 is None):
			xchat.prnt( "Could not access {0}, unknown error.".format(website3) )
			webworksC = False
		else:
			playerspagelist3 = playerspage3.split("\n")
			playerspagelist3 = playerspagelist3[:-1]
	if num == 4:
		if(playerview4 is None):
			xchat.prnt( "Could not access {0}, unknown error.".format(website4) )
			webworksD = False
		else:
			playerlist4 = playerview4.split("\n")
			playerlist4 = playerlist4[:-1]
		if(playerspage4 is None):
			xchat.prnt( "Could not access {0}, unknown error.".format(website4) )
			webworksD = False
		else:
			playerspagelist4 = playerspage4.split("\n")
			playerspagelist4 = playerspagelist4[:-1]

def playerarea(num):
	global playerlist
	global playerlist2
	global playerlist3
	global playerlist4
	global level
	global mysum
	global webworks
	global webworksB
	global webworksC
	global webworksD
	global charcount
	global location
	global locationtime
	global location2
	global locationtime2
	global location3
	global locationtime3
	global location4
	global locationtime4
	global townworkswitch
	
	if charcount >= 2:
		getitems(num)
	
	playeris = None

	atwork = False
	intown = False
	intheforest = False
	worktext = None
	towntext = None
	foresttext = None
	
	if num == 1:
		location = None
		locationtime = 0
		playerlists = playerlist
		webworkslist = webworks
	if num == 2:
		location2 = None
		locationtime2 = 0
		playerlists = playerlist2
		webworkslist = webworksB
	if num == 3:
		location3 = None
		locationtime3 = 0
		playerlists = playerlist3
		webworkslist = webworksC
	if num == 4:
		location4 = None
		locationtime4 = 0
		playerlists = playerlist4
		webworkslist = webworksD

	if webworkslist is True:
		for entry in playerlists:
			if "Player is:" in entry:
				playeris = entry
			if "Work Time:" in entry:
				worktext = entry
			if "Town Time:" in entry:
				towntext = entry
			if "Forest Time:" in entry:
				foresttext = entry
				
		if "at work" in playeris:
			atwork = True
		if "in town" in playeris:
			intown = True
		if "in the forest" in playeris:
			intheforest = True

	if townworkswitch is True:
		area = "work"
	if townworkswitch is False:
		area = "forest"

	if atwork is True:
		try:
			worktext = worktext.split(" ")
			workdays = int(worktext[8])
			worksplittime = worktext[10]
			worksplittime = worksplittime.strip("<br")
			if num == 1:
				locationtime = timetosecs(workdays, worksplittime)
				location = "At Work"
			if num == 2:
				locationtime2 = timetosecs(workdays, worksplittime)
				location2 = "At Work"
			if num == 3:
				locationtime3 = timetosecs(workdays, worksplittime)
				location3 = "At Work"
			if num == 4:
				locationtime4 = timetosecs(workdays, worksplittime)
				location4 = "At Work"
		except ValueError:
			usecommand("goto town", num)
	if intown is True:
		try:
			towntext = towntext.split(" ")
			towndays = int(towntext[8])
			townsplittime = towntext[10]
			townsplittime = townsplittime.strip("<br")
			if num == 1:
				locationtime = timetosecs(towndays, townsplittime)
				location = "In Town"
			if num == 2:
				locationtime2 = timetosecs(towndays, townsplittime)
				location2 = "In Town"
			if num == 3:
				locationtime3 = timetosecs(towndays, townsplittime)
				location3 = "In Town"
			if num == 4:
				locationtime4 = timetosecs(towndays, townsplittime)
				location4 = "In Town"
		except ValueError:
			usecommand("goto {0}".format(area), num)
	if intheforest is True:
		try:
			foresttext = foresttext.split(" ")
			forestdays = int(foresttext[8])
			forestsplittime = foresttext[10]
			forestsplittime = forestsplittime.strip("<br")
			if num == 1:
				locationtime = timetosecs(forestdays, forestsplittime)
				location = "In The Forest"
			if num == 2:
				locationtime2 = timetosecs(forestdays, forestsplittime)
				location2 = "In The Forest"
			if num == 3:
				locationtime3 = timetosecs(forestdays, forestsplittime)
				location3 = "In The Forest"
			if num == 4:
				locationtime4 = timetosecs(forestdays, forestsplittime)
				location4 = "In The Forest"
		except ValueError:
			usecommand("goto town", num)

	if num == 1:
		locations = location
		locationtimes = locationtime
	if num == 2:
		locations = location2
		locationtimes = locationtime2
	if num == 3:
		locations = location3
		locationtimes = locationtime3
	if num == 4:
		locations = location4
		locationtimes = locationtime4
		
#	xchat.prnt("{0} {1} Time: {2} seconds".format(num, locations, locationtimes))

	if (level <= 25):
		mintime = (3 * 60 * 60)
	if (level > 25 and level <= 40):
		mintime = (6 * 60 * 60)
	if (level > 40 and level <= 50):
		mintime = (12 * 60 * 60)
	if (level > 50):
		mintime = (24 * 60 * 60)

	if(intown is True and locationtimes >= mintime and mysum < 6000 and mysum != 0):
		usecommand("goto {0}".format(area), num)
	if(intown is True and mysum >= 6000):
		usecommand("goto {0}".format(area), num)
	if(atwork is True and locationtimes >= mintime):
		usecommand("goto town", num)
	if(intheforest is True and locationtimes >= (24 * 60 * 60)):
		usecommand("goto town", num)
       
def getvariables():
	global level
	global ttl
	global level2
	global level3
	global level4

	global ring
	global amulet
	global charm
	global weapon
	global helm
	global tunic
	global gloves
	global leggings
	global shield
	global boots

	global mysum
	global gold
	global upgradelevel
	global gems
	global ability
	global xp
	global life
	global fights
	global life2
	global fights2
	global life3
	global fights3
	global life4
	global fights4
	global scrolls
	global exp
	global luck
	global mana
	global powerpots
	global align
	global eatused

	global stone1
	global stone2
	global stone3
	global stoneb1
	global stoneb2
	global stoneb3
	global stonec1
	global stonec2
	global stonec3
	global stoned1
	global stoned2
	global stoned3
	global expert1
	global expert2
	global expert3

	global atime
	global stime
	global playerlist
	global playerlist2
	global playerlist3
	global playerlist4
	global webworks
	global webworksB
	global webworksC
	global webworksD
	global itemslist
	global char1
	global char2
	global char3
	global char4
	global lottonuma1
	global lottonuma2
	global lottonuma3
	global lottonumb1
	global lottonumb2
	global lottonumb3
	global lottonumc1
	global lottonumc2
	global lottonumc3
	global lottonumd1
	global lottonumd2
	global lottonumd3

	itemslist = []
	ttl2 = 0
	mysum2 = 0
	ring2 = 0
	amulet2 = 0
	charm2 = 0
	weapon2 = 0
	helm2 = 0
	tunic2 = 0
	gloves2 = 0
	leggings2 = 0
	shield2 = 0
	boots2 = 0
	ttl3 = 0
	mysum3 = 0
	ring3 = 0
	amulet3 = 0
	charm3 = 0
	weapon3 = 0
	helm3 = 0
	tunic3 = 0
	gloves3 = 0
	leggings3 = 0
	shield3 = 0
	boots3 = 0
	ttl4 = 0
	mysum4 = 0
	ring4 = 0
	amulet4 = 0
	charm4 = 0
	weapon4 = 0
	helm4 = 0
	tunic4 = 0
	gloves4 = 0
	leggings4 = 0
	shield4 = 0
	boots4 = 0

	gold2 = 0
	upgradelevel2 = 0
	gems2 = 0
	ability2 = None
	xp2 = 0
	scrolls2 = 0
	exp2 = 0
	luck2 = 0
	mana2 = 0 
	powerpots2 = 0
	align2 = None
	gold3 = 0
	upgradelevel3 = 0
	gems3 = 0
	ability3 = None
	xp3 = 0
	scrolls3 = 0
	exp3 = 0
	luck3 = 0
	mana3 = 0 
	powerpots3 = 0
	align3 = None
	gold4 = 0
	upgradelevel4 = 0
	gems4 = 0
	ability4 = None
	xp4 = 0
	scrolls4 = 0
	exp4 = 0
	luck4 = 0
	mana4 = 0 
	powerpots4 = 0
	align4 = None
	eatused2 = 0
	eatused3 = 0
	eatused4 = 0

	expertb1 = None
	expertb2 = None
	expertb3 = None
	expertc1 = None
	expertc2 = None
	expertc3 = None
	expertd1 = None
	expertd2 = None
	expertd3 = None

	atime2 = 0
	stime2 = 0
	atime3 = 0
	stime3 = 0
	atime4 = 0
	stime4 = 0
	
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
	lucktext = None
	powerpotstext = None
	manatext = None
	atimetext = None
	ctimetext = None
	eatusedtext = None
	
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

	if webworks is True:
		if char1 is True and playerlist != None:
			for entry in playerlist:
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
				if "Eat Used:" in entry:
					eatusedtext = entry
				if "Power Potion:" in entry:
					powerpotstext = entry
				if "Mana Potion:" in entry:
					manatext = entry
				if "Luck Potion:" in entry:
					lucktext = entry
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

			try:
				try:
					if "Neutral" in aligntext:
						align = "n"
					if "Evil" in aligntext:
						align = "e"
					if "Good" in aligntext:
						align = "g"
				except TypeError:
					align = "n"
				leveltext = leveltext.split(" ")
				levelsplit = leveltext[7]
				level = int(levelsplit.strip("<br"))
				ttltext = ttltext.split(" ")
				daystext = int(ttltext[8])
				timetext = ttltext[10].strip("<br")
				ttl = timetosecs(daystext, timetext)
				goldtext = goldtext.split(" ")
				goldsplit = goldtext[7]
				gold = int(goldsplit.strip("<br"))
				gemstext = gemstext.split(" ")
				gemssplit = gemstext[7]
				gems = int(gemssplit.strip("<br"))
				upgradetext = upgradetext.split(" ")
				upgradesplit = upgradetext[8]
				upgradelevel = int(upgradesplit.strip("<br"))

				if "Barbarian" in abilitytext:
					ability = "b"
				if "Rogue" in abilitytext:
					ability = "r"
				if "Paladin" in abilitytext:
					ability = "p"
				if "Wizard" in abilitytext:
					ability = "w"

				xptext = xptext.split(" ")
				xpsplit = xptext[7]
				xp = int(xpsplit.strip("<br"))
				exptext = exptext.split(" ")
				expsplit = exptext[8]
				expsplit = expsplit.split("/")
				try:
					exp = int(expsplit[0])
				except:
					exp = 0
				lifetext = lifetext.split(" ")
				lifesplit = lifetext[7]
				life = int(lifesplit.strip("<br"))
				scrollstext = scrollstext.split(" ")
				scrollssplit = scrollstext[8]
				scrollssplit = scrollssplit.split("/")
				try:
					scrolls = int(scrollssplit[0])
				except ValueError:
					scrolls = 0
				eatusedtext = eatusedtext.split(" ")
				eatusedsplit = eatusedtext[8]
				eatusedsplit = eatusedsplit.split("/")
				try:
					eatused = int(eatusedsplit[0])
				except ValueError:
					eatused = 0
				powerpotstext = powerpotstext.split(" ")
				powerpotssplit = powerpotstext[8]
				powerpotssplit = powerpotssplit.split("/")
				powerpots = int(powerpotssplit[0])
				manatext = manatext.split(" ")
				manasplit = manatext[8]
				manasplit = manasplit.split("/")
				mana = int(manasplit[0])
				lucktext = lucktext.split(" ")
				lucksplit = lucktext[8]
				lucksplit = lucksplit.split("/")
				luck = int(lucksplit[0])

				try:
					atimetext = atimetext.split(" ")
					daystext = int(atimetext[9])
					timetext = atimetext[11].strip("<br")
					atime = timetosecs(daystext, timetext)
				except ValueError:
					atime = 0
				try:
					stimetext = stimetext.split(" ")
					daystext = int(stimetext[9])
					timetext = stimetext[11].strip("<br")
					stime = timetosecs(daystext, timetext)
				except ValueError:
					stime = 0

				amulettext = amulettext.split(" ")
				amuletsplit = amulettext[7]
				amulet = int(amuletsplit.strip("<br"))
				bootstext = bootstext.split(" ")
				bootssplit = bootstext[7]
				boots = int(bootssplit.strip("<br"))
				charmtext = charmtext.split(" ")
				charmsplit = charmtext[7]
				charm = int(charmsplit.strip("<br"))
				glovestext = glovestext.split(" ")
				glovessplit = glovestext[7]
				gloves = int(glovessplit.strip("<br"))
				helmtext = helmtext.split(" ")
				helmsplit = helmtext[7]
				helm = int(helmsplit.strip("<br"))
				leggingstext = leggingstext.split(" ")
				leggingssplit = leggingstext[7]
				leggings = int(leggingssplit.strip("<br"))
				ringtext = ringtext.split(" ")
				ringsplit = ringtext[7]
				ring = int(ringsplit.strip("<br"))
				shieldtext = shieldtext.split(" ")
				shieldsplit = shieldtext[7]
				shield = int(shieldsplit.strip("<br"))
				tunictext = tunictext.split(" ")
				tunicsplit = tunictext[7]
				tunic = int(tunicsplit.strip("<br"))
				weapontext = weapontext.split(" ")
				weaponsplit = weapontext[7]
				weapon = int(weaponsplit.strip("<br"))

				sumtext = sumtext.split(" ")
				sumsplit = sumtext[7]
				mysum = int(sumsplit.strip("<br"))
				experttext1 = experttext1.split(" ")
				expertsplit1 = experttext1[8]
				expertsplitsplit1 = expertsplit1.split("<")
				expert1 = expertsplitsplit1[0]
				experttext2 = experttext2.split(" ")
				expertsplit2 = experttext2[8]
				expertsplitsplit2 = expertsplit2.split("<")
				expert2 = expertsplitsplit2[0]
				experttext3 = experttext3.split(" ")
				expertsplit3 = experttext3[8]
				expertsplitsplit3 = expertsplit3.split("<")
				expert3 = expertsplitsplit3[0]
				stonetext1 = stonetext1.split(" ")
				stonesplit1 = stonetext1[8]
				stonesplitsplit1 = stonesplit1.split("<")
				stone1 = stonesplitsplit1[0]
				stonetext2 = stonetext2.split(" ")
				stonesplit2 = stonetext2[8]
				stonesplitsplit2 = stonesplit2.split("<")
				stone2 = stonesplitsplit2[0]
				stonetext3 = stonetext3.split(" ")
				stonesplit3 = stonetext3[8]
				stonesplitsplit3 = stonesplit3.split("<")
				stone3 = stonesplitsplit3[0]
				fightstext = fightstext.split(" ")
				fightssplit = fightstext[13]
				fights = int(fightssplit.strip("<br"))
				lottonumtext1 = re.sub(r'<.*?>', ' ', lottonumtext1)
				lottonumtext1 = lottonumtext1.split(" ")
				lottonumtext2 = re.sub(r'<.*?>', ' ', lottonumtext2)
				lottonumtext2 = lottonumtext2.split(" ")
				lottonumtext3 = re.sub(r'<.*?>', ' ', lottonumtext3)
				lottonumtext3 = lottonumtext3.split(" ")
				lottonuma1 = "{0} {1} and {2}".format(lottonumtext1[11], lottonumtext1[12], lottonumtext1[13])                        
				lottonuma2 = "{0} {1} and {2}".format(lottonumtext2[11], lottonumtext2[12], lottonumtext2[13])                        
				lottonuma3 = "{0} {1} and {2}".format(lottonumtext3[11], lottonumtext3[12], lottonumtext3[13])                        
			except:
				webworks = False
				xchat.prnt("1 Variable Error")

	if webworksB is True:
		if char2 is True and playerlist2 != None:
			for entry in playerlist2:
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
				if "Eat Used:" in entry:
					eatusedtext = entry
				if "Power Potion:" in entry:
					powerpotstext = entry
				if "Mana Potion:" in entry:
					manatext = entry
				if "Luck Potion:" in entry:
					lucktext = entry
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

			try:
				try:
					if "Neutral" in aligntext:
						align2 = "n"
					if "Evil" in aligntext:
						align2 = "e"
					if "Good" in aligntext:
						align2 = "g"
				except TypeError:
					align2 = "n"
				leveltext = leveltext.split(" ")
				levelsplit = leveltext[7]
				level2 = int(levelsplit.strip("<br"))
				ttltext = ttltext.split(" ")
				daystext = int(ttltext[8])
				timetext = ttltext[10].strip("<br")
				ttl2 = timetosecs(daystext, timetext)
				goldtext = goldtext.split(" ")
				goldsplit = goldtext[7]
				gold2 = int(goldsplit.strip("<br"))
				gemstext = gemstext.split(" ")
				gemssplit = gemstext[7]
				gems2 = int(gemssplit.strip("<br"))
				upgradetext = upgradetext.split(" ")
				upgradesplit = upgradetext[8]
				upgradelevel2 = int(upgradesplit.strip("<br"))

				if "Barbarian" in abilitytext:
					ability2 = "b"
				if "Rogue" in abilitytext:
					ability2 = "r"
				if "Paladin" in abilitytext:
					ability2 = "p"
				if "Wizard" in abilitytext:
					ability2 = "w"

				xptext = xptext.split(" ")
				xpsplit = xptext[7]
				xp2 = int(xpsplit.strip("<br"))
				exptext = exptext.split(" ")
				expsplit = exptext[8]
				expsplit = expsplit.split("/")
				try:
					exp2 = int(expsplit[0])
				except:
					exp2 = 0
				lifetext = lifetext.split(" ")
				lifesplit = lifetext[7]
				life2 = int(lifesplit.strip("<br"))
				scrollstext = scrollstext.split(" ")
				scrollssplit = scrollstext[8]
				scrollssplit = scrollssplit.split("/")
				try:
					scrolls2 = int(scrollssplit[0])
				except ValueError:
					scrolls2 = 0
				eatusedtext = eatusedtext.split(" ")
				eatusedsplit = eatusedtext[8]
				eatusedsplit = eatusedsplit.split("/")
				try:
					eatused2 = int(eatusedsplit[0])
				except ValueError:
					eatused2 = 0
				powerpotstext = powerpotstext.split(" ")
				powerpotssplit = powerpotstext[8]
				powerpotssplit = powerpotssplit.split("/")
				powerpots2 = int(powerpotssplit[0])
				manatext = manatext.split(" ")
				manasplit = manatext[8]
				manasplit = manasplit.split("/")
				mana2 = int(manasplit[0])
				lucktext = lucktext.split(" ")
				lucksplit = lucktext[8]
				lucksplit = lucksplit.split("/")
				luck2 = int(lucksplit[0])

				try:
					atimetext = atimetext.split(" ")
					daystext = int(atimetext[9])
					timetext = atimetext[11].strip("<br")
					atime2 = timetosecs(daystext, timetext)
				except ValueError:
					atime2 = 0
				try:
					stimetext = stimetext.split(" ")
					daystext = int(stimetext[9])
					timetext = stimetext[11].strip("<br")
					stime2 = timetosecs(daystext, timetext)
				except ValueError:
					stime2 = 0

				amulettext = amulettext.split(" ")
				amuletsplit = amulettext[7]
				amulet2 = int(amuletsplit.strip("<br"))
				bootstext = bootstext.split(" ")
				bootssplit = bootstext[7]
				boots2 = int(bootssplit.strip("<br"))
				charmtext = charmtext.split(" ")
				charmsplit = charmtext[7]
				charm2 = int(charmsplit.strip("<br"))
				glovestext = glovestext.split(" ")
				glovessplit = glovestext[7]
				gloves2 = int(glovessplit.strip("<br"))
				helmtext = helmtext.split(" ")
				helmsplit = helmtext[7]
				helm2 = int(helmsplit.strip("<br"))
				leggingstext = leggingstext.split(" ")
				leggingssplit = leggingstext[7]
				leggings2 = int(leggingssplit.strip("<br"))
				ringtext = ringtext.split(" ")
				ringsplit = ringtext[7]
				ring2 = int(ringsplit.strip("<br"))
				shieldtext = shieldtext.split(" ")
				shieldsplit = shieldtext[7]
				shield2 = int(shieldsplit.strip("<br"))
				tunictext = tunictext.split(" ")
				tunicsplit = tunictext[7]
				tunic2 = int(tunicsplit.strip("<br"))
				weapontext = weapontext.split(" ")
				weaponsplit = weapontext[7]
				weapon2 = int(weaponsplit.strip("<br"))

				sumtext = sumtext.split(" ")
				sumsplit = sumtext[7]
				mysum2 = int(sumsplit.strip("<br"))
				experttext1 = experttext1.split(" ")
				expertsplit1 = experttext1[8]
				expertsplitsplit1 = expertsplit1.split("<")
				expertb1 = expertsplitsplit1[0]
				experttext2 = experttext2.split(" ")
				expertsplit2 = experttext2[8]
				expertsplitsplit2 = expertsplit2.split("<")
				expertb2 = expertsplitsplit2[0]
				experttext3 = experttext3.split(" ")
				expertsplit3 = experttext3[8]
				expertsplitsplit3 = expertsplit3.split("<")
				expertb3 = expertsplitsplit3[0]
				stonetext1 = stonetext1.split(" ")
				stonesplit1 = stonetext1[8]
				stonesplitsplit1 = stonesplit1.split("<")
				stoneb1 = stonesplitsplit1[0]
				stonetext2 = stonetext2.split(" ")
				stonesplit2 = stonetext2[8]
				stonesplitsplit2 = stonesplit2.split("<")
				stoneb2 = stonesplitsplit2[0]
				stonetext3 = stonetext3.split(" ")
				stonesplit3 = stonetext3[8]
				stonesplitsplit3 = stonesplit3.split("<")
				stoneb3 = stonesplitsplit3[0]
				fightstext = fightstext.split(" ")
				fightssplit = fightstext[13]
				fights2 = int(fightssplit.strip("<br"))
				lottonumtext1 = re.sub(r'<.*?>', ' ', lottonumtext1)
				lottonumtext1 = lottonumtext1.split(" ")
				lottonumtext2 = re.sub(r'<.*?>', ' ', lottonumtext2)
				lottonumtext2 = lottonumtext2.split(" ")
				lottonumtext3 = re.sub(r'<.*?>', ' ', lottonumtext3)
				lottonumtext3 = lottonumtext3.split(" ")
				lottonumb1 = "{0} {1} and {2}".format(lottonumtext1[11], lottonumtext1[12], lottonumtext1[13])                        
				lottonumb2 = "{0} {1} and {2}".format(lottonumtext2[11], lottonumtext2[12], lottonumtext2[13])                        
				lottonumb3 = "{0} {1} and {2}".format(lottonumtext3[11], lottonumtext3[12], lottonumtext3[13])                        
			except:
				webworksB = False
				xchat.prnt("2 Variable Error")

	if webworksC is True:
		if char3 is True and playerlist3 != None:
			for entry in playerlist3:
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
				if "Eat Used:" in entry:
					eatusedtext = entry
				if "Power Potion:" in entry:
					powerpotstext = entry
				if "Mana Potion:" in entry:
					manatext = entry
				if "Luck Potion:" in entry:
					lucktext = entry
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

			try:
				try:
					if "Neutral" in aligntext:
						align3 = "n"
					if "Evil" in aligntext:
						align3 = "e"
					if "Good" in aligntext:
						align3 = "g"
				except TypeError:
					align3 = "n"
				leveltext = leveltext.split(" ")
				levelsplit = leveltext[7]
				level3 = int(levelsplit.strip("<br"))
				ttltext = ttltext.split(" ")
				daystext = int(ttltext[8])
				timetext = ttltext[10].strip("<br")
				ttl3 = timetosecs(daystext, timetext)
				goldtext = goldtext.split(" ")
				goldsplit = goldtext[7]
				gold3 = int(goldsplit.strip("<br"))
				gemstext = gemstext.split(" ")
				gemssplit = gemstext[7]
				gems3 = int(gemssplit.strip("<br"))
				upgradetext = upgradetext.split(" ")
				upgradesplit = upgradetext[8]
				upgradelevel3 = int(upgradesplit.strip("<br"))

				if "Barbarian" in abilitytext:
					ability3 = "b"
				if "Rogue" in abilitytext:
					ability3 = "r"
				if "Paladin" in abilitytext:
					ability3 = "p"
				if "Wizard" in abilitytext:
					ability3 = "w"

				xptext = xptext.split(" ")
				xpsplit = xptext[7]
				xp3 = int(xpsplit.strip("<br"))
				exptext = exptext.split(" ")
				expsplit = exptext[8]
				expsplit = expsplit.split("/")
				try:
					exp3 = int(expsplit[0])
				except:
					exp3 = 0
				lifetext = lifetext.split(" ")
				lifesplit = lifetext[7]
				life3 = int(lifesplit.strip("<br"))
				scrollstext = scrollstext.split(" ")
				scrollssplit = scrollstext[8]
				scrollssplit = scrollssplit.split("/")
				try:
					scrolls3 = int(scrollssplit[0])
				except ValueError:
					scrolls3 = 0
				eatusedtext = eatusedtext.split(" ")
				eatusedsplit = eatusedtext[8]
				eatusedsplit = eatusedsplit.split("/")
				try:
					eatused3 = int(eatusedsplit[0])
				except ValueError:
					eatused3 = 0
				powerpotstext = powerpotstext.split(" ")
				powerpotssplit = powerpotstext[8]
				powerpotssplit = powerpotssplit.split("/")
				powerpots3 = int(powerpotssplit[0])
				manatext = manatext.split(" ")
				manasplit = manatext[8]
				manasplit = manasplit.split("/")
				mana3 = int(manasplit[0])
				lucktext = lucktext.split(" ")
				lucksplit = lucktext[8]
				lucksplit = lucksplit.split("/")
				luck3 = int(lucksplit[0])

				try:
					atimetext = atimetext.split(" ")
					daystext = int(atimetext[9])
					timetext = atimetext[11].strip("<br")
					atime3 = timetosecs(daystext, timetext)
				except ValueError:
					atime3 = 0
				try:
					stimetext = stimetext.split(" ")
					daystext = int(stimetext[9])
					timetext = stimetext[11].strip("<br")
					stime3 = timetosecs(daystext, timetext)
				except ValueError:
					stime3 = 0

				amulettext = amulettext.split(" ")
				amuletsplit = amulettext[7]
				amulet3 = int(amuletsplit.strip("<br"))
				bootstext = bootstext.split(" ")
				bootssplit = bootstext[7]
				boots3 = int(bootssplit.strip("<br"))
				charmtext = charmtext.split(" ")
				charmsplit = charmtext[7]
				charm3 = int(charmsplit.strip("<br"))
				glovestext = glovestext.split(" ")
				glovessplit = glovestext[7]
				gloves3 = int(glovessplit.strip("<br"))
				helmtext = helmtext.split(" ")
				helmsplit = helmtext[7]
				helm3 = int(helmsplit.strip("<br"))
				leggingstext = leggingstext.split(" ")
				leggingssplit = leggingstext[7]
				leggings3 = int(leggingssplit.strip("<br"))
				ringtext = ringtext.split(" ")
				ringsplit = ringtext[7]
				ring3 = int(ringsplit.strip("<br"))
				shieldtext = shieldtext.split(" ")
				shieldsplit = shieldtext[7]
				shield3 = int(shieldsplit.strip("<br"))
				tunictext = tunictext.split(" ")
				tunicsplit = tunictext[7]
				tunic3 = int(tunicsplit.strip("<br"))
				weapontext = weapontext.split(" ")
				weaponsplit = weapontext[7]
				weapon3 = int(weaponsplit.strip("<br"))

				sumtext = sumtext.split(" ")
				sumsplit = sumtext[7]
				mysum3 = int(sumsplit.strip("<br"))
				experttext1 = experttext1.split(" ")
				expertsplit1 = experttext1[8]
				expertsplitsplit1 = expertsplit1.split("<")
				expertc1 = expertsplitsplit1[0]
				experttext2 = experttext2.split(" ")
				expertsplit2 = experttext2[8]
				expertsplitsplit2 = expertsplit2.split("<")
				expertc2 = expertsplitsplit2[0]
				experttext3 = experttext3.split(" ")
				expertsplit3 = experttext3[8]
				expertsplitsplit3 = expertsplit3.split("<")
				expertc3 = expertsplitsplit3[0]
				stonetext1 = stonetext1.split(" ")
				stonesplit1 = stonetext1[8]
				stonesplitsplit1 = stonesplit1.split("<")
				stonec1 = stonesplitsplit1[0]
				stonetext2 = stonetext2.split(" ")
				stonesplit2 = stonetext2[8]
				stonesplitsplit2 = stonesplit2.split("<")
				stonec2 = stonesplitsplit2[0]
				stonetext3 = stonetext3.split(" ")
				stonesplit3 = stonetext3[8]
				stonesplitsplit3 = stonesplit3.split("<")
				stonec3 = stonesplitsplit3[0]
				fightstext = fightstext.split(" ")
				fightssplit = fightstext[13]
				fights3 = int(fightssplit.strip("<br"))
				lottonumtext1 = re.sub(r'<.*?>', ' ', lottonumtext1)
				lottonumtext1 = lottonumtext1.split(" ")
				lottonumtext2 = re.sub(r'<.*?>', ' ', lottonumtext2)
				lottonumtext2 = lottonumtext2.split(" ")
				lottonumtext3 = re.sub(r'<.*?>', ' ', lottonumtext3)
				lottonumtext3 = lottonumtext3.split(" ")
				lottonumc1 = "{0} {1} and {2}".format(lottonumtext1[11], lottonumtext1[12], lottonumtext1[13])                        
				lottonumc2 = "{0} {1} and {2}".format(lottonumtext2[11], lottonumtext2[12], lottonumtext2[13])                        
				lottonumc3 = "{0} {1} and {2}".format(lottonumtext3[11], lottonumtext3[12], lottonumtext3[13])                        
			except:
				webworksC = False
				xchat.prnt("3 Variable Error")

	if webworksD is True:
		if char4 is True and playerlist4 != None:
			for entry in playerlist4:
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
				if "Eat Used:" in entry:
					eatusedtext = entry
				if "Power Potion:" in entry:
					powerpotstext = entry
				if "Mana Potion:" in entry:
					manatext = entry
				if "Luck Potion:" in entry:
					lucktext = entry
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

			try:
				try:
					if "Neutral" in aligntext:
						align4 = "n"
					if "Evil" in aligntext:
						align4 = "e"
					if "Good" in aligntext:
						align4 = "g"
				except TypeError:
					align4 = "n"
				leveltext = leveltext.split(" ")
				levelsplit = leveltext[7]
				level4 = int(levelsplit.strip("<br"))
				ttltext = ttltext.split(" ")
				daystext = int(ttltext[8])
				timetext = ttltext[10].strip("<br")
				ttl4 = timetosecs(daystext, timetext)
				goldtext = goldtext.split(" ")
				goldsplit = goldtext[7]
				gold4 = int(goldsplit.strip("<br"))
				gemstext = gemstext.split(" ")
				gemssplit = gemstext[7]
				gems4 = int(gemssplit.strip("<br"))
				upgradetext = upgradetext.split(" ")
				upgradesplit = upgradetext[8]
				upgradelevel4 = int(upgradesplit.strip("<br"))

				if "Barbarian" in abilitytext:
					ability4 = "b"
				if "Rogue" in abilitytext:
					ability4 = "r"
				if "Paladin" in abilitytext:
					ability4 = "p"
				if "Wizard" in abilitytext:
					ability4 = "w"

				xptext = xptext.split(" ")
				xpsplit = xptext[7]
				xp4 = int(xpsplit.strip("<br"))
				exptext = exptext.split(" ")
				expsplit = exptext[8]
				expsplit = expsplit.split("/")
				try:
					exp4 = int(expsplit[0])
				except:
					exp4 = 0
				lifetext = lifetext.split(" ")
				lifesplit = lifetext[7]
				life4 = int(lifesplit.strip("<br"))
				scrollstext = scrollstext.split(" ")
				scrollssplit = scrollstext[8]
				scrollssplit = scrollssplit.split("/")
				try:
					scrolls4 = int(scrollssplit[0])
				except ValueError:
					scrolls4 = 0
				eatusedtext = eatusedtext.split(" ")
				eatusedsplit = eatusedtext[8]
				eatusedsplit = eatusedsplit.split("/")
				try:
					eatused4 = int(eatusedsplit[0])
				except ValueError:
					eatused4 = 0
				powerpotstext = powerpotstext.split(" ")
				powerpotssplit = powerpotstext[8]
				powerpotssplit = powerpotssplit.split("/")
				powerpots4 = int(powerpotssplit[0])
				manatext = manatext.split(" ")
				manasplit = manatext[8]
				manasplit = manasplit.split("/")
				mana4 = int(manasplit[0])
				lucktext = lucktext.split(" ")
				lucksplit = lucktext[8]
				lucksplit = lucksplit.split("/")
				luck4 = int(lucksplit[0])

				try:
					atimetext = atimetext.split(" ")
					daystext = int(atimetext[9])
					timetext = atimetext[11].strip("<br")
					atime4 = timetosecs(daystext, timetext)
				except ValueError:
					atime4 = 0
				try:
					stimetext = stimetext.split(" ")
					daystext = int(stimetext[9])
					timetext = stimetext[11].strip("<br")
					stime4 = timetosecs(daystext, timetext)
				except ValueError:
					stime4 = 0

				amulettext = amulettext.split(" ")
				amuletsplit = amulettext[7]
				amulet4 = int(amuletsplit.strip("<br"))
				bootstext = bootstext.split(" ")
				bootssplit = bootstext[7]
				boots4 = int(bootssplit.strip("<br"))
				charmtext = charmtext.split(" ")
				charmsplit = charmtext[7]
				charm4 = int(charmsplit.strip("<br"))
				glovestext = glovestext.split(" ")
				glovessplit = glovestext[7]
				gloves4 = int(glovessplit.strip("<br"))
				helmtext = helmtext.split(" ")
				helmsplit = helmtext[7]
				helm4 = int(helmsplit.strip("<br"))
				leggingstext = leggingstext.split(" ")
				leggingssplit = leggingstext[7]
				leggings4 = int(leggingssplit.strip("<br"))
				ringtext = ringtext.split(" ")
				ringsplit = ringtext[7]
				ring4 = int(ringsplit.strip("<br"))
				shieldtext = shieldtext.split(" ")
				shieldsplit = shieldtext[7]
				shield4 = int(shieldsplit.strip("<br"))
				tunictext = tunictext.split(" ")
				tunicsplit = tunictext[7]
				tunic4 = int(tunicsplit.strip("<br"))
				weapontext = weapontext.split(" ")
				weaponsplit = weapontext[7]
				weapon4 = int(weaponsplit.strip("<br"))

				sumtext = sumtext.split(" ")
				sumsplit = sumtext[7]
				mysum4 = int(sumsplit.strip("<br"))
				experttext1 = experttext1.split(" ")
				expertsplit1 = experttext1[8]
				expertsplitsplit1 = expertsplit1.split("<")
				expertd1 = expertsplitsplit1[0]
				experttext2 = experttext2.split(" ")
				expertsplit2 = experttext2[8]
				expertsplitsplit2 = expertsplit2.split("<")
				expertd2 = expertsplitsplit2[0]
				experttext3 = experttext3.split(" ")
				expertsplit3 = experttext3[8]
				expertsplitsplit3 = expertsplit3.split("<")
				expertd3 = expertsplitsplit3[0]
				stonetext1 = stonetext1.split(" ")
				stonesplit1 = stonetext1[8]
				stonesplitsplit1 = stonesplit1.split("<")
				stoned1 = stonesplitsplit1[0]
				stonetext2 = stonetext2.split(" ")
				stonesplit2 = stonetext2[8]
				stonesplitsplit2 = stonesplit2.split("<")
				stoned2 = stonesplitsplit2[0]
				stonetext3 = stonetext3.split(" ")
				stonesplit3 = stonetext3[8]
				stonesplitsplit3 = stonesplit3.split("<")
				stoned3 = stonesplitsplit3[0]
				fightstext = fightstext.split(" ")
				fightssplit = fightstext[13]
				fights4 = int(fightssplit.strip("<br"))
				lottonumtext1 = re.sub(r'<.*?>', ' ', lottonumtext1)
				lottonumtext1 = lottonumtext1.split(" ")
				lottonumtext2 = re.sub(r'<.*?>', ' ', lottonumtext2)
				lottonumtext2 = lottonumtext2.split(" ")
				lottonumtext3 = re.sub(r'<.*?>', ' ', lottonumtext3)
				lottonumtext3 = lottonumtext3.split(" ")
				lottonumd1 = "{0} {1} and {2}".format(lottonumtext1[11], lottonumtext1[12], lottonumtext1[13])                        
				lottonumd2 = "{0} {1} and {2}".format(lottonumtext2[11], lottonumtext2[12], lottonumtext2[13])                        
				lottonumd3 = "{0} {1} and {2}".format(lottonumtext3[11], lottonumtext3[12], lottonumtext3[13])                        
			except:
				webworksD = False
				xchat.prnt("4 Variable Error")

	itemslist.append( ( "align", align, "align", align2, "align", align3, "align", align4 ) )
	itemslist.append( ( "level", level, "level", level2, "level", level3, "level", level4 ) )
	itemslist.append( ( "ttl", ttl, "ttl", ttl2, "ttl", ttl3, "ttl", ttl4 ) )
	itemslist.append( ( "gold", gold, "gold", gold2, "gold", gold3, "gold", gold4 ) )
	itemslist.append( ( "gems", gems, "gems", gems2, "gems", gems3, "gems", gems4 ) )
	itemslist.append( ( "upgradelevel", upgradelevel, "upgradelevel", upgradelevel2, "upgradelevel", upgradelevel3, "upgradelevel", upgradelevel4 ) )
	itemslist.append( ( "ability", ability, "ability", ability2, "ability", ability3, "ability", ability4 ) )
	itemslist.append( ( "xp", xp, "xp", xp2, "xp", xp3, "xp", xp4 ) )
	itemslist.append( ( "exp", exp, "exp", exp2, "exp", exp3, "exp", exp4 ) )
	itemslist.append( ( "life", life, "life", life2, "life", life3, "life", life4 ) )
	itemslist.append( ( "scrolls", scrolls, "scrolls", scrolls2, "scrolls", scrolls3, "scrolls", scrolls4 ) )
	itemslist.append( ( "eatused", eatused, "eatused", eatused2, "eatused", eatused3, "eatused", eatused4 ) )
	itemslist.append( ( "powerpots", powerpots, "powerpots", powerpots2, "powerpots", powerpots3, "powerpots", powerpots4 ) )
	itemslist.append( ( "mana", mana, "mana", mana2, "mana", mana3, "mana", mana4 ) )
	itemslist.append( ( "luck", luck, "luck", luck2, "luck", luck3, "luck", luck4 ) )
	itemslist.append( ( "atime", atime, "atime", atime2, "atime", atime3, "atime", atime4 ) )
	itemslist.append( ( "stime", stime, "stime", stime2, "stime", stime3, "stime", stime4 ) )

	itemslist.append( ( "amulet", amulet, "amulet", amulet2, "amulet", amulet3, "amulet", amulet4 ) )
	itemslist.append( ( "boots", boots, "boots", boots2, "boots", boots3, "boots", boots4 ) )
	itemslist.append( ( "charm", charm, "charm", charm2, "charm", charm3, "charm", charm4 ) )
	itemslist.append( ( "gloves", gloves, "gloves", gloves2, "gloves", gloves3, "gloves", gloves4 ) )
	itemslist.append( ( "helm", helm, "helm", helm2, "helm", helm3, "helm", helm4 ) )
	itemslist.append( ( "leggings", leggings, "leggings", leggings2, "leggings", leggings3, "leggings", leggings4 ) )
	itemslist.append( ( "ring", ring, "ring", ring2, "ring", ring3, "ring", ring4 ) )
	itemslist.append( ( "shield", shield, "shield", shield2, "shield", shield3, "shield", shield4 ) )
	itemslist.append( ( "tunic", tunic, "tunic", tunic2, "tunic", tunic3, "tunic", tunic4 ) )
	itemslist.append( ( "weapon", weapon, "weapon", weapon2, "weapon", weapon3, "weapon", weapon4 ) )

	itemslist.append( ( "mysum", mysum, "mysum", mysum2, "mysum", mysum3, "mysum", mysum4 ) )
	itemslist.append( ( "expert1", expert1, "expert1", expertb1, "expert1", expertc1, "expert1", expertd1 ) )
	itemslist.append( ( "expert2", expert2, "expert2", expertb2, "expert2", expertc2, "expert2", expertd2 ) )
	itemslist.append( ( "expert3", expert3, "expert3", expertb3, "expert3", expertc3, "expert3", expertd3 ) )
	itemslist.append( ( "stone1", stone1, "stone1", stoneb1, "stone1", stonec1, "stone1", stoned1 ) )
	itemslist.append( ( "stone2", stone2, "stone2", stoneb2, "stone2", stonec2, "stone2", stoned2 ) )
	itemslist.append( ( "stone3", stone3, "stone3", stoneb3, "stone3", stonec3, "stone3", stoned3 ) )
	itemslist.append( ( "fights", fights, "fights", fights2, "fights", fights3, "fights", fights4 ) )
	
def getitems(num):
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
	global eatused
	global powerpots
	global mana
	global luck
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

	global itemslist
	
	if num == 1:
		itemname = 0
		itemscore = 1
	if num == 2:
		itemname = 2
		itemscore = 3
	if num == 3:
		itemname = 4
		itemscore = 5
	if num == 4:
		itemname = 6
		itemscore = 7
		
	for entry in itemslist:
		if(entry[itemname] == "align"):
			align = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "level"):
			level = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "ttl"):
			ttl = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "gold"):
			gold = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "gems"):
			gems = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "upgradelevel"):
			upgradelevel = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "ability"):
			ability = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "xp"):
			xp = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "exp"):
			exp = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "life"):
			life = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "scrolls"):
			scrolls = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "eatused"):
			eatused = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "powerpots"):
			powerpots = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "mana"):
			mana = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "luck"):
			luck = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "atime"):
			atime = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "stime"):
			stime = entry[itemscore]

	for entry in itemslist:
		if(entry[itemname] == "amulet"):
			amulet = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "charm"):
			charm = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "helm"):
			helm = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "boots"):
			boots = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "gloves"):
			gloves = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "ring"):
			ring = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "leggings"):
			leggings = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "shield"):
			shield = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "tunic"):
			tunic = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "weapon"):
			weapon = entry[itemscore]

	for entry in itemslist:
		if(entry[itemname] == "mysum"):
			mysum = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "expert1"):
			expert1 = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "expert2"):
			expert2 = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "expert3"):
			expert3 = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "stone1"):
			stone1 = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "stone2"):
			stone2 = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "stone3"):
			stone3 = entry[itemscore]
	for entry in itemslist:
		if(entry[itemname] == "fights"):
			fights = entry[itemscore]

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
	global channame2
	global botname2
	global channame3
	global botname3
	global channame4
	global botname4
	global nickname
	global netname
	global nickname2
	global netname2
	global nickname3
	global netname3
	global nickname4
	global netname4
	global servername
	global servername2
	global servername3
	global servername4
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
	global webworksB
	global webworksC
	global webworksD
	global rank
	global rank2
	global rank3
	global rank4
	global offline
	global offline2
	global offline3
	global offline4
	global playerspagelist
	global playerspagelist2
	global playerspagelist3
	global playerspagelist4
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
	global level2
	global fights2
	global level3
	global fights3
	global level4
	global fights4
	global gameactive
	global char1
	global char2
	global char3
	global char4
	global chanmessagecount
	global life
	global life2
	global life3
	global life4
	global charcount
	global intervaltext
	
	if intervaltext is True:
		xchat.prnt( "INTERVAL {0}".format(time.asctime()) )
	if chanmessage is True:
		chanmessagecount += 1

	if char1 is True:
		botcheck = False
		chancheck = True
	if char2 is True:
		botcheck2 = False
		chancheck2 = True
	if char3 is True:
		botcheck3 = False
		chancheck3 = True
	if char4 is True:
		botcheck4 = False
		chancheck4 = True
	intervaldisable = False

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
				 xchat.prnt( "1 Game Bot not in channel" )
	if char2 is True:
		if game_chan2.get_info("channel").lower() != channame2:
			chancheck2 = False
		if chancheck2 is False:
			if ZNC2 is True:
				game_chan2.command( "quote PASS {0}:{1}".format(ZNCUser2, ZNCPass2) )
			game_chan2.command( "join {0}".format(channame2) )
			botcheck2 = False
		if chancheck2 is True:
			userlist = game_chan2.get_list("users")
			for user in userlist:
				if botname2 in user.nick:
					botcheck2 = True
			if botcheck2 is False:
				 xchat.prnt( "2 Game Bot not in channel" )
	if char3 is True:
		if game_chan3.get_info("channel").lower() != channame3:
			chancheck3 = False
		if chancheck3 is False:
			if ZNC3 is True:
				game_chan3.command( "quote PASS {0}:{1}".format(ZNCUser3, ZNCPass3) )
			game_chan3.command( "join {0}".format(channame3) )
			botcheck3 = False
		if chancheck3 is True:
			userlist = game_chan3.get_list("users")
			for user in userlist:
				if botname3 in user.nick:
					botcheck3 = True
			if botcheck3 is False:
				 xchat.prnt( "3 Game Bot not in channel" )
	if char4 is True:
		if game_chan4.get_info("channel").lower() != channame4:
			chancheck4 = False
		if chancheck4 is False:
			if ZNC4 is True:
				game_chan4.command( "quote PASS {0}:{1}".format(ZNCUser4, ZNCPass4) )
			game_chan4.command( "join {0}".format(channame4) )
			botcheck4 = False
		if chancheck4 is True:
			userlist = game_chan4.get_list("users")
			for user in userlist:
				if botname4 in user.nick:
					botcheck4 = True
			if botcheck4 is False:
				 xchat.prnt( "4 Game Bot not in channel" )

	if private is True and chanmessagecount == 1:
		xchat.hook_print("Private Message", private_cb)
		xchat.hook_print("Private Message to Dialog", private_cb)
		
	if chanmessage is True and chanmessagecount == 1:
		xchat.hook_print("Channel Message", on_message)
		xchat.hook_print("Channel Msg Hilight", on_message)

	if(char1 is True and botcheck is True):
		webdata2(1)
	if(char2 is True and botcheck2 is True):
		webdata2(2)
	if(char3 is True and botcheck3 is True):
		webdata2(3)
	if(char4 is True and botcheck4 is True):
		webdata2(4)
	if((webworks is True and botcheck is True) or (webworksB is True and botcheck2 is True) or (webworksC is True and botcheck3 is True) or (webworksD is True and botcheck4 is True)):
		getvariables()

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
				test = test.split('">')
				ranktext = test[1]
				ranktext = ranktext.split("</")
				rank = int(ranktext[0])
	if webworksB is True:
		if char2 is True and botcheck2 is True:
			for entry in playerspagelist2:
				if "playerview.php" in entry and name2 in entry:
					test = entry
			if "offline" in test:
				offline2 = True
			if offline2 is False:
				test = test.split('">')
				ranktext = test[1]
				ranktext = ranktext.split("</")
				rank2 = int(ranktext[0])
	if webworksC is True:
		if char3 is True and botcheck3 is True:
			for entry in playerspagelist3:
				if "playerview.php" in entry and name3 in entry:
					test = entry
			if "offline" in test:
				offline3 = True
			if offline3 is False:
				test = test.split('">')
				ranktext = test[1]
				ranktext = ranktext.split("</")
				rank3 = int(ranktext[0])
	if webworksD is True:
		if char4 is True and botcheck4 is True:
			for entry in playerspagelist4:
				if "playerview.php" in entry and name4 in entry:
					test = entry
			if "offline" in test:
				offline4 = True
			if offline4 is False:
				test = test.split('">')
				ranktext = test[1]
				ranktext = ranktext.split("</")
				rank4 = int(ranktext[0])
	if char1 is True and botcheck is True:
		if(webworks is True and offline is True):
			xchat.prnt("1 Player Offline")
	if char2 is True and botcheck2 is True:
		if(webworksB is True and offline2 is True):
			xchat.prnt("2 Player Offline")
	if char3 is True and botcheck3 is True:
		if(webworksC is True and offline3 is True):
			xchat.prnt("3 Player Offline")
	if char4 is True and botcheck4 is True:
		if(webworksD is True and offline4 is True):
			xchat.prnt("4 Player Offline")

	if char1 is True:
		nickname = game_chan.get_info("nick")
		netname = game_chan.get_info("network")
		if game_chan.get_info("server") is None:
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
			xchat.prnt( "2 Not connected!" )
			if ZNC2 is False:
				game_chan2.command( "server {0}".format(servername2) )
			if ZNC2 is True:
				game_chan2.command( "server {0} {1}".format(ZNCServer2, ZNCPort2) )
			interval = 45
			hookmain()
			intervaldisable = True

		if webworksB is True and offline2 is True and botcheck2 is True:
			usecommand("login {0} {1}".format(name2, pswd2),2)
			interval = 45
			hookmain()
			intervaldisable = True
	if char3 is True:
		nickname3 = game_chan3.get_info("nick")
		netname3 = game_chan3.get_info("network")
		if game_chan3.get_info("server") is None:
			xchat.prnt( "3 Not connected!" )
			if ZNC3 is False:
				game_chan3.command( "server {0}".format(servername3) )
			if ZNC3 is True:
				game_chan3.command( "server {0} {1}".format(ZNCServer3, ZNCPort3) )
			interval = 45
			hookmain()
			intervaldisable = True

		if webworksC is True and offline3 is True and botcheck3 is True:
			usecommand("login {0} {1}".format(name3, pswd3),3)
			interval = 45
			hookmain()
			intervaldisable = True
	if char4 is True:
		nickname4 = game_chan4.get_info("nick")
		netname4 = game_chan4.get_info("network")
		if game_chan4.get_info("server") is None:
			xchat.prnt( "4 Not connected!" )
			if ZNC4 is False:
				game_chan4.command( "server {0}".format(servername4) )
			if ZNC4 is True:
				game_chan4.command( "server {0} {1}".format(ZNCServer4, ZNCPort4) )
			interval = 45
			hookmain()
			intervaldisable = True

		if webworksD is True and offline4 is True and botcheck4 is True:
			usecommand("login {0} {1}".format(name4, pswd4),4)
			interval = 45
			hookmain()
			intervaldisable = True

	if (webworks is True or webworksB is True or webworksC is True or webworksD is True) and intervaldisable is False:
		intervalcalc()
	if charcount == 1:
		if webworks is False and intervaldisable is False:
			interval = 300
			hookmain()
	if charcount == 2:
		if webworks is False and webworksB is False and intervaldisable is False:
			interval = 300
			hookmain()
	if charcount == 3:
		if webworks is False and webworksB is False and webworksC is False and intervaldisable is False:
			interval = 300
			hookmain()
	if charcount == 4:
		if webworks is False and webworksB is False and webworksC is False and webworksD is False and intervaldisable is False:
			interval = 300
			hookmain()

	if webworks is True:
		if char1 is True and offline is False and botcheck is True:
			playerarea(1)
			spendmoney(1)
			timercheck(1)
			if(level >= 25 and fights >= 0 and fights < 5 and life > 0):
				xchat.prnt("Fights available")
			if(level >= 25 and fights >= 0 and fights < 5 and life > 10):
				newlister(1)
				fight_fight(1)
	if webworksB is True:
		if char2 is True and offline2 is False and botcheck2 is True:
			playerarea(2)
			spendmoney(2)
			timercheck(2)
			if(level2 >= 25 and fights2 >= 0 and fights2 < 5 and life2 > 0):
				xchat.prnt("Fights available")
			if(level2 >= 25 and fights2 >= 0 and fights2 < 5 and life2 > 10):
				newlister(2)
				fight_fight(2)
	if webworksC is True:
		if char3 is True and offline3 is False and botcheck3 is True:
			playerarea(3)
			spendmoney(3)
			timercheck(3)
			if(level3 >= 25 and fights3 >= 0 and fights3 < 5 and life3 > 0):
				xchat.prnt("Fights available")
			if(level3 >= 25 and fights3 >= 0 and fights3 < 5 and life3 > 10):
				newlister(3)
				fight_fight(3)
	if webworksD is True:
		if char4 is True and offline4 is False and botcheck4 is True:
			playerarea(4)
			spendmoney(4)
			timercheck(4)
			if(level4 >= 25 and fights4 >= 0 and fights4 < 5 and life4 > 0):
				xchat.prnt("Fights available")
			if(level4 >= 25 and fights4 >= 0 and fights4 < 5 and life4 > 10):
				newlister(4)
				fight_fight(4)

	return True	# <- tells timer to repeat

def intervalcalc():
	global interval
	global level
	global fights
	global level2
	global fights2
	global level3
	global fights3
	global level4
	global fights4
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
	global life2
	global life3
	global life4
	global fightmode
	
	sixty = 60
	onetwenty = 120
	interval = 5
	interval *= 60			# conv from min to sec
	intervallist = []

	if char1 is True:
		if botcheck is False or offline is True:
			intervallist.append( ( "interval", sixty ) )
		if botcheck is True:
			if(level >= 25 and life > 10 and fightmode is True):
				if(fights >= 0 and fights < 5):
					intervallist.append( ( "interval", onetwenty ) )
	if char2 is True:
		if botcheck2 is False or offline2 is True:
			intervallist.append( ( "interval", sixty ) )
		if botcheck2 is True:
			if(level2 >= 25 and life2 > 10 and fightmode is True):
				if(fights2 >= 0 and fights2 < 5):
					intervallist.append( ( "interval", onetwenty ) )
	if char3 is True:
		if botcheck3 is False or offline3 is True:
			intervallist.append( ( "interval", sixty ) )
		if botcheck3 is True:
			if(level3 >= 25 and life3 > 10 and fightmode is True):
				if(fights3 >= 0 and fights3 < 5):
					intervallist.append( ( "interval", onetwenty ) )
	if char4 is True:
		if botcheck4 is False or offline4 is True:
			intervallist.append( ( "interval", sixty ) )
		if botcheck4 is True:
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
	global fights
	global attackslaySum
	global attackslaySum2
	global attackslaySum3
	global attackslaySum4
	global mana
	global powerpots
	global gold
	global charcount
	global life
	global buypower
	global slaysum
	
	if charcount >= 2:
		getitems(num)

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
		if powerpots == 0 and gold >= 1100 and buypower is True:
			usecommand("buy power", num)
			gold -= 1000
			powerpots = 1

		timer = (atime+10)*1000
		xchat.prnt("Set attack {0} timer. Going off in {1} minutes.".format(num, timer // 60000))
		slaydisable = True

		if powerpots == 0:
			if num == 1:
				xchat.hook_timer(timer, attack)
			if num == 2:
				xchat.hook_timer(timer, attack2)
			if num == 3:
				xchat.hook_timer(timer, attack3)
			if num == 4:
				xchat.hook_timer(timer, attack4)
		if powerpots == 1:
			if num == 1:
				xchat.hook_timer(timer, attackb)
			if num == 2:
				xchat.hook_timer(timer, attackb2)
			if num == 3:
				xchat.hook_timer(timer, attackb3)
			if num == 4:
				xchat.hook_timer(timer, attackb4)

	if(level >= 30 and attackslaySumlist >= 1000 and stime <= interval and stime <= ttl and slaydisable is False and life > 10):
		if(mana == 0 and gold >= 1100 and attackslaySumlist < 6300000):
			usecommand("buy mana", num)
			gold -= 1000
			mana = 1
		timer = (stime+10)*1000
		if mana == 0 and attackslaySumlist >= slaysum:
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
			xchat.prnt("Set slay {0} timer. Going off in {1} minutes.".format(num, timer // 60000))
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
	global charcount
	global luck
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
	global buyluck
	global expbuy
	
	# level 15 >= buy - decide what to spend our gold on! :D
	# level 1 >= blackbuy - requires 15 gems per buy
	# level 1 >= get x gems - 150 gold per gem
	# xpget 20xp minimum
	# buy exp - 1000 gold - 10% off TTL
	
	if charcount >= 2:
		getitems(num)

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

	if(level >= 15 and buyluck is True):
		if(luck == 0 and gold >= 2100):
			usecommand("buy luck", num)
			luck = 1
			gold -= 1000

	if(expbuy is True and exp < 5):
		expdiff = 5 - exp
		expcost = expdiff * 1000
		if(gold >= (expcost + 1100)):
			for i in range(expdiff):
				usecommand("buy exp", num)
				gold -= 1000
				exp += 1
		elif(gold >= 1000 + 1100):
			golddiff = gold - 1100
			expcalc = golddiff // 1000
			if expcalc >= 1:
				for i in range(expcalc):
					usecommand("buy exp", num)
					gold -= 1000
					exp += 1
					
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
		
#        xchat.prnt("{0} goldsave: {1}  gembuy: {2}  level: {3}  upgradelevel: {4}  align: {5}".format(num, goldsave, gembuy, level, upgradelevel, align))

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
					usecommand("blackbuy {0} 14".format(lowestitem[0]), num)
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
	global gold
	global powerpots
	global charcount
	global life
	global buypower

	if charcount >= 2:
		getitems(num)
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
	
	xchat.prnt("{0} has reached level {1}!".format(namelist, level))

	if(level >= 16 and life > 10):
		if powerpots == 0 and gold >= 1100 and buypower is True:
			usecommand("buy power", num)
			gold -= 1000
			powerpots = 1

		if powerpots == 0:
			if num == 1:
				xchat.hook_timer(0, attack)
			if num == 2:
				xchat.hook_timer(0, attack2)
			if num == 3:
				xchat.hook_timer(0, attack3)
			if num == 4:
				xchat.hook_timer(0, attack4)
		if powerpots == 1:
			if num == 1:
				xchat.hook_timer(0, attackb)
			if num == 2:
				xchat.hook_timer(0, attackb2)
			if num == 3:
				xchat.hook_timer(0, attackb3)
			if num == 4:
				xchat.hook_timer(0, attackb4)

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
	global charcount

	if charcount >= 2:
		getitems(num)

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
	global fightlevellimit
	global fightlevellimit2
	global fightlevellimit3
	global fightlevellimit4
	global charcount

	if charcount >= 2:
		getitems(num)
	
	if num == 1:
		newlists = newlist
		namelist = name
		itemSumlist = itemSum
		expertSumlist = expertSum
		fightlevellimits = fightlevellimit
	if num == 2:
		newlists = newlist2
		namelist = name2
		itemSumlist = itemSum2
		expertSumlist = expertSum2
		fightlevellimits = fightlevellimit2
	if num == 3:
		newlists = newlist3
		namelist = name3
		itemSumlist = itemSum3
		expertSumlist = expertSum3
		fightlevellimits = fightlevellimit3
	if num == 4:
		newlists = newlist4
		namelist = name4
		itemSumlist = itemSum4
		expertSumlist = expertSum4
		fightlevellimits = fightlevellimit4
		
	upgradeSum1 = upgradelevel * 100
	fightSumTotal = float(itemSumlist + expertSumlist)
	lifepercent = (float(life) / 100)
	test = []
	
	diff = 0
	best = ("Doctor Who?", 9999999999.0, 9999999999.0, 0, 0, "p", 0)
	newlists.sort( key=operator.itemgetter(2))
	if newlists != None:
		for entry in newlists:
			if fightlevellimits is True:
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

			if fightlevellimits is False:
				if(entry[0] != namelist):
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
	attackmulti(1, 1)

def attack2(userdata):
	attackmulti(2, 1)

def attack3(userdata):
	attackmulti(3, 1)

def attack4(userdata):
	attackmulti(4, 1)

def attackb(userdata):
	attackmulti(1, 2)

def attackb2(userdata):
	attackmulti(2, 2)

def attackb3(userdata):
	attackmulti(3, 2)

def attackb4(userdata):
	attackmulti(4, 2)

def attackmulti(num, num2):
	global creepattack
	global setcreeptarget

	if creepattack is True:
		creep = bestattack(num, num2)
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

def bestattack(num, num2):
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
	if num2 == 1:
		multi = 1
	if num2 == 2:
		multi = 2
	for thing in creeps:
		if((attackslaySumlist * multi) <= thing[1]):
			good = thing
	return good[0]

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
			good = thing
	return good[0]

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