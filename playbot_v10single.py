#!/usr/bin/env python

import xchat
import operator
import time
import pickle
import os
import sys
import socket
import ssl
import re ##

__module_name__ = "Multirpg Playbot Script"
__module_version__ = "10.0"
__module_description__ = "Multirpg Playbot Script"

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
# Creep Recovery Multipliers:
# Bush, Locust x 1
# Spider, Goblin, Lich, Skeleton, Ghost, Shadow x 2
# Troll, Cyclops, Mutant, Monkey x 3
# Phoenix, Minotaur, Beholder, Wyvern x 4
# Ogre x 5

creeps = [      ["Bush",        10],    \
		["Locust",      15],    \
		["Spider",      20],    \
		["Goblin",      30],    \
		["Lich",        40],    \
#               ["Skeleton",    50],    \
#               ["Ghost",       60],    \
		["Shadow",      70],    \
#               ["Troll",       80],    \
#               ["Cyclops",     90],    \
#               ["Mutant",      100],   \
		["Monkey",      110],   \
		["Phoenix",     120],   \
		["Minotaur",    130],   \
		["Beholder",    140],   \
		["Wyvern",      150],   \
		["Ogre",        1600]  ]

monsters = [    ["Medusa",      3500],  \
		["Centaur",     4000],  \
		["Mammoth",     5000],  \
		["Vampire",     6000],  \
		["Dragon",      7000],  \
		["Sphinx",      8000],  \
		["Hippogriff",  999999] ]

# list of all networks
#               Network,        Server,                         NoLag   SNum    Port            SSLPort         BotHostMask
networklist = [ ["AyoChat",     "irc.ayochat.or.id",            False,  1,      6667,           6667,           ".skralg.com"],  \
		["AyoChat",     "51.79.146.180",                False,  2,      6667,           6667,           ".skralg.com"],  \
		["ChatLounge",  "irc.chatlounge.net",           True,   1,      6667,           "+6697",        "multirpg@venus.skralg.com"],  \
		["ChatLounge",  "185.34.216.32",                True,   2,      6667,           "+6697",        "multirpg@venus.skralg.com"],  \
		["DALnet",      "irc.dal.net",                  False,  1,      6667,           "+6697",        ".skralg.com"], \
		["DALnet",      "94.125.182.251",               False,  2,      6667,           "+6697",        ".skralg.com"], \
		["EFnet",       "irc.efnet.net",                False,  1,      6667,           "+9999",        "multirpg@venus.skralg.com"], \
		["EFnet",       "66.225.225.225",               False,  2,      6667,           "+9999",        "multirpg@venus.skralg.com"], \
		["GameSurge",   "irc.gamesurge.net",            True,   1,      6667,           6667,           "multirpg@multirpg.bot.gamesurge"],  \
		["GameSurge",   "192.223.27.109",               True,   2,      6667,           6667,           "multirpg@multirpg.bot.gamesurge"],  \
		["IRC4Fun",     "irc.irc4fun.net",              False,  1,      6667,           "+6697",        "multirpg@bots/multirpg"],  \
		["IRC4Fun",     "139.99.113.250",               False,  2,      6667,           "+6697",        "multirpg@bots/multirpg"],  \
		["Koach",       "irc.koach.com",                False,  1,      6667,           "+6697",        ".skralg.com"], \
		["Koach",       "172.105.168.90",               False,  2,      6667,           "+6697",        ".skralg.com"], \
		["Libera",      "irc.libera.chat",              False,  1,      6667,           "+6697",        "multirpg@venus.skralg.com"], \
		["Libera",      "130.185.232.126",              False,  2,      6667,           "+6697",        "multirpg@venus.skralg.com"], \
		["mIRCPhantom", "irc.mircphantom.net",          False,  1,      6667,           "+6697",        ".skralg.com"], \
		["mIRCPhantom", "51.89.198.165",                False,  2,      6667,           "+6697",        ".skralg.com"], \
		["Pissnet",     "irc.shitposting.space",        False,  1,      6667,           "+6697",        ".skralg.com"], \
		["Pissnet",     "91.92.144.105",                False,  2,      6667,           "+6697",        ".skralg.com"], \
		["QuakeNet",    "irc.quakenet.org",             False,  1,      6667,           6667,           "multirpg@multirpg.users.quakenet.org"], \
		["QuakeNet",    "188.240.145.70",               False,  2,      6667,           6667,           "multirpg@multirpg.users.quakenet.org"], \
		["Rizon",       "irc.rizon.net",                False,  1,      6667,           "+6697",        ".skralg.com"], \
		["Rizon",       "45.88.6.116",                  False,  2,      6667,           "+6697",        ".skralg.com"], \
		["ScaryNet",    "irc.scarynet.org",             True,   1,      6667,           6667,           "multirpg@venus.skralg.com"],  \
		["ScaryNet",    "69.162.163.62",                True,   2,      6667,           6667,           "multirpg@venus.skralg.com"],  \
		["SkyChatz",    "irc.skychatz.org",             False,  1,      6667,           "+6697",        "multirpg@skychatz.user.multirpg"],  \
		["SkyChatz",    "15.235.141.21",                False,  2,      6667,           "+6697",        "multirpg@skychatz.user.multirpg"],  \
		["Techtronix",  "irc.techtronix.net",           True,   1,      "+6697",        "+6697",        "multirpg@multirpg.net"],  \
		["Techtronix",  "35.229.28.106",                True,   2,      "+6697",        "+6697",        "multirpg@multirpg.net"],  \
		["Undernet",    "irc.undernet.org",             False,  1,      6667,           6667,           "multirpg@idlerpg.users.undernet.org"], \
		["Undernet",    "185.117.74.172",               False,  2,      6667,           6667,           "multirpg@idlerpg.users.undernet.org"], \
		["UnderX",      "irc.underx.org",               False,  1,      6667,           6667,           "multirpg@venus.skralg.com"], \
		["UnderX",      "150.136.80.10",                False,  2,      6667,           6667,           "multirpg@venus.skralg.com"], \
		["UniversalNet","irc.universalnet.org",         False,  1,      6667,           "+6697",        "multirpg@venus.skralg.com"], \
		["UniversalNet","62.171.172.8",                 False,  2,      6667,           "+6697",        "multirpg@venus.skralg.com"], \
		["Virtulus",    "virtulus.ftp.sh",              True,   1,      "+6697",        "+6697",        "multirpg@B790DC3F.D0CDF40.88109D7.IP"], \
		["Virtulus",    "129.153.131.239",              True,   2,      "+6697",        "+6697",        "multirpg@B790DC3F.D0CDF40.88109D7.IP"] ]

creeps.reverse()
monsters.reverse()

multirpgweb = "https://www.multirpg.net/"
idlerpgweb = "http://www.idlerpg.org/"
russweb = "http://russellb.x10.mx/"
gitweb = "https://github.com/RussellBeech/xchat-plugins"
gitweb2 = "https://raw.githubusercontent.com/RussellBeech/xchat-plugins/master/"
rawplayers3 = None
rawstatsweb = None
interval = 300
newlist = None
playerlist = None
xmlplayerlist = None
mainhook = None
myentry = None
rawmyentry = None
rawstatsmyentry = None
rawmyentryfail = 0
currentversion = __module_version__
currentversion = float( currentversion )

CONFIG_FILE_LOCATION = xchat.get_info('xchatdir')+"/.playbotsingle"
CONFIG_FILE_LOCATION2 = xchat.get_info('xchatdir')+"/.autostartsingle"

try:
	f = open(CONFIG_FILE_LOCATION,"rb")
	configList = pickle.load(f)
	f.close()
except:
	xchat.prnt("ConfigList Load Error - Using Default Settings")
	configList = []
try:
	f = open(CONFIG_FILE_LOCATION2,"rb")
	autoconfigList = pickle.load(f)
	f.close()
except:
	xchat.prnt("AutoConfigList Load Error - Using Default Settings")
	autoconfigList = []

# custom network settings - For linked networks or networks which are not on the networklist
customnetworksettings = False # True = on, False = off - For custom networks which are not on the networklist
customservername = "irc.mircphantom.net" # Custom Server address
customservername2 = "176.31.181.159" # Custom Server address
customchanname = "#multirpg" # Custom Channel Name
custombotname = "multirpg/fun" # Custom Botname
customnolag = False # True = on, False = off - If network is on the nolag network list
custombosthostmask = "multirpg@multirpg.users.IRC4Fun.net" # Custom Bot Host Name
customport = 6667 # Port Number.  If port is an SSL port use "+6697" format

# ZNC settings
ZNC = False # ZNC Server Mode - True = On, False = Off
ZNCServer = "*.*.*.*" # ZNC Server Address
ZNCPort = 6005 # ZNC Port Number.  If port is an SSL port use "+6697" format
ZNCUser = "********" # ZNC Username/Network
ZNCPass = "********" # ZNC Password

# Changeable settings
multirpgclass = "MultiRPG PlayBot" # Class to be used when re-registering if player gets removed
nickserv = False # True = on, False = off
nickservpass = "*********" # NickServ Password
connectretry = 6 # Retries to connect to network before it switch to another server
laglevel = 20 # If using rawstats and a laggy network it will switch between using rawstats and rawplayers
setalign = 40 # Level in which alignment changes from permanent priest to human/priest switching
upgradeall = True # True = on, False = off - Upgrades all 1 and above after Hero and Engineer is upgraded to level 9
itemupgrader = True # True = on, False = off - Upgrades individual items after Hero and Engineer is upgraded to level 9
betmoney = 220 # Money kept in bank to be used for bets
sethero = 1200 # item score to start to buy/upgrading hero
setengineer = 25 # level to start to buy/upgrading engineer
setbuy = 16 # level to start buying items from
singlefight = True # True = on, False = off
evilmode = False # True = on, False = off
webnum = 1 # 1 = multirpg.net, 2 = idlerpg.org
bottextmode = True # True = on, False = off
errortextmode = True # True = on, False = off
intervaltextmode = True # True = on, False = off
ssl1 = False # True = switches on SSL Port, False = uses normal port
autostartdelay = 60 #seconds delay for autostart when you have the plugin auto loaded from startup
remotekill = True # True = on, False = off # Gives me the option if the PlayBot is flooding the GameBot to disable the PlayBot
fightcalcmin = 0.9 # minimum fightcalc you can fight somebody at

# declare stats as global
name = None
pswd = None
servername = None
networkname = None
servernum = 1
connectfail = 0
webfail = 0
nolag = None
port = None
charcount = 0
private = True
notice = True
chanmessage = True
chanmessagecount = 0
rankplace = 0
level = 0
alignlevel = 0
mysum = 0
gold = 0
bank = 0
team = 0
ufightcalc = 0
fightSum = 0

hero = 0
hlvl = 0
eng = 0
elvl = 0
ttl = 0
atime = 0 # regentm
ctime = 0 # challengetm
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

bets = 0
fights = 0
powerpots = 0
firstalign = "priest"
secondalign = "human"
rawstatsmode = False
rawstatsswitch = False
levelrank1 = 0

nickname = None
netname = None
channame = None
botname = None
botcheck = None
bothostmask = None
chancheck = None
game_chan = None
webworks = True
gameactive = None
ttlfrozen = 0
ttlfrozenmode = False
botdisable1 = False
autostartmode = False
attackcount1 = 0
challengecount1 = 0
slaycount1 = 0
alignlvlupcount1 = 0
lvlupcount1 = 0
online = False
align = "n"

for entry in configList:
	if(entry[0] == "autostartmode"):
		autostartmode = entry[1]
	if(entry[0] == "betmoney"):
		betmoney = entry[1]
	if(entry[0] == "bottextmode"):
		bottextmode = entry[1]
	if(entry[0] == "errortextmode"):
		errortextmode = entry[1]
	if(entry[0] == "evilmode"):
		evilmode = entry[1]
	if(entry[0] == "intervaltextmode"):
		intervaltextmode = entry[1]
	if(entry[0] == "itemupgrader"):
		itemupgrader = entry[1]
	if(entry[0] == "rawstatsmode"):
		rawstatsmode = entry[1]
	if(entry[0] == "rawstatsswitch"):
		rawstatsswitch = entry[1]
	if(entry[0] == "setalign"):
		setalign = entry[1]
	if(entry[0] == "sethero"):
		sethero = entry[1]
	if(entry[0] == "setengineer"):
		setengineer = entry[1]
	if(entry[0] == "setbuy"):
		setbuy = entry[1]
	if(entry[0] == "singlefight"):
		singlefight = entry[1]
	if(entry[0] == "upgradeall"):
		upgradeall = entry[1]

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
			text = urllib2.urlopen(russweb + "playbotversion.txt")
		if python3 is True:
			text = urllib.request.urlopen(russweb + "playbotversion.txt")
		webversion = text.read()
		webversion = float( webversion )
		text.close()

	except:
		xchat.prnt( "Could not access {0}".format(russweb))

	try:
		if python3 is False:
			text2 = urllib2.urlopen(gitweb2 + "playbotversion.txt")
		if python3 is True:
			text2 = urllib.request.urlopen(gitweb2 + "playbotversion.txt")
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
	global autostartmode
	global betmoney
	global evilmode
	global itemupgrader
	global rawstatsmode
	global setalign
	global setbuy
	global setengineer
	global sethero
	global singlefight
	global upgradeall
	global rawstatsswitch
	global bottextmode
	global errortextmode
	global intervaltextmode

	configList = []
	configList.append( ( "autostartmode", autostartmode ) )
	configList.append( ( "betmoney", betmoney ) )
	configList.append( ( "bottextmode", bottextmode ) )
	configList.append( ( "errortextmode", errortextmode ) )
	configList.append( ( "evilmode", evilmode ) )
	configList.append( ( "intervaltextmode", intervaltextmode ) )
	configList.append( ( "itemupgrader", itemupgrader ) )
	configList.append( ( "rawstatsmode", rawstatsmode ) )
	configList.append( ( "rawstatsswitch", rawstatsswitch ) )
	configList.append( ( "setalign", setalign ) )
	configList.append( ( "setbuy", setbuy ) )
	configList.append( ( "setengineer", setengineer ) )
	configList.append( ( "sethero", sethero ) )
	configList.append( ( "singlefight", singlefight ) )
	configList.append( ( "upgradeall", upgradeall ) )
	f = open(CONFIG_FILE_LOCATION,"wb")
	pickle.dump(configList,f)
	f.close()

def configwrite2():
	global name
	global pswd

	autoconfigList = []
	autoconfigList.append( ( "name", name ) )
	autoconfigList.append( ( "pswd", pswd ) )
	f = open(CONFIG_FILE_LOCATION2,"wb")
	pickle.dump(autoconfigList,f)
	f.close()

def autostarton(word, word_eol, userdata):
	global autostartmode
	global gameactive

	if gameactive is True:
		autostartmode = True
		configwrite()
		configwrite2()
		xchat.prnt("Autostart mode on")
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL
	
xchat.hook_command("autostarton", autostarton, help="/autostarton - Turns autostart mode on")

def autostartoff(word, word_eol, userdata):
	global autostartmode
	global gameactive

	if gameactive is True:
		autostartmode = False
		configwrite()
		autoconfigList = []
		f = open(CONFIG_FILE_LOCATION2,"wb")
		pickle.dump(autoconfigList,f)
		f.close()
		xchat.prnt("Autostart mode off")
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("autostartoff", autostartoff, help="/autostartoff - Turns autostart mode off")

def eraseconfig(word, word_eol, userdata):
	configList = []
	f = open(CONFIG_FILE_LOCATION,"wb")
	pickle.dump(configList,f)
	f.close()
	autoconfigList = []
	f = open(CONFIG_FILE_LOCATION2,"wb")
	pickle.dump(autoconfigList,f)
	f.close()
	xchat.prnt("Config Erased")
	return xchat.EAT_ALL

xchat.hook_command("eraseconfig", eraseconfig, help="/eraseconfig - Erases config file")
	
def bottester():
	global game_chan
	global botname
	global channame
	global netname
	global botdisable1
	
	botcount1 = 0
	try:
		if("undernet" in netname.lower()):
			channame = "#idlerpg"
			botname = "idlerpg"
		else:
			channame = "#multirpg"
			botname = "multirpg"
	except AttributeError:
		xchat.prnt( "AttributeError" )

	bottest = botname
	bottest2 = "multirpg"
	botentry = []

	try:
		userlist = game_chan.get_list("users")

		for user in userlist:
			if bottest in user.nick and user.nick != bottest:
				botprefix = user.prefix
				if(botprefix == "@" or botprefix == "%"):
					botentry.append(user.nick)
					botname10 = user.nick
			if("undernet" in netname.lower()):
				if bottest2 in user.nick:
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

def usecommand(commanded):
	global game_chan
	global botname
	global channame
	global customnetworksettings
	global botdisable1
	global gameactive
	
	if customnetworksettings is False and gameactive is True:
		bottester()
	if(botdisable1 is False):
		try:
			game_chan.command( "msg {0} {1}".format(botname, commanded) )
		except AttributeError:
			xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame) )

def autostart(userdata):
	global name
	global pswd
	global netname
	global nickname
	global channame
	global botname
	global game_chan
	global charcount
	global rawstatsmode
	global rawstatsswitch
	global gameactive
	global customnetworksettings
	global custombotname
	global customchanname
	global autostartmode
	global autostartdelay
	
	for entry in autoconfigList:
		if(entry[0] == "name"):
			name = entry[1]
		if(entry[0] == "pswd"):
			pswd = entry[1]

	if name != None and pswd != None:
		charcount += 1

	if charcount == 1:
		# use login command
		gameactive = True
		netname = xchat.get_info("network")
		
		if netname is None:
			netname = xchat.get_info("network")
			charcount = 0
			mainhook = xchat.hook_timer(autostartdelay * 1000, autostart)  # hook_timer requires milliseconds                       
			return

		nickname = xchat.get_info("nick")
		if customnetworksettings is False:
			if("undernet" in netname.lower()):
				channame = "#idlerpg"
				botname = "idlerpg"
			else:
				channame = "#multirpg"
				botname = "multirpg"

		if customnetworksettings is True:
			channame = customchanname
			botname = custombotname
			
		# find context
		game_chan = xchat.find_context(channel=channame)
		xmlwebdata()

		if(game_chan is None):
			xchat.prnt("Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame))
			charcount = 0
			gameactive = False
			xchat.prnt("Autostart Failed")
			autostartmode = False
			configwrite()
			return

		if rawstatsmode is True or rawstatsswitch is True:
			opcheck = False
			userlist = game_chan.get_list("users")
			for user in userlist:
				if user.nick == botname:
					botprefix = user.prefix
					if(botprefix == "@" or botprefix == "%"):
						opcheck = True
			if opcheck is False:
				rawstatsmode = False
				rawstatsswitch = False
				xchat.prnt("GameBot Not Opped Changing to RawPlayers")
				configwrite()
		if(name != None and pswd != None):
			loginstart()
	if charcount == 0:
		gameactive = False
		xchat.prnt("Autostart Failed")
		autostartmode = False
		configwrite()


if autostartmode is False:
	xchat.prnt( "To start PlayBot use /login CharName Password" )

def updatenick(word, word_eol, userdata):
	global gameactive
	global channame
	global netname
	global nickname
	global botname
	global game_chan
	global autostartmode
	
	if gameactive is True:
		checknet = xchat.get_info("network")
		checknick = xchat.get_info("nick")
		nickswitch = False

		if checknet != netname:
			nickswitch = True
		if checknet == netname:
			if checknick != nickname:
				nickswitch = True
			if checknick == nickname:
				xchat.prnt("{0} is already in use on {1}".format(nickname, netname))
		if nickswitch is True:
			netname = xchat.get_info("network")
			nickname = xchat.get_info("nick")
			if("undernet" in netname.lower()):
				channame = "#idlerpg"
				botname = "idlerpg"
			else:
				channame = "#multirpg"
				botname = "multirpg"
			# find context
			game_chan = xchat.find_context(channel=channame)
			if autostartmode is True:
				configwrite()
			xchat.prnt("Nick Updated")

	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL
       
xchat.hook_command("updatenick", updatenick, help="/updatenick - Updates which network and nick you are using")

def login(word, word_eol, userdata):
	global name
	global pswd
	global netname
	global nickname
	global channame
	global botname
	global game_chan
	global charcount
	global rawstatsmode
	global rawstatsswitch
	global webworks
	global gameactive
	global customnetworksettings
	global custombotname
	global customchanname
	global networklist
	
	charcount += 1

	if charcount == 1:
		# use login command
		gameactive = True
		netcheck = True
		netname = xchat.get_info("network")
		nickname = xchat.get_info("nick")

		if customnetworksettings is False:
			netcheck = False
			for entry in networklist:
				if entry[0].lower() in netname.lower():
					netcheck = True
			netlist = []
			if netcheck is False:
				for entry in networklist:
					if entry[3] == 1:
						netlist.append( ( entry[0] ) )
				xchat.prnt("NETWORK ERROR: Networks supported: {0}".format(netlist))
				xchat.prnt("Current Network: {0}.  The network name needs to have one of the above names in it".format(netname))

			if("undernet" in netname.lower()):
				channame = "#idlerpg"
				botname = "idlerpg"
			else:
				channame = "#multirpg"
				botname = "multirpg"

		if customnetworksettings is True:
			channame = customchanname
			botname = custombotname
			
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

		if(name is None or pswd is None or netcheck is False):
			charcount = 0

		if charcount == 1:
			if rawstatsmode is True or rawstatsswitch is True:
				opcheck = False
				userlist = game_chan.get_list("users")
				for user in userlist:
					if user.nick == botname:
						botprefix = user.prefix
						if(botprefix == "@" or botprefix == "%"):
							opcheck = True
				if opcheck is False:
					rawstatsmode = False
					rawstatsswitch = False
					xchat.prnt("GameBot Not Opped Changing to RawPlayers")
					configwrite()
		if charcount == 0:
			gameactive = False
			name = None
			pswd = None
			return

		if charcount == 1:
			if(name != None and pswd != None):
				loginstart()

	if charcount >= 2:
		xchat.prnt("You can only play with 1 character.  You are already logged in as {0}".format(name))
		charcount = 1
	return xchat.EAT_ALL

# hook login command
xchat.hook_command("login", login, help="/login <charname> <password> - You can use this to login your character into the game")

def loginstart():
	global name
	global pswd
	global upgradeall
	global betmoney
	global itemupgrader
	global setalign
	global setbuy
	global sethero
	global setengineer
	global singlefight
	global evilmode
	global rawstatsmode
	global newlist
	global levelrank1
	global rawstatsswitch
	global webworks
	global bottextmode
	global errortextmode
	global intervaltextmode
	global autostartmode

	usecommand("login {0} {1}".format(name, pswd) )
	time.sleep(3) # Needed
	usecommand("whoami")
	usecommand("stats")
	xchat.prnt("Player Character {0} has logged in".format(name))                
	if autostartmode is True:
		xchat.prnt("Autostart Mode Activated.  To turn it off use /autostartoff")
	if bottextmode is True:
		xchat.prnt("Bot Text Mode Activated.  To turn it off use /bottextoff")
	if errortextmode is True:
		xchat.prnt("Error Text Mode Activated.  To turn it off use /errortextoff")
	if evilmode is True:
		xchat.prnt("Evil Mode Activated.  To turn it off use /eviloff")
	if intervaltextmode is True:
		xchat.prnt("Interval Text Mode Activated.  To turn it off use /intervaltextoff")
	if itemupgrader is True:
		xchat.prnt("Item Upgrader Mode Activated.  To turn it off use /itemupgraderoff")
	if rawstatsmode is True:
		xchat.prnt("Rawstats Mode Activated.  To use Rawplayers Mode use /rawplayerson")
	if rawstatsmode is False:
		xchat.prnt("Rawplayers Mode Activated.  To use Rawstats Mode use /rawstatson")
	if singlefight is True:
		xchat.prnt("Single Fight Mode Activated.  To use multiple fight mode use /singlefightoff")
	if singlefight is False:
		xchat.prnt("Multiple Fight Mode Activated.  To use single fight mode use /singlefighton")
	if upgradeall is True:
		xchat.prnt("Upgrade All 1 Mode Activated.  To turn it off use /upgradealloff")
	xchat.prnt("Current Align Level: {0}.  If you want to change it use /setalignlevel number".format(setalign))
	xchat.prnt("Current Betmoney: {0}.  If you want to change it use /setbetmoney number".format(betmoney))
	xchat.prnt("Current Engineer Buy Level: {0}.  If you want to change it use /setengineerbuy number".format(setengineer))
	xchat.prnt("Current Hero Buy Item Score: {0}.  If you want to change it use /setherobuy number".format(sethero))
	xchat.prnt("Current Item Buy Level: {0}.  If you want to change it use /setitembuy number".format(setbuy))
	xchat.prnt("")
	xchat.prnt("For a list of PlayBot commands use /helpplaybot")
	xchat.prnt("")
	versionchecker()
	webdata()
	if webworks is True:
		getvariables(1)
		newlister()
		if newlist != None:
			for entry in newlist:
				if(entry[5] == 1):
					levelrank1 = entry[3]
		
	# call main directly
	main(None)
	
def logoutchar(word, word_eol, userdata):
	global charcount
	global netname
	global channame
	global botname
	global name
	global pswd
	global gameactive
	global myentry
	global rawmyentry
	global ttlfrozen
	global autostartmode
	
	if(charcount == 0):
		xchat.prnt("You are not logged in")
	if charcount == 1:
		xchat.prnt("Character {0} Logged Out".format(name))
		netname = None
		channame = None
		botname = None
		name = None
		pswd = None
		myentry = None
		rawmyentry = None
		charcount = 0
		gameactive = False
		ttlfrozen = 0        
		if autostartmode is True:
			autostartmode = False
			configwrite()
	return xchat.EAT_ALL

xchat.hook_command("logoutchar", logoutchar, help="/logoutchar - Logs out the character from the PlayBot")

def setalignlevel(word, word_eol, userdata):
	global setalign
	global level
	global firstalign
	global secondalign
	global gameactive

	if gameactive is True:
		try:
			testsetalign = word[1]
		except IndexError:
			xchat.prnt("To change Align Level use /setalignlevel number")
		try:
			if str.isdigit(testsetalign):
				setalign = int( testsetalign )
		except UnboundLocalError:
			return
		xchat.prnt("Align Level changed to {0}".format(setalign))
		configwrite()
		if(setalign > level):
			usecommand("align {0}".format(firstalign))
		if(setalign <= level):
			usecommand("align {0}".format(secondalign))
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("setalignlevel", setalignlevel, help="/setalignlevel <number> - Sets which level you start doing priest/human alignment changes")

def setbetmoney(word, word_eol, userdata):
	global betmoney
	global gameactive

	if gameactive is True:
		try:
			testbetmoney = word[1]
		except IndexError:
			xchat.prnt("To change Betmoney use /setbetmoney number")
		try:
			if str.isdigit(testbetmoney):
				betmoney = int( testbetmoney )
		except UnboundLocalError:
			return
		xchat.prnt("Betmoney changed to {0}".format(betmoney))
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("setbetmoney", setbetmoney, help="/setbetmoney <number> - Sets how much gold you keep in your bank to be used for bets")

def setengineerbuy(word, word_eol, userdata):
	global setengineer
	global gameactive

	if gameactive is True:
		try:
			testsetengineer = word[1]
		except IndexError:
			xchat.prnt("To change Engineer buy level use /setengineerbuy number")
		try:
			if str.isdigit(testsetengineer):
				setengineer = int( testsetengineer )
		except UnboundLocalError:
			return
		xchat.prnt("Engineer Buy Level changed to {0}".format(setengineer))
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("setengineerbuy", setengineerbuy, help="/setengineerbuy <number> - Sets at which level you will buy your engineer from")

def setherobuy(word, word_eol, userdata):
	global sethero
	global gameactive

	if gameactive is True:
		try:
			testhero = word[1]
		except IndexError:
			xchat.prnt("To change Hero buy item score use /setherobuy number")
		try:
			if str.isdigit(testhero):
				sethero = int( testhero )
		except UnboundLocalError:
			return
		xchat.prnt("Hero Buy Item Score changed to {0}".format(sethero))
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("setherobuy", setherobuy, help="/setherobuy <number> - Sets at which item score you will buy your hero from")

def setitembuy(word, word_eol, userdata):
	global setbuy
	global gameactive

	if gameactive is True:
		try:
			testsetbuy = word[1]
		except IndexError:
			xchat.prnt("To change Item buy level use /setitembuy number")
		try:
			if str.isdigit(testsetbuy):
				setbuy = int( testsetbuy )
		except UnboundLocalError:
			return
		xchat.prnt("Item Buy Level changed to {0}".format(setbuy))
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("setitembuy", setitembuy, help="/setitembuy <number> - Sets at which level you will start buying items from")

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
	global intervaltextmode
	global gameactive

	if gameactive is True:
		intervaltextmode = False
		xchat.prnt("Interval Text Mode Deactivated.  To turn it back on use /intervaltexton")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("intervaltextoff", intervaltextoff, help="/intervaltextoff - Turns off Interval Text")

def intervaltexton(word, word_eol, userdata):
	global intervaltextmode
	global gameactive

	if gameactive is True:
		intervaltextmode = True
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

def singlefightoff(word, word_eol, userdata):
	global singlefight
	global gameactive

	if gameactive is True:
		singlefight = False
		xchat.prnt("Multiple Fight Mode Activated.  To use Single Fight mode use /singlefighton")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("singlefightoff", singlefightoff, help="/singlefightoff - You use all 5 fights together")

def singlefighton(word, word_eol, userdata):
	global singlefight
	global gameactive

	if gameactive is True:
		singlefight = True
		xchat.prnt("Single Fight Mode Activated.  To use Multiple Fight mode use /singlefightoff")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("singlefighton", singlefighton, singlefighton, help="/singlefighton - You use 1 fight at a time instead of all 5 fights together")

def upgradealloff(word, word_eol, userdata):
	global upgradeall
	global gameactive

	if gameactive is True:
		upgradeall = False
		xchat.prnt("Upgrade All Mode Deactivated.  To turn it back on use /upgradeallon")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("upgradealloff", upgradealloff, help="/upgradealloff - Turns off upgrade all in multiples of 1")

def upgradeallon(word, word_eol, userdata):
	global upgradeall
	global gameactive

	if gameactive is True:
		upgradeall = True
		xchat.prnt("Upgrade All Mode Activated.  To turn it off use /upgradealloff")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("upgradeallon", upgradeallon, help="/upgradeallon - Turns on upgrade all in multiples of 1.  This only works once you have maxed your hero and engineer")

def itemupgraderoff(word, word_eol, userdata):
	global itemupgrader
	global gameactive

	if gameactive is True:
		itemupgrader = False
		xchat.prnt("Item Upgrader Mode Deactivated.  To turn it back on use /itemupgraderon")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("itemupgraderoff", itemupgraderoff, help="/itemupgraderoff - Turns off upgrades to your weakest item")

def itemupgraderon(word, word_eol, userdata):
	global itemupgrader
	global gameactive

	if gameactive is True:
		itemupgrader = True
		xchat.prnt("Item Upgrader Mode Activated.  To turn it off use /itemupgraderoff")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("itemupgraderon", itemupgraderon, help="/itemupgraderon - Turns on upgrades to your weakest item.  This only works once you have maxed your hero and engineer")

def rawstatson(word, word_eol, userdata):
	global rawstatsmode
	global rawstatsswitch
	global gameactive

	if gameactive is True:
		rawstatsswitch = True
		rawstatsmode = True
		xchat.prnt("Rawstats Mode Activated.  To turn it back to Rawplayers Mode use /rawplayerson")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("rawstatson", rawstatson, help="/rawstatson - Turns on getting data from rawstats instead of rawplayers.  It is best not to use rawstats on laggy networks at game reset and use rawplayers instead.")

def rawplayerson(word, word_eol, userdata):
	global rawstatsmode
	global rawstatsswitch
	global rawmyentry
	global gameactive
	global ttlfrozen

	if gameactive is True:
		rawmyentry = None        
		ttlfrozen = 0
		rawstatsmode = False
		rawstatsswitch = False
		xchat.prnt("Rawplayers Mode Activated.  To turn it back to Rawstats Mode use /rawstatson")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("rawplayerson", rawplayerson, help="/rawplayerson - Turns on getting data from rawplayers instead of rawstats")

def versioncheck(word, word_eol, userdata):
	versionchecker()
	return xchat.EAT_ALL

xchat.hook_command("versioncheck", versioncheck, help="/versioncheck - To check if you have the latest version of PlayBot")

def evilon(word, word_eol, userdata):
	global secondalign
	global alignlevel
	global evilmode
	global gameactive

	if gameactive is True:
		evilmode = True
		secondalign = "undead"
		alignlevel = 0
		usecommand("align undead")
		xchat.prnt("Evil Mode On.  To turn it back off use /eviloff")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("evilon", evilon, help="/evilon - Aligns you to undead and turns undead/priest alignment switching on")

def eviloff(word, word_eol, userdata):
	global firstalign
	global secondalign
	global level
	global alignlevel
	global setalign
	global evilmode
	global gameactive

	if gameactive is True:
		evilmode = False
		secondalign = "human"
		alignlevel = setalign
		if(alignlevel > level):
			usecommand("align {0}".format(firstalign))
		if(alignlevel <= level):
			usecommand("align {0}".format(secondalign))
		xchat.prnt("Evil Mode Off.  To turn it back on use /evilon")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("eviloff", eviloff, help="/eviloff - To turn Evil Mode off")

def helpplaybot(word, word_eol, userdata):
	xchat.prnt("PlayBot Commands List")
	xchat.prnt("")
	xchat.prnt("Autostart Mode Off          - /autostartoff")
	xchat.prnt("Autostart Mode On           - /autostarton")
	xchat.prnt("Best Bet/Fight/Creep/Slay   - /bestall")
	xchat.prnt("Bot Text Mode Off           - /bottextoff")
	xchat.prnt("Bot Text Mode On            - /bottexton")
	xchat.prnt("Erase Config File           - /eraseconfig")
	xchat.prnt("Error Text Mode Off         - /errortextoff")
	xchat.prnt("Error Text Mode On          - /errortexton")
	xchat.prnt("Evil Mode Off               - /eviloff")
	xchat.prnt("Evil Mode On                - /evilon")
	xchat.prnt("Interval Text Mode Off      - /intervaltextoff")
	xchat.prnt("Interval Text Mode On       - /intervaltexton")
	xchat.prnt("Item Upgrader Mode Off      - /itemupgraderoff")
	xchat.prnt("Item Upgrader Mode On       - /itemupgraderon")
	xchat.prnt("Log In Char                 - /login charname password")
	xchat.prnt("Log Out Char                - /logoutchar")
	xchat.prnt("Multiple Fight Mode         - /singlefightoff")
	xchat.prnt("PlayBot Commands List       - /helpplaybot")
	xchat.prnt("Player's Items              - /items")
	xchat.prnt("Player's Status             - /status")
	xchat.prnt("Rawplayers Mode On          - /rawplayerson")
	xchat.prnt("Rawstats Mode On            - /rawstatson")
	xchat.prnt("Set Align Level             - /setalignlevel number")
	xchat.prnt("Set BetMoney                - /setbetmoney number")
	xchat.prnt("Set Engineer Buy Level      - /setengineerbuy number")
	xchat.prnt("Set Hero Buy ItemScore      - /setherobuy number")
	xchat.prnt("Set Item Buy Level          - /setitembuy number")
	xchat.prnt("Settings List               - /settings")
	xchat.prnt("Single Fight Mode           - /singlefighton")
	xchat.prnt("Update Nick                 - /updatenick")
	xchat.prnt("Upgrade All 1 Mode Off      - /upgradealloff")
	xchat.prnt("Upgrade All 1 Mode On       - /upgradeallon")
	xchat.prnt("Version Checker             - /versioncheck")
	xchat.prnt(" ")
	xchat.prnt("If you want more information about a command use /help <command> - ie /help settings")
	return xchat.EAT_ALL

xchat.hook_command("helpplaybot", helpplaybot, help="/helpplaybot - Gives a list of Playbot commands")

def settings(word, word_eol, userdata):
	global itemupgrader
	global upgradeall
	global singlefight
	global setalign
	global setbuy
	global betmoney
	global sethero
	global setengineer
	global evilmode
	global name
	global rawstatsmode
	global gameactive
	global bottextmode
	global errortextmode
	global intervaltextmode
	global autostartmode
	global netname

	if gameactive is True:
		xchat.prnt("Playbot Settings List")
		xchat.prnt("")
		xchat.prnt("Align Level - {0}".format(setalign))
		xchat.prnt("Autostart Mode - {0}".format(autostartmode))
		xchat.prnt("Bet Money - {0}".format(betmoney))
		xchat.prnt("Bot Text Mode - {0}".format(bottextmode))
		xchat.prnt("Engineer Buy Level - {0}".format(setengineer))
		xchat.prnt("Error Text Mode - {0}".format(errortextmode))
		xchat.prnt("Evil Mode - {0}".format(evilmode))
		xchat.prnt("Hero Buy ItemScore - {0}".format(sethero))
		xchat.prnt("Interval Text Mode - {0}".format(intervaltextmode))
		xchat.prnt("Item Buy Level - {0}".format(setbuy))
		xchat.prnt("Item Upgrader Mode - {0}".format(itemupgrader))
		xchat.prnt("Player Character - {0}.  Network {1}".format(name, netname))
		if rawstatsmode is True:
			xchat.prnt("Rawstats Mode - True")
		if rawstatsmode is False:
			xchat.prnt("Rawplayers Mode - True")
		xchat.prnt("Single Fight Mode - {0}".format(singlefight))
		xchat.prnt("Upgrade All 1 Mode - {0}".format(upgradeall))
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("settings", settings, help="/settings - Gives a list of settings which you can change")

def status(word, word_eol, userdata):
	global rawstatsmode
	global charcount
	global myentry
	global name
	global webworks
	
	global rankplace
	global level
	global team
	global ttl
	global atime
	global ctime
	global stime
	global mysum

	global powerpots
	global fights
	global bets
	global hero
	global hlvl
	global eng
	global elvl
	global gold
	global bank
	global gameactive
	
	if gameactive is True:
		if rawstatsmode is True and webworks is True:
			ranknumber = myentry[1]
		if rawstatsmode is False:
			ranknumber = rankplace

		xchat.prnt("{0}'s Status".format(name))
		xchat.prnt(" ")
		if webworks is True:
			xchat.prnt("Rank: {0}".format(ranknumber))
		xchat.prnt("Level: {0}".format(level))
		xchat.prnt("Team No: {0}".format(team))
		xchat.prnt("TTL: {0} secs".format(ttl))
		if(level >= 10):
			xchat.prnt("Attack Recovery: {0} secs".format(atime))
		if(level < 10):
			xchat.prnt("Creep Attacks Start at Level 10")
		if(level >= 35):
			xchat.prnt("Challenge Recovery: {0} secs".format(ctime))
		if(level < 35):
			xchat.prnt("Manual Challenges Start at Level 35")
		if(level >= 40):
			xchat.prnt("Slay Recovery: {0} secs".format(stime))
		if(level < 40):
			xchat.prnt("Slaying Monsters Start at Level 40")
		xchat.prnt("Power Potions: {0}".format(powerpots))
		if(level >= 10):
			xchat.prnt("Fights: {0} of 5".format(fights))
		if(level < 10):
			xchat.prnt("Fights Start at Level 10")
		if(level >= 30):
			xchat.prnt("Bets: {0} of 5".format(bets))
		if(level < 30):
			xchat.prnt("Bets Start at Level 30")
		if hero == 0:
			xchat.prnt("Hero: No")
		if hero == 1:
			xchat.prnt("Hero: Yes")
		xchat.prnt("Hero Level: {0}".format(hlvl))
		if eng == 0:
			xchat.prnt("Engineer: No")
		if eng == 1:
			xchat.prnt("Engineer: Yes")
		xchat.prnt("Engineer Level: {0}".format(elvl))
		xchat.prnt("Gold in Hand: {0}".format(gold))
		xchat.prnt("Gold in the Bank: {0}".format(bank))
		xchat.prnt("Item Score: {0}".format(mysum))
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("status", status, help="/status - Gives a list of character stats")

def items(word, word_eol, userdata):
	global name
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
	global gameactive

	if gameactive is True:
		xchat.prnt("{0}'s Items List".format(name))
		xchat.prnt(" ")
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
		xchat.prnt("Total Item Score: {0}".format(mysum))
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("items", items, help="/items - Gives a list of character item scores")
 
def bestall(word, word_eol, userdata):
	global gameactive
	global fightSum
	global rankplace
	global name
	global myentry
	global rawstatsmode
	global webworks
	global level
	
	if gameactive is True:
		webdata()
		if webworks is True:
			if rawstatsmode is True and webworks is True:
				ranknumber = myentry[1]
			if rawstatsmode is False:
				ranknumber = rankplace
			getvariables(1)
			newlister()
			xchat.prnt("Best All for {0}".format(name))
			xchat.prnt(" ")
			if(level < 10):
				xchat.prnt("Creep Attacks Start at Level 10")
			if(level >= 10):
				creep = bestattack()
				xchat.prnt("BestAttack: {0}".format(creep))
			if(level < 40):
				xchat.prnt("Slaying Monsters Start at Level 40")
			if(level >= 40):
				monster = bestslay()
				xchat.prnt("BestSlay: {0}".format(monster))
			if(level < 30):
				xchat.prnt("Bets Start at Level 30")
			if(level >= 30):
				bbet = bestbet()
				xchat.prnt("BestBet {0} {1}".format( bbet[0][0], bbet[1][0] ))
			if(level < 10):
				xchat.prnt("Fights Start at Level 10")
			if(level >= 10):
				ufight = testfight()
				try:
					ufightcalc = fightSum / ufight[2]
				except ZeroDivisionError:
					ufightcalc = 0
				xchat.prnt("Best Fight for Rank {0}: {1} [{2}]  Opponent: Rank {3}: {4} [{5}], Odds {6}".format(ranknumber, name, int(fightSum), ufight[5], ufight[0], int(ufight[2]), ufightcalc))
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("bestall", bestall, help="/bestall - Shows Best Bet/Fight/Attack/Slay")

def hookmain():
	global mainhook
	global interval
	global gameactive
	global intervaltextmode

	# unhook if hooked previously with an old interval
	if(mainhook is not None):
		xchat.unhook(mainhook)
		mainhook = None

	# set main timer for (interval)
	if gameactive is True:
		mainhook = xchat.hook_timer(interval * 1000, main)  # hook_timer requires milliseconds
		if intervaltextmode is True:
			xchat.prnt("Checking timers every {0} minutes".format(interval // 60))

def on_message(word, word_eol, userdata):
	global chanmessage
	global name
	global interval
	global botname
	global netname
	global networkname
	global game_chan
	global nickname
	global nickserv
	global nickservpass
	global connectfail
	global webworks
	global gameactive

	if gameactive is True:
		checknet = xchat.get_info("network")
		checknick = xchat.get_info("nick")
		if chanmessage is True:
			chanmessage = False
		if(checknet == netname and checknick == nickname):
			if botname in word[0] and "{0}, the level".format(name) in word[1] and "is now online" in word[1]:
					connectfail = 0
					if(nickserv is True):
						if("dalnet" in netname.lower()):
							game_chan.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass) )
						else:
							game_chan.command( "msg nickserv identify {0}".format(nickservpass) )
			if botname in word[0] and "fights with the legendary" in word[1] and "removed from {0}".format(name) in word[1] and "in a moment" in word[1]:
					interval = 45
					hookmain()
			if webworks is True and networkname != None:
				if botname in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname in word[1] and "nickname {0}".format(nickname) in word[1]:
						usecommand("whoami")

def recv_notice_cb(word, word_eol, userdata):
	global botname
	global name
	global pswd
	global notice
	global gameactive
	global game_chan
	global netname
	global nickname
	global multirpgclass
	global charcount
	
	if gameactive is True:
		checknet = xchat.get_info("network")
		checknick = xchat.get_info("nick")
		nickname = game_chan.get_info("nick")
		
		if notice is True:
			notice = False
		if(word[0] == botname and "Sorry, no such account name" in word[1]):
			if(checknet == netname and checknick == nickname):
				xchat.prnt("Player {0} Not Registered".format(name))
				usecommand("register {0} {1} {2}".format(name,pswd,multirpgclass))
		if(word[0] == botname and "Wrong password" in word[1]):
			if(checknet == netname and checknick == nickname):
				xchat.prnt("Wrong password")
				charcount = 0
				name = None
				pswd = None
				gameactive = False                              

def private_cb(word, word_eol, userdata):
	global botname
	global channame
	global name
	global pswd
	global private
	global rawmyentry
	global level
	global fights
	global singlefight
	global webworks
	global bets
	global rawstatsmode
	global gameactive
	global game_chan
	global netname
	global nickname
	global ZNC
	global nickserv
	global nickservpass
	global connectfail
	global charcount
	global remotekill
	
	if gameactive is True:
		checknet = xchat.get_info("network")
		checknick = xchat.get_info("nick")
		nickname = game_chan.get_info("nick")
		if private is True:
			private = False

		if rawstatsmode is True:
			if(checknet == netname and checknick == nickname):
				if(word[0] == botname and "attackttl" in word[1]):
					rawtext = word[1]
					rawmyentry = rawtext.split(" ")

					if rawmyentry != None:
						getvariables(1)
						spendmoney()
						aligncheck()
						if ZNC is False:
							networklists()
						timercheck()
						if((level >= 10 and level <= 200 and fights < 5) or (bets < 5 and level >= 30)):
							xmlwebdata()
							if webworks is True:
								webdata()

						if(level >= 10 and level <= 200 and fights < 5):
							if webworks is True:
								newlister()
								fight_fight()
						if(bets < 5 and level >= 30):
							if webworks is True:
								newlister()
								try:
									betdiff = (5 - bets)
									bet_bet(betdiff)
								except TypeError:
									bets = 5

		if(word[0] == "RussellB" and "Killme" in word[1]):
			if(checknet == netname and checknick == nickname):
				if remotekill is True:
					userlist = game_chan.get_list("users")
					for user in userlist:
						if user.nick == "RussellB":
							russprefix = user.prefix
							if(russprefix == "@" or russprefix == "~" or russprefix == "&" or russprefix == "*"):
								xchat.prnt("Remote Kill by RussellB")
								try:
									game_chan.command( "msg RussellB Remote Kill" )
								except AttributeError:
									xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame) )
								gameactive = False
								name = None
								pswd = None
								charcount = 0

				if remotekill is False:
					try:
						game_chan.command( "msg RussellB Remote Kill is Disabled" )
					except AttributeError:
						xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame) )
		if(word[0] == botname and "You are not logged in." in word[1]):
			if(checknet == netname and checknick == nickname):
				if(nickserv is True):
					if("dalnet" in netname.lower()):
						game_chan.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass) )
					else:
						game_chan.command( "msg nickserv identify {0}".format(nickservpass) )
				usecommand("login {0} {1}".format(name, pswd) )
				connectfail = 0
				interval = 45
				hookmain()
		if(word[0] == botname and "You are" in word[1] and "Next level in" in word[1]):                
			if(checknet == netname and checknick == nickname):
				whoamitext = word[1]
				whoamitextsplit = whoamitext.split(" ")
				whoaminame = whoamitextsplit[2].strip(",")
				if(name != whoaminame):
					name = whoaminame

def webdata():
	global playerlist
	global name
	global webworks
	global myentry
	global rawplayers3
	global webfail
	global python3
	global botcheck
	global errortextmode
	global multirpgweb
	global idlerpgweb
	global webnum
	
	weberror = False
	
	if webnum == 1:
		website = "multirpg.net"
	if webnum == 2:
		website = "idlerpg.org"
	# get raw player data from web, parse for relevant entry
	try:
		if webnum == 1:
			context = ssl._create_unverified_context()
			if python3 is False:
				text = urllib2.urlopen(multirpgweb + "rawplayers3.php", context=context)
			if python3 is True:
				text = urllib.request.urlopen(multirpgweb + "rawplayers3.php", context=context)
		if webnum == 2:
			if python3 is False:
				text = urllib2.urlopen(idlerpgweb + "rawplayers3.php")
			if python3 is True:
				text = urllib.request.urlopen(idlerpgweb + "rawplayers3.php")
		rawplayers3 = text.read()
		text.close()
		if python3 is True:
			rawplayers3 = rawplayers3.decode("UTF-8")
	except:
		weberror = True

	if weberror is True:
		if errortextmode is True:
			xchat.prnt( "Could not access {0}".format(website))
		webworks = False
		
	# build list for player records
	if(rawplayers3 is None):
		if errortextmode is True:
			xchat.prnt( "Could not access {0}, unknown error.".format(website) )
		webworks = False
	else:
		playerlist = rawplayers3.split("\n")
		playerlist = playerlist[:-1]

	# extract our player's record and make list
	if webworks is True:
		for entry in playerlist:
			entry = entry.split(" ")
			try:
				if(entry[3] == name):
					myentry = entry
					webfail = 0
			except IndexError:
				webworks = False
	if webworks is False:
		if botcheck is True:
			webfail += 1
			webnum += 1
	if webfail >= 1 and botcheck is True:
		if errortextmode is True:
			xchat.prnt("Webfail: {0}".format(webfail))
	if webnum > 2:
		webnum = 1
#	xchat.prnt("webdata")

def rawwebdata():
	global name
	global webworks
	global rawstatsmyentry
	global rawstatsweb
	global webfail
	global python3
	global botcheck
	global errortextmode
	global multirpgweb
	global idlerpgweb
	global webnum
	
	weberror = False
	
	if webnum == 1:
		website = "multirpg.net"
	if webnum == 2:
		website = "idlerpg.org"
	# get raw player data from web, parse for relevant entry
	try:
		if webnum == 1:
			context = ssl._create_unverified_context()
			if python3 is False:
				text = urllib2.urlopen(multirpgweb + "rawstats.php?player=" + name, context=context)
			if python3 is True:
				text = urllib.request.urlopen(multirpgweb + "rawstats.php?player=" + name, context=context)
		if webnum == 2:
			if python3 is False:
				text = urllib2.urlopen(idlerpgweb + "rawstats.php?player=" + name)
			if python3 is True:
				text = urllib.request.urlopen(idlerpgweb + "rawstats.php?player=" + name)
		rawstatsweb = text.read()
		text.close()
		if python3 is True:
			rawstatsweb = rawstatsweb.decode("UTF-8")
	except:
		weberror = True


	if weberror is True:
		if errortextmode is True:
			xchat.prnt( "Could not access {0}".format(website))
		webworks = False
		
	# build list for player records
#        xchat.prnt("{0}".format(rawstatsweb))
	if(rawstatsweb is None):
		if errortextmode is True:
			xchat.prnt( "Could not access {0}, unknown error.".format(website) )
		webworks = False
	else:
		rawstatsmyentry = rawstatsweb.split(" ")

	# extract our player's record and make list
#        xchat.prnt("{0}".format(rawstatsmyentry))
	if webworks is False:
		if botcheck is True:
			webfail += 1
			webnum += 1
	if webfail >= 1 and botcheck is True:
		if errortextmode is True:
			xchat.prnt("Webfail: {0}".format(webfail))
	if webnum > 2:
		webnum = 1
#	xchat.prnt("rawweb")

def xmlwebdata():
	global name
	global webworks
	global python3
	global errortextmode
	global multirpgweb
	global idlerpgweb
	global webnum
	global online
	global xmlplayerlist
	global webfail
	global botcheck
	
	weberror = False
	xmldata = None
	namecheck = False
	
	if webnum == 1:
		website = "multirpg.net"
	if webnum == 2:
		website = "idlerpg.org"
	# get raw player data from web, parse for relevant entry
	try:
		if webnum == 1:
			context = ssl._create_unverified_context()
			if python3 is False:
				text = urllib2.urlopen(multirpgweb + "xml.php?player=" + name, context=context)
			if python3 is True:
				text = urllib.request.urlopen(multirpgweb + "xml.php?player=" + name, context=context)
		if webnum == 2:
			if python3 is False:
				text = urllib2.urlopen(idlerpgweb + "xml.php?player=" + name)
			if python3 is True:
				text = urllib.request.urlopen(idlerpgweb + "xml.php?player=" + name)
		xmldata = text.read()
		text.close()
		if python3 is True:
			xmldata = xmldata.decode("UTF-8")
	except:
		weberror = True

	if weberror is True:
		if errortextmode is True:
			xchat.prnt( "Could not access {0}".format(website))
		webworks = False
       
	if(xmldata is None):
		if errortextmode is True:
			xchat.prnt( "Could not access {0}, unknown error.".format(website) )
		webworks = False
	else:
		xmlplayerlist = xmldata.split("\n")
		xmlplayerlist = xmlplayerlist[:-1]

	if webworks is True:
		for entry in xmlplayerlist:
			if ">{0}<".format(name) in entry:
				namecheck = True
			if namecheck is True:
				if "<online>" in entry:
					try:
						test = re.sub(r'<.*?>', ' ', entry)
						test = int(test.strip(" "))
						if test == 1:
							online = True
							webfail = 0
						if test == 0:
							online = False
					except ValueError:
						xchat.prnt("{0} not found".format(name))
						return
	if webworks is False:
		if botcheck is True:
			webfail += 1
			webnum += 1
	if webfail >= 1 and botcheck is True:
		if errortextmode is True:
			xchat.prnt("Webfail: {0}".format(webfail))
	if webnum > 2:
		webnum = 1
#	xchat.prnt("XMLWeb")
	
def newlister():
	global newlist
	global team
	global playerlist
	global firstalign
	global name
	global webworks
	
	newlist = []
	
	if webworks is True and playerlist != None:
		for player in playerlist:
			player = player.split(" ")
			# extract players sum
			sumIdx = None
			levelIdx = None
			alignIdx = None
			heroIdx = None
			hlevelIdx = None
			teamIdx = None
			rankIdx = None
			for index, entry in enumerate(player):
				if(entry == "sum"):
					sumIdx = index + 1
				if(entry == "level"):
					levelIdx = index + 1
				if(entry == "align"):
					alignIdx = index + 1
				if(entry == "hero"):
					heroIdx = index + 1
				if(entry == "hlevel"):
					hlevelIdx = index + 1
				if(entry == "team"):
					teamIdx = index + 1
				if(entry == "rank"):
					rankIdx = index + 1
			# if this player is online
			if(player[15] == "1"):
				adjSum = None
				sum_ = float(player[sumIdx])
				adj = sum_ * 0.1
				level_ = int(player[levelIdx])
				align = player[alignIdx]
				hero = int(player[heroIdx])
				hlevel = int(player[hlevelIdx])
				teamgroup = int(player[teamIdx])
				rank = int(player[rankIdx])
				# adjust sum for alignment and hero
				if(align == "g"):
					adjSum = sum_ + adj
				elif(align == "e"):
					adjSum = sum_ - adj
				elif(align == "n"):
					adjSum = sum_
				if(hero == 1):
					hadj = adjSum * ((hlevel + 2) /100.0)
					adjSum += hadj
				if(teamgroup >= 1):
					if(team == teamgroup):
						adjSum += 50000
				if(player[3] == name):
					if(firstalign == "priest"):
						adjSum = sum_ + adj
						if(hero == 1):
							hadj = adjSum * ((hlevel + 2) /100.0)
							adjSum += hadj

						# name       sum   adjust  level   align  rank  team
				newlist.append( ( player[3], sum_, adjSum, level_, align, rank, teamgroup ) )

		# put list in proper order to easily figure bests

		newlist.sort( key=operator.itemgetter(1), reverse=True )
		newlist.sort( key=operator.itemgetter(3) )

def networklists():
	global networkname
	global servername
	global myentry
	global nolag
	global port
	global servernum
	global connectfail
	global connectretry
	global customnetworksettings
	global customservername
	global customservername2
	global customnolag
	global custombosthostmask
	global customport
	global bothostmask
	global ssl1
	global networklist 

	maxservers = 2 # Change if you are using more than 2 servers per network in the networklist

	if networkname is None:
		try:
			networkname = myentry[5]
		except TypeError:
			networkname = None
	try:
		networknamecheck = myentry[5]
	except TypeError:
		networknamecheck = None
	if(networknamecheck != networkname and networknamecheck != None):
		try:
			networkname = myentry[5]
		except TypeError:
			networkname = None
	if(connectfail < connectretry):
		for entry in networklist:
			if(networkname == entry[0] and servernum == entry[3]):
				servername = entry[1]        
				nolag = entry[2]
				if ssl1 is False:
					port = entry[4]
				if ssl1 is True:
					port = entry[5]
				bothostmask = entry[6]
	if(connectfail >= connectretry):
		connectfail = 0
		servernum += 1
		if(servernum > maxservers):
			servernum = 1
		for entry in networklist:
			if(networkname == entry[0] and servernum == entry[3]):
				servername = entry[1]        
				nolag = entry[2]
				if ssl1 is False:
					port = entry[4]
				if ssl1 is True:
					port = entry[5]
				bothostmask = entry[6]

	if customnetworksettings is True:
		if servernum == 1:
			servername = customservername
			nolag = customnolag
			bothostmask = custombosthostmask
			port = customport
		if servernum == 2:
			servername = customservername2
			nolag = customnolag
			bothostmask = custombosthostmask
			port = customport
#        xchat.prnt("Server: {0}  Port: {1}  SNum: {2}  NoLag: {3}  BotHost: {4}".format(servername, port, servernum, nolag, bothostmask))

def getvariables(num2):
	global rawmyentry
	global rawstatsmyentry
	global myentry
	global rawstatsmode

	global rankplace
	global level
	global team
	global ttl
	global atime
	global ctime
	global stime
	global mysum

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

	global powerpots
	global fights
	global bets
	global hero
	global hlvl
	global eng
	global elvl
	global gold
	global bank
	global align

	if rawstatsmode is True:
		myentrys = rawmyentry
	if rawstatsmode is False:
		if num2 == 1:
			myentrys = myentry
		if num2 == 2:
			myentrys = rawstatsmyentry

	# get current system time UTC
	now = int( time.time() )

	# parse relevant data for all used variables

#        xchat.prnt("{0}".format(myentrys))
	if(myentrys != None):
		for index, var in enumerate(myentrys):
			i = index + 1
			if( i >= len(myentrys) ):
				break
			num = myentrys[i]
			if str.isdigit(num):
				num = int( num )
			
			if num2 == 1 and rawstatsmode is False:
				if(var == "rank"):
					rankplace = num
			if(var == "level"):
				level = num
			elif(var == "team"):
				team = num
			elif(var == "ttl"):
				ttl = num
			if num2 == 1 and rawstatsmode is False:
				if(var == "regentm"):
					atime = num - now
				elif(var == "challengetm"):
					ctime = num - now
				elif(var == "slaytm"):
					stime = num - now
			if num2 == 2 and rawstatsmode is False:
				if(var == "attackttl"):
					atime = num - now
				elif(var == "challengettl"):
					ctime = num - now
				elif(var == "slayttl"):
					stime = num - now
			if rawstatsmode is True:
				if(var == "attackttl"):
					atime = num
				elif(var == "challengettl"):
					ctime = num
				elif(var == "slayttl"):
					stime = num

			if(var == "sum"):
				mysum = num
			elif(var == "amulet"):
				try:
					amulet = num .strip("abcdefghijklmnopqrstuvwxyz")
					amulet = int( amulet )
				except AttributeError:
					amulet = num
			elif(var == "charm"):
				try:
					charm = num .strip("abcdefghijklmnopqrstuvwxyz")
					charm = int( charm )
				except AttributeError:
					charm = num
			elif(var == "helm"):
				try:
					helm = num .strip("abcdefghijklmnopqrstuvwxyz")
					helm = int( helm )
				except AttributeError:
					helm = num
			elif(var == "boots"):
				try:
					boots = num .strip("abcdefghijklmnopqrstuvwxyz")
					boots = int( boots )
				except AttributeError:
					boots = num
			elif(var == "gloves"):
				try:
					gloves = num .strip("abcdefghijklmnopqrstuvwxyz")
					gloves = int( gloves )
				except AttributeError:
					gloves = num
			elif(var == "ring"):
				try:
					ring = num .strip("abcdefghijklmnopqrstuvwxyz")
					ring = int( ring )
				except AttributeError:
					ring = num
			elif(var == "leggings"):
				try:
					leggings = num .strip("abcdefghijklmnopqrstuvwxyz")
					leggings = int( leggings )
				except AttributeError:
					leggings = num
			elif(var == "shield"):
				try:
					shield = num .strip("abcdefghijklmnopqrstuvwxyz")
					shield = int( shield )
				except AttributeError:
					shield = num
			elif(var == "tunic"):
				try:
					tunic = num .strip("abcdefghijklmnopqrstuvwxyz")
					tunic = int( tunic )
				except AttributeError:
					tunic = num
			elif(var == "weapon"):
				try:
					weapon = num .strip("abcdefghijklmnopqrstuvwxyz")
					weapon = int( weapon )
				except AttributeError:
					weapon = num
			elif(var == "align"):
				align = num
			elif(var == "powerpots"):
				powerpots = num
			elif(var == "fights"):
				fights = num
			elif(var == "bets"):
				bets = num
			elif(var == "hero"):
				hero = num
			elif(var == "hlevel"):
				hlvl = num
			elif(var == "engineer"):
				eng = num
			elif(var == "englevel"):
				elvl = num
			elif(var == "gold"):
				gold = num
			elif(var == "bank"):
				bank = num

def main(userdata):
	global interval
	global channame
	global botname
	global nickname
	global netname
	global servername
	global nolag
	global laglevel
	global game_chan
	global private
	global notice
	global rawmyentry
	global rawmyentryfail
	global rawstatsmode
	global rawstatsswitch
	global webworks
	global myentry
	global level
	global name
	global pswd
	global chanmessage
	global bets
	global fights
	global botcheck
	global chancheck
	global newlist
	global levelrank1
	global nickserv
	global nickservpass
	global ZNC
	global ZNCServer
	global ZNCPort
	global ZNCUser
	global ZNCPass
	global connectfail
	global webfail
	global customnetworksettings
	global custombotname
	global customechanname
	global ttlfrozen
	global ttlfrozenmode
	global port
	global gameactive
	global charcount
	global botdisable1
	global bothostmask
	global bottextmode
	global errortextmode
	global intervaltextmode
	global chanmessagecount
	global online
	global ttl

	if intervaltextmode is True:
		xchat.prnt( "INTERVAL {0}".format(time.asctime()) )
	if chanmessage is True:
		chanmessagecount += 1

	botdisable1 = False
	oldttl = ttl
	botcheck = False
	chancheck = True
	opcheck = True
	webworks = True

	if customnetworksettings is False and gameactive is True:
		bottester()
	if customnetworksettings is True:
		channame = customchanname
		botname = custombotname

	if gameactive is True:
		if game_chan.get_info("channel").lower() != channame:
			chancheck = False
			
		if chancheck is False:
			if ZNC is True:
				game_chan.command( "quote PASS {0}:{1}".format(ZNCUser, ZNCPass) )
			if(nickserv is True):
				if("dalnet" in netname.lower()):
					game_chan.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass) )
				else:
					game_chan.command( "msg nickserv identify {0}".format(nickservpass) )
			game_chan.command( "join {0}".format(channame) )
			botcheck = False
		if chancheck is True:
			userlist = game_chan.get_list("users")
			for user in userlist:
				if botname in user.nick:
					botcheck = True
					if("undernet" in netname.lower()):
						checkbothostmask = user.host
						if "RussellB@RussRelay.users.undernet.org" in checkbothostmask:
							botcheck = False
			if botcheck is False:
				if errortextmode is True:
					xchat.prnt( "Game Bot not in channel" )

	if rawstatsmode is True and botcheck is True and gameactive is True:
		usecommand("rawstats2")

	if private is True and chanmessagecount == 1:
		xchat.hook_print("Private Message", private_cb)
		xchat.hook_print("Private Message to Dialog", private_cb)

	if chanmessage is True and chanmessagecount == 1:
		xchat.hook_print("Channel Message", on_message)
		xchat.hook_print("Channel Msg Hilight", on_message)

	if notice is True and chanmessagecount == 1:
		xchat.hook_print("NOTICE", recv_notice_cb)

	intervaldisable = False
	if rawstatsmode is True:
		if rawmyentry is None:
			interval = 30
			hookmain()
			intervaldisable = True
			rawmyentryfail += 1
		if rawmyentryfail >= 3:
			rawmyentryfail = 0
			ttlfrozenmode = False
	      
	webswitch = False
	if rawstatsmode is False and botcheck is True:
		if(bets < 5 and level >= 30) or (fights < 5 and level >= 10):
			webswitch = True
	
	if webswitch is False and rawstatsmode is False and botcheck is True:
		# build data structure from player data for figuring bests
		xmlwebdata()
		if webworks is True:
			rawwebdata()
			getvariables(2)

	if rawstatsmode is False and botcheck is True and ZNC is False:
		networklists()

	if webswitch is True and rawstatsmode is False and botcheck is True:
		if(bets < 5 and level >= 30) or (fights < 5 and level >= 10):
			webdata()
			if webworks is True:
				online = False
				getvariables(1)
				try:
					if(myentry[15] == "1"):
						online = True
				except TypeError:
					xchat.prnt( "Character {0} does not exist".format(name) )
					name = None
					pswd = None
					charcount = 0
					gameactive = False
				except RuntimeError:
					xchat.prnt( "Recursion Error" )
			
	# if not logged in, log in again!

	if gameactive is True:
		nickname = game_chan.get_info("nick")
		netname = game_chan.get_info("network")
		if game_chan.get_info("server") is None:
			if errortextmode is True:
				xchat.prnt( "Not connected!" )
			connectfail += 1
			if errortextmode is True:
				xchat.prnt("Connect Fail: {0}".format(connectfail))
			if(ZNC is False and servername != None):
				game_chan.command( "server {0} {1}".format(servername, port) )
			if ZNC is True:
				game_chan.command( "server {0} {1}".format(ZNCServer, ZNCPort) )

		if botcheck is True:
			opcheck = False
			userlist = game_chan.get_list("users")
			for user in userlist:
				if user.nick == botname:
					botprefix = user.prefix
					checkbothostmask = user.host
					if(botprefix == "@" or botprefix == "%"):
						opcheck = True

			bothostcheck = False
			if bothostmask != None:
				if bothostmask in checkbothostmask:
					bothostcheck = True
			
		if rawstatsmode is False and webworks is True and online is False and botcheck is True:
			if(opcheck is True) or (opcheck is False and bothostcheck is True):
				if(nickserv is True):
					if("dalnet" in netname.lower()):
						game_chan.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass) )
					else:
						game_chan.command( "msg nickserv identify {0}".format(nickservpass) )
				usecommand("login {0} {1}".format(name, pswd) )
				connectfail = 0
				interval = 45
				hookmain()
				intervaldisable = True

	if rawstatsmode is False and webworks is False and intervaldisable is False:
		interval = 300
		hookmain()
		intervaldisable = True
	if rawstatsmode is False and webworks is True and intervaldisable is False:
		# calculate acceptable interval
		intervalcalc()
	if rawstatsmode is True and intervaldisable is False:
		intervalcalc()

	if rawstatsmode is False and webworks is True:
		# build data structure from player data for figuring bests
		newlister()

	if rawstatsmode is False and webworks is True and botcheck is True:
		# Check if fights or bets happen to not be done.
		if(bets < 5 and level >= 30):
			try:
				betdiff = (5 - bets)
				bet_bet(betdiff)
			except TypeError:
				bets = 5

		spendmoney()
		aligncheck()

#                xchat.prnt("TTL: {0}, INTERVAL:{1}".format(ttl, interval))
		# check time til levelup
		# if I will before next interval,
		# set timer to call lvlup within 10 sec after leveling
		timercheck()
		# If so, do it (giggity)

		if(level >= 10 and level <= 200):
			if(fights < 5):
				fight_fight()

	if webworks is True and newlist != None:
		for entry in newlist:
			if(entry[5] == 1):
				levelrank1 = entry[3]
	
	rawstatsmodeon = False
	rawplayersmodeon = False
	opswitch = False
	if(opcheck is False):
		opswitch = True
	if(rawstatsswitch is False and opswitch is False):
		if(rawstatsmode is True and webworks is True and ttlfrozenmode is False):
			rawplayersmodeon = True
		if(rawstatsmode is False and webworks is False and webfail >= 3):
			rawstatsmodeon = True
	if(rawstatsswitch is True and opswitch is False and nolag is False):
		if(levelrank1 < laglevel and rawstatsmode is True):
			rawplayersmodeon = True
		if(levelrank1 >= laglevel and rawstatsmode is False):
			rawstatsmodeon = True
	if(rawstatsmode is True and opswitch is True):
		rawplayersmodeon = True
	if rawstatsmodeon is True:
		rawstatsmode = True
		if bottextmode is True:
			xchat.prnt("Rawstats Mode Activated")
		configwrite()
	if rawplayersmodeon is True:
		rawstatsmode = False
		if bottextmode is True:
			xchat.prnt("Rawplayers Mode Activated")
		rawmyentry = None
		configwrite()

	if(rawstatsmode is False and webworks is True and botcheck is True and opswitch is False):
		if online is True:
			if(ttl == oldttl):
				ttlfrozen += 1
				if errortextmode is True:
					xchat.prnt("TTL Frozen {0}".format(ttlfrozen))
	if (ttlfrozen >= 2):
		rawstatsmode = True
		ttlfrozenmode = True
		if bottextmode is True:
			xchat.prnt("Rawstats Mode Activated")
		ttlfrozen = 0
	
	return True        # <- tells timer to repeat

def intervalcalc():
	global interval
	global level
	global fights
	global ufightcalc
	global bets
	global botcheck
	global singlefight
	global nolag
	global rawstatsmode
	global webworks
	global fightcalcmin
	
	interval = 5
	interval *= 60                  # conv from min to sec
	if botcheck is False:
		interval = 60
	if botcheck is True:
		if(level >= 10 and level < 30 and webworks is True):
			if(fights < 5):
				interval = 60
		if(bets == 5 and fights < 5 and level <= 200 and webworks is True):
			interval = 60
		if(bets < 5 and level >= 30 and webworks is True):
			interval = 60
		if(fights < 5 and ufightcalc >= fightcalcmin and level >= 10 and level <= 200 and singlefight is True and nolag is True and rawstatsmode is True and webworks is True):
			interval = 30
	hookmain()

def timercheck():
	global alignlevel
	global ttl
	global interval
	global atime
	global stime
	global ctime
	global level
	global newlist
	global mysum
	global webworks
	global bottextmode
	global attackcount1
	global challengecount1
	global slaycount1
	global alignlvlupcount1
	global lvlupcount1
	
	attl = ttl - 60
	# make sure no times are negative
	if(attl < 0):
		attl = 0
	if(atime < 0):
		atime = 0
	if(ctime < 0):
		ctime = 0
	if(stime < 0):
		stime = 0
	if(alignlvlupcount1 < 0):
		alignlvlupcount1 = 0
	if(lvlupcount1 < 0):
		lvlupcount1 = 0
	if(attackcount1 < 0):
		attackcount1 = 0
	if(challengecount1 < 0):
		challengecount1 = 0
	if(slaycount1 < 0):
		slaycount1 = 0
	
#	xchat.prnt("TTL: {0}  Atime: {1}  Ctime: {2}  Stime: {3}".format(ttl,atime,ctime,stime))

	challengecheck = False
	if(level >= 35):
		leveldiff = level + 10
		sumdiff = mysum + (mysum * 0.15)
		challengediff = ("Doctor Who?", 999999)
		if webworks is True and newlist != None:
			for entry in newlist:
				if(entry[3] <= leveldiff and entry[2] <= sumdiff):
					challengecheck = True
					challengediff = entry

	if(level >= alignlevel and attl <= interval):
		timer = (attl)*1000
		if bottextmode is True:
			xchat.prnt("Set align lvlup timer. Going off in {0} minutes.".format(timer // 60000))
		xchat.hook_timer(timer, alignlvlup)
		alignlvlupcount1 += 1
	if(ttl <= interval and ttl > 0):
		timer = (ttl+10)*1000
		if bottextmode is True:
			xchat.prnt("Set lvlup timer. Going off in {0} minutes.".format(timer // 60000))
		xchat.hook_timer(timer, lvlup)
		lvlupcount1 += 1                        
	
	# do checks for other actions.
	if(level >= 10 and atime <= interval and atime <= ttl):
		timer = (atime+10)*1000
		if bottextmode is True:
			xchat.prnt("Set attack timer. Going off in {0} minutes.".format(timer // 60000))
		xchat.hook_timer(timer, attack)
		attackcount1 += 1

	if(level >= 40 and stime <= interval and stime <= ttl):
		timer = (stime+10)*1000
		if bottextmode is True:
			xchat.prnt("Set slay timer. Going off in {0} minutes.".format(timer // 60000))
		xchat.hook_timer(timer, slay)
		slaycount1 += 1

	if challengecheck is True or webworks is False:
		if(level >= 35 and ctime <= interval and ctime <= ttl):
			timer = (ctime+10)*1000
			if bottextmode is True:
				xchat.prnt("Set challenge timer. Going off in {0} minutes.".format(timer // 60000))
			xchat.hook_timer(timer, challenge)
			challengecount1 += 1
	if(attl > 350 and alignlvlupcount1 >= 1):
		alignlvlupcount1 = 0
	if(ttl > 350 and lvlupcount1 >= 1):
		lvlupcount1 = 0
	if(level >= 10 and atime > 350 and attackcount1 >= 1):
		attackcount1 = 0
	if(level >= 35 and ctime > 350 and challengecount1 >= 1):
		challengecount1 = 0
	if(level >= 40 and stime > 350 and slaycount1 >= 1):
		slaycount1 = 0              
	if(level >= 10 and atime == 0 and attackcount1 >= 0):
		attackcount1 = 1
	if(level >= 35 and ctime == 0 and challengecount1 >= 0):
		challengecount1 = 1
	if(level >= 40 and stime == 0 and slaycount1 >= 0):
		slaycount1 = 1          
#        xchat.prnt("AttackCount: {0} ChallengeCount: {1} SlayCount: {2} AlignlvlupCount: {3} LvlupCount: {4}".format(attackcount1, challengecount1, slaycount1, alignlvlupcount1, lvlupcount1))

def spendmoney():
	global level
	global mysum
	global gold
	global bank
	global hero
	global hlvl
	global eng
	global elvl
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
	global betmoney
	global bets
	global upgradeall
	global itemupgrader
	global sethero
	global setengineer
	global fightSum
	global firstalign
	global setbuy
	
	# decide what to spend our gold on! :D
		
	lowestitem = worstitem()
#        xchat.prnt("Worst item {0}".format(lowestitem))
	if(level >= 0):
		try:
			if(gold >= 41):
				usecommand("bank deposit {0}".format(gold - 40))
				bank += (gold - 40)
				gold = 40
			elif(gold <= 20 and bank >= 20):
				usecommand("bank withdraw 20")
				bank -= 20
				gold += 20
		except TypeError:
			gold = 0

	if(level >= setbuy):
		buycost = level * 6
		buyitem = level * 2
		buydiff = 19
		if(bank > buycost + betmoney):
			if(amulet < (buyitem - buydiff)):
				usecommand("bank withdraw {0}".format(buycost))
				usecommand("buy amulet {0}".format(buyitem))
				bank -= buycost
				amulet = buyitem
		if(bank > buycost + betmoney):
			if(charm < (buyitem - buydiff)):
				usecommand("bank withdraw {0}".format(buycost))
				usecommand("buy charm {0}".format(buyitem))
				bank -= buycost
				charm = buyitem
		if(bank > buycost + betmoney):
			if(helm < (buyitem - buydiff)):
				usecommand("bank withdraw {0}".format(buycost))
				usecommand("buy helm {0}".format(buyitem))
				bank -= buycost
				helm = buyitem
		if(bank > buycost + betmoney):
			if(boots < (buyitem - buydiff)):
				usecommand("bank withdraw {0}".format(buycost))
				usecommand("buy boots {0}".format(buyitem))
				bank -= buycost
				boots = buyitem
		if(bank > buycost + betmoney):
			if(gloves < (buyitem - buydiff)):
				usecommand("bank withdraw {0}".format(buycost))
				usecommand("buy gloves {0}".format(buyitem))
				bank -= buycost
				gloves = buyitem
		if(bank > buycost + betmoney):
			if(ring < (buyitem - buydiff)):
				usecommand("bank withdraw {0}".format(buycost))
				usecommand("buy ring {0}".format(buyitem))
				bank -= buycost
				ring = buyitem
		if(bank > buycost + betmoney):
			if(leggings < (buyitem - buydiff)):
				usecommand("bank withdraw {0}".format(buycost))
				usecommand("buy leggings {0}".format(buyitem))
				bank -= buycost
				leggings = buyitem
		if(bank > buycost + betmoney):
			if(shield < (buyitem - buydiff)):
				usecommand("bank withdraw {0}".format(buycost))
				usecommand("buy shield {0}".format(buyitem))
				bank -= buycost
				shield = buyitem
		if(bank > buycost + betmoney):
			if(tunic < (buyitem - buydiff)):
				usecommand("bank withdraw {0}".format(buycost))
				usecommand("buy tunic {0}".format(buyitem))
				bank -= buycost
				tunic = buyitem
		if(bank > buycost + betmoney):
			if(weapon < (buyitem - buydiff)):
				usecommand("bank withdraw {0}".format(buycost))
				usecommand("buy weapon {0}".format(buyitem))
				bank -= buycost
				weapon = buyitem

	if(level >= setengineer) or (level >= 15 and bank >= 2800 + betmoney):
		if(eng == 0 and bank >= 1000):
			usecommand("bank withdraw 1000")
			usecommand("hire engineer")
			bank -= 1000
			eng = 1
		if(eng == 1 and elvl < 9):
			elvldiff = 9 - elvl
			elvlcost = elvldiff * 200
			if(bank >= elvlcost + betmoney):
				usecommand("bank withdraw {0}".format(elvlcost))
				for i in range(elvldiff):
					usecommand("engineer level")
				bank -= elvlcost
				elvl += elvldiff
			elif(bank > betmoney):
				moneycalc = bank - betmoney
				upgradeengcalc = moneycalc // 200
				if(upgradeengcalc >= 1):
					engmoney = upgradeengcalc * 200
					usecommand("bank withdraw {0}".format(engmoney))
					for i in range(upgradeengcalc):
						usecommand("engineer level")
					bank -= engmoney
					elvl += upgradeengcalc
	
	if(mysum >= sethero and level >= 15) or (level >= 15 and elvl == 9 and bank >= 2800 + betmoney):
		if(hero == 0 and bank >= betmoney + 1000):
			usecommand("bank withdraw 1000")
			usecommand("summon hero")
			bank -= 1000
			hero = 1
		if(hero == 1 and hlvl < 9):
			hlvldiff = 9 - hlvl
			hlvlcost = hlvldiff * 200
			if(bank >= hlvlcost + betmoney):
				usecommand("bank withdraw {0}".format(hlvlcost))
				for i in range(hlvldiff):
					usecommand("hero level")
				bank -= hlvlcost
				hlvl += hlvldiff
			elif(bank > betmoney):
				moneycalc = bank - betmoney
				upgradeherocalc = moneycalc // 200
				if(upgradeherocalc >= 1):
					heromoney = upgradeherocalc * 200
					usecommand("bank withdraw {0}".format(heromoney))
					for i in range(upgradeherocalc):
						usecommand("hero level")
					bank -= heromoney
					hlvl += upgradeherocalc

	upgradeallon = False
	if(level >= 15 and level < 29 and hlvl == 9 and elvl == 9) or (bets == 5 and (hlvl < 9 or elvl < 9) or (bets == 5 and upgradeall is False and itemupgrader is False)):
		upgradeallon = True
		multi = 5
	if upgradeall is True:
		if(hlvl == 9 and elvl == 9 and bets == 5):
			upgradeallon = True
			multi = 1
		
	if upgradeallon is True:
		if(bank > betmoney):
			moneycalc = bank - betmoney
			upgradeallcalc = moneycalc // (200 * multi)
			if(upgradeallcalc >= 1):
				itemmoney = upgradeallcalc * (200 * multi) 
				usecommand("bank withdraw {0}".format(itemmoney))
				usecommand("upgrade all {0}".format(upgradeallcalc * multi))
				bank -= itemmoney
				amulet += upgradeallcalc * multi
				charm += upgradeallcalc * multi
				helm += upgradeallcalc * multi
				boots += upgradeallcalc * multi
				gloves += upgradeallcalc * multi
				ring += upgradeallcalc * multi
				leggings += upgradeallcalc * multi
				shield += upgradeallcalc * multi
				tunic += upgradeallcalc * multi
				weapon += upgradeallcalc * multi


	if itemupgrader is True:
		if(hlvl == 9 and elvl == 9 and bets == 5):
			if(bank > betmoney):
				moneycalc = bank - betmoney
				upgradecalc = moneycalc // 20
				if(upgradecalc >= 1):
					itemmoney = upgradecalc * 20
					usecommand("bank withdraw {0}".format(itemmoney))
					itemupgrade(upgradecalc)
					bank -= itemmoney
	NewSum = amulet + charm + helm + boots + gloves + ring + leggings + shield + tunic + weapon
	fightSum = NewSum
	if(firstalign == "priest"):
		priestadjust = NewSum * 0.10
		fightSum += priestadjust
	if(hero == 1):
		heroadj = fightSum * ((hlvl + 2) /100.0)
		fightSum += heroadj

def alignlvlup(userdata):
	global level
	global alignlevel
	global alignlvlupcount1

	if alignlvlupcount1 == 1:
		if(level >= alignlevel):
			usecommand("align priest")
	alignlvlupcount1 -= 1

def lvlup(userdata):
	global name
	global level
	global interval
	global webworks
	global rawstatsmode
	global rawmyentry
	global ttlfrozenmode
	global ttlfrozen
	global bottextmode
	global lvlupcount1
	
	if lvlupcount1 == 1:
		# rehook main timer for potential new interval
		webdata()
		if webworks is True:
			getvariables(1)
			newlister()

		if rawstatsmode is False:
			if(level < 30):
				interval = 60
			elif(level >= 30):
				interval = 120
		if rawstatsmode is True:
			interval = 60
		hookmain()
		if rawstatsmode is True:
			level += 1
		
		# fix level stat for lvlup
		if bottextmode is True:
			xchat.prnt("{0} has reached level {1}!".format(name, level))

		if(level <= 10):
			usecommand("load power 0")
		if ttlfrozenmode is True:
			    ttlfrozenmode = False
			    rawstatsmode = False
			    if bottextmode is True:
				    xchat.prnt("Rawplayers Mode Activated")
			    rawmyentry = None
		ttlfrozen = 0

		if rawstatsmode is False:
			if(level >= 30):
				if webworks is True:
					try:
						bet_bet(5)
					except TypeError:
						bets = 5
			if(level >= 10):
				xchat.hook_timer(0, attack)
			if(level >= 40):
				xchat.hook_timer(0, slay)
			if(level >= 35):
				xchat.hook_timer(0, challenge)
	lvlupcount1 -= 1

def bet_bet(num1):
	global level
	global bank
	global bets
	
	if(level >= 30):
		bbet = bestbet()
		if(bank >= 100):
#                       xchat.prnt("bestbet {0} {1}".format( bbet[0][0], bbet[1][0] ))
			usecommand("bank withdraw 100")
			for i in range(num1):
				usecommand("bet {0} {1} 100".format( bbet[0][0], bbet[1][0] ))
			bank -=100

def fight_fight():
	global name
	global level
	global powerpots
	global alignlevel
	global rankplace
	global fights
	global firstalign
	global secondalign
	global ufightcalc
	global fightSum
	global bets
	global singlefight
	global team
	global myentry
	global rawstatsmode
	global bottextmode
	global fightcalcmin

	ufight = testfight()
	ufightcalc = fightSum / ufight[2]
	if(ufight[0] == name):
		ufightcalc = 0.1
		usecommand("bank deposit 1")
	if(team >= 1):
		if(ufight[6] == team):
			ufightcalc = 0.1

	if(level >= 30 and bets < 5):
		ufightcalc = 0.1
	fightdiff = 5 - fights
	if(powerpots >= fightdiff):
		spendpower = fightdiff
	if(powerpots < fightdiff):
		spendpower = powerpots

	if rawstatsmode is True:
		ranknumber = myentry[1]
	if rawstatsmode is False:
		ranknumber = rankplace

	if(level >= 10):
		if bottextmode is True:
			xchat.prnt("Best fight for Rank {0}: {1} [{2}]  Opponent: Rank {3}: {4} [{5}], Odds {6}".format(ranknumber, name, int(fightSum), ufight[5], ufight[0], int(ufight[2]), ufightcalc))
		if(ufightcalc >= fightcalcmin):
			if(level >= 95 and powerpots >= 1):
				if(singlefight is True):
					usecommand("load power 1")
				if(singlefight is False):
					usecommand("load power {0}".format(spendpower))
			if(level >= alignlevel):
				usecommand("align {0}".format(firstalign))
			if(singlefight is True):
				usecommand("fight {0}".format( ufight[0] ))
				fights += 1
			if(singlefight is False):
				for i in range(fightdiff):
					usecommand("fight {0}".format( ufight[0] ))
				fights += fightdiff
			if(level >= alignlevel):
				usecommand("align {0}".format(secondalign))

def aligncheck():
	global alignlevel
	global level
	global firstalign
	global secondalign
	global evilmode
	global setalign
	global align

	if evilmode is True:
		secondalign = "undead"
		alignlevel = 0
	if evilmode is False:
		secondalign = "human"
		alignlevel = setalign

	if(secondalign == "human" and level >= alignlevel):
		if(align == "g"):
			usecommand("align {0}".format(secondalign))
		if(align == "e"):
			usecommand("align {0}".format(secondalign))
	if(secondalign == "human" and level < alignlevel):
		if(align == "n"):
			usecommand("align {0}".format(firstalign))
		if(align == "e"):
			usecommand("align {0}".format(firstalign))
	if(secondalign == "undead"):
		if(align == "n"):
			usecommand("align {0}".format(secondalign))
		if(align == "g"):
			usecommand("align {0}".format(secondalign))

def attack(userdata):
	global level
	global alignlevel
	global firstalign
	global secondalign
	global attackcount1

	if attackcount1 == 1:
		creep = bestattack()
		if creep != "CreepList Error":
			if(level >= alignlevel):
				usecommand("align {0}".format(firstalign))
			usecommand("attack " + creep)
			if(level >= alignlevel):
				usecommand("align {0}".format(secondalign))
		if creep == "CreepList Error":
			xchat.prnt("{0}".format(creep))
	attackcount1 -= 1

def slay(userdata):
	global level
	global alignlevel
	global firstalign
	global secondalign
	global slaycount1

	if slaycount1 == 1:
		monster = bestslay()
		if monster != "MonsterList Error":
			if(level >= alignlevel):
				usecommand("align {0}".format(firstalign))
			usecommand("slay " + monster)
			if(level >= alignlevel):
				usecommand("align {0}".format(secondalign))
		if monster == "MonsterList Error":
			xchat.prnt("{0}".format(monster))
	slaycount1 -= 1
		
def challenge(userdata):
	global level
	global alignlevel
	global firstalign
	global secondalign
	global challengecount1

	if challengecount1 == 1:
		if(level >= alignlevel):
			usecommand("align {0}".format(firstalign))
		usecommand("challenge")
		if(level >= alignlevel):
			usecommand("align {0}".format(secondalign))
	challengecount1 -= 1

def bestattack():
	global creeps
	global level
	good = "CreepList Error"
	for thing in creeps:
		if(level <= thing[1]):
			good = thing[0]
	return good

def bestslay():
	global monsters
	global mysum
	good = "MonsterList Error"
	for thing in monsters:
		if(mysum <= thing[1]):
			good = thing[0]
	return good

def bestbet():
	global newlist
	diff = 0
	bestbet = None
	if newlist != None:
		for entry in newlist:
			best = bestfight(entry[0], 1)
			try:
				currdiff = entry[1] / best[1]
			except ZeroDivisionError:
				currdiff = 0
			if(currdiff > diff):
				if(entry[3] >= 30 and best[3] >= 30):
					diff = currdiff
					bestbet = ( entry, best )
	return bestbet

def bestfight(name, flag):
	global newlist
	
	idx = None
	length = len(newlist)
	diff = 999999
	best = ("Doctor Who?", 999999.0, 999999.0, 0, "n", 0, 0)

	for index, entry in enumerate(newlist):
		if(name == entry[0]):
			idx = index + 1
			break
	templist = newlist[idx:length]
	for entry in templist:
		if(entry[flag] < diff):
			diff = entry[flag]
			best = entry
	return best

def testfight():
	global newlist
	global fightSum
	global level
	global name
	
	diff = 0
	best = ("Doctor Who?", 999999.0, 999999.0, 0, "n", 0, 0)
	newlist.sort( key=operator.itemgetter(2))
	if newlist != None:
		for entry in newlist:
			if(entry[3] >= level and entry[0] != name):
				try:
					currdiff = fightSum / entry[2]
				except ZeroDivisionError:
					currdiff = 0
				if(currdiff > diff):
					diff = entry[2]
					best = entry
	return best

def worstitem():
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

	itemlist = [    ["amulet",      amulet],        \
			["charm",       charm],  \
			["helm",        helm],  \
			["boots",       boots],  \
			["gloves",      gloves],        \
			["ring",        ring],  \
			["leggings",    leggings],      \
			["shield",      shield],  \
			["tunic",       tunic], \
			["weapon",      weapon] ]

	itemlist.sort( key=operator.itemgetter(1), reverse=True )
	good = itemlist
	diff = 999999
	for thing in itemlist:
		if(thing[1] < diff):
			good = thing
	return good

def itemupgrade(num1):
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

	lowestitem = worstitem()
	usecommand("upgrade {0} {1}".format(lowestitem[0], num1))
	if(lowestitem[0] == "amulet"):
		amulet += num1
	elif(lowestitem[0] == "charm"):
		charm += num1
	elif(lowestitem[0] == "helm"):
		helm += num1
	elif(lowestitem[0] == "boots"):
		boots += num1
	elif(lowestitem[0] == "gloves"):
		gloves += num1
	elif(lowestitem[0] == "ring"):
		ring += num1
	elif(lowestitem[0] == "leggings"):
		leggings += num1
	elif(lowestitem[0] == "shield"):
		shield += num1
	elif(lowestitem[0] == "tunic"):
		tunic += num1
	elif(lowestitem[0] == "weapon"):
		weapon += num1

if autostartmode is True:
	autostart(None)
