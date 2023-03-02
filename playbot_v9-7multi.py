#!/usr/bin/env python

import xchat
import operator
import time
import pickle
import os
import sys
import socket
import ssl

__module_name__ = "Multirpg Playbot Script"
__module_version__ = "9.7"
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
		["Ogre",        1600],  ]

monsters = [    ["Medusa",      3500],  \
		["Centaur",     4000],  \
		["Mammoth",     5000],  \
		["Vampire",     6000],  \
		["Dragon",      7000],  \
		["Sphinx",      8000],  \
		["Hippogriff",  999999] ]

# list of all networks
#               Network,        Server,                         NoLag   SNum    Port            SSLPort         BotHostMask
networklist = [ ["AyoChat",     "irc.ayochat.or.id",            False,  1,      6667,           6667,           "multirpg@venus.skralg.com"],  \
		["AyoChat",     "149.202.240.157",              False,  2,      6667,           6667,           "multirpg@venus.skralg.com"],  \
		["ChatLounge",  "irc.chatlounge.net",           True,   1,      6667,           "+6697",        "multirpg@2001:579:9f05:1800:9119:8531:5e14:559"],  \
		["ChatLounge",  "185.34.216.32",                True,   2,      6667,           "+6697",        "multirpg@2001:579:9f05:1800:9119:8531:5e14:559"],  \
		["DALnet",      "irc.dal.net",                  False,  1,      6667,           "+6697",        "multirpg@venus.skralg.com"], \
		["DALnet",      "94.125.182.251",               False,  2,      6667,           "+6697",        "multirpg@venus.skralg.com"], \
		["EFnet",       "irc.efnet.net",                False,  1,      6667,           "+9999",        "multirpg@venus.skralg.com"], \
		["EFnet",       "66.225.225.225",               False,  2,      6667,           "+9999",        "multirpg@venus.skralg.com"], \
		["GameSurge",   "irc.gamesurge.net",            True,   1,      6667,           6667,           "multirpg@multirpg.bot.gamesurge"],  \
		["GameSurge",   "195.68.206.250",               True,   2,      6667,           6667,           "multirpg@multirpg.bot.gamesurge"],  \
		["IRC4Fun",     "irc.irc4fun.net",              False,  1,      6667,           "+6697",        "multirpg@bots/multirpg"],  \
		["IRC4Fun",     "139.99.113.250",               False,  2,      6667,           "+6697",        "multirpg@bots/multirpg"],  \
		["Koach",       "irc.koach.com",                False,  1,      6667,           "+6697",        ".skralg.com"], \
		["Koach",       "172.105.168.90",               False,  2,      6667,           "+6697",        ".skralg.com"], \
		["Libera",      "irc.libera.chat",              False,  1,      6667,           "+6697",        "multirpg@venus.skralg.com"], \
		["Libera",      "130.185.232.126",              False,  2,      6667,           "+6697",        "multirpg@venus.skralg.com"], \
		["mIRCPhantom", "irc.mircphantom.net",          False,  1,      6667,           "+6697",        ".skralg.com"], \
		["mIRCPhantom", "51.89.198.165",                False,  2,      6667,           "+6697",        ".skralg.com"], \
		["Pissnet",     "irc.letspiss.net",             False,  1,      6667,           "+6697",        ".skralg.com"], \
		["Pissnet",     "91.92.144.105",                False,  2,      6667,           "+6697",        ".skralg.com"], \
		["QuakeNet",    "irc.quakenet.org",             False,  1,      6667,           6667,           "multirpg@multirpg.users.quakenet.org"], \
		["QuakeNet",    "188.240.145.70",               False,  2,      6667,           6667,           "multirpg@multirpg.users.quakenet.org"], \
		["Rizon",       "irc.rizon.net",                False,  1,      6667,           "+6697",        ".skralg.com"], \
		["Rizon",       "80.65.57.18",                  False,  2,      6667,           "+6697",        ".skralg.com"], \
		["ScaryNet",    "irc.scarynet.org",             True,   1,      6667,           6667,           "multirpg@venus.skralg.com"],  \
		["ScaryNet",    "69.162.163.62",                True,   2,      6667,           6667,           "multirpg@venus.skralg.com"],  \
		["SkyChatz",    "irc.skychatz.org",             False,  1,      6667,           "+6697",        "multirpg@skychatz.user.multirpg"],  \
		["SkyChatz",    "15.235.141.21",                False,  2,      6667,           "+6697",        "multirpg@skychatz.user.multirpg"],  \
		["Techtronix",  "irc.techtronix.net",           True,   1,      "+6697",        "+6697",        "multirpg@multirpg.net"],  \
		["Techtronix",  "35.229.28.106",                True,   2,      "+6697",        "+6697",        "multirpg@multirpg.net"],  \
		["Undernet",    "irc.undernet.org",             False,  1,      6667,           6667,           "multirpg@idlerpg.users.undernet.org"], \
		["Undernet",    "154.35.136.18",                False,  2,      6667,           6667,           "multirpg@idlerpg.users.undernet.org"], \
		["UniversalNet","irc.universalnet.org",         False,  1,      6667,           "+6697",        "multirpg@venus.skralg.com"], \
		["UniversalNet","62.171.172.8",                 False,  2,      6667,           "+6697",        "multirpg@venus.skralg.com"], \
		["Virtulus",    "irc.virtulus.net",             True,   1,      6667,           "+6697",        "multirpg@B790DC3F.D0CDF40.88109D7.IP"], \
		["Virtulus",    "18.193.247.191",               True,   2,      6667,           "+6697",        "multirpg@B790DC3F.D0CDF40.88109D7.IP"] ]

creeps.reverse()
monsters.reverse()

multirpgweb = "https://www.multirpg.net/"
idlerpgweb = "http://www.idlerpg.org/"
russweb = "https://russellb.000webhostapp.com/"
gitweb = "https://github.com/RussellBeech/xchat-plugins"
rawplayers3 = None
interval = 300
newlist = None
newlist2 = None
newlist3 = None
newlist4 = None
newlist5 = None
playerlist = None
mainhook = None
myentry = None
myentry2 = None
myentry3 = None
myentry4 = None
myentry5 = None
rawmyentry = None
rawmyentry2 = None
rawmyentry3 = None
rawmyentry4 = None
rawmyentry5 = None
rawmyentryfail = 0
itemslists = None
align = "n"
currentversion = __module_version__
currentversion = float( currentversion )

CONFIG_FILE_LOCATION = xchat.get_info('xchatdir')+"/.playbotmulti"
try:
	f = open(CONFIG_FILE_LOCATION,"rb")
	configList = pickle.load(f)
	f.close()
except:
	xchat.prnt("ConfigList Load Error - Using Default Settings")
	configList = []

# custom network settings - For linked networks or networks which are not on the networklist
customnetworksettings = False # True = on, False = off - For custom networks which are not on the networklist
customservername = "irc.mircphantom.net" # Custom Server address
customservername2 = "176.31.181.159" # Custom Server address
customchanname = "#multirpg" # Custom Channel Name
custombotname = "multirpg/fun" # Custom Botname
customnolag = False # True = on, False = off - If network is on the nolag network list
custombosthostmask = "multirpg@multirpg.users.IRC4Fun.net" # Custom Bot Host Name
customport1 = 6667 # Port Number.  If port is an SSL port use "+6697" format

customnetworksettings2 = False # True = on, False = off - For custom networks which are not on the networklist
customservernameb = "irc.mircphantom.net" # Custom Server address
customservernameb2 = "176.31.181.159" # Custom Server address
customchanname2 = "#multirpg" # Custom Channel Name
custombotname2 = "multirpg/fun" # Custom Botname
customnolag2 = False # True = on, False = off - If network is on the nolag network list
custombosthostmask2 = "multirpg@multirpg.users.IRC4Fun.net" # Custom Bot Host Name
customport2 = 6667 # Port Number.  If port is an SSL port use "+6697" format

customnetworksettings3 = False # True = on, False = off - For custom networks which are not on the networklist
customservernamec = "irc.mircphantom.net" # Custom Server address
customservernamec2 = "176.31.181.159" # Custom Server address
customchanname3 = "#multirpg" # Custom Channel Name
custombotname3 = "multirpg/fun" # Custom Botname
customnolag3 = False # True = on, False = off - If network is on the nolag network list
custombosthostmask3 = "multirpg@multirpg.users.IRC4Fun.net" # Custom Bot Host Name
customport3 = 6667 # Port Number.  If port is an SSL port use "+6697" format

customnetworksettings4 = False # True = on, False = off - For custom networks which are not on the networklist
customservernamed = "irc.mircphantom.net" # Custom Server address
customservernamed2 = "176.31.181.159" # Custom Server address
customchanname4 = "#multirpg" # Custom Channel Name
custombotname4 = "multirpg/fun" # Custom Botname
customnolag4 = False # True = on, False = off - If network is on the nolag network list
custombosthostmask4 = "multirpg@multirpg.users.IRC4Fun.net" # Custom Bot Host Name
customport4 = 6667 # Port Number.  If port is an SSL port use "+6697" format

customnetworksettings5 = False # True = on, False = off - For custom networks which are not on the networklist
customservernamee = "irc.mircphantom.net" # Custom Server address
customservernamee2 = "176.31.181.159" # Custom Server address
customchanname5 = "#multirpg" # Custom Channel Name
custombotname5 = "multirpg/fun" # Custom Botname
customnolag5 = False # True = on, False = off - If network is on the nolag network list
custombosthostmask5 = "multirpg@multirpg.users.IRC4Fun.net" # Custom Bot Host Name
customport5 = 6667 # Port Number.  If port is an SSL port use "+6697" format

# ZNC settings
ZNC1 = False # ZNC1 Server Mode - True = On, False = Off
ZNCServer1 = "*.*.*.*" # ZNC1 Server Address
ZNCPort1 = 6005 # ZNC1 Port Number
ZNCUser1 = "*******" # ZNC1 Username/Network
ZNCPass1 = "*******" # ZNC1 Password
ZNC2 = False # ZNC2 Server Mode - True = On, False = Off
ZNCServer2 = "*.*.*.*" # ZNC2 Server Address
ZNCPort2 = 6005 # ZNC2 Port Number
ZNCUser2 = "*******" # ZNC2 Username/Network
ZNCPass2 = "*******" # ZNC2 Password
ZNC3 = False # ZNC3 Server Mode - True = On, False = Off
ZNCServer3 = "*.*.*.*" # ZNC3 Server Address
ZNCPort3 = 6005 # ZNC3 Port Number
ZNCUser3 = "******" # ZNC3 Username/Network
ZNCPass3 = "******" # ZNC3 Password
ZNC4 = False # ZNC4 Server Mode - True = On, False = Off
ZNCServer4 = "*.*.*.*" # ZNC4 Server Address
ZNCPort4 = 6005 # ZNC4 Port Number
ZNCUser4 = "*******" # ZNC4 Username/Network
ZNCPass4 = "*******" # ZNC4 Password
ZNC5 = False # ZNC5 Server Mode - True = On, False = Off
ZNCServer5 = "*.*.*.*" # ZNC5 Server Address
ZNCPort5 = 6005 # ZNC5 Port Number
ZNCUser5 = "*******" # ZNC5 Username/Network
ZNCPass5 = "*******" # ZNC5 Password

# Changeable setting
multirpgclass = "MultiRPG PlayBot" # Class to be used when re-registering if player gets removed
nickserv1 = False # True = on, False = off
nickserv2 = False # True = on, False = off
nickserv3 = False # True = on, False = off
nickserv4 = False # True = on, False = off
nickserv5 = False # True = on, False = off
nickservpass1 = "*********" # NickServ Password
nickservpass2 = "*********" # NickServ Password
nickservpass3 = "*********" # NickServ Password
nickservpass4 = "*********" # NickServ Password
nickservpass5 = "*********" # NickServ Password
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
ssl2 = False # True = switches on SSL Port, False = uses normal port
ssl3 = False # True = switches on SSL Port, False = uses normal port
ssl4 = False # True = switches on SSL Port, False = uses normal port
ssl5 = False # True = switches on SSL Port, False = uses normal port
remotekill = True # True = on, False = off # Gives me the option if the PlayBot is flooding the GameBot to disable the PlayBot

# declare stats as global
name = None
name2 = None
name3 = None
name4 = None
name5 = None
pswd = None
pswd2 = None
pswd3 = None
pswd4 = None
pswd5 = None
servername = None
networkname = None
servername2 = None
networkname2 = None
servername3 = None
networkname3 = None
servername4 = None
networkname4 = None
servername5 = None
networkname5 = None
servernum1 = 1
servernum2 = 1
servernum3 = 1
servernum4 = 1
servernum5 = 1
connectfail1 = 0
connectfail2 = 0
connectfail3 = 0
connectfail4 = 0
connectfail5 = 0
webfail = 0
nolag1 = None
nolag2 = None
nolag3 = None
nolag4 = None
nolag5 = None
port1 = None
port2 = None
port3 = None
port4 = None
port5 = None

char1 = False
char2 = False
char3 = False
char4 = False
char5 = False
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
ufightcalc1 = 0
ufightcalc2 = 0
ufightcalc3 = 0
ufightcalc4 = 0
ufightcalc5 = 0
fightSum1 = 0
fightSum2 = 0
fightSum3 = 0
fightSum4 = 0
fightSum5 = 0

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
levelrank1 = 99

nickname = None
nickname2 = None
nickname3 = None
nickname4 = None
nickname5 = None
netname = None
netname2 = None
netname3 = None
netname4 = None
netname5 = None
channame = None
channame2 = None
channame3 = None
channame4 = None
channame5 = None
botname = None
botname2 = None
botname3 = None
botname4 = None
botname5 = None
game_chan = None
game_chan2 = None
game_chan3 = None
game_chan4 = None
game_chan5 = None
botcheck1 = None
botcheck2 = None
botcheck3 = None
botcheck4 = None
botcheck5 = None
bothostmask1 = None
bothostmask2 = None
bothostmask3 = None
bothostmask4 = None
bothostmask5 = None
chancheck1 = None
chancheck2 = None
chancheck3 = None
chancheck4 = None
chancheck5 = None
webworks = None
gameactive = None

ttlfrozen1 = 0
ttlfrozen2 = 0
ttlfrozen3 = 0
ttlfrozen4 = 0
ttlfrozen5 = 0
ttlfrozenmode = False
botdisable1 = False
botdisable2 = False
botdisable3 = False
botdisable4 = False
botdisable5 = False
attackcount1 = 0
attackcount2 = 0
attackcount3 = 0
attackcount4 = 0
attackcount5 = 0
challengecount1 = 0
challengecount2 = 0
challengecount3 = 0
challengecount4 = 0
challengecount5 = 0
slaycount1 = 0
slaycount2 = 0
slaycount3 = 0
slaycount4 = 0
slaycount5 = 0
alignlvlupcount1 = 0
alignlvlupcount2 = 0
alignlvlupcount3 = 0
alignlvlupcount4 = 0
alignlvlupcount5 = 0
lvlupcount1 = 0
lvlupcount2 = 0
lvlupcount3 = 0
lvlupcount4 = 0
lvlupcount5 = 0

for entry in configList:
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
xchat.prnt( "To start PlayBot use /login CharName Password" )

def versionchecker():
	global currentversion
	global python3
	global russweb
	global gitweb

	webversion = None
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

	xchat.prnt("Current version {0}".format(currentversion))
	xchat.prnt("Web version {0}".format(webversion))
	if webversion != None:
		if(currentversion == webversion):
			xchat.prnt("You have the current version of PlayBot")
		if(currentversion < webversion):
			xchat.prnt("You have an old version of PlayBot")
			xchat.prnt("You can download a new version from {0} or {1}".format(russweb, gitweb))
		if(currentversion > webversion):
			xchat.prnt("Give me, Give me")

def configwrite():
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

def eraseconfig(word, word_eol, userdata):
	configList = []
	f = open(CONFIG_FILE_LOCATION,"wb")
	pickle.dump(configList,f)
	f.close()
	xchat.prnt("Config Erased")
	return xchat.EAT_ALL

xchat.hook_command("eraseconfig", eraseconfig, help="/eraseconfig - Erases config file")
	
def bottester(num):
	global game_chan
	global game_chan2
	global game_chan3
	global game_chan4
	global game_chan5
	global botname
	global botname2
	global botname3
	global botname4
	global botname5
	global channame
	global channame2
	global channame3
	global channame4
	global channame5
	global netname
	global netname2
	global netname3
	global netname4
	global netname5
	global char1
	global char2
	global char3
	global char4
	global char5
	global botdisable1
	global botdisable2
	global botdisable3
	global botdisable4
	global botdisable5
	
	botcount1 = 0
	botcount2 = 0
	botcount3 = 0
	botcount4 = 0
	botcount5 = 0
	bottest2 = "multirpg"

	if num == 1 and char1 is True:
		if("undernet" in netname.lower()):
			channame = "#idlerpg"
			botname = "idlerpg"
		else:
			channame = "#multirpg"
			botname = "multirpg"

		userlist = game_chan.get_list("users")
		bottest = botname
		botentry = []

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
		botcount1 = len(botentry)
		if botcount1 == 1:
			botname = botname10
		if botcount1 >= 2:
			botdisable1 = True
	if num == 2 and char2 is True:
		if("undernet" in netname2.lower()):
			channame2 = "#idlerpg"
			botname2 = "idlerpg"
		else:
			channame2 = "#multirpg"
			botname2 = "multirpg"

		userlist = game_chan2.get_list("users")
		bottest = botname2
		botentry = []
		
		for user in userlist:
			if bottest in user.nick and user.nick != bottest:
				botprefix = user.prefix
				if(botprefix == "@" or botprefix == "%"):
					botentry.append(user.nick)
					botname10 = user.nick
			if("undernet" in netname2.lower()):
				if bottest2 in user.nick:
					botprefix = user.prefix
					if(botprefix == "@"):
						botentry.append(user.nick)
						botname10 = user.nick
		botcount2 = len(botentry)
		if botcount2 == 1:
			botname2 = botname10
		if botcount2 >= 2:
			botdisable2 = True

	if num == 3 and char3 is True:
		if("undernet" in netname3.lower()):
			channame3 = "#idlerpg"
			botname3 = "idlerpg"
		else:
			channame3 = "#multirpg"
			botname3 = "multirpg"

		userlist = game_chan3.get_list("users")
		bottest = botname3
		botentry = []
		
		for user in userlist:
			if bottest in user.nick and user.nick != bottest:
				botprefix = user.prefix
				if(botprefix == "@" or botprefix == "%"):
					botentry.append(user.nick)
					botname10 = user.nick
			if("undernet" in netname3.lower()):
				if bottest2 in user.nick:
					botprefix = user.prefix
					if(botprefix == "@"):
						botentry.append(user.nick)
						botname10 = user.nick
		botcount3 = len(botentry)
		if botcount3 == 1:
			botname3 = botname10
		if botcount3 >= 2:
			botdisable3 = True

	if num == 4 and char4 is True:
		if("undernet" in netname4.lower()):
			channame4 = "#idlerpg"
			botname4 = "idlerpg"
		else:
			channame4 = "#multirpg"
			botname4 = "multirpg"

		userlist = game_chan4.get_list("users")
		bottest = botname4
		botentry = []
		
		for user in userlist:
			if bottest in user.nick and user.nick != bottest:
				botprefix = user.prefix
				if(botprefix == "@" or botprefix == "%"):
					botentry.append(user.nick)
					botname10 = user.nick
			if("undernet" in netname4.lower()):
				if bottest2 in user.nick:
					botprefix = user.prefix
					if(botprefix == "@"):
						botentry.append(user.nick)
						botname10 = user.nick
		botcount4 = len(botentry)
		if botcount4 == 1:
			botname4 = botname10
		if botcount4 >= 2:
			botdisable4 = True

	if num == 5 and char5 is True:
		if("undernet" in netname5.lower()):
			channame5 = "#idlerpg"
			botname5 = "idlerpg"
		else:
			channame5 = "#multirpg"
			botname5 = "multirpg"

		userlist = game_chan5.get_list("users")
		bottest = botname5
		botentry = []
		
		for user in userlist:
			if bottest in user.nick and user.nick != bottest:
				botprefix = user.prefix
				if(botprefix == "@" or botprefix == "%"):
					botentry.append(user.nick)
					botname10 = user.nick
			if("undernet" in netname5.lower()):
				if bottest2 in user.nick:
					botprefix = user.prefix
					if(botprefix == "@"):
						botentry.append(user.nick)
						botname10 = user.nick
		botcount5 = len(botentry)
		if botcount5 == 1:
			botname5 = botname10
		if botcount5 >= 2:
			botdisable5 = True

def usecommand(commanded, num):
	global game_chan
	global game_chan2
	global game_chan3
	global game_chan4
	global game_chan5
	global botname
	global botname2
	global botname3
	global botname4
	global botname5
	global channame
	global channame2
	global channame3
	global channame4
	global channame5
	global customnetworksettings
	global customnetworksettings2
	global customnetworksettings3
	global customnetworksettings4
	global customnetworksettings5
	global botdisable1
	global botdisable2
	global botdisable3
	global botdisable4
	global botdisable5

	if num == 1 and customnetworksettings is False:
		bottester(1)
	if num == 2 and customnetworksettings2 is False:
		bottester(2)
	if num == 3 and customnetworksettings3 is False:
		bottester(3)
	if num == 4 and customnetworksettings4 is False:
		bottester(4)
	if num == 5 and customnetworksettings5 is False:
		bottester(5)
	
	if(num == 1 and botdisable1 is False):
		try:
			game_chan.command( "msg {0} {1}".format(botname, commanded) )
		except AttributeError:
			xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame) )
	if(num == 2 and botdisable2 is False):
		try:
			game_chan2.command( "msg {0} {1}".format(botname2, commanded) )
		except AttributeError:
			xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame2) )
	if(num == 3 and botdisable3 is False):
		try:
			game_chan3.command( "msg {0} {1}".format(botname3, commanded) )
		except AttributeError:
			xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame3) )
	if(num == 4 and botdisable4 is False):
		try:
			game_chan4.command( "msg {0} {1}".format(botname4, commanded) )
		except AttributeError:
			xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame4) )
	if(num == 5 and botdisable5 is False):
		try:
			game_chan5.command( "msg {0} {1}".format(botname5, commanded) )
		except AttributeError:
			xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame5) )

def updatenick(word, word_eol, userdata):
	global gameactive
	global channame
	global netname
	global nickname
	global botname
	global game_chan
	global channame2
	global netname2
	global nickname2
	global botname2
	global game_chan2
	global channame3
	global netname3
	global nickname3
	global botname3
	global game_chan3
	global channame4
	global netname4
	global nickname4
	global botname4
	global game_chan4
	global channame5
	global netname5
	global nickname5
	global botname5
	global game_chan5
	global char1
	global char2
	global char3
	global char4
	global char5
	global charcount

	if gameactive is True:
		try:
			testnum = word[1]
		except IndexError:
			xchat.prnt("To updatenick use /updatenick charnum")
		try:
			if str.isdigit(testnum):
				num = int( testnum )
		except UnboundLocalError:
			return
		checknet = xchat.get_info("network")
		checknick = xchat.get_info("nick")
		nickswitch = False
		
		if num == 1 and char1 is True:
			if charcount == 1:
				if checknet != netname:
					nickswitch = True
				if checknet == netname:
					if checknick != nickname:
						nickswitch = True
					if checknick == nickname:
						xchat.prnt("{0} is already in use on {1}".format(nickname, netname))
			if charcount == 2:
				if checknet != netname and checknet != netname2:
					nickswitch = True
				if checknet == netname:
					if checknick != nickname:
						nickswitch = True
					if checknick == nickname:
						xchat.prnt("{0} is already in use on {1}".format(nickname, netname))
				if checknet == netname2:
					if checknick != nickname2:
						nickswitch = True
					if checknick == nickname2:
						xchat.prnt("{0} is already in use on {1}".format(nickname2, netname2))
			if charcount == 3:
				if checknet != netname and checknet != netname2 and checknet != netname3:
					nickswitch = True
				if checknet == netname:
					if checknick != nickname:
						nickswitch = True
					if checknick == nickname:
						xchat.prnt("{0} is already in use on {1}".format(nickname, netname))
				if checknet == netname2:
					if checknick != nickname2:
						nickswitch = True
					if checknick == nickname2:
						xchat.prnt("{0} is already in use on {1}".format(nickname2, netname2))
				if checknet == netname3:
					if checknick != nickname3:
						nickswitch = True
					if checknick == nickname3:
						xchat.prnt("{0} is already in use on {1}".format(nickname3, netname3))
			if charcount == 4:
				if checknet != netname and checknet != netname2 and checknet != netname3 and checknet != netname4:
					nickswitch = True
				if checknet == netname:
					if checknick != nickname:
						nickswitch = True
					if checknick == nickname:
						xchat.prnt("{0} is already in use on {1}".format(nickname, netname))
				if checknet == netname2:
					if checknick != nickname2:
						nickswitch = True
					if checknick == nickname2:
						xchat.prnt("{0} is already in use on {1}".format(nickname2, netname2))
				if checknet == netname3:
					if checknick != nickname3:
						nickswitch = True
					if checknick == nickname3:
						xchat.prnt("{0} is already in use on {1}".format(nickname3, netname3))
				if checknet == netname4:
					if checknick != nickname4:
						nickswitch = True
					if checknick == nickname4:
						xchat.prnt("{0} is already in use on {1}".format(nickname4, netname4))
			if charcount == 5:
				if checknet != netname and checknet != netname2 and checknet != netname3 and checknet != netname4 and checknet != netname5:
					nickswitch = True
				if checknet == netname:
					if checknick != nickname:
						nickswitch = True
					if checknick == nickname:
						xchat.prnt("{0} is already in use on {1}".format(nickname, netname))
				if checknet == netname2:
					if checknick != nickname2:
						nickswitch = True
					if checknick == nickname2:
						xchat.prnt("{0} is already in use on {1}".format(nickname2, netname2))
				if checknet == netname3:
					if checknick != nickname3:
						nickswitch = True
					if checknick == nickname3:
						xchat.prnt("{0} is already in use on {1}".format(nickname3, netname3))
				if checknet == netname4:
					if checknick != nickname4:
						nickswitch = True
					if checknick == nickname4:
						xchat.prnt("{0} is already in use on {1}".format(nickname4, netname4))
				if checknet == netname5:
					if checknick != nickname5:
						nickswitch = True
					if checknick == nickname5:
						xchat.prnt("{0} is already in use on {1}".format(nickname5, netname5))
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
				xchat.prnt("Nick 1 Updated")
		if num == 2 and char2 is True:
			if charcount == 2:
				if checknet != netname and checknet != netname2:
					nickswitch = True
				if checknet == netname:
					if checknick != nickname:
						nickswitch = True
					if checknick == nickname:
						xchat.prnt("{0} is already in use on {1}".format(nickname, netname))
				if checknet == netname2:
					if checknick != nickname2:
						nickswitch = True
					if checknick == nickname2:
						xchat.prnt("{0} is already in use on {1}".format(nickname2, netname2))
			if charcount == 3:
				if checknet != netname and checknet != netname2 and checknet != netname3:
					nickswitch = True
				if checknet == netname:
					if checknick != nickname:
						nickswitch = True
					if checknick == nickname:
						xchat.prnt("{0} is already in use on {1}".format(nickname, netname))
				if checknet == netname2:
					if checknick != nickname2:
						nickswitch = True
					if checknick == nickname2:
						xchat.prnt("{0} is already in use on {1}".format(nickname2, netname2))
				if checknet == netname3:
					if checknick != nickname3:
						nickswitch = True
					if checknick == nickname3:
						xchat.prnt("{0} is already in use on {1}".format(nickname3, netname3))
			if charcount == 4:
				if checknet != netname and checknet != netname2 and checknet != netname3 and checknet != netname4:
					nickswitch = True
				if checknet == netname:
					if checknick != nickname:
						nickswitch = True
					if checknick == nickname:
						xchat.prnt("{0} is already in use on {1}".format(nickname, netname))
				if checknet == netname2:
					if checknick != nickname2:
						nickswitch = True
					if checknick == nickname2:
						xchat.prnt("{0} is already in use on {1}".format(nickname2, netname2))
				if checknet == netname3:
					if checknick != nickname3:
						nickswitch = True
					if checknick == nickname3:
						xchat.prnt("{0} is already in use on {1}".format(nickname3, netname3))
				if checknet == netname4:
					if checknick != nickname4:
						nickswitch = True
					if checknick == nickname4:
						xchat.prnt("{0} is already in use on {1}".format(nickname4, netname4))
			if charcount == 5:
				if checknet != netname and checknet != netname2 and checknet != netname3 and checknet != netname4 and checknet != netname5:
					nickswitch = True
				if checknet == netname:
					if checknick != nickname:
						nickswitch = True
					if checknick == nickname:
						xchat.prnt("{0} is already in use on {1}".format(nickname, netname))
				if checknet == netname2:
					if checknick != nickname2:
						nickswitch = True
					if checknick == nickname2:
						xchat.prnt("{0} is already in use on {1}".format(nickname2, netname2))
				if checknet == netname3:
					if checknick != nickname3:
						nickswitch = True
					if checknick == nickname3:
						xchat.prnt("{0} is already in use on {1}".format(nickname3, netname3))
				if checknet == netname4:
					if checknick != nickname4:
						nickswitch = True
					if checknick == nickname4:
						xchat.prnt("{0} is already in use on {1}".format(nickname4, netname4))
				if checknet == netname5:
					if checknick != nickname5:
						nickswitch = True
					if checknick == nickname5:
						xchat.prnt("{0} is already in use on {1}".format(nickname5, netname5))
			if nickswitch is True:
				netname2 = xchat.get_info("network")
				nickname2 = xchat.get_info("nick")
				if("undernet" in netname2.lower()):
					channame2 = "#idlerpg"
					botname2 = "idlerpg"
				else:
					channame2 = "#multirpg"
					botname2 = "multirpg"
				# find context
				game_chan2 = xchat.find_context(channel=channame2)
				xchat.prnt("Nick 2 Updated")
		if num == 3 and char3 is True:
			if charcount == 3:
				if checknet != netname and checknet != netname2 and checknet != netname3:
					nickswitch = True
				if checknet == netname:
					if checknick != nickname:
						nickswitch = True
					if checknick == nickname:
						xchat.prnt("{0} is already in use on {1}".format(nickname, netname))
				if checknet == netname2:
					if checknick != nickname2:
						nickswitch = True
					if checknick == nickname2:
						xchat.prnt("{0} is already in use on {1}".format(nickname2, netname2))
				if checknet == netname3:
					if checknick != nickname3:
						nickswitch = True
					if checknick == nickname3:
						xchat.prnt("{0} is already in use on {1}".format(nickname3, netname3))
			if charcount == 4:
				if checknet != netname and checknet != netname2 and checknet != netname3 and checknet != netname4:
					nickswitch = True
				if checknet == netname:
					if checknick != nickname:
						nickswitch = True
					if checknick == nickname:
						xchat.prnt("{0} is already in use on {1}".format(nickname, netname))
				if checknet == netname2:
					if checknick != nickname2:
						nickswitch = True
					if checknick == nickname2:
						xchat.prnt("{0} is already in use on {1}".format(nickname2, netname2))
				if checknet == netname3:
					if checknick != nickname3:
						nickswitch = True
					if checknick == nickname3:
						xchat.prnt("{0} is already in use on {1}".format(nickname3, netname3))
				if checknet == netname4:
					if checknick != nickname4:
						nickswitch = True
					if checknick == nickname4:
						xchat.prnt("{0} is already in use on {1}".format(nickname4, netname4))
			if charcount == 5:
				if checknet != netname and checknet != netname2 and checknet != netname3 and checknet != netname4 and checknet != netname5:
					nickswitch = True
				if checknet == netname:
					if checknick != nickname:
						nickswitch = True
					if checknick == nickname:
						xchat.prnt("{0} is already in use on {1}".format(nickname, netname))
				if checknet == netname2:
					if checknick != nickname2:
						nickswitch = True
					if checknick == nickname2:
						xchat.prnt("{0} is already in use on {1}".format(nickname2, netname2))
				if checknet == netname3:
					if checknick != nickname3:
						nickswitch = True
					if checknick == nickname3:
						xchat.prnt("{0} is already in use on {1}".format(nickname3, netname3))
				if checknet == netname4:
					if checknick != nickname4:
						nickswitch = True
					if checknick == nickname4:
						xchat.prnt("{0} is already in use on {1}".format(nickname4, netname4))
				if checknet == netname5:
					if checknick != nickname5:
						nickswitch = True
					if checknick == nickname5:
						xchat.prnt("{0} is already in use on {1}".format(nickname5, netname5))
			if nickswitch is True:
				netname3 = xchat.get_info("network")
				nickname3 = xchat.get_info("nick")
				if("undernet" in netname3.lower()):
					channame3 = "#idlerpg"
					botname3 = "idlerpg"
				else:
					channame3 = "#multirpg"
					botname3 = "multirpg"
				# find context
				game_chan3 = xchat.find_context(channel=channame3)
				xchat.prnt("Nick 3 Updated")
		if num == 4 and char4 is True:
			if charcount == 4:
				if checknet != netname and checknet != netname2 and checknet != netname3 and checknet != netname4:
					nickswitch = True
				if checknet == netname:
					if checknick != nickname:
						nickswitch = True
					if checknick == nickname:
						xchat.prnt("{0} is already in use on {1}".format(nickname, netname))
				if checknet == netname2:
					if checknick != nickname2:
						nickswitch = True
					if checknick == nickname2:
						xchat.prnt("{0} is already in use on {1}".format(nickname2, netname2))
				if checknet == netname3:
					if checknick != nickname3:
						nickswitch = True
					if checknick == nickname3:
						xchat.prnt("{0} is already in use on {1}".format(nickname3, netname3))
				if checknet == netname4:
					if checknick != nickname4:
						nickswitch = True
					if checknick == nickname4:
						xchat.prnt("{0} is already in use on {1}".format(nickname4, netname4))
			if charcount == 5:
				if checknet != netname and checknet != netname2 and checknet != netname3 and checknet != netname4 and checknet != netname5:
					nickswitch = True
				if checknet == netname:
					if checknick != nickname:
						nickswitch = True
					if checknick == nickname:
						xchat.prnt("{0} is already in use on {1}".format(nickname, netname))
				if checknet == netname2:
					if checknick != nickname2:
						nickswitch = True
					if checknick == nickname2:
						xchat.prnt("{0} is already in use on {1}".format(nickname2, netname2))
				if checknet == netname3:
					if checknick != nickname3:
						nickswitch = True
					if checknick == nickname3:
						xchat.prnt("{0} is already in use on {1}".format(nickname3, netname3))
				if checknet == netname4:
					if checknick != nickname4:
						nickswitch = True
					if checknick == nickname4:
						xchat.prnt("{0} is already in use on {1}".format(nickname4, netname4))
				if checknet == netname5:
					if checknick != nickname5:
						nickswitch = True
					if checknick == nickname5:
						xchat.prnt("{0} is already in use on {1}".format(nickname5, netname5))
			if nickswitch is True:
				netname4 = xchat.get_info("network")
				nickname4 = xchat.get_info("nick")
				if("undernet" in netname4.lower()):
					channame4 = "#idlerpg"
					botname4 = "idlerpg"
				else:
					channame4 = "#multirpg"
					botname4 = "multirpg"
				# find context
				game_chan4 = xchat.find_context(channel=channame4)
				xchat.prnt("Nick 4 Updated")
		if num == 5 and char5 is True:
			if charcount == 5:
				if checknet != netname and checknet != netname2 and checknet != netname3 and checknet != netname4 and checknet != netname5:
					nickswitch = True
				if checknet == netname:
					if checknick != nickname:
						nickswitch = True
					if checknick == nickname:
						xchat.prnt("{0} is already in use on {1}".format(nickname, netname))
				if checknet == netname2:
					if checknick != nickname2:
						nickswitch = True
					if checknick == nickname2:
						xchat.prnt("{0} is already in use on {1}".format(nickname2, netname2))
				if checknet == netname3:
					if checknick != nickname3:
						nickswitch = True
					if checknick == nickname3:
						xchat.prnt("{0} is already in use on {1}".format(nickname3, netname3))
				if checknet == netname4:
					if checknick != nickname4:
						nickswitch = True
					if checknick == nickname4:
						xchat.prnt("{0} is already in use on {1}".format(nickname4, netname4))
				if checknet == netname5:
					if checknick != nickname5:
						nickswitch = True
					if checknick == nickname5:
						xchat.prnt("{0} is already in use on {1}".format(nickname5, netname5))
			if nickswitch is True:
				netname5 = xchat.get_info("network")
				nickname5 = xchat.get_info("nick")
				if("undernet" in netname5.lower()):
					channame5 = "#idlerpg"
					botname5 = "idlerpg"
				else:
					channame5 = "#multirpg"
					botname5 = "multirpg"
				# find context
				game_chan5 = xchat.find_context(channel=channame5)
				xchat.prnt("Nick 5 Updated")
			
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("updatenick", updatenick, help="/updatenick <number> - Updates which network and nick you are using")

def login(word, word_eol, userdata):
	global name
	global pswd
	global name2
	global pswd2
	global name3
	global pswd3
	global name4
	global pswd4
	global name5
	global pswd5
	global upgradeall
	global betmoney
	global itemupgrader
	global setalign
	global setbuy
	global sethero
	global setengineer
	global singlefight
	global netname
	global netname2
	global netname3
	global netname4
	global netname5
	global nickname
	global nickname2
	global nickname3
	global nickname4
	global nickname5
	global channame
	global channame2
	global channame3
	global channame4
	global channame5
	global botname
	global botname2
	global botname3
	global botname4
	global botname5
	global game_chan
	global game_chan2
	global game_chan3
	global game_chan4
	global game_chan5
	global evilmode
	global rawstatsmode
	global char1
	global char2
	global char3
	global char4
	global char5
	global charcount
	global rawstatsswitch
	global gameactive
	global customnetworksettings
	global custombotname
	global customchanname
	global customnetworksettings2
	global custombotname2
	global customchanname2
	global customnetworksettings3
	global custombotname3
	global customchanname3
	global customnetworksettings4
	global custombotname4
	global customchanname4
	global customnetworksettings5
	global custombotname5
	global customchanname5
	global bottextmode
	global errortextmode
	global intervaltextmode
	global networklist
	
	charcount += 1
	
	netlist = []
	for entry in networklist:
		if entry[3] == 1:
			netlist.append( ( entry[0] ) )
	if charcount == 1:
		gameactive = True
		netcheck = True
		netname = xchat.get_info("network")
		nickname = xchat.get_info("nick")

		if customnetworksettings is False:
			netcheck = False
			for entry in networklist:
				if entry[0].lower() in netname.lower():
					netcheck = True
			if netcheck is False:
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
			char1 = False
			gameactive = False
			name = None
			pswd = None
			return

		if charcount == 1:
			if(name != None and pswd != None):
				char1 = True
				usecommand("login {0} {1}".format(name, pswd), 1 )
		
	if charcount == 2:
		netcheck = True
		netname2 = xchat.get_info("network")
		nickname2 = xchat.get_info("nick")

		if customnetworksettings2 is False:
			netcheck = False
			for entry in networklist:
				if entry[0].lower() in netname2.lower():
					netcheck = True
			if netcheck is False:
				xchat.prnt("NETWORK ERROR: Networks supported: {0}".format(netlist))
				xchat.prnt("Current Network: {0}.  The network name needs to have one of the above names in it".format(netname2))

			if("undernet" in netname2.lower()):
				channame2 = "#idlerpg"
				botname2 = "idlerpg"
			else:
				channame2 = "#multirpg"
				botname2 = "multirpg"

		if customnetworksettings2 is True:
			channame2 = customchanname2
			botname2 = custombotname2
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

		if(name2 is None or pswd2 is None or netcheck is False):
			charcount = 1
		if charcount == 2:
			if rawstatsmode is True or rawstatsswitch is True:
				opcheck = False
				userlist = game_chan2.get_list("users")
				for user in userlist:
					if user.nick == botname2:
						botprefix = user.prefix
						if(botprefix == "@" or botprefix == "%"):
							opcheck = True
				if opcheck is False:
					rawstatsmode = False
					rawstatsswitch = False
					xchat.prnt("GameBot Not Opped Changing to RawPlayers")
					configwrite()
			if(netname2 != netname and name2 != name):
				char2 = True
				usecommand("login {0} {1}".format(name2, pswd2), 2 )
			if(netname2 != netname and name2 == name):
				charcount = 1
				xchat.prnt("Character {0} is already logged in".format(name))
			if(netname2 == netname):
				if(nickname2 != nickname):
					char2 = True
					usecommand("login {0} {1}".format(name2, pswd2), 2 )
				if(nickname2 == nickname):
					charcount = 1
					xchat.prnt("Character {0} is already logged in".format(name))
		if charcount == 1:
			char2 = False
			netname2 = None
			nickname2 = None
			channame2 = None
			botname2 = None
			game_chan2 = None
			name2 = None
			pswd2 = None
			return

	if charcount == 3:
		netcheck = True
		netname3 = xchat.get_info("network")
		nickname3 = xchat.get_info("nick")
		if customnetworksettings3 is False:
			netcheck = False
			for entry in networklist:
				if entry[0].lower() in netname3.lower():
					netcheck = True
			if netcheck is False:
				xchat.prnt("NETWORK ERROR: Networks supported: {0}".format(netlist))
				xchat.prnt("Current Network: {0}.  The network name needs to have one of the above names in it".format(netname3))
			if("undernet" in netname3.lower()):
				channame3 = "#idlerpg"
				botname3 = "idlerpg"
			else:
				channame3 = "#multirpg"
				botname3 = "multirpg"

		if customnetworksettings3 is True:
			channame3 = customchanname3
			botname3 = custombotname3
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

		if(name3 is None or pswd3 is None or netcheck is False):
			charcount = 2

		if charcount == 3:
			if rawstatsmode is True or rawstatsswitch is True:
				opcheck = False
				userlist = game_chan3.get_list("users")
				for user in userlist:
					if user.nick == botname3:
						botprefix = user.prefix
						if(botprefix == "@" or botprefix == "%"):
							opcheck = True
				if opcheck is False:
					rawstatsmode = False
					rawstatsswitch = False
					xchat.prnt("GameBot Not Opped Changing to RawPlayers")
					configwrite()
			if(netname3 != netname and netname3 != netname2 and name3 != name and name3 != name2):
				char3 = True
				usecommand("login {0} {1}".format(name3, pswd3), 3 )

			if((netname3 != netname and netname3 != netname2) and (name3 == name or name3 == name2)):
				charcount = 2
				xchat.prnt("Character {0} is already logged in".format(word[1]))
				
			if(netname3 == netname):
				if(nickname3 != nickname):
					char3 = True
					usecommand("login {0} {1}".format(name3, pswd3), 3 )
				if(nickname3 == nickname): 
					charcount = 2
					xchat.prnt("Character {0} is already logged in".format(word[1]))

			if(netname3 == netname2):
				if(nickname3 != nickname2):
					char3 = True
					usecommand("login {0} {1}".format(name3, pswd3), 3 )
				if(nickname3 == nickname2): 
					charcount = 2
					xchat.prnt("Character {0} is already logged in".format(word[1]))
		if charcount == 2:
			char3 = False
			netname3 = None
			nickname3 = None
			channame3 = None
			botname3 = None
			game_chan3 = None
			name3 = None
			pswd3 = None
			return

	if charcount == 4:
		netcheck = True
		netname4 = xchat.get_info("network")
		nickname4 = xchat.get_info("nick")
		if customnetworksettings4 is False:
			netcheck = False
			for entry in networklist:
				if entry[0].lower() in netname4.lower():
					netcheck = True
			if netcheck is False:
				xchat.prnt("NETWORK ERROR: Networks supported: {0}".format(netlist))
				xchat.prnt("Current Network: {0}.  The network name needs to have one of the above names in it".format(netname4))
			if("undernet" in netname4.lower()):
				channame4 = "#idlerpg"
				botname4 = "idlerpg"
			else:
				channame4 = "#multirpg"
				botname4 = "multirpg"

		if customnetworksettings4 is True:
			channame4 = customchanname4
			botname4 = custombotname4
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

		if(name4 is None or pswd4 is None or netcheck is False):
			charcount = 3
		if charcount == 4:
			if rawstatsmode is True or rawstatsswitch is True:
				opcheck = False
				userlist = game_chan4.get_list("users")
				for user in userlist:
					if user.nick == botname4:
						botprefix = user.prefix
						if(botprefix == "@" or botprefix == "%"):
							opcheck = True
				if opcheck is False:
					rawstatsmode = False
					rawstatsswitch = False
					xchat.prnt("GameBot Not Opped Changing to RawPlayers")
					configwrite()
			if(netname4 != netname and netname4 != netname2 and netname4 != netname3 and name4 != name and name4 != name2 and name4 != name3):
				char4 = True
				usecommand("login {0} {1}".format(name4, pswd4), 4 )
			if((netname4 != netname and netname4 != netname2 and netname4 != netname3) and (name4 == name or name4 == name2 or name4 == name3)):
				charcount = 3
				xchat.prnt("Character {0} is already logged in".format(word[1]))

			if(netname4 == netname):
				if(nickname4 != nickname):
					char4 = True
					usecommand("login {0} {1}".format(name4, pswd4), 4 )
				if(nickname4 == nickname):
					charcount = 3
					xchat.prnt("Character {0} is already logged in".format(word[1]))
			if(netname4 == netname2):
				if(nickname4 != nickname2):
					char4 = True
					usecommand("login {0} {1}".format(name4, pswd4), 4 )
				if(nickname4 == nickname2):
					charcount = 3
					xchat.prnt("Character {0} is already logged in".format(word[1]))
			if(netname4 == netname3):
				if(nickname4 != nickname3):
					char4 = True
					usecommand("login {0} {1}".format(name4, pswd4), 4 )
				if(nickname4 == nickname3):
					charcount = 3
					xchat.prnt("Character {0} is already logged in".format(word[1]))
		if charcount == 3:
			char4 = False
			netname4 = None
			nickname4 = None
			channame4 = None
			botname4 = None
			game_chan4 = None
			name4 = None
			pswd4 = None
			return

	if charcount == 5:
		netcheck = True
		netname5 = xchat.get_info("network")
		nickname5 = xchat.get_info("nick")
		if customnetworksettings5 is False:
			netcheck = False
			for entry in networklist:
				if entry[0].lower() in netname5.lower():
					netcheck = True
			if netcheck is False:
				xchat.prnt("NETWORK ERROR: Networks supported: {0}".format(netlist))
				xchat.prnt("Current Network: {0}.  The network name needs to have one of the above names in it".format(netname5))
			if("undernet" in netname5.lower()):
				channame5 = "#idlerpg"
				botname5 = "idlerpg"
			else:
				channame5 = "#multirpg"
				botname5 = "multirpg"

		if customnetworksettings5 is True:
			channame5 = customchanname5
			botname5 = custombotname5
		# find context
		game_chan5 = xchat.find_context(channel=channame5)
	
		if(game_chan5 is None):
			xchat.prnt("Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame5))
			charcount = 4
		try:
			if(name5 is None or pswd5 is None):
				name5 = word[1]
				pswd5 = word[2]
		except IndexError:
			xchat.prnt( "LOGIN ERROR: To log in use /login CharName Password" )
			charcount = 4
		if(name5 is None or pswd5 is None or netcheck is False):
			charcount = 4
		if charcount == 5:
			if rawstatsmode is True or rawstatsswitch is True:
				opcheck = False
				userlist = game_chan5.get_list("users")
				for user in userlist:
					if user.nick == botname5:
						botprefix = user.prefix
						if(botprefix == "@" or botprefix == "%"):
							opcheck = True
				if opcheck is False:
					rawstatsmode = False
					rawstatsswitch = False
					xchat.prnt("GameBot Not Opped Changing to RawPlayers")
					configwrite()
			if(netname5 != netname and netname5 != netname2 and netname5 != netname3 and netname5 != netname4 and name5 != name and name5 != name2 and name5 != name3 and name5 != name4):
				char5 = True
				usecommand("login {0} {1}".format(name5, pswd5), 5 )
			if((netname5 != netname and netname5 != netname2 and netname5 != netname3 and netname5 != netname4) and (name5 == name or name5 == name2 or name5 == name3 or name5 == name4)):
				charcount = 4
				xchat.prnt("Character {0} is already logged in".format(word[1]))
				
			if(netname5 == netname):
				if(nickname5 != nickname):
					char5 = True
					usecommand("login {0} {1}".format(name5, pswd5), 5 )
				if(nickname5 == nickname):
					charcount = 4
					xchat.prnt("Character {0} is already logged in".format(word[1]))
			if(netname5 == netname2):
				if(nickname5 != nickname2):
					char5 = True
					usecommand("login {0} {1}".format(name5, pswd5), 5 )
				if(nickname5 == nickname2):
					charcount = 4
					xchat.prnt("Character {0} is already logged in".format(word[1]))
			if(netname5 == netname3):
				if(nickname5 != nickname3):
					char5 = True
					usecommand("login {0} {1}".format(name5, pswd5), 5 )
				if(nickname5 == nickname3):
					charcount = 4
					xchat.prnt("Character {0} is already logged in".format(word[1]))
			if(netname5 == netname4):
				if(nickname5 != nickname4):
					char5 = True
					usecommand("login {0} {1}".format(name5, pswd5), 5 )
				if(nickname5 == nickname4):
					charcount = 4
					xchat.prnt("Character {0} is already logged in".format(word[1]))
		if charcount == 4:
			char5 = False
			netname5 = None
			nickname5 = None
			channame5 = None
			botname5 = None
			game_chan5 = None
			name5 = None
			pswd5 = None
			return

	if (charcount >= 1 and charcount <= 5):        
		time.sleep(3) # Needed
		usecommand("whoami", charcount)
		usecommand("stats", charcount)
		xchat.prnt("Player Character {0} has logged in".format(charcount))
	if charcount == 1:
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
	if charcount >= 6:
		xchat.prnt("You can only play with 5 characters")
		charcount = 5

	if rawstatsswitch is True or rawstatsmode is True:
		webdata()

	# call main directly
	main(None)
	return xchat.EAT_ALL

# hook login command
xchat.hook_command("login", login, help="/login <charname> <password> - You can use this to login upto 5 characters into the game")

def logoutchar(word, word_eol, userdata):
	global charcount
	global char1
	global char2
	global char3
	global char4
	global char5
	global netname
	global netname2
	global netname3
	global netname4
	global netname5
	global channame
	global channame2
	global channame3
	global channame4
	global channame5
	global botname
	global botname2
	global botname3
	global botname4
	global botname5
	global game_chan
	global game_chan2
	global game_chan3
	global game_chan4
	global game_chan5
	global name
	global name2
	global name3
	global name4
	global name5
	global pswd
	global pswd2
	global pswd3
	global pswd4
	global pswd5
	global gameactive
	global myentry
	global rawmyentry
	global myentry2
	global rawmyentry2
	global myentry3
	global rawmyentry3
	global myentry4
	global rawmyentry4
	global myentry5
	global rawmyentry5
	global ttlfrozen1
	global ttlfrozen2
	global ttlfrozen3
	global ttlfrozen4
	global ttlfrozen5
	
	if charcount == 5:
		xchat.prnt("Character {0} Logged Out".format(name5))
		char5 = False
		netname5 = None
		channame5 = None
		botname5 = None
		game_chan5 = None
		name5 = None
		pswd5 = None
		myentry5 = None
		rawmyentry5 = None
		ttlfrozen5 = 0        
	if charcount == 4:
		xchat.prnt("Character {0} Logged Out".format(name4))
		char4 = False
		netname4 = None
		channame4 = None
		botname4 = None
		game_chan4 = None
		name4 = None
		pswd4 = None
		myentry4 = None
		rawmyentry4 = None
		ttlfrozen4 = 0        
	if charcount == 3:
		xchat.prnt("Character {0} Logged Out".format(name3))
		char3 = False
		netname3 = None
		channame3 = None
		botname3 = None
		game_chan3 = None
		name3 = None
		pswd3 = None
		myentry3 = None
		rawmyentry3 = None
		ttlfrozen3 = 0        
	if charcount == 2:
		xchat.prnt("Character {0} Logged Out".format(name2))
		char2 = False
		netname2 = None
		channame2 = None
		botname2 = None
		game_chan2 = None
		name2 = None
		pswd2 = None
		myentry2 = None
		rawmyentry2 = None
		ttlfrozen2 = 0        
	if charcount == 1:
		xchat.prnt("Character {0} Logged Out".format(name))
		char1 = False
		netname = None
		channame = None
		botname = None
		game_chan = None
		name = None
		pswd = None
		myentry = None
		rawmyentry = None
		gameactive = False
		ttlfrozen1 = 0        
	if(charcount == 0):
		xchat.prnt("All Characters have already been Logged Out")
	if(charcount >= 1 and charcount <= 5):
		charcount -= 1
	return xchat.EAT_ALL

xchat.hook_command("logoutchar", logoutchar, help="/logoutchar - Logs out the last character from the PlayBot")

def setalignlevel(word, word_eol, userdata):
	global setalign
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
	global rawmyentry2
	global rawmyentry3
	global rawmyentry4
	global rawmyentry5
	global char1
	global char2
	global char3
	global char4
	global char5
	global gameactive
	global ttlfrozen1
	global ttlfrozen2
	global ttlfrozen3
	global ttlfrozen4
	global ttlfrozen5

	if gameactive is True:
		if char1 is True:
			rawmyentry = None
			ttlfrozen1 = 0
		if char2 is True:
			rawmyentry2 = None
			ttlfrozen2 = 0
		if char3 is True:
			rawmyentry3 = None
			ttlfrozen3 = 0
		if char4 is True:
			rawmyentry4 = None
			ttlfrozen4 = 0
		if char5 is True:
			rawmyentry5 = None
			ttlfrozen5 = 0
		rawstatsmode = False
		rawstatsswitch = False
		webdata()
		newitemslister(1, 1)
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
	global char1
	global char2
	global char3
	global char4
	global char5
	
	if gameactive is True:
		evilmode = True
		secondalign = "undead"
		alignlevel = 0
		if char1 is True:
			usecommand("align undead", 1)
		if char2 is True:
			usecommand("align undead", 2)
		if char3 is True:
			usecommand("align undead", 3)
		if char4 is True:
			usecommand("align undead", 4)
		if char5 is True:
			usecommand("align undead", 5)
		xchat.prnt("Evil Mode On.  To turn it back off use /eviloff")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("evilon", evilon, help="/evilon - Aligns you to undead and turns undead/priest alignment switching on")

def eviloff(word, word_eol, userdata):
	global secondalign
	global alignlevel
	global setalign
	global evilmode
	global gameactive

	if gameactive is True:
		evilmode = False
		secondalign = "human"
		alignlevel = setalign
		xchat.prnt("Evil Mode Off.  To turn it back on use /evilon")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("eviloff", eviloff, help="/eviloff - To turn Evil Mode off")

def helpplaybot(word, word_eol, userdata):
	xchat.prnt("PlayBot Commands List")
	xchat.prnt("")
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
	xchat.prnt("Update Nick                 - /updatenick charnum")
	xchat.prnt("Upgrade All 1 Mode Of       - /upgradealloff")
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
	global char1
	global char2
	global char3
	global char4
	global char5
	global name
	global name2
	global name3
	global name4
	global name5
	global rawstatsmode
	global gameactive
	global bottextmode
	global errortextmode
	global intervaltextmode
	global netname
	global netname2
	global netname3
	global netname4
	global netname5
	
	if gameactive is True:
		xchat.prnt("Playbot Settings List")
		xchat.prnt("")
		xchat.prnt("Align Level - {0}".format(setalign))
		xchat.prnt("Bet Money - {0}".format(betmoney))
		xchat.prnt("Bot Text Mode - {0}".format(bottextmode))
		xchat.prnt("Engineer Buy Level - {0}".format(setengineer))
		xchat.prnt("Error Text Mode - {0}".format(errortextmode))
		xchat.prnt("Evil Mode - {0}".format(evilmode))
		xchat.prnt("Hero Buy ItemScore - {0}".format(sethero))
		xchat.prnt("Interval Text Mode - {0}".format(intervaltextmode))
		xchat.prnt("Item Buy Level - {0}".format(setbuy))
		xchat.prnt("Item Upgrader Mode - {0}".format(itemupgrader))
		xchat.prnt("Player Character 1 - {0}, {1}.  Network {2}".format(char1, name, netname))
		xchat.prnt("Player Character 2 - {0}, {1}.  Network {2}".format(char2, name2, netname2))
		xchat.prnt("Player Character 3 - {0}, {1}.  Network {2}".format(char3, name3, netname3))
		xchat.prnt("Player Character 4 - {0}, {1}.  Network {2}".format(char4, name4, netname4))
		xchat.prnt("Player Character 5 - {0}, {1}.  Network {2}".format(char5, name5, netname5))
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
	global char1
	global char2
	global char3
	global char4
	global char5
	global name
	global name2
	global name3
	global name4
	global name5
	global gameactive
	
	if gameactive is True:
		if char1 is True:
			xchat.prnt("{0}'s Status".format(name))
			xchat.prnt(" ")
			characterstats(1)
		if char2 is True:
			xchat.prnt(" ")
			xchat.prnt("{0}'s Status".format(name2))
			xchat.prnt(" ")
			characterstats(2)
		if char3 is True:
			xchat.prnt(" ")
			xchat.prnt("{0}'s Status".format(name3))
			xchat.prnt(" ")
			characterstats(3)
		if char4 is True:
			xchat.prnt(" ")
			xchat.prnt("{0}'s Status".format(name4))
			xchat.prnt(" ")
			characterstats(4)
		if char5 is True:
			xchat.prnt(" ")
			xchat.prnt("{0}'s Status".format(name5))
			xchat.prnt(" ")
			characterstats(5)
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("status", status, help="/status - Gives a list of character stats")

def characterstats(num):
	global rawstatsmode
	global myentry
	global myentry2
	global myentry3
	global myentry4
	global myentry5
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

	getitems2(num)

	if num == 1:
		myentrys = myentry
	if num == 2:
		myentrys = myentry2
	if num == 3:
		myentrys = myentry3
	if num == 4:
		myentrys = myentry4
	if num == 5:
		myentrys = myentry5

	if rawstatsmode is True and webworks is True:
		ranknumber = myentrys[1]
	if rawstatsmode is False:
		ranknumber = rankplace

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

def items(word, word_eol, userdata):
	global char1
	global char2
	global char3
	global char4
	global char5
	global name
	global name2
	global name3
	global name4
	global name5
	global gameactive

	if gameactive is True:
		if char1 is True:
			xchat.prnt("{0}'s Items List".format(name))
			xchat.prnt(" ")
			characteritems(1)
		if char2 is True:
			xchat.prnt(" ")
			xchat.prnt("{0}'s Items List".format(name2))
			xchat.prnt(" ")
			characteritems(2)
		if char3 is True:
			xchat.prnt(" ")
			xchat.prnt("{0}'s Items List".format(name3))
			xchat.prnt(" ")
			characteritems(3)
		if char4 is True:
			xchat.prnt(" ")
			xchat.prnt("{0}'s Items List".format(name4))
			xchat.prnt(" ")
			characteritems(4)
		if char5 is True:
			xchat.prnt(" ")
			xchat.prnt("{0}'s Items List".format(name5))
			xchat.prnt(" ")
			characteritems(5)
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
	global mysum

	getitems2(num)
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

def bestall(word, word_eol, userdata):
	global gameactive
	global name
	global name2
	global name3
	global name4
	global name5
	global webworks
	global char1
	global char2
	global char3
	global char4
	global char5
	
	if gameactive is True:
		webdata()
		if webworks is True:
			if char1 is True:
				xchat.prnt("Best All for {0}".format(name))
				xchat.prnt(" ")
				bestallmulti(1)
			if char2 is True:
				xchat.prnt(" ")
				xchat.prnt("Best All for {0}".format(name2))
				xchat.prnt(" ")
				bestallmulti(2)
			if char3 is True:
				xchat.prnt(" ")
				xchat.prnt("Best All for {0}".format(name3))
				xchat.prnt(" ")
				bestallmulti(3)
			if char4 is True:
				xchat.prnt(" ")
				xchat.prnt("Best All for {0}".format(name4))
				xchat.prnt(" ")
				bestallmulti(4)
			if char5 is True:
				xchat.prnt(" ")
				xchat.prnt("Best All for {0}".format(name5))
				xchat.prnt(" ")
				bestallmulti(5)
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("bestall", bestall, help="/bestall - Shows Best Bet/Fight/Attack/Slay")

def bestallmulti(num):
	global fightSum1
	global fightSum2
	global fightSum3
	global fightSum4
	global fightSum5
	global rankplace
	global name
	global name2
	global name3
	global name4
	global name5
	global charcount
	global myentry
	global myentry2
	global myentry3
	global myentry4
	global myentry5
	global rawstatsmode
	global webworks
	global level

	if charcount >= 2:
		getitems2(num)
	if num == 1:
		fightsumlist = fightSum1
		names = name
		myentrys = myentry
	if num == 2:
		fightsumlist = fightSum2
		names = name2
		myentrys = myentry2
	if num == 3:
		fightsumlist = fightSum3
		names = name3
		myentrys = myentry3
	if num == 4:
		fightsumlist = fightSum4
		names = name4
		myentrys = myentry4
	if num == 5:
		fightsumlist = fightSum5
		names = name5
		myentrys = myentry5

	if rawstatsmode is True and webworks is True:
		ranknumber = myentrys[1]
	if rawstatsmode is False:
		ranknumber = rankplace
	newitemslister(num,1)
	newitemslister(num,2)
	if(level < 10):
		xchat.prnt("Creep Attacks Start at Level 10")
	if(level >= 10):
		creep = bestattack(num)
		xchat.prnt("BestAttack: {0}".format(creep))
	if(level < 40):
		xchat.prnt("Slaying Monsters Start at Level 40")
	if(level >= 40):
		monster = bestslay(num)
		xchat.prnt("BestSlay: {0}".format(monster))
	if(level < 30):
		xchat.prnt("Bets Start at Level 30")
	if(level >= 30):
		bbet = bestbet(num)
		xchat.prnt("BestBet {0} {1}".format( bbet[0][0], bbet[1][0] ))
	if(level < 10):
		xchat.prnt("Fights Start at Level 10")
	if(level >= 10):
		ufight = testfight(num)
		try:
			ufightcalc = fightsumlist / ufight[2]
		except ZeroDivisionError:
			ufightcalc = 0
		xchat.prnt("Best Fight for Rank {0}: {1} [{2}]  Opponent: Rank {3}: {4} [{5}], Odds {6}".format(ranknumber, names, int(fightsumlist), ufight[5], ufight[0], int(ufight[2]), ufightcalc))
	
def on_message(word, word_eol, userdata):
	global chanmessage
	global name
	global name2
	global name3
	global name4
	global name5
	global interval
	global botname
	global botname2
	global botname3
	global botname4
	global botname5
	global netname
	global netname2
	global netname3
	global netname4
	global netname5
	global networkname
	global networkname2
	global networkname3
	global networkname4
	global networkname5
	global char1
	global char2
	global char3
	global char4
	global char5
	global game_chan
	global game_chan2
	global game_chan3
	global game_chan4
	global game_chan5
	global nickname
	global nickname2
	global nickname3
	global nickname4
	global nickname5
	global nickserv1
	global nickserv2
	global nickserv3
	global nickserv4
	global nickserv5
	global nickservpass1
	global nickservpass2
	global nickservpass3
	global nickservpass4
	global nickservpass5
	global connectfail1
	global connectfail2
	global connectfail3
	global connectfail4
	global connectfail5
	global webworks
	global gameactive

	if gameactive is True:
		checknet = xchat.get_info("network")
		checknick = xchat.get_info("nick")
		if chanmessage is True:
			chanmessage = False

		if char1 is True:
			if(checknet == netname and checknick == nickname):
				if(botname in word[0] and "{0}, the level".format(name) in word[1] and "is now online" in word[1]):
						connectfail1 = 0
						if(nickserv1 is True):
							if("dalnet" in netname.lower()):
								game_chan.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass1) )
							else:
								game_chan.command( "msg nickserv identify {0}".format(nickservpass1) )
				if botname in word[0] and "fights with the legendary" in word[1] and "removed from {0}".format(name) in word[1] and "in a moment" in word[1]:
						interval = 60
						hookmain()
				if webworks is True and networkname != None:
					if char1 is True:
						if botname in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname in word[1] and "nickname {0}".format(nickname) in word[1]:
								usecommand("whoami", 1)
					if char2 is True and networkname == networkname2:
						if botname in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname in word[1] and "nickname {0}".format(nickname2) in word[1]:
								usecommand("whoami", 1)
					if char3 is True and networkname == networkname3:
						if botname in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname in word[1] and "nickname {0}".format(nickname3) in word[1]:
								usecommand("whoami", 1)
					if char4 is True and networkname == networkname4:
						if botname in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname in word[1] and "nickname {0}".format(nickname4) in word[1]:
								usecommand("whoami", 1)
					if char5 is True and networkname == networkname5:
						if botname in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname in word[1] and "nickname {0}".format(nickname5) in word[1]:
								usecommand("whoami", 1)
		if char2 is True:
			if(checknet == netname2 and checknick == nickname2):
				if(botname2 in word[0] and "{0}, the level".format(name2) in word[1] and "is now online" in word[1]):
						connectfail2 = 0
						if(nickserv2 is True):
							if("dalnet" in netname2.lower()):
								game_chan2.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass2) )
							else:
								game_chan2.command( "msg nickserv identify {0}".format(nickservpass2) )
				if botname2 in word[0] and "fights with the legendary" in word[1] and "removed from {0}".format(name2) in word[1] and "in a moment" in word[1]:
						interval = 60
						hookmain()
				if webworks is True and networkname2 != None:
					if char1 is True and networkname2 == networkname:
						if botname2 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname2 in word[1] and "nickname {0}".format(nickname) in word[1]:
								usecommand("whoami", 2)
					if char2 is True:
						if botname2 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname2 in word[1] and "nickname {0}".format(nickname2) in word[1]:
								usecommand("whoami", 2)
					if char3 is True and networkname2 == networkname3:
						if botname2 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname2 in word[1] and "nickname {0}".format(nickname3) in word[1]:
								usecommand("whoami", 2)
					if char4 is True and networkname2 == networkname4:
						if botname2 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname2 in word[1] and "nickname {0}".format(nickname4) in word[1]:
								usecommand("whoami", 2)
					if char5 is True and networkname2 == networkname5:
						if botname2 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname2 in word[1] and "nickname {0}".format(nickname5) in word[1]:
								usecommand("whoami", 2)
		if char3 is True:
			if(checknet == netname3 and checknick == nickname3):
				if(botname3 in word[0] and "{0}, the level".format(name3) in word[1] and "is now online" in word[1]):
						connectfail3 = 0
						if(nickserv3 is True):
							if("dalnet" in netname3.lower()):
								game_chan3.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass3) )
							else:
								game_chan3.command( "msg nickserv identify {0}".format(nickservpass3) )
				if botname3 in word[0] and "fights with the legendary" in word[1] and "removed from {0}".format(name3) in word[1] and "in a moment" in word[1]:
						interval = 60
						hookmain()
				if webworks is True and networkname3 != None:
					if char1 is True and networkname3 == networkname:
						if botname3 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname3 in word[1] and "nickname {0}".format(nickname) in word[1]:
								usecommand("whoami", 3)
					if char2 is True and networkname3 == networkname2:
						if botname3 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname3 in word[1] and "nickname {0}".format(nickname2) in word[1]:
								usecommand("whoami", 3)
					if char3 is True:
						if botname3 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname3 in word[1] and "nickname {0}".format(nickname3) in word[1]:
								usecommand("whoami", 3)
					if char4 is True and networkname3 == networkname4:
						if botname3 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname3 in word[1] and "nickname {0}".format(nickname4) in word[1]:
								usecommand("whoami", 3)
					if char5 is True and networkname3 == networkname5:
						if botname3 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname3 in word[1] and "nickname {0}".format(nickname5) in word[1]:
								usecommand("whoami", 3)
		if char4 is True:
			if(checknet == netname4 and checknick == nickname4):
				if(botname4 in word[0] and "{0}, the level".format(name4) in word[1] and "is now online" in word[1]):
						connectfail4 = 0
						if(nickserv4 is True):
							if("dalnet" in netname4.lower()):
								game_chan4.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass4) )
							else:
								game_chan4.command( "msg nickserv identify {0}".format(nickservpass4) )
				if botname4 in word[0] and "fights with the legendary" in word[1] and "removed from {0}".format(name4) in word[1] and "in a moment" in word[1]:
						interval = 60
						hookmain()
				if webworks is True and networkname4 != None:
					if char1 is True and networkname4 == networkname:
						if botname4 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname4 in word[1] and "nickname {0}".format(nickname) in word[1]:
								usecommand("whoami", 4)
					if char2 is True and networkname4 == networkname2:
						if botname4 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname4 in word[1] and "nickname {0}".format(nickname2) in word[1]:
								usecommand("whoami", 4)
					if char3 is True and networkname4 == networkname3:
						if botname4 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname4 in word[1] and "nickname {0}".format(nickname3) in word[1]:
								usecommand("whoami", 4)
					if char4 is True:
						if botname4 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname4 in word[1] and "nickname {0}".format(nickname4) in word[1]:
								usecommand("whoami", 4)
					if char5 is True and networkname4 == networkname5:
						if botname4 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname4 in word[1] and "nickname {0}".format(nickname5) in word[1]:
								usecommand("whoami", 4)
		if char5 is True:
			if(checknet == netname5 and checknick == nickname5):
				if(botname5 in word[0] and "{0}, the level".format(name5) in word[1] and "is now online" in word[1]):
						connectfail5 = 0
						if(nickserv5 is True):
							if("dalnet" in netname5.lower()):
								game_chan5.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass5) )
							else:
								game_chan5.command( "msg nickserv identify {0}".format(nickservpass5) )
				if botname5 in word[0] and "fights with the legendary" in word[1] and "removed from {0}".format(name5) in word[1] and "in a moment" in word[1]:
						interval = 60
						hookmain()
				if webworks is True and networkname5 != None:
					if char1 is True and networkname5 == networkname:
						if botname5 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname5 in word[1] and "nickname {0}".format(nickname) in word[1]:
								usecommand("whoami", 5)
					if char2 is True and networkname5 == networkname2:
						if botname5 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname5 in word[1] and "nickname {0}".format(nickname2) in word[1]:
								usecommand("whoami", 5)
					if char3 is True and networkname5 == networkname3:
						if botname5 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname5 in word[1] and "nickname {0}".format(nickname3) in word[1]:
								usecommand("whoami", 5)
					if char4 is True and networkname5 == networkname4:
						if botname5 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname5 in word[1] and "nickname {0}".format(nickname4) in word[1]:
								usecommand("whoami", 5)
					if char5 is True:
						if botname5 in word[0] and ", the level" in word[1] and "is now online" in word[1] and networkname5 in word[1] and "nickname {0}".format(nickname5) in word[1]:
								usecommand("whoami", 5)

def recv_notice_cb(word, word_eol, userdata):
	global botname
	global botname2
	global botname3
	global botname4
	global botname5
	global name
	global name2
	global name3
	global name4
	global name5
	global pswd
	global pswd2
	global pswd3
	global pswd4
	global pswd5
	global notice
	global gameactive
	global char1
	global char2
	global char3
	global char4
	global char5
	global game_chan
	global game_chan2
	global game_chan3
	global game_chan4
	global game_chan5
	global netname
	global netname2
	global netname3
	global netname4
	global netname5
	global nickname
	global nickname2
	global nickname3
	global nickname4
	global nickname5
	global multirpgclass
	global charcount

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
		if char5 is True:
			nickname5 = game_chan5.get_info("nick")

		if notice is True:
			notice = False
		if char1 is True:
			if(word[0] == botname and "Sorry, no such account name" in word[1]):                
				if(checknet == netname and checknick == nickname):
					xchat.prnt("Player {0} Not Registered".format(name))
					usecommand("register {0} {1} {2}".format(name,pswd,multirpgclass),1)
			if(word[0] == botname and "Wrong password" in word[1]):                
				if(checknet == netname and checknick == nickname):
					xchat.prnt("Wrong password")
					charcount = 0
					name = None
					pswd = None
					gameactive = False                              
					char1 = False
		if char2 is True:
			if(word[0] == botname2 and "Sorry, no such account name" in word[1]):                
				if(checknet == netname2 and checknick == nickname2):
					xchat.prnt("Player {0} Not Registered".format(name2))
					usecommand("register {0} {1} {2}".format(name2,pswd2,multirpgclass),2)
			if(word[0] == botname2 and "Wrong password" in word[1]):                
				if(checknet == netname2 and checknick == nickname2):
					xchat.prnt("Wrong password")
					charcount = 1
					name2 = None
					pswd2 = None
					char2 = False
		if char3 is True:
			if(word[0] == botname3 and "Sorry, no such account name" in word[1]):                
				if(checknet == netname3 and checknick == nickname3):
					xchat.prnt("Player {0} Not Registered".format(name3))
					usecommand("register {0} {1} {2}".format(name3,pswd3,multirpgclass),3)
			if(word[0] == botname3 and "Wrong password" in word[1]):                
				if(checknet == netname3 and checknick == nickname3):
					xchat.prnt("Wrong password")
					charcount = 2
					name3 = None
					pswd3 = None
					char3 = False
		if char4 is True:
			if(word[0] == botname4 and "Sorry, no such account name" in word[1]):                
				if(checknet == netname4 and checknick == nickname4):
					xchat.prnt("Player {0} Not Registered".format(name4))
					usecommand("register {0} {1} {2}".format(name4,pswd4,multirpgclass),4)
			if(word[0] == botname4 and "Wrong password" in word[1]):                
				if(checknet == netname4 and checknick == nickname4):
					xchat.prnt("Wrong password")
					charcount = 3
					name4 = None
					pswd4 = None
					char4 = False
		if char5 is True:
			if(word[0] == botname5 and "Sorry, no such account name" in word[1]):                
				if(checknet == netname5 and checknick == nickname5):
					xchat.prnt("Player {0} Not Registered".format(name5))
					usecommand("register {0} {1} {2}".format(name5,pswd5,multirpgclass),5)
			if(word[0] == botname5 and "Wrong password" in word[1]):                
				if(checknet == netname5 and checknick == nickname5):
					xchat.prnt("Wrong password")
					charcount = 4
					name5 = None
					pswd5 = None
					char5 = False

def private_cb(word, word_eol, userdata):
	global botname
	global botname2
	global botname3
	global botname4
	global botname5
	global channame
	global channame2
	global channame3
	global channame4
	global channame5
	global name
	global name2
	global name3
	global name4
	global name5
	global pswd
	global pswd2
	global pswd3
	global pswd4
	global pswd5
	global private
	global rawmyentry
	global rawmyentry2
	global rawmyentry3
	global rawmyentry4
	global rawmyentry5
	global level
	global fights
	global singlefight
	global webworks
	global bets
	global rawstatsmode
	global char1
	global char2
	global char3
	global char4
	global char5
	global gameactive
	global game_chan
	global game_chan2
	global game_chan3
	global game_chan4
	global game_chan5
	global netname
	global netname2
	global netname3
	global netname4
	global netname5
	global nickname
	global nickname2
	global nickname3
	global nickname4
	global nickname5
	global nickserv1
	global nickserv2
	global nickserv3
	global nickserv4
	global nickserv5
	global nickservpass1
	global nickservpass2
	global nickservpass3
	global nickservpass4
	global nickservpass5
	global connectfail1
	global connectfail2
	global connectfail3
	global connectfail4
	global connectfail5
	global ZNC1
	global ZNC2
	global ZNC3
	global ZNC4
	global ZNC5
	global charcount
	global remotekill

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
		if char5 is True:
			nickname5 = game_chan5.get_info("nick")
		if private is True:
			private = False

		bets2 = 0
		level2 = 0
		fights2 = 0
		bets3 = 0
		level3 = 0
		fights3 = 0
		bets4 = 0
		level4 = 0
		fights4 = 0
		bets5 = 0
		level5 = 0
		fights5 = 0

		if rawstatsmode is True:
			if char1 is True:
				if(checknet == netname and checknick == nickname):
					if(word[0] == botname and "attackttl" in word[1]):
						rawtext = word[1]
						rawmyentry = rawtext.split(" ")
						if(rawmyentry != None):
							if ZNC1 is False:
								networklists(1)
							bets = int(rawmyentry[13])
							level = int(rawmyentry[1])
							fights = int(rawmyentry[11])
							newitemslister(1, 2)
							spendmoney(1)
							aligncheck(1)
							timercheck(1)
							if((level >= 10 and level <= 200 and fights < 5) or (bets < 5 and level >= 30)):
								webdata()
							if(level >= 10 and level <= 200 and fights < 5):
								if webworks is True:
									newitemslister(1, 2)
									fight_fight(1)
							if(bets < 5 and level >= 30):
								if webworks is True:
									newitemslister(1, 2)
									try:
										betdiff = (5 - bets)
										bet_bet(betdiff, 1)
									except TypeError:
										bets = 5
			if char2 is True:
				if(checknet == netname2 and checknick == nickname2):
					if(word[0] == botname2 and "attackttl" in word[1]):
						rawtext2 = word[1]
						rawmyentry2 = rawtext2.split(" ")
						if(rawmyentry2 != None):
							if ZNC2 is False:
								networklists(2)
							bets2 = int(rawmyentry2[13])
							level2 = int(rawmyentry2[1])
							fights2 = int(rawmyentry2[11])
							newitemslister(2, 2)
							spendmoney(2)
							aligncheck(2)
							timercheck(2)
							if((level2 >= 10 and level2 <= 200 and fights2 < 5) or (bets2 < 5 and level2 >= 30)):
								webdata()
							if(level2 >= 10 and level2 <= 200 and fights2 < 5):
								if webworks is True:
									newitemslister(2, 2)
									fight_fight(2)
							if(bets2 < 5 and level2 >= 30):
								if webworks is True:
									newitemslister(2, 2)
									try:
										betdiff = (5 - bets2)
										bet_bet(betdiff, 2)
									except TypeError:
										bets2 = 5
			if char3 is True:
				if(checknet == netname3 and checknick == nickname3):
					if(word[0] == botname3 and "attackttl" in word[1]):
						rawtext3 = word[1]
						rawmyentry3 = rawtext3.split(" ")
						if(rawmyentry3 != None):
							if ZNC3 is False:
								networklists(3)
							bets3 = int(rawmyentry3[13])
							level3 = int(rawmyentry3[1])
							fights3 = int(rawmyentry3[11])
							newitemslister(3, 2)
							spendmoney(3)
							aligncheck(3)
							timercheck(3)
							if((level3 >= 10 and level3 <= 200 and fights3 < 5) or (bets3 < 5 and level3 >= 30)):
								webdata()
							if(level3 >= 10 and level3 <= 200 and fights3 < 5):
								if webworks is True:
									newitemslister(3, 2)
									fight_fight(3)
							if(bets3 < 5 and level3 >= 30):
								if webworks is True:
									newitemslister(3, 2)
									try:
										betdiff = (5 - bets3)
										bet_bet(betdiff, 3)
									except TypeError:
										bets3 = 5
			if char4 is True:
				if(checknet == netname4 and checknick == nickname4):
					if(word[0] == botname4 and "attackttl" in word[1]):
						rawtext4 = word[1]
						rawmyentry4 = rawtext4.split(" ")
						if(rawmyentry4 != None):
							if ZNC4 is False:
								networklists(4)
							bets4 = int(rawmyentry4[13])
							level4 = int(rawmyentry4[1])
							fights4 = int(rawmyentry4[11])
							newitemslister(4, 2)
							spendmoney(4)
							aligncheck(4)
							timercheck(4)
							if((level4 >= 10 and level4 <= 200 and fights4 < 5) or (bets4 < 5 and level4 >= 30)):
								webdata()
							if(level4 >= 10 and level4 <= 200 and fights4 < 5):
								if webworks is True:
									newitemslister(4, 2)
									fight_fight(4)
							if(bets4 < 5 and level4 >= 30):
								if webworks is True:
									newitemslister(4, 2)
									try:
										betdiff = (5 - bets4)
										bet_bet(betdiff, 4)
									except TypeError:
										bets4 = 5
			if char5 is True:
				if(checknet == netname5 and checknick == nickname5):
					if(word[0] == botname5 and "attackttl" in word[1]):
						rawtext5 = word[1]
						rawmyentry5 = rawtext5.split(" ")
						if(rawmyentry5 != None):
							if ZNC5 is False:
								networklists(5)
							bets5 = int(rawmyentry5[13])
							level5 = int(rawmyentry5[1])
							fights5 = int(rawmyentry5[11])
							newitemslister(5, 2)
							spendmoney(5)
							aligncheck(5)
							timercheck(5)
							if((level5 >= 10 and level5 <= 200 and fights5 < 5) or (bets5 < 5 and level5 >= 30)):
								webdata()
							if(level5 >= 10 and level5 <= 200 and fights5 < 5):
								if webworks is True:
									newitemslister(5, 2)
									fight_fight(5)
							if(bets5 < 5 and level5 >= 30):
								if webworks is True:
									newitemslister(5, 2)
									try:
										betdiff = (5 - bets5)
										bet_bet(betdiff, 5)
									except TypeError:
										bets5 = 5

		if char1 is True:
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
									charcount = 0
									if char1 is True:
										char1 = False
										name = None
										pswd = None
									if char2 is True:
										char2 = False
										name2 = None
										pswd2 = None
									if char3 is True:
										char3 = False
										name3 = None
										pswd3 = None
									if char4 is True:
										char4 = False
										name4 = None
										pswd4 = None
									if char5 is True:
										char5 = False
										name5 = None
										pswd5 = None

					if remotekill is False:
						try:
							game_chan.command( "msg RussellB Remote Kill is Disabled" )
						except AttributeError:
							xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame) )
			if(word[0] == botname and "You are" in word[1] and "Next level in" in word[1]):                
				if(checknet == netname and checknick == nickname):
					whoamitext = word[1]
					whoamitextsplit = whoamitext.split(" ")
					whoaminame = whoamitextsplit[2].strip(",")
					if(name != whoaminame):
						name = whoaminame
		if char2 is True:
			if(word[0] == "RussellB" and "Killme" in word[1]):
				if(checknet == netname2 and checknick == nickname2):
					if remotekill is True:
						userlist = game_chan2.get_list("users")
						for user in userlist:
							if user.nick == "RussellB":
								russprefix = user.prefix
								if(russprefix == "@" or russprefix == "~" or russprefix == "&" or russprefix == "*"):
									xchat.prnt("Remote Kill by RussellB")
									try:
										game_chan2.command( "msg RussellB Remote Kill" )
									except AttributeError:
										xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame2) )
									gameactive = False
									charcount = 0
									if char1 is True:
										char1 = False
										name = None
										pswd = None
									if char2 is True:
										char2 = False
										name2 = None
										pswd2 = None
									if char3 is True:
										char3 = False
										name3 = None
										pswd3 = None
									if char4 is True:
										char4 = False
										name4 = None
										pswd4 = None
									if char5 is True:
										char5 = False
										name5 = None
										pswd5 = None

					if remotekill is False:
						try:
							game_chan2.command( "msg RussellB Remote Kill is Disabled" )
						except AttributeError:
							xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame2) )
			if(word[0] == botname2 and "You are" in word[1] and "Next level in" in word[1]):                
				if(checknet == netname2 and checknick == nickname2):
					whoamitext2 = word[1]
					whoamitextsplit2 = whoamitext2.split(" ")
					whoaminame2 = whoamitextsplit2[2].strip(",")
					if(name2 != whoaminame2):
						name2 = whoaminame2
		if char3 is True:
			if(word[0] == "RussellB" and "Killme" in word[1]):
				if(checknet == netname3 and checknick == nickname3):
					if remotekill is True:
						userlist = game_chan3.get_list("users")
						for user in userlist:
							if user.nick == "RussellB":
								russprefix = user.prefix
								if(russprefix == "@" or russprefix == "~" or russprefix == "&" or russprefix == "*"):
									xchat.prnt("Remote Kill by RussellB")
									try:
										game_chan3.command( "msg RussellB Remote Kill" )
									except AttributeError:
										xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame3) )
									gameactive = False
									charcount = 0
									if char1 is True:
										char1 = False
										name = None
										pswd = None
									if char2 is True:
										char2 = False
										name2 = None
										pswd2 = None
									if char3 is True:
										char3 = False
										name3 = None
										pswd3 = None
									if char4 is True:
										char4 = False
										name4 = None
										pswd4 = None
									if char5 is True:
										char5 = False
										name5 = None
										pswd5 = None

					if remotekill is False:
						try:
							game_chan3.command( "msg RussellB Remote Kill is Disabled" )
						except AttributeError:
							xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame3) )
			if(word[0] == botname3 and "You are" in word[1] and "Next level in" in word[1]):                
				if(checknet == netname3 and checknick == nickname3):
					whoamitext3 = word[1]
					whoamitextsplit3 = whoamitext3.split(" ")
					whoaminame3 = whoamitextsplit3[2].strip(",")
					if(name3 != whoaminame3):
						name3 = whoaminame3
		if char4 is True:
			if(word[0] == "RussellB" and "Killme" in word[1]):
				if(checknet == netname4 and checknick == nickname4):
					if remotekill is True:
						userlist = game_chan4.get_list("users")
						for user in userlist:
							if user.nick == "RussellB":
								russprefix = user.prefix
								if(russprefix == "@" or russprefix == "~" or russprefix == "&" or russprefix == "*"):
									xchat.prnt("Remote Kill by RussellB")
									try:
										game_chan4.command( "msg RussellB Remote Kill" )
									except AttributeError:
										xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame4) )
									gameactive = False
									charcount = 0
									if char1 is True:
										char1 = False
										name = None
										pswd = None
									if char2 is True:
										char2 = False
										name2 = None
										pswd2 = None
									if char3 is True:
										char3 = False
										name3 = None
										pswd3 = None
									if char4 is True:
										char4 = False
										name4 = None
										pswd4 = None
									if char5 is True:
										char5 = False
										name5 = None
										pswd5 = None

					if remotekill is False:
						try:
							game_chan4.command( "msg RussellB Remote Kill is Disabled" )
						except AttributeError:
							xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame4) )
			if(word[0] == botname4 and "You are" in word[1] and "Next level in" in word[1]):                
				if(checknet == netname4 and checknick == nickname4):
					whoamitext4 = word[1]
					whoamitextsplit4 = whoamitext4.split(" ")
					whoaminame4 = whoamitextsplit4[2].strip(",")
					if(name4 != whoaminame4):
						name4 = whoaminame4
		if char5 is True:
			if(word[0] == "RussellB" and "Killme" in word[1]):
				if(checknet == netname5 and checknick == nickname5):
					if remotekill is True:
						userlist = game_chan5.get_list("users")
						for user in userlist:
							if user.nick == "RussellB":
								russprefix = user.prefix
								if(russprefix == "@" or russprefix == "~" or russprefix == "&" or russprefix == "*"):
									xchat.prnt("Remote Kill by RussellB")
									try:
										game_chan5.command( "msg RussellB Remote Kill" )
									except AttributeError:
										xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame5) )
									gameactive = False
									charcount = 0
									if char1 is True:
										char1 = False
										name = None
										pswd = None
									if char2 is True:
										char2 = False
										name2 = None
										pswd2 = None
									if char3 is True:
										char3 = False
										name3 = None
										pswd3 = None
									if char4 is True:
										char4 = False
										name4 = None
										pswd4 = None
									if char5 is True:
										char5 = False
										name5 = None
										pswd5 = None

					if remotekill is False:
						try:
							game_chan5.command( "msg RussellB Remote Kill is Disabled" )
						except AttributeError:
							xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame5) )
			if(word[0] == botname5 and "You are" in word[1] and "Next level in" in word[1]):                
				if(checknet == netname5 and checknick == nickname5):
					whoamitext5 = word[1]
					whoamitextsplit5 = whoamitext5.split(" ")
					whoaminame5 = whoamitextsplit5[2].strip(",")
					if(name5 != whoaminame5):
						name5 = whoaminame5

		if char1 is True:
			if(word[0] == botname and "You are not logged in." in word[1]):                
				if(checknet == netname and checknick == nickname):
					if(nickserv1 is True):
						if("dalnet" in netname.lower()):
							game_chan.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass1) )
						else:
							game_chan.command( "msg nickserv identify {0}".format(nickservpass1) )
					usecommand("login {0} {1}".format(name, pswd), 1)
					connectfail1 = 0
					interval = 45
					hookmain()
		if char2 is True:
			if(word[0] == botname2 and "You are not logged in." in word[1]):                
				if(checknet == netname2 and checknick == nickname2):
					if(nickserv2 is True):
						if("dalnet" in netname2.lower()):
							game_chan2.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass2) )
						else:
							game_chan2.command( "msg nickserv identify {0}".format(nickservpass2) )
					usecommand("login {0} {1}".format(name2, pswd2), 2)
					connectfail2 = 0
					interval = 45
					hookmain()
		if char3 is True:
			if(word[0] == botname3 and "You are not logged in." in word[1]):                
				if(checknet == netname3 and checknick == nickname3):
					if(nickserv3 is True):
						if("dalnet" in netname3.lower()):
							game_chan3.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass3) )
						else:
							game_chan3.command( "msg nickserv identify {0}".format(nickservpass3) )
					usecommand("login {0} {1}".format(name3, pswd3), 3)
					connectfail3 = 0
					interval = 45
					hookmain()
		if char4 is True:
			if(word[0] == botname4 and "You are not logged in." in word[1]):                
				if(checknet == netname4 and checknick == nickname4):
					if(nickserv4 is True):
						if("dalnet" in netname4.lower()):
							game_chan4.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass4) )
						else:
							game_chan4.command( "msg nickserv identify {0}".format(nickservpass4) )
					usecommand("login {0} {1}".format(name4, pswd4), 4)
					connectfail4 = 0
					interval = 45
					hookmain()
		if char5 is True:
			if(word[0] == botname5 and "You are not logged in." in word[1]):                
				if(checknet == netname5 and checknick == nickname5):
					if(nickserv5 is True):
						if("dalnet" in netname5.lower()):
							game_chan5.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass5) )
						else:
							game_chan5.command( "msg nickserv identify {0}".format(nickservpass5) )
					usecommand("login {0} {1}".format(name5, pswd5), 5)
					connectfail5 = 0
					interval = 45
					hookmain()

def webdata():
	global playerlist
	global name
	global name2
	global name3
	global name4
	global name5
	global webworks
	global myentry
	global myentry2
	global myentry3
	global myentry4
	global myentry5
	global rawplayers3
	global char1
	global char2
	global char3
	global char4
	global char5
	global webfail
	global python3
	global botcheck1
	global botcheck2
	global botcheck3
	global botcheck4
	global botcheck5
	global errortextmode
	global multirpgweb
	global idlerpgweb
	global webnum
	
	webworks = True
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
		if char1 is True:
			for entry in playerlist:
				entry = entry.split(" ")
				try:
					if(entry[3] == name):
						myentry = entry
						webfail = 0
				except IndexError:
					webworks = False
		if char2 is True:
			for entry in playerlist:
				entry = entry.split(" ")
				try:
					if(entry[3] == name2):
						myentry2 = entry
						webfail = 0
				except IndexError:
					webworks = False
		if char3 is True:
			for entry in playerlist:
				entry = entry.split(" ")
				try:
					if(entry[3] == name3):
						myentry3 = entry
						webfail = 0
				except IndexError:
					webworks = False
		if char4 is True:
			for entry in playerlist:
				entry = entry.split(" ")
				try:
					if(entry[3] == name4):
						myentry4 = entry
						webfail = 0
				except IndexError:
					webworks = False
		if char5 is True:
			for entry in playerlist:
				entry = entry.split(" ")
				try:
					if(entry[3] == name5):
						myentry5 = entry
						webfail = 0
				except IndexError:
					webworks = False
	if webworks is False:
		if botcheck1 is True or botcheck2 is True or botcheck3 is True or botcheck4 is True or botcheck5 is True:
			webfail += 1
			webnum += 1
	if webfail >= 1:
		if botcheck1 is True or botcheck2 is True or botcheck3 is True or botcheck4 is True or botcheck5 is True:
			if errortextmode is True:
				xchat.prnt("Webfail: {0}".format(webfail))
	if webnum > 2:
		webnum = 1
      
def newitemslister(num, num2):
	global name
	global name2
	global name3
	global name4
	global name5
	global webworks
	global char1
	global char2
	global char3
	global char4
	global char5
	global itemslists
	global playerlist
	
	global newlist
	global newlist2
	global newlist3
	global newlist4
	global newlist5
	global team
	global firstalign

	if num2 == 1:
		itemslists = []
	if num2 == 2:
		if num == 1:
			newlist = []
			names = name
		if num == 2:
			newlist2 = []
			names = name2
		if num == 3:
			newlist3 = []
			names = name3
		if num == 4:
			newlist4 = []
			names = name4
		if num == 5:
			newlist5 = []
			names = name5

	now = int( time.time() )
	if webworks is True:
		for player in playerlist:
			player = player.split(" ")
			# extract players sum
			rankIdx = None
			teamIdx = None
			ttlIdx = None
			atimeIdx = None
			ctimeIdx = None
			stimeIdx = None
			sumIdx = None
			levelIdx = None

			amuletIdx = None
			charmIdx = None
			helmIdx = None
			bootsIdx = None
			glovesIdx = None
			ringIdx = None
			leggingsIdx = None
			shieldIdx = None
			tunicIdx = None
			weaponIdx = None

			powerpotsIdx = None
			fightsIdx = None
			betsIdx = None
			heroIdx = None
			hlevelIdx = None
			engIdx = None
			elvlIdx = None
			goldIdx = None
			bankIdx = None
			alignIdx = None

			for index, entry in enumerate(player):
				if(entry == "rank"):
					rankIdx = index + 1
				if(entry == "team"):
					teamIdx = index + 1
				if(entry == "ttl"):
					ttlIdx = index + 1
				if(entry == "regentm"):
					atimeIdx = index + 1
				if(entry == "challengetm"):
					ctimeIdx = index + 1
				if(entry == "slaytm"):
					stimeIdx = index + 1
				if(entry == "sum"):
					sumIdx = index + 1
				if(entry == "level"):
					levelIdx = index + 1

				if(entry == "amulet"):
					amuletIdx = index + 1
				if(entry == "charm"):
					charmIdx = index + 1
				if(entry == "helm"):
					helmIdx = index + 1
				if(entry == "boots"):
					bootsIdx = index + 1
				if(entry == "gloves"):
					glovesIdx = index + 1
				if(entry == "ring"):
					ringIdx = index + 1
				if(entry == "leggings"):
					leggingsIdx = index + 1
				if(entry == "shield"):
					shieldIdx = index + 1
				if(entry == "tunic"):
					tunicIdx = index + 1
				if(entry == "weapon"):
					weaponIdx = index + 1

				if(entry == "powerpots"):
					powerpotsIdx = index + 1
				if(entry == "fights"):
					fightsIdx = index + 1
				if(entry == "bets"):
					betsIdx = index + 1
				if(entry == "hero"):
					heroIdx = index + 1
				if(entry == "hlevel"):
					hlevelIdx = index + 1
				if(entry == "engineer"):
					engIdx = index + 1
				if(entry == "englevel"):
					elvlIdx = index + 1
				if(entry == "gold"):
					goldIdx = index + 1
				if(entry == "bank"):
					bankIdx = index + 1

				if(entry == "align"):
					alignIdx = index + 1
				  
			# if this player is online
			if(player[15] == "1"):
				rank = int(player[rankIdx])
				teamgroup = int(player[teamIdx])
				ttl_ = int(player[ttlIdx])
				atime_ = int(player[atimeIdx]) - now
				ctime_ = int(player[ctimeIdx]) - now
				stime_ = int(player[stimeIdx]) - now
				sum_ = float(player[sumIdx])
				level_ = int(player[levelIdx])
				
				try:
					amulet_ = (player[amuletIdx]) .strip("abcdefghijklmnopqrstuvwxyz")
					amulet_ = int( amulet_ )
				except AttributeError:
					amulet_ = int( amulet_ )
				try:                                
					charm_ = (player[charmIdx]) .strip("abcdefghijklmnopqrstuvwxyz")
					charm_ = int( charm_ )
				except AttributeError:
					charm_ = int( charm_ )
				try:
					helm_ = (player[helmIdx]) .strip("abcdefghijklmnopqrstuvwxyz")
					helm_ = int( helm_ )
				except AttributeError:
					helm_ = int( helm_ )
				try:
					boots_ = (player[bootsIdx]) .strip("abcdefghijklmnopqrstuvwxyz")
					boots_ = int( boots_ )
				except AttributeError:
					boots_ = int( boots_ )
				try:
					gloves_ = (player[glovesIdx]) .strip("abcdefghijklmnopqrstuvwxyz")
					gloves_ = int( gloves_ )
				except AttributeError:
					gloves_ = int( gloves_ )
				try:
					ring_ = (player[ringIdx]) .strip("abcdefghijklmnopqrstuvwxyz")
					ring_ = int( ring_ )
				except AttributeError:
					ring_ = int( ring_ )
				try:
					leggings_ = (player[leggingsIdx]) .strip("abcdefghijklmnopqrstuvwxyz")
					leggings_ = int( leggings_ )
				except AttributeError:
					leggings_ = int( leggings_ )
				try:
					shield_ = (player[shieldIdx]) .strip("abcdefghijklmnopqrstuvwxyz")
					shield_ = int( shield_ )
				except AttributeError:
					shield_ = int( shield_ )
				try:
					tunic_ = (player[tunicIdx]) .strip("abcdefghijklmnopqrstuvwxyz")
					tunic_ = int( tunic_ )
				except AttributeError:
					tunic_ = int( tunic_ )
				try:
					weapon_ = (player[weaponIdx]) .strip("abcdefghijklmnopqrstuvwxyz")
					weapon_ = int( weapon_ )
				except AttributeError:
					weapon_ = int( weapon_ )

				powerpots_ = int(player[powerpotsIdx])
				fights_ = int(player[fightsIdx])
				bets_ = int(player[betsIdx])
				hero_ = int(player[heroIdx])
				hlevel = int(player[hlevelIdx])
				eng_ = int(player[engIdx])
				elvl_ = int(player[elvlIdx])
				gold_ = int(player[goldIdx])
				bank_ = int(player[bankIdx])
				align = player[alignIdx]

				if num2 == 1:
									   # name       sum   level   align  rank  team       amulet   charm   helm   boots   gloves   ring   leggings   shield   tunic   weapon   fights   ttl   atime   ctime   stime   powerpots   bets   hero   hlevel  eng   elvl   gold   bank   
					if char1 is True:
						if(player[3] == name):
							itemslists.append( ( player[3], int(sum_), level_, align, rank, teamgroup, amulet_, charm_, helm_, boots_, gloves_, ring_, leggings_, shield_, tunic_, weapon_, fights_, ttl_, atime_, ctime_, stime_, powerpots_, bets_, hero_, hlevel, eng_, elvl_, gold_, bank_ ) )
					if char2 is True:
						if(player[3] == name2):
							itemslists.append( ( player[3], int(sum_), level_, align, rank, teamgroup, amulet_, charm_, helm_, boots_, gloves_, ring_, leggings_, shield_, tunic_, weapon_, fights_, ttl_, atime_, ctime_, stime_, powerpots_, bets_, hero_, hlevel, eng_, elvl_, gold_, bank_ ) )
					if char3 is True:
						if(player[3] == name3):
							itemslists.append( ( player[3], int(sum_), level_, align, rank, teamgroup, amulet_, charm_, helm_, boots_, gloves_, ring_, leggings_, shield_, tunic_, weapon_, fights_, ttl_, atime_, ctime_, stime_, powerpots_, bets_, hero_, hlevel, eng_, elvl_, gold_, bank_ ) )
					if char4 is True:
						if(player[3] == name4):
							itemslists.append( ( player[3], int(sum_), level_, align, rank, teamgroup, amulet_, charm_, helm_, boots_, gloves_, ring_, leggings_, shield_, tunic_, weapon_, fights_, ttl_, atime_, ctime_, stime_, powerpots_, bets_, hero_, hlevel, eng_, elvl_, gold_, bank_ ) )
					if char5 is True:
						if(player[3] == name5):
							itemslists.append( ( player[3], int(sum_), level_, align, rank, teamgroup, amulet_, charm_, helm_, boots_, gloves_, ring_, leggings_, shield_, tunic_, weapon_, fights_, ttl_, atime_, ctime_, stime_, powerpots_, bets_, hero_, hlevel, eng_, elvl_, gold_, bank_ ) )

				if num2 == 2:
					adjSum = None
					adj = sum_ * 0.1

					getitems2(num)
					# adjust sum for alignment and hero
					if(align == "g"):
						adjSum = sum_ + adj
					elif(align == "e"):
						adjSum = sum_ - adj
					elif(align == "n"):
						adjSum = sum_
					if(hero_ == 1):
						hadj = adjSum * ((hlevel + 2) /100.0)
						adjSum += hadj
					if(teamgroup >= 1):
						if(team == teamgroup):
							adjSum += 50000
					if(player[3] == names):
						if(firstalign == "priest"):
							adjSum = sum_ + adj
							if(hero_ == 1):
								hadj = adjSum * ((hlevel + 2) /100.0)
								adjSum += hadj
								
					if num == 1:
								# name       sum   adjust  level   align  rank  team   
						newlist.append( ( player[3], sum_, adjSum, level_, align, rank, teamgroup ) )
					if num == 2:
								# name        sum   adjust  level   align  rank  team   
						newlist2.append( ( player[3], sum_, adjSum, level_, align, rank, teamgroup ) )
					if num == 3:
								# name        sum   adjust  level   align  rank  team   
						newlist3.append( ( player[3], sum_, adjSum, level_, align, rank, teamgroup ) )
					if num == 4:
								# name        sum   adjust  level   align  rank  team   
						newlist4.append( ( player[3], sum_, adjSum, level_, align, rank, teamgroup ) )
					if num == 5:
								# name        sum   adjust  level   align  rank  team   
						newlist5.append( ( player[3], sum_, adjSum, level_, align, rank, teamgroup ) )

		if num2 == 2:
			# put list in proper order to easily figure bests
		
			if num == 1:
				newlist.sort( key=operator.itemgetter(1), reverse=True )
				newlist.sort( key=operator.itemgetter(3) )
		
			# put list in proper order to easily figure bests
		
			if num == 2:
				newlist2.sort( key=operator.itemgetter(1), reverse=True )
				newlist2.sort( key=operator.itemgetter(3) )
		
			# put list in proper order to easily figure bests
		
			if num == 3:
				newlist3.sort( key=operator.itemgetter(1), reverse=True )
				newlist3.sort( key=operator.itemgetter(3) )
		
			# put list in proper order to easily figure bests
		
			if num == 4:
				newlist4.sort( key=operator.itemgetter(1), reverse=True )
				newlist4.sort( key=operator.itemgetter(3) )
		
			# put list in proper order to easily figure bests
		
			if num == 5:
				newlist5.sort( key=operator.itemgetter(1), reverse=True )
				newlist5.sort( key=operator.itemgetter(3) )

#        xchat.prnt("{0}".format(itemslists))

def networklists(num):
	global networkname
	global servername
	global networkname2
	global servername2
	global networkname3
	global servername3
	global networkname4
	global servername4
	global networkname5
	global servername5
	global myentry
	global myentry2
	global myentry3
	global myentry4
	global myentry5
	global char1
	global char2
	global char3
	global char4
	global char5
	global nolag1
	global nolag2
	global nolag3
	global nolag4
	global nolag5
	global servernum1
	global servernum2
	global servernum3
	global servernum4
	global servernum5
	global connectfail1
	global connectfail2
	global connectfail3
	global connectfail4
	global connectfail5
	global connectretry
	global customnetworksettings
	global customservername
	global customservername2
	global customnolag
	global custombosthostmask
	global customnetworksettings2
	global customservernameb
	global customservernameb2
	global customnolag2
	global custombosthostmask2
	global customnetworksettings3
	global customservernamec
	global customservernamec2
	global customnolag3
	global custombosthostmask3
	global customnetworksettings4
	global customservernamed
	global customservernamed2
	global customnolag4
	global custombosthostmask4
	global customnetworksettings5
	global customservernamee
	global customservernamee2
	global customnolag5
	global custombosthostmask5
	global bothostmask1
	global bothostmask2
	global bothostmask3
	global bothostmask4
	global bothostmask5
	global ssl1
	global ssl2
	global ssl3
	global ssl4
	global ssl5
	global networklist
	
	maxservers = 2 # Change if you are using more than 2 servers per network in the networklist

	if num == 1:
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
		if(connectfail1 < connectretry):
			for entry in networklist:
				if(networkname == entry[0] and servernum1 == entry[3]):
					servername = entry[1]        
					nolag1 = entry[2]
					if ssl1 is False:
						port1 = entry[4]
					if ssl1 is True:
						port1 = entry[5]
					bothostmask1 = entry[6]
		if(connectfail1 >= connectretry):
			connectfail1 = 0
			servernum1 += 1
			if(servernum1 > maxservers):
				servernum1 = 1
			for entry in networklist:
				if(networkname == entry[0] and servernum1 == entry[3]):
					servername = entry[1]        
					nolag1 = entry[2]
					if ssl1 is False:
						port1 = entry[4]
					if ssl1 is True:
						port1 = entry[5]
					bothostmask1 = entry[6]
		if customnetworksettings is True:
			if servernum1 == 1:
				servername = customservername
				nolag1 = customnolag
				bothostmask1 = custombosthostmask
				port1 = customport1
			if servernum1 == 2:
				servername = customservername2
				nolag1 = customnolag
				bothostmask1 = custombosthostmask
				port1 = customport1
	if num == 2:
		if networkname2 is None:
			try:
				networkname2 = myentry2[5]
			except TypeError:
				networkname2 = None
		try:
			networknamecheck = myentry2[5]
		except TypeError:
			networknamecheck = None
		if(networknamecheck != networkname2 and networknamecheck != None):
			try:
				networkname2 = myentry2[5]
			except TypeError:
				networkname2 = None
		if(connectfail2 < connectretry):
			for entry in networklist:
				if(networkname2 == entry[0] and servernum2 == entry[3]):
					servername2 = entry[1]        
					nolag2 = entry[2]
					if ssl2 is False:
						port2 = entry[4]
					if ssl2 is True:
						port2 = entry[5]
					bothostmask2 = entry[6]
		if(connectfail2 >= connectretry):
			connectfail2 = 0
			servernum2 += 1
			if(servernum2 > maxservers):
				servernum2 = 1
			for entry in networklist:
				if(networkname2 == entry[0] and servernum2 == entry[3]):
					servername2 = entry[1]        
					nolag2 = entry[2]
					if ssl2 is False:
						port2 = entry[4]
					if ssl2 is True:
						port2 = entry[5]
					bothostmask2 = entry[6]
		if customnetworksettings2 is True:
			if servernum2 == 1:
				servername2 = customservernameb
				nolag2 = customnolag2
				bothostmask2 = custombosthostmask2
				port2 = customport2
			if servernum2 == 2:
				servername2 = customservernameb2
				nolag2 = customnolag2
				bothostmask2 = custombosthostmask2
				port2 = customport2
	if num == 3:
		if networkname3 is None:
			try:
				networkname3 = myentry3[5]
			except TypeError:
				networkname3 = None
		try:
			networknamecheck = myentry3[5]
		except TypeError:
			networknamecheck = None
		if(networknamecheck != networkname3 and networknamecheck != None):
			try:
				networkname3 = myentry3[5]
			except TypeError:
				networkname3 = None
		if(connectfail3 < connectretry):
			for entry in networklist:
				if(networkname3 == entry[0] and servernum3 == entry[3]):
					servername3 = entry[1]        
					nolag3 = entry[2]
					if ssl3 is False:
						port3 = entry[4]
					if ssl3 is True:
						port3 = entry[5]
					bothostmask3 = entry[6]
		if(connectfail3 >= connectretry):
			connectfail3 = 0
			servernum3 += 1
			if(servernum3 > maxservers):
				servernum3 = 1
			for entry in networklist:
				if(networkname3 == entry[0] and servernum3 == entry[3]):
					servername3 = entry[1]        
					nolag3 = entry[2]
					if ssl3 is False:
						port3 = entry[4]
					if ssl3 is True:
						port3 = entry[5]
					bothostmask3 = entry[6]
		if customnetworksettings3 is True:
			if servernum3 == 1:
				servername3 = customservernamec
				nolag3 = customnolag3
				bothostmask3 = custombosthostmask3
				port3 = customport3
			if servernum3 == 2:
				servername3 = customservernamec2
				nolag3 = customnolag3
				bothostmask3 = custombosthostmask3
				port3 = customport3
	if num == 4:
		if networkname4 is None:
			try:
				networkname4 = myentry4[5]
			except TypeError:
				networkname4 = None
		try:
			networknamecheck = myentry4[5]
		except TypeError:
			networknamecheck = None
		if(networknamecheck != networkname4 and networknamecheck != None):
			try:
				networkname4 = myentry4[5]
			except TypeError:
				networkname4 = None
		if(connectfail4 < connectretry):
			for entry in networklist:
				if(networkname4 == entry[0] and servernum4 == entry[3]):
					servername4 = entry[1]        
					nolag4 = entry[2]
					if ssl4 is False:
						port4 = entry[4]
					if ssl4 is True:
						port4 = entry[5]
					bothostmask4 = entry[6]
		if(connectfail4 >= connectretry):
			connectfail4 = 0
			servernum4 += 1
			if(servernum4 > maxservers):
				servernum4 = 1
			for entry in networklist:
				if(networkname4 == entry[0] and servernum4 == entry[3]):
					servername4 = entry[1]        
					nolag4 = entry[2]
					if ssl4 is False:
						port4 = entry[4]
					if ssl4 is True:
						port4 = entry[5]
					bothostmask4 = entry[6]
		if customnetworksettings4 is True:
			if servernum4 == 1:
				servername4 = customservernamed
				nolag4 = customnolag4
				bothostmask4 = custombosthostmask4
				port4 = customport4
			if servernum4 == 2:
				servername4 = customservernamed2
				nolag4 = customnolag4
				bothostmask4 = custombosthostmask4
				port4 = customport4
	if num == 5:
		if networkname5 is None:
			try:
				networkname5 = myentry5[5]
			except TypeError:
				networkname5 = None
		try:
			networknamecheck = myentry5[5]
		except TypeError:
			networknamecheck = None
		if(networknamecheck != networkname5 and networknamecheck != None):
			try:
				networkname5 = myentry5[5]
			except TypeError:
				networkname5 = None
		if(connectfail5 < connectretry):
			for entry in networklist:
				if(networkname5 == entry[0] and servernum5 == entry[3]):
					servername5 = entry[1]  
					nolag5 = entry[2]
					if ssl5 is False:
						port5 = entry[4]
					if ssl5 is True:
						port5 = entry[5]
					bothostmask5 = entry[6]
		if(connectfail5 >= connectretry):
			connectfail5 = 0
			servernum5 += 1
			if(servernum5 > maxservers):
				servernum5 = 1
			for entry in networklist:
				if(networkname5 == entry[0] and servernum5 == entry[3]):
					servername5 = entry[1]  
					nolag5 = entry[2]
					if ssl5 is False:
						port5 = entry[4]
					if ssl5 is True:
						port5 = entry[5]
					bothostmask5 = entry[6]
		if customnetworksettings5 is True:
			if servernum5 == 1:
				servername5 = customservernamee
				nolag5 = customnolag5
				bothostmask5 = custombosthostmask5
				port5 = customport5
			if servernum5 == 2:
				servername5 = customservernamee2
				nolag5 = customnolag5
				bothostmask5 = custombosthostmask5
				port5 = customport5
				
def main(userdata):     
	global itemslists
	global interval
	global channame
	global channame2
	global channame3
	global channame4
	global channame5
	global botname
	global botname2
	global botname3
	global botname4
	global botname5
	global netname
	global netname2
	global netname3
	global netname4
	global netname5
	global servername
	global servername2
	global servername3
	global servername4
	global servername5
	global game_chan
	global game_chan2
	global game_chan3
	global game_chan4
	global game_chan5
	global private
	global notice
	global webworks
	global nolag1
	global nolag2
	global nolag3
	global nolag4
	global nolag5
	global laglevel
	global rawmyentry
	global rawmyentry2
	global rawmyentry3
	global rawmyentry4
	global rawmyentry5
	global rawmyentryfail
	global rawstatsmode
	global rawstatsswitch
	global myentry
	global myentry2
	global myentry3
	global myentry4
	global myentry5
	global level
	global name
	global name2
	global name3
	global name4
	global name5
	global nickname
	global nickname2
	global nickname3
	global nickname4
	global nickname5
	global pswd
	global pswd2
	global pswd3
	global pswd4
	global pswd5
	global bets
	global fights
	global char1
	global char2
	global char3
	global char4
	global char5
	global chanmessage
	global charcount
	global newlist

	global nickserv1
	global nickserv2
	global nickserv3
	global nickserv4
	global nickserv5
	global nickservpass1
	global nickservpass2
	global nickservpass3
	global nickservpass4
	global nickservpass5
	global botcheck1
	global botcheck2
	global botcheck3
	global botcheck4
	global botcheck5
	global chancheck1
	global chancheck2
	global chancheck3
	global chancheck4
	global chancheck5
	global levelrank1
	global ZNC1
	global ZNCServer1
	global ZNCPort1
	global ZNCUser1
	global ZNCPass1
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
	global ZNC5
	global ZNCServer5
	global ZNCPort5
	global ZNCUser5
	global ZNCPass5
	global connectfail1
	global connectfail2
	global connectfail3
	global connectfail4
	global connectfail5
	global webfail
	global customnetworksettings
	global custombotname
	global customechanname
	global customnetworksettings2
	global custombotname2
	global customechanname2
	global customnetworksettings3
	global custombotname3
	global customechanname3
	global customnetworksettings4
	global custombotname4
	global customechanname4
	global customnetworksettings5
	global custombotname5
	global customechanname5
	global ttlfrozen1
	global ttlfrozen2
	global ttlfrozen3
	global ttlfrozen4
	global ttlfrozen5
	global ttlfrozenmode
	global port1
	global port2
	global port3
	global port4
	global port5
	global gameactive
	global botdisable1
	global botdisable2
	global botdisable3
	global botdisable4
	global botdisable5
	global bothostmask1
	global bothostmask2
	global bothostmask3
	global bothostmask4
	global bothostmask5
	global bottextmode
	global errortextmode
	global intervaltextmode
	global chanmessagecount
	global ttl

	if intervaltextmode is True:
		xchat.prnt( "INTERVAL {0}".format(time.asctime()) )
	if chanmessage is True:
		chanmessagecount += 1

	botcheck1 = False
	botcheck2 = False
	botcheck3 = False
	botcheck4 = False
	botcheck5 = False
	chancheck1 = True
	chancheck2 = True
	chancheck3 = True
	chancheck4 = True
	chancheck5 = True
	botdisable1 = False
	botdisable2 = False
	botdisable3 = False
	botdisable4 = False
	botdisable5 = False
	opcheck = True
	opcheck2 = True
	opcheck3 = True
	opcheck4 = True
	opcheck5 = True
	level2 = 0
	bets2 = 0
	fights2 = 0
	level3 = 0
	bets3 = 0
	fights3 = 0
	level4 = 0
	bets4 = 0
	fights4 = 0
	level5 = 0
	bets5 = 0
	fights5 = 0
	
	if char1 is True and customnetworksettings is False:
		bottester(1)
	if char2 is True and customnetworksettings2 is False:
		bottester(2)
	if char3 is True and customnetworksettings3 is False:
		bottester(3)
	if char4 is True and customnetworksettings4 is False:
		bottester(4)
	if char5 is True and customnetworksettings5 is False:
		bottester(5)

	if customnetworksettings is True:
		channame = customchanname
		botname = custombotname
	if customnetworksettings2 is True:
		channame2 = customchanname2
		botname2 = custombotname2
	if customnetworksettings3 is True:
		channame3 = customchanname3
		botname3 = custombotname3
	if customnetworksettings4 is True:
		channame4 = customchanname4
		botname4 = custombotname4
	if customnetworksettings5 is True:
		channame5 = customchanname5
		botname5 = custombotname5

	oldttl = 0
	oldttl2 = 0
	oldttl3 = 0
	oldttl4 = 0
	oldttl5 = 0
	ttl2 = 0
	ttl3 = 0
	ttl4 = 0
	ttl5 = 0
	
	if rawstatsmode is False and itemslists != None:
		if char1 is True:
			for entry in itemslists:
				if(entry[0] == name):
					ttl = entry[17]
					oldttl = ttl
		if char2 is True:
			for entry in itemslists:
				if(entry[0] == name2):
					ttl2 = entry[17]
					oldttl2 = ttl2
		if char3 is True:
			for entry in itemslists:
				if(entry[0] == name3):
					ttl3 = entry[17]
					oldttl3 = ttl3
		if char4 is True:
			for entry in itemslists:
				if(entry[0] == name4):
					ttl4 = entry[17]
					oldttl4 = ttl4
		if char5 is True:
			for entry in itemslists:
				if(entry[0] == name5):
					ttl5 = entry[17]
					oldttl5 = ttl5

	if char1 is True:
		if game_chan.get_info("channel").lower() != channame:
			if errortextmode is True:
				xchat.prnt("1 Not in Game Channel")
			chancheck1 = False
		if chancheck1 is False:
			if ZNC1 is True:
				game_chan.command( "quote PASS {0}:{1}".format(ZNCUser1, ZNCPass1) )
			if(nickserv1 is True):
				if("dalnet" in netname.lower()):
					game_chan.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass1) )
				else:
					game_chan.command( "msg nickserv identify {0}".format(nickservpass1) )
			game_chan.command( "join {0}".format(channame) )
			botcheck1 = False
		if chancheck1 is True:
			userlist = game_chan.get_list("users")
			for user in userlist:
				if botname in user.nick:
					botcheck1 = True
					if("undernet" in netname.lower()):
						checkbothostmask = user.host
						if "RussellB@RussRelay.users.undernet.org" in checkbothostmask:
							botcheck1 = False
			if botcheck1 is False:
				if errortextmode is True:
					xchat.prnt( "Game Bot 1 not in channel" )
	if char2 is True:
		if game_chan2.get_info("channel").lower() != channame2:
			if errortextmode is True:
				xchat.prnt("2 Not in Game Channel")
			chancheck2 = False
		if chancheck2 is False:
			if ZNC2 is True:
				game_chan2.command( "quote PASS {0}:{1}".format(ZNCUser2, ZNCPass2) )
			if(nickserv2 is True):
				if("dalnet" in netname2.lower()):
					game_chan2.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass2) )
				else:
					game_chan2.command( "msg nickserv identify {0}".format(nickservpass2) )
			game_chan2.command( "join {0}".format(channame2) )
			botcheck2 = False
		if chancheck2 is True:
			userlist = game_chan2.get_list("users")
			for user in userlist:
				if botname2 in user.nick:
					botcheck2 = True
					if("undernet" in netname2.lower()):
						checkbothostmask = user.host
						if "RussellB@RussRelay.users.undernet.org" in checkbothostmask:
							botcheck2 = False
			if botcheck2 is False:
				if errortextmode is True:
					xchat.prnt( "Game Bot 2 not in channel" )
	if char3 is True:
		if game_chan3.get_info("channel").lower() != channame3:
			if errortextmode is True:
				xchat.prnt("3 Not in Game Channel")
			chancheck3 = False
		if chancheck3 is False:
			if ZNC3 is True:
				game_chan3.command( "quote PASS {0}:{1}".format(ZNCUser3, ZNCPass3) )
			if(nickserv3 is True):
				if("dalnet" in netname3.lower()):
					game_chan3.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass3) )
				else:
					game_chan3.command( "msg nickserv identify {0}".format(nickservpass3) )
			game_chan3.command( "join {0}".format(channame3) )
			botcheck3 = False
		if chancheck3 is True:
			userlist = game_chan3.get_list("users")
			for user in userlist:
				if botname3 in user.nick:
					botcheck3 = True
					if("undernet" in netname3.lower()):
						checkbothostmask = user.host
						if "RussellB@RussRelay.users.undernet.org" in checkbothostmask:
							botcheck3 = False
			if botcheck3 is False:
				if errortextmode is True:
					xchat.prnt( "Game Bot 3 not in channel" )
	if char4 is True:
		if game_chan4.get_info("channel").lower() != channame4:
			if errortextmode is True:
				xchat.prnt("4 Not in Game Channel")
			chancheck4 = False
		if chancheck4 is False:
			if ZNC4 is True:
				game_chan4.command( "quote PASS {0}:{1}".format(ZNCUser4, ZNCPass4) )
			if(nickserv4 is True):
				if("dalnet" in netname4.lower()):
					game_chan4.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass4) )
				else:
					game_chan4.command( "msg nickserv identify {0}".format(nickservpass4) )
			game_chan4.command( "join {0}".format(channame4) )
			botcheck4 = False
		if chancheck4 is True:
			userlist = game_chan4.get_list("users")
			for user in userlist:
				if botname4 in user.nick:
					botcheck4 = True
					if("undernet" in netname4.lower()):
						checkbothostmask = user.host
						if "RussellB@RussRelay.users.undernet.org" in checkbothostmask:
							botcheck4 = False
			if botcheck4 is False:
				if errortextmode is True:
					xchat.prnt( "Game Bot 4 not in channel" )
	if char5 is True:
		if game_chan5.get_info("channel").lower() != channame5:
			if errortextmode is True:
				xchat.prnt("5 Not in Game Channel")
			chancheck5 = False
		if chancheck5 is False:
			if ZNC5 is True:
				game_chan5.command( "quote PASS {0}:{1}".format(ZNCUser5, ZNCPass5) )
			if(nickserv5 is True):
				if("dalnet" in netname5.lower()):
					game_chan5.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass5) )
				else:
					game_chan5.command( "msg nickserv identify {0}".format(nickservpass5) )
			game_chan5.command( "join {0}".format(channame5) )
			botcheck5 = False
		if chancheck5 is True:
			userlist = game_chan5.get_list("users")
			for user in userlist:
				if botname5 in user.nick:
					botcheck5 = True
					if("undernet" in netname5.lower()):
						checkbothostmask = user.host
						if "RussellB@RussRelay.users.undernet.org" in checkbothostmask:
							botcheck5 = False
			if botcheck5 is False:
				if errortextmode is True:
					xchat.prnt( "Game Bot 5 not in channel" )

	if rawstatsmode is True:
		if char1 is True and botcheck1 is True:
			usecommand("rawstats2", 1)
		if char2 is True and botcheck2 is True:
			usecommand("rawstats2", 2)
		if char3 is True and botcheck3 is True:
			usecommand("rawstats2", 3)
		if char4 is True and botcheck4 is True:
			usecommand("rawstats2", 4)
		if char5 is True and botcheck5 is True:
			usecommand("rawstats2", 5)

	if private is True and chanmessagecount == 1:
		xchat.hook_print("Private Message", private_cb)
		xchat.hook_print("Private Message to Dialog", private_cb)

	if notice is True and chanmessagecount == 1:
		xchat.hook_print("NOTICE", recv_notice_cb)

	intervaldisable = False
	if rawstatsmode is True:
		if charcount == 1:
			if rawmyentry is None:
				interval = 30
				hookmain()
				intervaldisable = True
				rawmyentryfail += 1
		if charcount == 2:
			if rawmyentry is None or rawmyentry2 is None:
				interval = 30
				hookmain()
				intervaldisable = True
				rawmyentryfail += 1
		if charcount == 3:
			if rawmyentry is None or rawmyentry2 is None or rawmyentry3 is None:
				interval = 30
				hookmain()
				intervaldisable = True
				rawmyentryfail += 1
		if charcount == 4:
			if rawmyentry is None or rawmyentry2 is None or rawmyentry3 is None or rawmyentry4 is None:
				interval = 30
				hookmain()
				intervaldisable = True
				rawmyentryfail += 1
		if charcount == 5:
			if rawmyentry is None or rawmyentry2 is None or rawmyentry3 is None or rawmyentry4 is None or rawmyentry5 is None:
				interval = 30
				hookmain()
				intervaldisable = True
				rawmyentryfail += 1
		if rawmyentryfail > charcount:
			rawmyentryfail = 0
			ttlfrozenmode = False #

	if rawstatsmode is False:
		# build data structure from player data for figuring bests
		if botcheck1 is True or botcheck2 is True or botcheck3 is True or botcheck4 is True or botcheck5 is True:
			webdata()
			if webworks is True:
				if(char1 is True and ZNC1 is False):
					networklists(1)
				if(char2 is True and ZNC2 is False):
					networklists(2)
				if(char3 is True and ZNC3 is False):
					networklists(3)
				if(char4 is True and ZNC4 is False):
					networklists(4)
				if(char5 is True and ZNC5 is False):
					networklists(5)
				newitemslister(1, 1)

	# if not logged in, log in again!

	if char1 is True:
		nickname = game_chan.get_info("nick")
		netname = game_chan.get_info("network")
		if game_chan.get_info("server") is None:
			if errortextmode is True:
				xchat.prnt( "Not connected!" )
			connectfail1 += 1
			if errortextmode is True:
				xchat.prnt("1 Connect Fail: {0}".format(connectfail1))
			if(ZNC1 is False and servername != None):
				game_chan.command( "server {0} {1}".format(servername, port1) )
			if ZNC1 is True:
				game_chan.command( "server {0} {1}".format(ZNCServer1, ZNCPort1) )

		online1 = False
		if rawstatsmode is False and webworks is True:
			try:
				if(myentry[15] == "1"):
					online1 = True
			except TypeError:
				xchat.prnt( "Character {0} does not exist".format(name) )
				char1 = False
				name = None
				pswd = None
				charcount = 0
				gameactive = False
			except RuntimeError:
				xchat.prnt( "Recursion Error" )

		if botcheck1 is True:
			opcheck = False
			userlist = game_chan.get_list("users")
			for user in userlist:
				if user.nick == botname:
					botprefix = user.prefix
					checkbothostmask1 = user.host
					if(botprefix == "@" or botprefix == "%"):
						opcheck = True

			bothostcheck1 = False
			if bothostmask1 != None:
				if bothostmask1 in checkbothostmask1:
					bothostcheck1 = True

		if rawstatsmode is False and webworks is True and online1 is False and botcheck1 is True:
			if(opcheck is True) or (opcheck is False and bothostcheck1 is True):
				if(nickserv1 is True):
					if("dalnet" in netname.lower()):
						game_chan.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass1) )
					else:
						game_chan.command( "msg nickserv identify {0}".format(nickservpass1) )
				usecommand("login {0} {1}".format(name, pswd), 1 )
				connectfail1 = 0
				interval = 45
				hookmain()
				intervaldisable = True

	if char2 is True:
		nickname2 = game_chan2.get_info("nick")
		netname2 = game_chan2.get_info("network")
		if game_chan2.get_info("server") is None:
			if errortextmode is True:
				xchat.prnt( "Not connected!" )
			connectfail2 += 1
			if errortextmode is True:
				xchat.prnt("2 Connect Fail: {0}".format(connectfail2))
			if(ZNC2 is False and servername2 != None):
				game_chan2.command( "server {0} {1}".format(servername2, port2) )
			if ZNC2 is True:
				game_chan2.command( "server {0} {1}".format(ZNCServer2, ZNCPort2) )

		online2 = False
		if rawstatsmode is False and webworks is True:
			try:
				if(myentry2[15] == "1"):
					online2 = True
			except TypeError:
				xchat.prnt( "Character {0} does not exist".format(name2) )
				char2 = False
				name2 = None
				pswd2 = None
				charcount = 1

			except RuntimeError:
				xchat.prnt( "Recursion Error" )

		if botcheck2 is True:
			opcheck2 = False
			userlist = game_chan2.get_list("users")
			for user in userlist:
				if user.nick == botname2:
					botprefix = user.prefix
					checkbothostmask2 = user.host
					if(botprefix == "@" or botprefix == "%"):
						opcheck2 = True

			bothostcheck2 = False
			if bothostmask2 != None:
				if bothostmask2 in checkbothostmask2:
					bothostcheck2 = True

		if rawstatsmode is False and webworks is True and online2 is False and botcheck2 is True:
			if(opcheck2 is True) or (opcheck2 is False and bothostcheck2 is True):
				if(nickserv2 is True):
					if("dalnet" in netname2.lower()):
						game_chan2.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass2) )
					else:
						game_chan2.command( "msg nickserv identify {0}".format(nickservpass2) )
				usecommand("login {0} {1}".format(name2, pswd2), 2 )
				connectfail2 = 0
				interval = 45
				hookmain()
				intervaldisable = True
		
	if char3 is True:
		nickname3 = game_chan3.get_info("nick")
		netname3 = game_chan3.get_info("network")
		if game_chan3.get_info("server") is None:
			if errortextmode is True:
				xchat.prnt( "Not connected!" )
			connectfail3 += 1
			if errortextmode is True:
				xchat.prnt("3 Connect Fail: {0}".format(connectfail3))
			if(ZNC3 is False and servername3 != None):
				game_chan3.command( "server {0} {1}".format(servername3, port3) )
			if ZNC3 is True:
				game_chan3.command( "server {0} {1}".format(ZNCServer3, ZNCPort3) )

		online3 = False
		if rawstatsmode is False and webworks is True:
			try:
				if(myentry3[15] == "1"):
					online3 = True
			except TypeError:
				xchat.prnt( "Character {0} does not exist".format(name3) )
				char3 = False
				name3 = None
				pswd3 = None
				charcount = 2

			except RuntimeError:
				xchat.prnt( "Recursion Error" )

		if botcheck3 is True:
			opcheck3 = False
			userlist = game_chan3.get_list("users")
			for user in userlist:
				if user.nick == botname3:
					botprefix = user.prefix
					checkbothostmask3 = user.host
					if(botprefix == "@" or botprefix == "%"):
						opcheck3 = True

			bothostcheck3 = False
			if bothostmask3 != None:
				if bothostmask3 in checkbothostmask3:
					bothostcheck3 = True

		if rawstatsmode is False and webworks is True and online3 is False and botcheck3 is True:
			if(opcheck3 is True) or (opcheck3 is False and bothostcheck3 is True):
				if(nickserv3 is True):
					if("dalnet" in netname3.lower()):
						game_chan3.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass3) )
					else:
						game_chan3.command( "msg nickserv identify {0}".format(nickservpass3) )
				usecommand("login {0} {1}".format(name3, pswd3), 3 )
				connectfail3 = 0
				interval = 45
				hookmain()
				intervaldisable = True

	if char4 is True:
		nickname4 = game_chan4.get_info("nick")
		netname4 = game_chan4.get_info("network")
		if game_chan4.get_info("server") is None:
			if errortextmode is True:
				xchat.prnt( "Not connected!" )
			connectfail4 += 1
			if errortextmode is True:
				xchat.prnt("4 Connect Fail: {0}".format(connectfail4))
			if(ZNC4 is False and servername4 != None):
				game_chan4.command( "server {0} {1}".format(servername4, port4) )
			if ZNC4 is True:
				game_chan4.command( "server {0} {1}".format(ZNCServer4, ZNCPort4) )

		online4 = False
		if rawstatsmode is False and webworks is True:
			try:
				if(myentry4[15] == "1"):
					online4 = True
			except TypeError:
				xchat.prnt( "Character {0} does not exist".format(name4) )
				char4 = False
				name4 = None
				pswd4 = None
				charcount = 3

			except RuntimeError:
				xchat.prnt( "Recursion Error" )

		if botcheck4 is True:
			opcheck4 = False
			userlist = game_chan4.get_list("users")
			for user in userlist:
				if user.nick == botname4:
					botprefix = user.prefix
					checkbothostmask4 = user.host
					if(botprefix == "@" or botprefix == "%"):
						opcheck4 = True

			bothostcheck4 = False
			if bothostmask4 != None:
				if bothostmask4 in checkbothostmask4:
					bothostcheck4 = True

		if rawstatsmode is False and webworks is True and online4 is False and botcheck4 is True:
			if(opcheck4 is True) or (opcheck4 is False and bothostcheck4 is True):
				if(nickserv4 is True):
					if("dalnet" in netname4.lower()):
						game_chan4.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass4) )
					else:
						game_chan4.command( "msg nickserv identify {0}".format(nickservpass4) )
				usecommand("login {0} {1}".format(name4, pswd4), 4 )
				connectfail4 = 0
				interval = 45
				hookmain()
				intervaldisable = True
				
	if char5 is True:
		nickname5 = game_chan5.get_info("nick")
		netname5 = game_chan5.get_info("network")
		if game_chan5.get_info("server") is None:
			if errortextmode is True:
				xchat.prnt( "Not connected!" )
			connectfail5 += 1
			if errortextmode is True:
				xchat.prnt("5 Connect Fail: {0}".format(connectfail5))
			if(ZNC5 is False and servername5 != None):
				game_chan5.command( "server {0} {1}".format(servername5, port5) )
			if ZNC5 is True:
				game_chan5.command( "server {0} {1}".format(ZNCServer5, ZNCPort5) )

		online5 = False
		if rawstatsmode is False and webworks is True:
			try:
				if(myentry5[15] == "1"):
					online5 = True
			except TypeError:
				xchat.prnt( "Character {0} does not exist".format(name5) )
				char5 = False
				name5 = None
				pswd5 = None
				charcount = 4
			except RuntimeError:
				xchat.prnt( "Recursion Error" )

		if botcheck5 is True:
			opcheck5 = False
			userlist = game_chan5.get_list("users")
			for user in userlist:
				if user.nick == botname5:
					botprefix = user.prefix
					checkbothostmask5 = user.host
					if(botprefix == "@" or botprefix == "%"):
						opcheck5 = True

			bothostcheck5 = False
			if bothostmask5 != None:
				if bothostmask5 in checkbothostmask5:
					bothostcheck5 = True

		if rawstatsmode is False and webworks is True and online5 is False and botcheck5 is True:
			if(opcheck5 is True) or (opcheck5 is False and bothostcheck5 is True):
				if(nickserv5 is True):
					if("dalnet" in netname5.lower()):
						game_chan5.command( "msg NickServ@services.dal.net IDENTIFY {0}".format(nickservpass5) )
					else:
						game_chan5.command( "msg nickserv identify {0}".format(nickservpass5) )
				usecommand("login {0} {1}".format(name5, pswd5), 5 )
				connectfail5 = 0
				interval = 45
				hookmain()
				intervaldisable = True
				
	if itemslists is None and rawstatsmode is False and intervaldisable is False:
		interval = 30
		hookmain()
		intervaldisable = True
	if botcheck1 is False and botcheck2 is False and botcheck3 is False and botcheck4 is False and botcheck5 is False and intervaldisable is False:
		interval = 300
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
		if char1 is True:
			newitemslister(1,2)
		if char2 is True:
			newitemslister(2,2)
		if char3 is True:
			newitemslister(3,2)
		if char4 is True:
			newitemslister(4,2)
		if char5 is True:
			newitemslister(5,2)

		# Check if fights or bets happen to not be done.
		if char1 is True and botcheck1 is True and itemslists != None:
			for entry in itemslists:
				if(entry[0] == name):
					level = entry[2]
					bets = entry[22]
			if(bets < 5 and level >= 30):
				try:
					betdiff = (5 - bets)
					bet_bet(betdiff, 1)
				except TypeError:
					bets = 5
		if char2 is True and botcheck2 is True and itemslists != None:
			for entry in itemslists:
				if(entry[0] == name2):
					level2 = entry[2]
					bets2 = entry[22]
			if(bets2 < 5 and level2 >= 30):
				try:
					betdiff = (5 - bets2)
					bet_bet(betdiff, 2)
				except TypeError:
					bets2 = 5
		if char3 is True and botcheck3 is True and itemslists != None:
			for entry in itemslists:
				if(entry[0] == name3):
					level3 = entry[2]
					bets3 = entry[22]
			if(bets3 < 5 and level3 >= 30):
				try:
					betdiff = (5 - bets3)
					bet_bet(betdiff, 3)
				except TypeError:
					bets3 = 5
		if char4 is True and botcheck4 is True and itemslists != None:
			for entry in itemslists:
				if(entry[0] == name4):
					level4 = entry[2]
					bets4 = entry[22]
			if(bets4 < 5 and level4 >= 30):
				try:
					betdiff = (5 - bets4)
					bet_bet(betdiff, 4)
				except TypeError:
					bets4 = 5
		if char5 is True and botcheck5 is True and itemslists != None:
			for entry in itemslists:
				if(entry[0] == name5):
					level5 = entry[2]
					bets5 = entry[22]
			if(bets5 < 5 and level5 >= 30):
				try:
					betdiff = (5 - bets5)
					bet_bet(betdiff, 5)
				except TypeError:
					bets5 = 5

		if char1 is True and botcheck1 is True:
			spendmoney(1)
			aligncheck(1)
		if char2 is True and botcheck2 is True:
			spendmoney(2)
			aligncheck(2)
		if char3 is True and botcheck3 is True:
			spendmoney(3)
			aligncheck(3)
		if char4 is True and botcheck4 is True:
			spendmoney(4)
			aligncheck(4)
		if char5 is True and botcheck5 is True:
			spendmoney(5)
			aligncheck(5)

#                xchat.prnt("TTL: {0}, INTERVAL:{1}".format(ttl, interval))
		# check time til levelup
		# if I will before next interval,
		# set timer to call lvlup within 10 sec after leveling
		if char1 is True and botcheck1 is True:
			timercheck(1)
		if char2 is True and botcheck2 is True:
			timercheck(2)
		if char3 is True and botcheck3 is True:
			timercheck(3)
		if char4 is True and botcheck4 is True:
			timercheck(4)
		if char5 is True and botcheck5 is True:
			timercheck(5)

		# If so, do it (giggity)
		if char1 is True and botcheck1 is True and itemslists != None:
			for entry in itemslists:
				if(entry[0] == name):
					level = entry[2]
					fights = entry[16]

			if(level >= 10 and level <= 200):
				if(fights < 5):
					fight_fight(1)
		if char2 is True and botcheck2 is True and itemslists != None:
			for entry in itemslists:
				if(entry[0] == name2):
					level2 = entry[2]
					fights2 = entry[16]

			if(level2 >= 10 and level2 <= 200):
				if(fights2 < 5):
					fight_fight(2)
		if char3 is True and botcheck3 is True and itemslists != None:
			for entry in itemslists:
				if(entry[0] == name3):
					level3 = entry[2]
					fights3 = entry[16]

			if(level3 >= 10 and level3 <= 200):
				if(fights3 < 5):
					fight_fight(3)
		if char4 is True and botcheck4 is True and itemslists != None:
			for entry in itemslists:
				if(entry[0] == name4):
					level4 = entry[2]
					fights4 = entry[16]

			if(level4 >= 10 and level4 <= 200):
				if(fights4 < 5):
					fight_fight(4)
		if char5 is True and botcheck5 is True and itemslists != None:
			for entry in itemslists:
				if(entry[0] == name5):
					level5 = entry[2]
					fights5 = entry[16]

			if(level5 >= 10 and level5 <= 200):
				if(fights5 < 5):
					fight_fight(5)

	if chanmessage is True and chanmessagecount == 1:
		xchat.hook_print("Channel Message", on_message)
		xchat.hook_print("Channel Msg Hilight", on_message)

	if webworks is True and char1 is True and newlist != None:
		for entry in newlist:
			if(entry[5] == 1):
				levelrank1 = entry[3]

	rawstatsmodeon = False
	rawplayersmodeon = False
	opswitch = False
	if(opcheck is False or opcheck2 is False or opcheck3 is False or opcheck4 is False or opcheck5 is False):
		opswitch = True
	if(rawstatsswitch is False and rawstatsmode is True and webworks is True and ttlfrozenmode is False and opswitch is False):
		rawplayersmodeon = True
	if(rawstatsswitch is False and rawstatsmode is False and webworks is False and webfail >= 3  and opswitch is False):
		rawstatsmodeon = True
	if(levelrank1 < laglevel and rawstatsswitch is True and rawstatsmode is True  and opswitch is False):
		if(nolag1 is False or nolag2 is False or nolag3 is False or nolag4 is False or nolag5 is False):
			rawplayersmodeon = True
	if(levelrank1 >= laglevel and rawstatsswitch is True and rawstatsmode is False  and opswitch is False):
		rawstatsmodeon = True
	if(rawstatsmode is True and opswitch is True):
		rawplayersmodeon = True
	if rawstatsmodeon is True:
		rawstatsmode = True
		if bottextmode is True:
			xchat.prnt("Rawstats Mode Activated")
		configwrite()
	if rawplayersmodeon is True:
		if botcheck1 is True or botcheck2 is True or botcheck3 is True or botcheck4 is True or botcheck5 is True:
			rawstatsmode = False
			webdata()
			newitemslister(1, 1)
			if bottextmode is True:
				xchat.prnt("Rawplayers Mode Activated")
			if char1 is True:
				rawmyentry = None
			if char2 is True:
				rawmyentry2 = None
			if char3 is True:
				rawmyentry3 = None
			if char4 is True:
				rawmyentry4 = None
			if char5 is True:
				rawmyentry5 = None
			configwrite()

	ttlrawstatson = False
	if(rawstatsmode is False and webworks is True  and opswitch is False):
		if(char1 is True and botcheck1 is True and itemslists != None):
			for entry in itemslists:
				if(entry[0] == name):
					ttl = entry[17]
			if online1 is True:
				if ttl == oldttl:
					if errortextmode is True:
						xchat.prnt("TTL Frozen1")
					ttlfrozen1 += 1
			if ttlfrozen1 > charcount:
				if(nolag1 is True) or (nolag1 is False and levelrank1 >= laglevel):
					ttlrawstatson = True
		if(char2 is True and botcheck2 is True and itemslists != None):
			for entry in itemslists:
				if(entry[0] == name2):
					ttl2 = entry[17]
			if online2 is True:
				if ttl2 == oldttl2:
					if errortextmode is True:
						xchat.prnt("TTL Frozen2")
					ttlfrozen2 += 1
			if ttlfrozen2 > charcount:
				if(nolag2 is True) or (nolag2 is False and levelrank1 >= laglevel):
					ttlrawstatson = True
		if(char3 is True and botcheck3 is True and itemslists != None):
			for entry in itemslists:
				if(entry[0] == name3):
					ttl3 = entry[17]
			if online3 is True:
				if ttl3 == oldttl3:
					if errortextmode is True:
						xchat.prnt("TTL Frozen3")
					ttlfrozen3 += 1
			if ttlfrozen3 > charcount:
				if(nolag3 is True) or (nolag3 is False and levelrank1 >= laglevel):
					ttlrawstatson = True
		if(char4 is True and botcheck4 is True and itemslists != None):
			for entry in itemslists:
				if(entry[0] == name4):
					ttl4 = entry[17]
			if online4 is True:
				if ttl4 == oldttl4:
					if errortextmode is True:
						xchat.prnt("TTL Frozen4")
					ttlfrozen4 += 1
			if ttlfrozen4 > charcount:
				if(nolag4 is True) or (nolag4 is False and levelrank1 >= laglevel):
					ttlrawstatson = True
		if(char5 is True and botcheck5 is True and itemslists != None):
			for entry in itemslists:
				if(entry[0] == name5):
					ttl5 = entry[17]
			if online5 is True:
				if ttl5 == oldttl5:
					if errortextmode is True:
						xchat.prnt("TTL Frozen5")
					ttlfrozen5 += 1
			if ttlfrozen5 > charcount:
				if(nolag5 is True) or (nolag5 is False and levelrank1 >= laglevel):
					ttlrawstatson = True
		if ttlrawstatson is True:
			rawstatsmode = True
			ttlfrozenmode = True
			if bottextmode is True:
				xchat.prnt("Rawstats Mode Activated")

		if (ttlfrozen1 > charcount or ttlfrozen2 > charcount or ttlfrozen3 > charcount or ttlfrozen4 > charcount or ttlfrozen5 > charcount):
			ttlfrozen1 = 0
			ttlfrozen2 = 0
			ttlfrozen3 = 0
			ttlfrozen4 = 0
			ttlfrozen5 = 0
		
	return True        # <- tells timer to repeat

def intervalcalc():
	global interval
	global level
	global fights
	global ufightcalc1
	global ufightcalc2
	global ufightcalc3
	global ufightcalc4
	global ufightcalc5
	global bets
	global char1
	global char2
	global char3
	global char4
	global char5
	global itemslists
	global botcheck1
	global botcheck2
	global botcheck3
	global botcheck4
	global botcheck5
	global singlefight
	global nolag1
	global nolag2
	global nolag3
	global nolag4
	global nolag5
	global rawstatsmode
	global webworks
	global rawmyentry
	global rawmyentry2
	global rawmyentry3
	global rawmyentry4
	global rawmyentry5
	global name
	global name2
	global name3
	global name4
	global name5
	
	sixty = 60
	thirty = 30
	level2 = 0
	fights2 = 0
	bets2 = 0
	level3 = 0
	fights3 = 0
	bets3 = 0
	level4 = 0
	fights4 = 0
	bets4 = 0
	level5 = 0
	fights5 = 0
	bets5 = 0
	
	if char1 is True:
		if rawstatsmode is False and itemslists != None:
			for entry in itemslists:
				if(entry[0] == name):
					level = entry[2]
					fights = entry[16]
					bets = entry[22]
		if rawstatsmode is True and rawmyentry != None:
				level = int(rawmyentry[1])
				fights = int(rawmyentry[11])
				bets = int(rawmyentry[13])
	if char2 is True:
		if rawstatsmode is False and itemslists != None:
			for entry in itemslists:
				if(entry[0] == name2):
					level2 = entry[2]
					fights2 = entry[16]
					bets2 = entry[22]
		if rawstatsmode is True and rawmyentry2 != None:
				level2 = int(rawmyentry2[1])
				fights2 = int(rawmyentry2[11])
				bets2 = int(rawmyentry2[13])
	if char3 is True:
		if rawstatsmode is False and itemslists != None:
			for entry in itemslists:
				if(entry[0] == name3):
					level3 = entry[2]
					fights3 = entry[16]
					bets3 = entry[22]
		if rawstatsmode is True and rawmyentry3 != None:
				level3 = int(rawmyentry3[1])
				fights3 = int(rawmyentry3[11])
				bets3 = int(rawmyentry3[13])
	if char4 is True:
		if rawstatsmode is False and itemslists != None:
			for entry in itemslists:
				if(entry[0] == name4):
					level4 = entry[2]
					fights4 = entry[16]
					bets4 = entry[22]
		if rawstatsmode is True and rawmyentry4 != None:
				level4 = int(rawmyentry4[1])
				fights4 = int(rawmyentry4[11])
				bets4 = int(rawmyentry4[13])
	if char5 is True:
		if rawstatsmode is False and itemslists != None:
			for entry in itemslists:
				if(entry[0] == name5):
					level5 = entry[2]
					fights5 = entry[16]
					bets5 = entry[22]
		if rawstatsmode is True and rawmyentry5 != None:
				level5 = int(rawmyentry5[1])
				fights5 = int(rawmyentry5[11])
				bets5 = int(rawmyentry5[13])

	interval = 5
	interval *= 60                  # conv from min to sec
	intervallist = []
	if char1 is True:
		if botcheck1 is False:
			intervallist.append( ( "interval", sixty ) )
		if botcheck1 is True:
			if(level >= 10 and level < 30 and webworks is True):
				if(fights < 5):
					intervallist.append( ( "interval", sixty ) )
			if(bets == 5 and fights < 5 and level <= 200 and webworks is True):
				intervallist.append( ( "interval", sixty ) )
			if(bets < 5 and level >= 30 and webworks is True):
				intervallist.append( ( "interval", sixty ) )
			if(fights < 5 and ufightcalc1 >= 0.9 and level >= 10 and level <= 200 and singlefight is True and nolag1 is True and rawstatsmode is True and webworks is True):
				intervallist.append( ( "interval", thirty ) )
	if char2 is True:
		if botcheck2 is False:
			intervallist.append( ( "interval", sixty ) )
		if botcheck2 is True:
			if(level2 >= 10 and level2 < 30 and webworks is True):
				if(fights2 < 5):
					intervallist.append( ( "interval", sixty ) )
			if(bets2 == 5 and fights2 < 5 and level2 <= 200 and webworks is True):
				intervallist.append( ( "interval", sixty ) )
			if(bets2 < 5 and level2 >= 30 and webworks is True):
				intervallist.append( ( "interval", sixty ) )
			if(fights2 < 5 and ufightcalc2 >= 0.9 and level2 >= 10 and level2 <= 200 and singlefight is True and nolag2 is True and rawstatsmode is True and webworks is True):
				intervallist.append( ( "interval", thirty ) )
	if char3 is True:
		if botcheck3 is False:
			intervallist.append( ( "interval", sixty ) )
		if botcheck3 is True:
			if(level3 >= 10 and level3 < 30 and webworks is True):
				if(fights3 < 5):
					intervallist.append( ( "interval", sixty ) )
			if(bets3 == 5 and fights3 < 5 and level3 <= 200 and webworks is True):
				intervallist.append( ( "interval", sixty ) )
			if(bets3 < 5 and level3 >= 30 and webworks is True):
				intervallist.append( ( "interval", sixty ) )
			if(fights3 < 5 and ufightcalc3 >= 0.9 and level3 >= 10 and level3 <= 200 and singlefight is True and nolag3 is True and rawstatsmode is True and webworks is True):
				intervallist.append( ( "interval", thirty ) )
	if char4 is True:
		if botcheck4 is False:
			intervallist.append( ( "interval", sixty ) )
		if botcheck4 is True:
			if(level4 >= 10 and level4 < 30 and webworks is True):
				if(fights4 < 5):
					intervallist.append( ( "interval", sixty ) )
			if(bets4 == 5 and fights4 < 5 and level4 <= 200 and webworks is True):
				intervallist.append( ( "interval", sixty ) )
			if(bets4 < 5 and level4 >= 30 and webworks is True):
				intervallist.append( ( "interval", sixty ) )
			if(fights4 < 5 and ufightcalc4 >= 0.9 and level4 >= 10 and level4 <= 200 and singlefight is True and nolag4 is True and rawstatsmode is True and webworks is True):
				intervallist.append( ( "interval", thirty ) )
	if char5 is True:
		if botcheck5 is False:
			intervallist.append( ( "interval", sixty ) )
		if botcheck5 is True:
			if(level5 >= 10 and level5 < 30 and webworks is True):
				if(fights5 < 5):
					intervallist.append( ( "interval", sixty ) )
			if(bets5 == 5 and fights5 < 5 and level5 <= 200 and webworks is True):
				intervallist.append( ( "interval", sixty ) )
			if(bets5 < 5 and level5 >= 30 and webworks is True):
				intervallist.append( ( "interval", sixty ) )
			if(fights5 < 5 and ufightcalc5 >= 0.9 and level5 >= 10 and level5 <= 200 and singlefight is True and nolag5 is True and rawstatsmode is True and webworks is True):
				intervallist.append( ( "interval", thirty ) )

	intervallist.sort( key=operator.itemgetter(1), reverse=True )
	diff = 999999        
	for entry in intervallist:
		if(entry[1] < diff):
			interval = entry[1]

	hookmain()

def timercheck(num):
	global alignlevel
	global ttl
	global interval
	global atime
	global stime
	global ctime
	global level
	global newlist
	global newlist2
	global newlist3
	global newlist4
	global newlist5
	global mysum
	global webworks
	global bottextmode
	global attackcount1
	global attackcount2
	global attackcount3
	global attackcount4
	global attackcount5
	global challengecount1
	global challengecount2
	global challengecount3
	global challengecount4
	global challengecount5
	global slaycount1
	global slaycount2
	global slaycount3
	global slaycount4
	global slaycount5
	global alignlvlupcount1
	global alignlvlupcount2
	global alignlvlupcount3
	global alignlvlupcount4
	global alignlvlupcount5
	global lvlupcount1
	global lvlupcount2
	global lvlupcount3
	global lvlupcount4
	global lvlupcount5
	
	getitems2(num)
	if num == 1:
		newlists = newlist
	if num == 2:
		newlists = newlist2
	if num == 3:
		newlists = newlist3
	if num == 4:
		newlists = newlist4
	if num == 5:
		newlists = newlist5
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
	if num == 1:
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
	if num == 2:
		if(alignlvlupcount2 < 0):
			alignlvlupcount2 = 0
		if(lvlupcount2 < 0):
			lvlupcount2 = 0
		if(attackcount2 < 0):
			attackcount2 = 0
		if(challengecount2 < 0):
			challengecount2 = 0
		if(slaycount2 < 0):
			slaycount2 = 0
	if num == 3:
		if(alignlvlupcount3 < 0):
			alignlvlupcount3 = 0
		if(lvlupcount3 < 0):
			lvlupcount3 = 0
		if(attackcount3 < 0):
			attackcount3 = 0
		if(challengecount3 < 0):
			challengecount3 = 0
		if(slaycount3 < 0):
			slaycount3 = 0
	if num == 4:
		if(alignlvlupcount4 < 0):
			alignlvlupcount4 = 0
		if(lvlupcount4 < 0):
			lvlupcount4 = 0
		if(attackcount4 < 0):
			attackcount4 = 0
		if(challengecount4 < 0):
			challengecount4 = 0
		if(slaycount4 < 0):
			slaycount4 = 0
	if num == 5:
		if(alignlvlupcount5 < 0):
			alignlvlupcount5 = 0
		if(lvlupcount5 < 0):
			lvlupcount5 = 0
		if(attackcount5 < 0):
			attackcount5 = 0
		if(challengecount5 < 0):
			challengecount5 = 0
		if(slaycount5 < 0):
			slaycount5 = 0

#        xchat.prnt("{0} TTL: {1}  Atime: {2}  Ctime: {3}  Stime: {4}".format(num,ttl,atime,ctime,stime))
	
	challengecheck = False
	if(level >= 35):
		leveldiff = level + 10
		sumdiff = mysum + (mysum * 0.15)
		challengediff = ("Doctor Who?", 999999)
		if webworks is True and newlists != None:
			for entry in newlists:
				if(entry[3] <= leveldiff and entry[2] <= sumdiff):
					challengecheck = True
					challengediff = entry
	if(level >= alignlevel and attl <= interval):
		timer = (attl)*1000
		if bottextmode is True:
			xchat.prnt("Set align lvlup {0} timer. Going off in {1} minutes.".format(num, timer // 60000))
		if num == 1:
			xchat.hook_timer(timer, alignlvlup)
			alignlvlupcount1 += 1
		if num == 2:
			xchat.hook_timer(timer, alignlvlup2)
			alignlvlupcount2 += 1
		if num == 3:
			xchat.hook_timer(timer, alignlvlup3)
			alignlvlupcount3 += 1
		if num == 4:
			xchat.hook_timer(timer, alignlvlup4)
			alignlvlupcount4 += 1
		if num == 5:
			xchat.hook_timer(timer, alignlvlup5)
			alignlvlupcount5 += 1
	if(ttl <= interval and ttl > 0):
		timer = (ttl+10)*1000
		if bottextmode is True:
			xchat.prnt("Set lvlup {0} timer. Going off in {1} minutes.".format(num, timer // 60000))
		if num == 1:
			xchat.hook_timer(timer, lvlup)
			lvlupcount1 += 1                        
		if num == 2:
			xchat.hook_timer(timer, lvlup2)
			lvlupcount2 += 1                        
		if num == 3:
			xchat.hook_timer(timer, lvlup3)
			lvlupcount3 += 1                        
		if num == 4:
			xchat.hook_timer(timer, lvlup4)
			lvlupcount4 += 1                        
		if num == 5:
			xchat.hook_timer(timer, lvlup5)
			lvlupcount5 += 1                        
	
	# do checks for other actions.
	if(level >= 10 and atime <= interval and atime <= ttl):
		timer = (atime+10)*1000
		if bottextmode is True:
			xchat.prnt("Set attack {0} timer. Going off in {1} minutes.".format(num, timer // 60000))
		if num == 1:
			xchat.hook_timer(timer, attack)
			attackcount1 += 1
		if num == 2:
			xchat.hook_timer(timer, attack2)
			attackcount2 += 1
		if num == 3:
			xchat.hook_timer(timer, attack3)
			attackcount3 += 1
		if num == 4:
			xchat.hook_timer(timer, attack4)
			attackcount4 += 1
		if num == 5:
			xchat.hook_timer(timer, attack5)
			attackcount5 += 1

	if(level >= 40 and stime <= interval and stime <= ttl):
		timer = (stime+10)*1000
		if bottextmode is True:
			xchat.prnt("Set slay {0} timer. Going off in {1} minutes.".format(num, timer // 60000))
		if num == 1:
			xchat.hook_timer(timer, slay)
			slaycount1 += 1
		if num == 2:
			xchat.hook_timer(timer, slay2)
			slaycount2 += 1
		if num == 3:
			xchat.hook_timer(timer, slay3)
			slaycount3 += 1
		if num == 4:
			xchat.hook_timer(timer, slay4)
			slaycount4 += 1
		if num == 5:
			xchat.hook_timer(timer, slay5)
			slaycount5 += 1

	if challengecheck is True or webworks is False:
		if(level >= 35 and ctime <= interval and ctime <= ttl):
			timer = (ctime+10)*1000
			if bottextmode is True:
				xchat.prnt("Set challenge {0} timer. Going off in {1} minutes.".format(num, timer // 60000))
			if num == 1:
				xchat.hook_timer(timer, challenge)
				challengecount1 += 1
			if num == 2:
				xchat.hook_timer(timer, challenge2)
				challengecount2 += 1
			if num == 3:
				xchat.hook_timer(timer, challenge3)
				challengecount3 += 1
			if num == 4:
				xchat.hook_timer(timer, challenge4)
				challengecount4 += 1
			if num == 5:
				xchat.hook_timer(timer, challenge5)
				challengecount5 += 1
	if num == 1:
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
#                xchat.prnt("1 AttackCount: {0} ChallengeCount: {1} SlayCount: {2} AlignlvlupCount: {3} LvlupCount: {4}".format(attackcount1, challengecount1, slaycount1, alignlvlupcount1, lvlupcount1))
	if num == 2:
		if(attl > 350 and alignlvlupcount2 >= 1):
			alignlvlupcount2 = 0
		if(ttl > 350 and lvlupcount2 >= 1):
			lvlupcount2 = 0
		if(level >= 10 and atime > 350 and attackcount2 >= 1):
			attackcount2 = 0
		if(level >= 35 and ctime > 350 and challengecount2 >= 1):
			challengecount2 = 0
		if(level >= 40 and stime > 350 and slaycount2 >= 1):
			slaycount2 = 0              
		if(level >= 10 and atime == 0 and attackcount2 >= 0):
			attackcount2 = 1
		if(level >= 35 and ctime == 0 and challengecount2 >= 0):
			challengecount2 = 1
		if(level >= 40 and stime == 0 and slaycount2 >= 0):
			slaycount2 = 1          
#                xchat.prnt("2 AttackCount: {0} ChallengeCount: {1} SlayCount: {2} AlignlvlupCount: {3} LvlupCount: {4}".format(attackcount2, challengecount2, slaycount2, alignlvlupcount2, lvlupcount2))
	if num == 3:
		if(attl > 350 and alignlvlupcount3 >= 1):
			alignlvlupcount3 = 0
		if(ttl > 350 and lvlupcount3 >= 1):
			lvlupcount3 = 0
		if(level >= 10 and atime > 350 and attackcount3 >= 1):
			attackcount3 = 0
		if(level >= 35 and ctime > 350 and challengecount3 >= 1):
			challengecount3 = 0
		if(level >= 40 and stime > 350 and slaycount3 >= 1):
			slaycount3 = 0              
		if(level >= 10 and atime == 0 and attackcount3 >= 0):
			attackcount3 = 1
		if(level >= 35 and ctime == 0 and challengecount3 >= 0):
			challengecount3 = 1
		if(level >= 40 and stime == 0 and slaycount3 >= 0):
			slaycount3 = 1          
#                xchat.prnt("3 AttackCount: {0} ChallengeCount: {1} SlayCount: {2} AlignlvlupCount: {3} LvlupCount: {4}".format(attackcount3, challengecount3, slaycount3, alignlvlupcount3, lvlupcount3))
	if num == 4:
		if(attl > 350 and alignlvlupcount4 >= 1):
			alignlvlupcount4 = 0
		if(ttl > 350 and lvlupcount4 >= 1):
			lvlupcount4 = 0
		if(level >= 10 and atime > 350 and attackcount4 >= 1):
			attackcount4 = 0
		if(level >= 35 and ctime > 350 and challengecount4 >= 1):
			challengecount4 = 0
		if(level >= 40 and stime > 350 and slaycount4 >= 1):
			slaycount4 = 0              
		if(level >= 10 and atime == 0 and attackcount4 >= 0):
			attackcount4 = 1
		if(level >= 35 and ctime == 0 and challengecount4 >= 0):
			challengecount4 = 1
		if(level >= 40 and stime == 0 and slaycount4 >= 0):
			slaycount4 = 1          
#                xchat.prnt("4 AttackCount: {0} ChallengeCount: {1} SlayCount: {2} AlignlvlupCount: {3} LvlupCount: {4}".format(attackcount4, challengecount4, slaycount4, alignlvlupcount4, lvlupcount4))
	if num == 5:
		if(attl > 350 and alignlvlupcount5 >= 1):
			alignlvlupcount5 = 0
		if(ttl > 350 and lvlupcount5 >= 1):
			lvlupcount5 = 0
		if(level >= 10 and atime > 350 and attackcount5 >= 1):
			attackcount5 = 0
		if(level >= 35 and ctime > 350 and challengecount5 >= 1):
			challengecount5 = 0
		if(level >= 40 and stime > 350 and slaycount5 >= 1):
			slaycount5 = 0              
		if(level >= 10 and atime == 0 and attackcount5 >= 0):
			attackcount5 = 1
		if(level >= 35 and ctime == 0 and challengecount5 >= 0):
			challengecount5 = 1
		if(level >= 40 and stime == 0 and slaycount5 >= 0):
			slaycount5 = 1          
#                xchat.prnt("5 AttackCount: {0} ChallengeCount: {1} SlayCount: {2} AlignlvlupCount: {3} LvlupCount: {4}".format(attackcount5, challengecount5, slaycount5, alignlvlupcount5, lvlupcount5))

def getitems2(num):
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

	global itemslists
	global rawstatsmode
	global rawmyentry
	global rawmyentry2
	global rawmyentry3
	global rawmyentry4
	global rawmyentry5
	global myentry
	global myentry2
	global myentry3
	global myentry4
	global myentry5
	global name
	global name2
	global name3
	global name4
	global name5
	global align
	
	if num == 1:
		names = name
		rawmyentrys = rawmyentry
		myentrys = myentry
	if num == 2:
		names = name2
		rawmyentrys = rawmyentry2
		myentrys = myentry2
	if num == 3:
		names = name3
		rawmyentrys = rawmyentry3
		myentrys = myentry3
	if num == 4:
		names = name4
		rawmyentrys = rawmyentry4
		myentrys = myentry4
	if num == 5:
		names = name5
		rawmyentrys = rawmyentry5
		myentrys = myentry5
		
	if rawstatsmode is False and itemslists != None:
		for entry in itemslists:
			if(entry[0] == names):
				mysum = entry[1]
				level = entry[2]
				align = entry[3]
				rankplace = entry[4]
				team = entry[5]
				amulet = entry[6]
				charm = entry[7]
				helm = entry[8]
				boots = entry[9]
				gloves = entry[10]
				ring = entry[11]
				leggings = entry[12]
				shield = entry[13]
				tunic = entry[14]
				weapon = entry[15]
				fights = entry[16]
				ttl = entry[17]
				atime = entry[18]
				ctime = entry[19]
				stime = entry[20]
				powerpots = entry[21]
				bets = entry[22]
				hero = entry[23]
				hlvl = entry[24]
				eng = entry[25]
				elvl = entry[26]
				gold = entry[27]
				bank = entry[28]
	if rawstatsmode is True and rawmyentrys != None:
		level = int(rawmyentrys[1])
		gold = int(rawmyentrys[3])
		bank = int(rawmyentrys[5])
		team = int(rawmyentrys[7])
		mysum = int(rawmyentrys[9])
		fights = int(rawmyentrys[11])
		bets = int(rawmyentrys[13])
		powerpots = int(rawmyentrys[15])
		align = rawmyentrys[19]
		atime = int(rawmyentrys[21])
		ctime = int(rawmyentrys[23])
		stime = int(rawmyentrys[25])
		ttl = int(rawmyentrys[27])
		hero = int(rawmyentrys[29])
		hlvl = int(rawmyentrys[31])
		eng = int(rawmyentrys[33])
		elvl = int(rawmyentrys[35])

		try:
			ring = rawmyentrys[37] .strip("abcdefghijklmnopqrstuvwxyz")
			ring = int( ring )
		except AttributeError:
			ring = int(rawmyentrys[37])
		try:
			amulet = rawmyentrys[39] .strip("abcdefghijklmnopqrstuvwxyz")
			amulet = int( amulet )
		except AttributeError:
			amulet = int(rawmyentrys[39])
		try:
			charm = rawmyentrys[41] .strip("abcdefghijklmnopqrstuvwxyz")
			charm = int( charm )
		except AttributeError:
			charm = int(rawmyentrys[41])
		try:
			weapon = rawmyentrys[43] .strip("abcdefghijklmnopqrstuvwxyz")
			weapon = int( weapon )
		except AttributeError:
			weapon = int(rawmyentrys[43])
		try:
			helm = rawmyentrys[45] .strip("abcdefghijklmnopqrstuvwxyz")
			helm = int( helm )
		except AttributeError:
			helm = int(rawmyentrys[45])
		try:
			tunic = rawmyentrys[47] .strip("abcdefghijklmnopqrstuvwxyz")
			tunic = int( tunic )
		except AttributeError:
			tunic = int(rawmyentrys[47])
		try:
			gloves = rawmyentrys[49] .strip("abcdefghijklmnopqrstuvwxyz")
			gloves = int( gloves )
		except AttributeError:
			gloves = int(rawmyentrys[49])
		try:
			shield = rawmyentrys[51] .strip("abcdefghijklmnopqrstuvwxyz")
			shield = int( shield )
		except AttributeError:
			shield = int(rawmyentrys[51])
		try:
			leggings = rawmyentrys[53] .strip("abcdefghijklmnopqrstuvwxyz")
			leggings = int( leggings )
		except AttributeError:
			leggings = int(rawmyentrys[53])
		try:
			boots = rawmyentrys[55] .strip("abcdefghijklmnopqrstuvwxyz")
			boots = int( boots )
		except AttributeError:
			boots = int(rawmyentrys[55])

	if rawstatsmode is True and myentrys != None:
		rankplace = int(myentrys[1])

def spendmoney(num):
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
	global fightSum1
	global fightSum2
	global fightSum3
	global fightSum4
	global fightSum5
	global firstalign
	global setbuy
	
	# decide what to spend our gold on! :D
		
	getitems2(num)

	lowestitem = worstitem(num)
#        xchat.prnt("Worst item {0} {1}".format(num, lowestitem))
	if(level >= 0):
		try:
			if(gold >= 41):
				usecommand("bank deposit {0}".format(gold - 40), num)
				bank += (gold - 40)
				gold = 40
			elif(gold <= 20 and bank >= 20):
				usecommand("bank withdraw 20", num)
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
				usecommand("bank withdraw {0}".format(buycost), num) 
				usecommand("buy amulet {0}".format(buyitem), num)
				bank -= buycost
				amulet = buyitem
		if(bank > buycost + betmoney):
			if(charm < (buyitem - buydiff)):
				usecommand("bank withdraw {0}".format(buycost), num) 
				usecommand("buy charm {0}".format(buyitem), num)
				bank -= buycost
				charm = buyitem
		if(bank > buycost + betmoney):
			if(helm < (buyitem - buydiff)):
				usecommand("bank withdraw {0}".format(buycost), num) 
				usecommand("buy helm {0}".format(buyitem), num)
				bank -= buycost
				helm = buyitem
		if(bank > buycost + betmoney):
			if(boots < (buyitem - buydiff)):
				usecommand("bank withdraw {0}".format(buycost), num) 
				usecommand("buy boots {0}".format(buyitem), num)
				bank -= buycost
				boots = buyitem
		if(bank > buycost + betmoney):
			if(gloves < (buyitem - buydiff)):
				usecommand("bank withdraw {0}".format(buycost), num) 
				usecommand("buy gloves {0}".format(buyitem), num)
				bank -= buycost
				gloves = buyitem
		if(bank > buycost + betmoney):
			if(ring < (buyitem - buydiff)):
				usecommand("bank withdraw {0}".format(buycost), num) 
				usecommand("buy ring {0}".format(buyitem), num)
				bank -= buycost
				ring = buyitem
		if(bank > buycost + betmoney):
			if(leggings < (buyitem - buydiff)):
				usecommand("bank withdraw {0}".format(buycost), num) 
				usecommand("buy leggings {0}".format(buyitem), num)
				bank -= buycost
				leggings = buyitem
		if(bank > buycost + betmoney):
			if(shield < (buyitem - buydiff)):
				usecommand("bank withdraw {0}".format(buycost), num) 
				usecommand("buy shield {0}".format(buyitem), num)
				bank -= buycost
				shield = buyitem
		if(bank > buycost + betmoney):
			if(tunic < (buyitem - buydiff)):
				usecommand("bank withdraw {0}".format(buycost), num) 
				usecommand("buy tunic {0}".format(buyitem), num)
				bank -= buycost
				tunic = buyitem
		if(bank > buycost + betmoney):
			if(weapon < (buyitem - buydiff)):
				usecommand("bank withdraw {0}".format(buycost), num) 
				usecommand("buy weapon {0}".format(buyitem), num)
				bank -= buycost
				weapon = buyitem

	if(level >= setengineer) or (level >= 15 and bank >= 2800 + betmoney):
		if(eng == 0 and bank >= 1000):
			usecommand("bank withdraw 1000", num)
			usecommand("hire engineer", num)
			bank -= 1000
			eng = 1
		if(eng == 1 and elvl < 9):
			elvldiff = 9 - elvl
			elvlcost = elvldiff * 200
			if(bank >= elvlcost + betmoney):
				usecommand("bank withdraw {0}".format(elvlcost), num)
				for i in range(elvldiff):
					usecommand("engineer level", num)
				bank -= elvlcost
				elvl += elvldiff
			elif(bank > betmoney):
				moneycalc = bank - betmoney                                
				upgradeengcalc = moneycalc // 200
				if(upgradeengcalc >= 1):
					engmoney = upgradeengcalc * 200
					usecommand("bank withdraw {0}".format(engmoney), num)
					for i in range(upgradeengcalc):
						usecommand("engineer level", num)
					bank -= engmoney
					elvl += upgradeengcalc
	
	if(mysum >= sethero and level >= 15) or (level >= 15 and elvl == 9 and bank >= 2800 + betmoney):
		if(hero == 0 and bank >= betmoney + 1000):
			usecommand("bank withdraw 1000", num)
			usecommand("summon hero", num)
			bank -= 1000
			hero = 1
		if(hero == 1 and hlvl < 9):
			hlvldiff = 9 - hlvl
			hlvlcost = hlvldiff * 200
			if(bank >= hlvlcost + betmoney):
				usecommand("bank withdraw {0}".format(hlvlcost), num)
				for i in range(hlvldiff):
					usecommand("hero level", num)
				bank -= hlvlcost
				hlvl += hlvldiff
			elif(bank > betmoney):
				moneycalc = bank - betmoney                                
				upgradeherocalc = moneycalc // 200
				if(upgradeherocalc >= 1):
					heromoney = upgradeherocalc * 200
					usecommand("bank withdraw {0}".format(heromoney), num)
					for i in range(upgradeherocalc):
						usecommand("hero level", num)
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
				usecommand("bank withdraw {0}".format(itemmoney), num)
				usecommand("upgrade all {0}".format(upgradeallcalc * multi), num)
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
					usecommand("bank withdraw {0}".format(itemmoney), num)
					itemupgrade(upgradecalc, num)
					bank -= itemmoney

	NewSum = amulet + charm + helm + boots + gloves + ring + leggings + shield + tunic + weapon
	if num == 1:
		fightSum1 = NewSum
	if num == 2:
		fightSum2 = NewSum
	if num == 3:
		fightSum3 = NewSum
	if num == 4:
		fightSum4 = NewSum
	if num == 5:
		fightSum5 = NewSum
	if(firstalign == "priest"):
		priestadjust = NewSum * 0.10
		if num == 1:
			fightSum1 += priestadjust
		if num == 2:
			fightSum2 += priestadjust
		if num == 3:
			fightSum3 += priestadjust
		if num == 4:
			fightSum4 += priestadjust
		if num == 5:
			fightSum5 += priestadjust
	if(hero == 1):
		if num == 1:
			heroadj = fightSum1 * ((hlvl + 2) /100.0)
			fightSum1 += heroadj
		if num == 2:
			heroadj = fightSum2 * ((hlvl + 2) /100.0)
			fightSum2 += heroadj
		if num == 3:
			heroadj = fightSum3 * ((hlvl + 2) /100.0)
			fightSum3 += heroadj
		if num == 4:
			heroadj = fightSum4 * ((hlvl + 2) /100.0)
			fightSum4 += heroadj
		if num == 5:
			heroadj = fightSum5 * ((hlvl + 2) /100.0)
			fightSum5 += heroadj

def alignlvlup(userdata):
	global alignlvlupcount1

	if alignlvlupcount1 == 1:
		alignlvlupmulti(1)
	alignlvlupcount1 -= 1

def alignlvlup2(userdata):
	global alignlvlupcount2

	if alignlvlupcount2 == 1:
		alignlvlupmulti(2)
	alignlvlupcount2 -= 1

def alignlvlup3(userdata):
	global alignlvlupcount3

	if alignlvlupcount3 == 1:
		alignlvlupmulti(3)
	alignlvlupcount3 -= 1

def alignlvlup4(userdata):
	global alignlvlupcount4

	if alignlvlupcount4 == 1:
		alignlvlupmulti(4)
	alignlvlupcount4 -= 1

def alignlvlup5(userdata):
	global alignlvlupcount5

	if alignlvlupcount5 == 1:
		alignlvlupmulti(5)
	alignlvlupcount5 -= 1

def alignlvlupmulti(num):
	global level
	global alignlevel
	
	getitems2(num)
	if(level >= alignlevel):
		usecommand("align priest", num)

def lvlup(userdata):
	global lvlupcount1

	if lvlupcount1 == 1:
		lvlupmulti(1)
	lvlupcount1 -= 1

def lvlup2(userdata):
	global lvlupcount2

	if lvlupcount2 == 1:
		lvlupmulti(2)
	lvlupcount2 -= 1

def lvlup3(userdata):
	global lvlupcount3

	if lvlupcount3 == 1:
		lvlupmulti(3)
	lvlupcount3 -= 1

def lvlup4(userdata):
	global lvlupcount4

	if lvlupcount4 == 1:
		lvlupmulti(4)
	lvlupcount4 -= 1

def lvlup5(userdata):
	global lvlupcount5

	if lvlupcount5 == 1:
		lvlupmulti(5)
	lvlupcount5 -= 1

def lvlupmulti(num):
	global name
	global name2
	global name3
	global name4
	global name5
	global level
	global interval
	global webworks
	global rawstatsmode
	global rawmyentry 
	global rawmyentry2
	global rawmyentry3
	global rawmyentry4
	global rawmyentry5
	global ttlfrozenmode
	global ttlfrozen1
	global ttlfrozen2
	global ttlfrozen3
	global ttlfrozen4
	global ttlfrozen5
	global char1
	global char2
	global char3
	global char4
	global char5
	global bottextmode
	global attackcount1
	global attackcount2
	global attackcount3
	global attackcount4
	global attackcount5
	global challengecount1
	global challengecount2
	global challengecount3
	global challengecount4
	global challengecount5
	global slaycount1
	global slaycount2
	global slaycount3
	global slaycount4
	global slaycount5
	
	if rawstatsmode is True:
		usecommand("rawstats2", num)

	webdata()
	if webworks is True:
		newitemslister(num, 2)
		newitemslister(1, 1)
	getitems2(num)
	if num == 1:
		namelist = name
	if num == 2:
		namelist = name2
	if num == 3:
		namelist = name3
	if num == 4:
		namelist = name4
	if num == 5:
		namelist = name5

	# rehook main timer for potential new interval
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
		xchat.prnt("{0} has reached level {1}!".format(namelist, level))

	if(level <= 10):
		usecommand("load power 0", num)
	if ttlfrozenmode is True:
		    ttlfrozenmode = False
		    rawstatsmode = False
		    if bottextmode is True:
			    xchat.prnt("Rawplayers Mode Activated")
		    if char1 is True:
			    rawmyentry = None
		    if char2 is True:
			    rawmyentry2 = None
		    if char3 is True:
			    rawmyentry3 = None
		    if char4 is True:
			    rawmyentry4 = None
		    if char5 is True:
			    rawmyentry5 = None
	ttlfrozen1 = 0
	ttlfrozen2 = 0
	ttlfrozen3 = 0
	ttlfrozen4 = 0
	ttlfrozen5 = 0

	if rawstatsmode is False:
		if(level >= 30):
			if webworks is True:
				try:
					bet_bet(5, num)
				except TypeError:
					bets = 5
		if(level >= 10):
			if num == 1:
				attackcount1 = 1
				xchat.hook_timer(0, attack)
			if num == 2:
				attackcount2 = 1
				xchat.hook_timer(0, attack2)
			if num == 3:
				attackcount3 = 1
				xchat.hook_timer(0, attack3)
			if num == 4:
				attackcount4 = 1
				xchat.hook_timer(0, attack4)
			if num == 5:
				attackcount5 = 1
				xchat.hook_timer(0, attack5)
		if(level >= 40):
			if num == 1:
				slaycount1 = 1
				xchat.hook_timer(0, slay)
			if num == 2:
				slaycount2 = 1
				xchat.hook_timer(0, slay2)
			if num == 3:
				slaycount3 = 1
				xchat.hook_timer(0, slay3)
			if num == 4:
				slaycount4 = 1
				xchat.hook_timer(0, slay4)
			if num == 5:
				slaycount5 = 1
				xchat.hook_timer(0, slay5)
		if(level >= 35):
			if num == 1:
				challengecount1 = 1
				xchat.hook_timer(0, challenge)
			if num == 2:
				challengecount2 = 1
				xchat.hook_timer(0, challenge2)
			if num == 3:
				challengecount3 = 1
				xchat.hook_timer(0, challenge3)
			if num == 4:
				challengecount4 = 1
				xchat.hook_timer(0, challenge4)
			if num == 5:
				challengecount5 = 1
				xchat.hook_timer(0, challenge5)

def bet_bet(num1, num2):
	global level
	global bank
	global bets

	getitems2(num2)
	
	if(level >= 30):
		bbet = bestbet(num2)
#                xchat.prnt("bestbet {0} {1}".format( bbet[0][0], bbet[1][0] ))
		if(bank >= 100):
			usecommand("bank withdraw 100", num2)
			for i in range(num1):
				usecommand("bet {0} {1} 100".format( bbet[0][0], bbet[1][0] ), num2)
			bank -=100

def fight_fight(num):
	global name
	global name2
	global name3
	global name4
	global name5
	global level
	global powerpots
	global alignlevel
	global rankplace
	global fights
	global firstalign
	global secondalign
	global ufightcalc1
	global ufightcalc2
	global ufightcalc3
	global ufightcalc4
	global ufightcalc5
	global fightSum1
	global fightSum2
	global fightSum3
	global fightSum4
	global fightSum5
	global bets
	global singlefight
	global team
	global myentry
	global myentry2
	global myentry3
	global myentry4
	global myentry5
	global rawstatsmode
	global bottextmode
	
	getitems2(num)

	if num == 1:
		myentrys = myentry
		names = name
		ufight = testfight(1)
		fightsumlist = fightSum1
	if num == 2:
		myentrys = myentry2
		names = name2
		ufight = testfight(2)
		fightsumlist = fightSum2
	if num == 3:
		myentrys = myentry3
		names = name3
		ufight = testfight(3)
		fightsumlist = fightSum3
	if num == 4:
		myentrys = myentry4
		names = name4
		ufight = testfight(4)
		fightsumlist = fightSum4
	if num == 5:
		myentrys = myentry5
		names = name5
		ufight = testfight(5)
		fightsumlist = fightSum5

	if num == 1:
		ufightcalc1 = fightsumlist / ufight[2]
	if num == 2:
		ufightcalc2 = fightsumlist / ufight[2]
	if num == 3:
		ufightcalc3 = fightsumlist / ufight[2]
	if num == 4:
		ufightcalc4 = fightsumlist / ufight[2]
	if num == 5:
		ufightcalc5 = fightsumlist / ufight[2]
	if(ufight[0] == names):
		if num == 1:
			ufightcalc1 = 0.1
			usecommand("bank deposit 1", 1)
		if num == 2:
			ufightcalc2 = 0.1
			usecommand("bank deposit 1", 2)
		if num == 3:
			ufightcalc3 = 0.1
			usecommand("bank deposit 1", 3)
		if num == 4:
			ufightcalc4 = 0.1
			usecommand("bank deposit 1", 4)
		if num == 5:
			ufightcalc5 = 0.1
			usecommand("bank deposit 1", 5)
	if(team >= 1):
		if(ufight[6] == team):
			if num == 1:
				ufightcalc1 = 0.1
			if num == 2:
				ufightcalc2 = 0.1
			if num == 3:
				ufightcalc3 = 0.1
			if num == 4:
				ufightcalc4 = 0.1
			if num == 5:
				ufightcalc5 = 0.1

	if(level >= 30 and bets < 5):
		if num == 1:
			ufightcalc1 = 0.1
		if num == 2:
			ufightcalc2 = 0.1
		if num == 3:
			ufightcalc3 = 0.1
		if num == 4:
			ufightcalc4 = 0.1
		if num == 5:
			ufightcalc5 = 0.1
	fightdiff = 5 - fights
	if(powerpots >= fightdiff):
		spendpower = fightdiff
	if(powerpots < fightdiff):
		spendpower = powerpots

	if rawstatsmode is True:
		ranknumber = myentrys[1]
	if rawstatsmode is False:
		ranknumber = rankplace

	if(level >= 10):
		if num == 1:
			ufightcalclist = ufightcalc1
		if num == 2:
			ufightcalclist = ufightcalc2
		if num == 3:
			ufightcalclist = ufightcalc3
		if num == 4:
			ufightcalclist = ufightcalc4
		if num == 5:
			ufightcalclist = ufightcalc5
		if bottextmode is True:
			xchat.prnt("{0} Best fight for Rank {1}: {2} [{3}]  Opponent: Rank {4}: {5} [{6}], Odds {7}".format(num, ranknumber, names, int(fightsumlist), ufight[5], ufight[0], int(ufight[2]), ufightcalclist))
		if(ufightcalclist >= 0.9):
			if(level >= 95 and powerpots >= 1):
				if(singlefight is True):
					usecommand("load power 1", num)
				if(singlefight is False):
					usecommand("load power {0}".format(spendpower), num)
			if(level >= alignlevel):
				usecommand("align {0}".format(firstalign), num)
			if(singlefight is True):
				usecommand("fight {0}".format( ufight[0] ), num)
				fights += 1
			if(singlefight is False):
				for i in range(fightdiff):
					usecommand("fight {0}".format( ufight[0] ), num)
				fights += fightdiff
			if(level >= alignlevel):
				usecommand("align {0}".format(secondalign), num)

def aligncheck(num):
	global alignlevel
	global level
	global firstalign
	global secondalign
	global evilmode
	global setalign
	global rawmyentry
	global rawmyentry2
	global rawmyentry3
	global rawmyentry4
	global rawmyentry5
	global rawstatsmode
	global align
	
	getitems2(num)

	if evilmode is True:
		secondalign = "undead"
		alignlevel = 0
	if evilmode is False:
		secondalign = "human"
		alignlevel = setalign
	if num == 1:
		rawmyentrys = rawmyentry
	if num == 2:
		rawmyentrys = rawmyentry2
	if num == 3:
		rawmyentrys = rawmyentry3
	if num == 4:
		rawmyentrys = rawmyentry4
	if num == 5:
		rawmyentrys = rawmyentry5

	if rawstatsmode is True and rawmyentrys != None:
		if(secondalign == "human" and level >= alignlevel):
			if(rawmyentrys[19] == "g"):
				usecommand("align {0}".format(secondalign), num)
			if(rawmyentrys[19] == "e"):
				usecommand("align {0}".format(secondalign), num)

		if(secondalign == "human" and level < alignlevel):
			if(rawmyentrys[19] == "n"):
				usecommand("align {0}".format(firstalign), num)
			if(rawmyentrys[19] == "e"):
				usecommand("align {0}".format(firstalign), num)

		if(secondalign == "undead"):
			if(rawmyentrys[19] == "n"):
				usecommand("align {0}".format(secondalign), num)
			if(rawmyentrys[19] == "g"):
				usecommand("align {0}".format(secondalign), num)
	if rawstatsmode is False:
		if(secondalign == "human" and level >= alignlevel):
			if(align == "g"):
				usecommand("align {0}".format(secondalign), num)
			if(align == "e"):
				usecommand("align {0}".format(secondalign), num)
		if(secondalign == "human" and level < alignlevel):
			if(align == "n"):
				usecommand("align {0}".format(firstalign), num)
			if(align == "e"):
				usecommand("align {0}".format(firstalign), num)
		if(secondalign == "undead"):
			if(align == "n"):
				usecommand("align {0}".format(secondalign), num)
			if(align == "g"):
				usecommand("align {0}".format(secondalign), num)

def attack(userdata):
	global attackcount1

	if attackcount1 == 1:
		attackmulti(1)
	attackcount1 -= 1

def attack2(userdata):
	global attackcount2

	if attackcount2 == 1:
		attackmulti(2)
	attackcount2 -= 1

def attack3(userdata):
	global attackcount3

	if attackcount3 == 1:
		attackmulti(3)
	attackcount3 -= 1

def attack4(userdata):
	global attackcount4

	if attackcount4 == 1:
		attackmulti(4)
	attackcount4 -= 1

def attack5(userdata):
	global attackcount5

	if attackcount5 == 1:
		attackmulti(5)
	attackcount5 -= 1

def attackmulti(num):
	global level
	global alignlevel
	global firstalign
	global secondalign

	getitems2(num)
	creep = bestattack(num)
	if creep != "CreepList Error":
		if(level >= alignlevel):
			usecommand("align {0}".format(firstalign), num)
		usecommand("attack " + creep, num)
		if(level >= alignlevel):
			usecommand("align {0}".format(secondalign), num)
	if creep == "CreepList Error":
		xchat.prnt("{0}".format(creep))

def slay(userdata):
	global slaycount1

	if slaycount1 == 1:
		slaymulti(1)
	slaycount1 -= 1

def slay2(userdata):
	global slaycount2

	if slaycount2 == 1:
		slaymulti(2)
	slaycount2 -= 1

def slay3(userdata):
	global slaycount3

	if slaycount3 == 1:
		slaymulti(3)
	slaycount3 -= 1

def slay4(userdata):
	global slaycount4

	if slaycount4 == 1:
		slaymulti(4)
	slaycount4 -= 1

def slay5(userdata):
	global slaycount5

	if slaycount5 == 1:
		slaymulti(5)
	slaycount5 -= 1

def slaymulti(num):
	global level
	global alignlevel
	global firstalign
	global secondalign

	getitems2(num)
	monster = bestslay(num)
	if monster != "MonsterList Error":
		if(level >= alignlevel):
			usecommand("align {0}".format(firstalign), num)
		usecommand("slay " + monster, num)
		if(level >= alignlevel):
			usecommand("align {0}".format(secondalign), num)
	if monster == "MonsterList Error":
		xchat.prnt("{0}".format(monster))

def challenge(userdata):
	global challengecount1

	if challengecount1 == 1:
		challengemulti(1)
	challengecount1 -= 1

def challenge2(userdata):
	global challengecount2

	if challengecount2 == 1:
		challengemulti(2)
	challengecount2 -= 1

def challenge3(userdata):
	global challengecount3

	if challengecount3 == 1:
		challengemulti(3)
	challengecount3 -= 1

def challenge4(userdata):
	global challengecount4

	if challengecount4 == 1:
		challengemulti(4)
	challengecount4 -= 1

def challenge5(userdata):
	global challengecount5

	if challengecount5 == 1:
		challengemulti(5)
	challengecount5 -= 1

def challengemulti(num):
	global level
	global alignlevel
	global firstalign
	global secondalign

	getitems2(num)
	if(level >= alignlevel):
		usecommand("align {0}".format(firstalign), num)
	usecommand("challenge", num)
	if(level >= alignlevel):
		usecommand("align {0}".format(secondalign), num)

def bestattack(num):
	global creeps
	global level

	getitems2(num)
	good = "CreepList Error"
	for thing in creeps:
		if(level <= thing[1]):
			good = thing[0]
	return good

def bestslay(num):
	global monsters
	global mysum

	getitems2(num)
	good = "MonsterList Error"
	for thing in monsters:
		if(mysum <= thing[1]):
			good = thing[0]
	return good

def bestbet(num):
	global newlist
	global newlist2
	global newlist3
	global newlist4
	global newlist5
	
	if num == 1:
		newlists = newlist
	if num == 2:
		newlists = newlist2
	if num == 3:
		newlists = newlist3
	if num == 4:
		newlists = newlist4
	if num == 5:
		newlists = newlist5
	diff = 0
	bestbet = None
	if newlists != None:
		for entry in newlists:
			best = bestfight(entry[0], 1, num)
			try:
				currdiff = entry[1] / best[1]
			except ZeroDivisionError:
				currdiff = 0
			if(currdiff > diff):
				if(entry[3] >= 30 and best[3] >= 30):
					diff = currdiff
					bestbet = ( entry, best )
	return bestbet

def bestfight(name, flag, num):
	global newlist
	global newlist2
	global newlist3
	global newlist4
	global newlist5
	
	idx = None
	if num == 1:
		newlists = newlist
	if num == 2:
		newlists = newlist2
	if num == 3:
		newlists = newlist3
	if num == 4:
		newlists = newlist4
	if num == 5:
		newlists = newlist5

	length = len(newlists)
	diff = 999999
	best = ("Doctor Who?", 999999.0, 999999.0, 0, "n", 0, 0)

	for index, entry in enumerate(newlists):
		if(name == entry[0]):
			idx = index + 1
			break
	templist = newlists[idx:length]
	for entry in templist:
		if(entry[flag] < diff):
			diff = entry[flag]
			best = entry
	return best

def testfight(num):
	global newlist
	global newlist2
	global newlist3
	global newlist4
	global newlist5
	global fightSum1
	global fightSum2
	global fightSum3
	global fightSum4
	global fightSum5
	global level
	global name
	global name2
	global name3
	global name4
	global name5
	
	diff = 0
	best = ("Doctor Who?", 999999.0, 999999.0, 0, "n", 0, 0)
	
	getitems2(num)
	if num == 1:
		newlists = newlist
		fightsumlist = fightSum1
		names = name
	if num == 2:
		newlists = newlist2
		fightsumlist = fightSum2
		names = name2
	if num == 3:
		newlists = newlist3
		fightsumlist = fightSum3
		names = name3
	if num == 4:
		newlists = newlist4
		fightsumlist = fightSum4
		names = name4
	if num == 5:
		newlists = newlist5
		fightsumlist = fightSum5
		names = name5
	newlists.sort( key=operator.itemgetter(2))
	if newlists != None:
		for entry in newlists:
			if(entry[3] >= level and entry[0] != names): 
				try:
					currdiff = fightsumlist / entry[2]
				except ZeroDivisionError:
					currdiff = 0
				if(currdiff > diff):
					diff = entry[2]
					best = entry
	return best

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

def itemupgrade(num1, num):
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

	lowestitem = worstitem(num)        
	usecommand("upgrade {0} {1}".format(lowestitem[0], num1), num)
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
