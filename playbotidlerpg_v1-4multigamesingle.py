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

#               Network                 Website                                 Server                          FightLL ChanName        BotName
gamelist = [    ["abandoned",           "http://irpg.abandoned-irc.net",        "irc.abandoned-irc.net",        True,   "#zw-idlerpg",  "IdleRPG"                      ],  \
		["dalnet",              "https://tilde.green/~hellspawn",       "irc.dal.net",                  True,   "#irpg",        "DAL-IRPG"                     ], \
		["efnet",               "http://idle.rpgsystems.org",           "irc.efnet.net",                True,   "#idlerpg",     "IdleRPG"                      ], \
		["technet",             "http://evilnet.idleirpg.site",         "irc.technet.chat",             True,   "#idlerpg",     "IdleRPG/IRC-nERDs"            ],  \
		["irc-nerds",           "http://evilnet.idleirpg.site",         "irc.irc-nerds.net",            True,   "#idlerpg",     "IdleRPG"                      ],  \
		["twistednet",          "http://idlerpg.twistednet.org",        "irc.twistednet.org",           False,  "#idlerpg",     "IdleRPG"                      ]   ]

russweb = "https://russellb.000webhostapp.com/"
playerview = None
interval = 300
newlist = None
playerlist = None 
playerspage = None
playerspagelist = None
mainhook = None
currentversion = __module_version__
currentversion = float( currentversion )

CONFIG_FILE_LOCATION = xchat.get_info('xchatdir')+"/.playbotidlerpgmultigamesingle"
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
channame = None
botname = None
servername = None
website = None
name = None
pswd = None
charcount = 0
private = True
chanmessage = True
chanmessagecount = 0
level = 0
mysum = 0
itemSum = 0
expertSum = 0
attackslaySum = 0
ufightcalc = 0
gold = 0
rank = 0

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
luck = 0
powerpots = 0
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
gems = 0
ability = None
xp = 0
life = 0
align = "n"
upgradelevel = 0
eatused = 0

nickname = None
netname = None
offline = None
botcheck = None
webworks = None 
gameactive = None
lottonum1 = None
lottonum2 = None
lottonum3 = None
location = None
locationtime = 0

game_chan = None
botdisable1 = False

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
	f = open(CONFIG_FILE_LOCATION,"wb")
	pickle.dump(configList,f)
	f.close()

def bottester():
	global game_chan
	global botname
	global botdisable1
	global netname
	
	botcount1 = 0

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

def usecommand(commanded):
	global game_chan
	global botname
	global channame
	global botdisable1
					
	bottester()
	if(botdisable1 is False):
		try:
			game_chan.command( "msg {0} {1}".format(botname, commanded) )
		except AttributeError:
			raise NameError( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame) )

xchat.prnt( "To start PlayBot use /login CharName Password" )

def login(word, word_eol, userdata):
	global name
	global pswd
	global setbuy
	global buylife
	global netname
	global nickname
	global channame
	global game_chan
	global gameactive
	global fightmode
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
	global buyluck
	global buypower
	global expbuy
	global playerspagelist
	global webworks
	global slaysum
	
	charcount += 1

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
			webdata()
		netlist = []
		if netcheck is False:
			for entry in gamelist:
				netlist.append( ( entry[0] ) )
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
				usecommand("login {0} {1}".format(name, pswd))
	
	if (charcount == 1):        
		time.sleep(3) # Needed
		usecommand("whoami")
		xchat.prnt("Player Character {0} has logged in".format(charcount))
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

		# call main directly
		main(None)
	if charcount > 1:
		xchat.prnt("You can only play with 1 character")
		charcount = 1
	return xchat.EAT_ALL

# hook login command
xchat.hook_command("login", login, help="/login <charname> <password> - You can use this to login your character into the game")

def logoutchar(word, word_eol, userdata):
	global charcount
	global netname
	global game_chan
	global name
	global pswd
	global gameactive

	if(charcount == 0):
		xchat.prnt("All Characters have already been Logged Out")
	if charcount == 1:
		xchat.prnt("Character {0} Logged Out".format(name))
		netname = None
		game_chan = None
		name = None
		pswd = None
		gameactive = False
		charcount = 0
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
	global gameactive
	
	if gameactive is True:
		ZNC = False
		xchat.prnt("ZNC Mode Deactivated.  To turn it on use /zncon")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("zncoff", zncoff, help="/zncoff - Turns ZNC off")

def zncon(word, word_eol, userdata):
	global ZNC
	global gameactive

	if gameactive is True:
		ZNC = True
		xchat.prnt("ZNC Mode Activated.  To turn if off use /zncoff")
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
	xchat.prnt("Buy Luck Potion Mode Deactivated.  To turn it on use /buyluckon")
	configwrite()
	return xchat.EAT_ALL

xchat.hook_command("buyluckoff", buyluckoff, help="/buyluckoff - Turns buying luck potion off")

def buyluckon(word, word_eol, userdata):
	global buyluck
	buyluck = True
	xchat.prnt("Buy Luck Potion Mode Activated.  To turn if off use /buyluckoff")
	configwrite()
	return xchat.EAT_ALL

xchat.hook_command("buyluckon", buyluckon, help="/buyluckon - Turns buying luck potion on")

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
	xchat.prnt("Set Scrolls Buy ItemScore   - /setscrolls number")
	xchat.prnt("Set SlaySum Min ItemScore   - /setslaysum number")
	xchat.prnt("Set XPSpend for upgrades    - /setxpspend number")
	xchat.prnt("Settings List               - /settings")
	xchat.prnt("Town/Forest Switch Mode     - /townforest")
	xchat.prnt("Town/Work Switch Mode       - /townwork")
	xchat.prnt("Version Checker             - /versioncheck")
	xchat.prnt("XPUpgrade Mode Off          - /xpupgradeoff")
	xchat.prnt("XPUpgrade Mode On           - /xpupgradeon")
	xchat.prnt("ZNC Mode Off                - /zncoff")
	xchat.prnt("ZNC Mode On                 - /zncon")
	xchat.prnt(" ")
	xchat.prnt("If you want more information about a command use /help <command> - ie /help settings")
	return xchat.EAT_ALL

xchat.hook_command("helpplaybot", helpplaybot, help="/helpplaybot - Gives a list of Playbot commands")

def settings(word, word_eol, userdata):
	global buylife
	global buyluck
	global buypower
	global setbuy
	global name
	global gameactive
	global fightmode
	global ZNC
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
		xchat.prnt("Buy Luck Potion Mode - {0}".format(buyluck))
		xchat.prnt("Buy Power Potion Mode - {0}".format(buypower))
		xchat.prnt("CreepAttack Mode - {0}".format(creepattack))
		xchat.prnt("Experience Buying Mode - {0}".format(expbuy))
		xchat.prnt("Fighting Mode - {0}".format(fightmode))
		xchat.prnt("GetGems Mode - {0}".format(getgems))
		xchat.prnt("Goldsave - {0}".format(goldsave))
		xchat.prnt("Interval Text Mode - {0}".format(intervaltext))
		xchat.prnt("Item Buy Level - {0}".format(setbuy))
		xchat.prnt("Player Character - {0}.  Network {1}".format(name, netname))
		xchat.prnt("Scrolls Buy ItemScore - {0}".format(scrollssum))
		xchat.prnt("Set Creep Target - {0}".format(setcreeptarget))
		xchat.prnt("SlaySum Minimum - {0}".format(slaysum))
		xchat.prnt("XPSpend Upgrade Amount - {0}".format(xpspend))
		xchat.prnt("XPUpgrade Mode - {0}".format(xpupgrade))
		xchat.prnt("ZNC Mode - {0}".format(ZNC))
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("settings", settings, help="/settings - Gives a list of settings which you can change")

def newlister():
	global playerspagelist
	global newlist
	global ability
	global python3
	global webworks
	global charcount
	global website
	global level
	global fightlevellimit
	global netname
	
	test = []
	test2 = []
	test3 = []
	newlist = []
	newlistererror = False

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
					test = test.split(" ")
					if testnum == 1:
						del test[0:14]
					test2.append(test)        

		if fightlevellimit is True:
			for entry in test2:
				if(int(entry[8]) >= level):
					test3.append(entry)
		if fightlevellimit is False:
			test3 = test2
		for player in test3:
			name_ = player[5]

			webworks2 = True
			weberror = False
			playerview20 = None
			playerlist20 = []

			# get raw player data from web, parse for relevant entry
			try:
				if "dalnet" in netname.lower():
					context = ssl._create_unverified_context()
					if python3 is False:
						text = urllib2.urlopen(website + "/playerview.php?player={0}".format(name_), context=context)
					if python3 is True:
						text = urllib.request.urlopen(website + "/playerview.php?player={0}".format(name_), context=context)
				else:
					if python3 is False:
						text = urllib2.urlopen(website + "/playerview.php?player={0}".format(name_))
					if python3 is True:
						text = urllib.request.urlopen(website + "/playerview.php?player={0}".format(name_))
				playerview20 = text.read()
				text.close()
				if python3 is True:
					playerview20 = playerview20.decode("UTF-8")
			except:
				weberror = True
			if weberror is True:
				xchat.prnt( "Could not access {0}".format(website))
				webworks2 = False

			# build list for player records
			if(playerview20 is None):
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
			lucktext_ = None

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
					if "Luck Potion:" in entry:
						lucktext = entry
					
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
					
							# name       sum   adjsum       level   life   ability   rank 
					newlist.append( ( player[5], sum_, int(adjSum), level_, life_, ability_, rank_ ) )
				except:
					newlistererror = True

	if newlistererror is True:
		webworks = False
		xchat.prnt("Newlister Error")

	newlist.sort( key=operator.itemgetter(1), reverse=True )
	newlist.sort( key=operator.itemgetter(3) )
	
def status(word, word_eol, userdata):
	global name
	global gameactive       
	global level
	global ttl
	global atime
	global stime
	global location
	global locationtime

	global powerpots
	global fights
	global gold
	global gems
	global xp
	global mana
	global luck
	global upgradelevel
	global expertSum
	global itemSum
	global attackslaySum
	global life
	global exp
	global scrolls
	global rank
	global lottonum1
	global lottonum2
	global lottonum3
	global align
	global eatused

	if gameactive is True:
		xchat.prnt("{0}'s Status".format(name))
		xchat.prnt(" ")
		xchat.prnt("Rank: {0}".format(rank))
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
		xchat.prnt("Power Potions: {0}".format(powerpots))
		xchat.prnt("Luck Potion: {0}".format(luck))
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
		xchat.prnt("Eat Used: {0} of 200".format(eatused))
		xchat.prnt("Upgrade Level: {0}".format(upgradelevel))
		xchat.prnt("Items Sum Score: {0}".format(itemSum))
		xchat.prnt("Expert Items Score: {0}".format(expertSum))
		xchat.prnt("Attack/SlaySum Item Score: {0}".format(int(attackslaySum)))
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("status", status, help="/status - Gives a list of character stats")

def items(word, word_eol, userdata):
	global name
	global gameactive
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
	global stone1
	global stone2
	global stone3
	global expert1
	global expert2
	global expert3
	global expertitem1
	global expertitem2
	global expertitem3

	if gameactive is True:
		xchat.prnt("{0}'s Items List".format(name))
		xchat.prnt(" ")
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
		xchat.prnt("Items Sum Score: {0}".format(itemSum))
		xchat.prnt("Expert Items 1: {0} {1}  2: {2} {3}  3: {4} {5}".format(expert1, expertitem1, expert2, expertitem2, expert3, expertitem3))
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("items", items, help="/items - Gives a list of character item scores")

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
	global botname
	global netname
	global nickname
	global life
	global level
	global buylife
	global gameactive
	
	if gameactive is True:
		checknet = xchat.get_info("network")
		checknick = xchat.get_info("nick")
		if chanmessage is True:
			chanmessage = False
		    
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
					usecommand("buy life")
					life = 100

def private_cb(word, word_eol, userdata):
	global botname
	global netname
	global nickname
	global game_chan
	global name
	global pswd
	global private

	global interval
	global gameactive
	
	if gameactive is True:
		checknet = xchat.get_info("network")
		checknick = xchat.get_info("nick")
		nickname = game_chan.get_info("nick")
		if private is True:
			private = False

		if(word[0] == botname and "You are not logged in." in word[1]):                
			if(checknet == netname and checknick == nickname):
				usecommand("login {0} {1}".format(name, pswd))
				interval = 60
				hookmain()

def webdata():
	global playerlist
	global name
	global webworks
	global playerview
	global python3
	global playerspage
	global playerspagelist
	global website
	global netname
	
	webworks = True
	weberror = False

	# get raw player data from web, parse for relevant entry
	try:
		context = ssl._create_unverified_context()
		if "dalnet" in netname.lower():
			if python3 is False:
				text = urllib2.urlopen(website + "/playerview.php?player={0}".format(name), context=context)
			if python3 is True:
				text = urllib.request.urlopen(website + "/playerview.php?player={0}".format(name), context=context)
		else:
			if python3 is False:
				text = urllib2.urlopen(website + "/playerview.php?player={0}".format(name))
			if python3 is True:
				text = urllib.request.urlopen(website + "/playerview.php?player={0}".format(name))
		playerview = text.read()
		text.close()
		if python3 is True:
			playerview = playerview.decode("UTF-8")
		if "dalnet" in netname.lower():
			if python3 is False:
				text2 = urllib2.urlopen(website + "/players.php", context=context)
			if python3 is True:
				text2 = urllib.request.urlopen(website + "/players.php", context=context)
		else:
			if python3 is False:
				text2 = urllib2.urlopen(website + "/players.php")
			if python3 is True:
				text2 = urllib.request.urlopen(website + "/players.php")
		playerspage = text2.read()
		text2.close()
		if python3 is True:
			playerspage = playerspage.decode("UTF-8")
	except:
		weberror = True
	if weberror is True:
		xchat.prnt( "Could not access {0}".format(website))
		webworks = False

	# build list for player records
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

def playerarea():
	global playerlist
	global level
	global mysum
	global webworks
	global location
	global locationtime
	global townworkswitch
       
	playeris = None

	atwork = False
	intown = False
	intheforest = False
	worktext = None
	towntext = None
	foresttext = None        
	location = None
	locationtime = 0

	if webworks is True:
		for entry in playerlist:
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
			locationtime = timetosecs(workdays, worksplittime)
			location = "At Work"
		except ValueError:
			usecommand("goto town")
	if intown is True:
		try:
			towntext = towntext.split(" ")
			towndays = int(towntext[8])
			townsplittime = towntext[10]
			townsplittime = townsplittime.strip("<br")
			locationtime = timetosecs(towndays, townsplittime)
			location = "In Town"
		except ValueError:
			usecommand("goto work")
	if intheforest is True:
		try:
			foresttext = foresttext.split(" ")
			forestdays = int(foresttext[8])
			forestsplittime = foresttext[10]
			forestsplittime = forestsplittime.strip("<br")
			locationtime = timetosecs(forestdays, forestsplittime)
			location = "In The Forest"
		except ValueError:
			usecommand("goto town")
		
#        xchat.prnt("{0} Time: {1} seconds".format(location, locationtime))

	if (level <= 25):
		mintime = (3 * 60 * 60)
	if (level > 25 and level <= 40):
		mintime = (6 * 60 * 60)
	if (level > 40 and level <= 50):
		mintime = (12 * 60 * 60)
	if (level > 50):
		mintime = (24 * 60 * 60)

	if(intown is True and locationtime >= mintime and mysum < 6000 and mysum != 0):
		usecommand("goto {0}".format(area))
	if(intown is True and mysum >= 6000):
		usecommand("goto {0}".format(area))
	if(atwork is True and locationtime >= mintime):
		usecommand("goto town")
	if(intheforest is True and locationtime >= (24 * 60 * 60)):
		usecommand("goto town")
       
def getvariables():
	global level
	global ttl

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
	global expert1
	global expert2
	global expert3

	global atime
	global stime
	global playerlist
	global webworks
	global gameactive
	global lottonum1
	global lottonum2
	global lottonum3
	
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

	if webworks is True and gameactive is True and playerlist != None:
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
			lottonum1 = "{0} {1} and {2}".format(lottonumtext1[11], lottonumtext1[12], lottonumtext1[13])                        
			lottonum2 = "{0} {1} and {2}".format(lottonumtext2[11], lottonumtext2[12], lottonumtext2[13])                        
			lottonum3 = "{0} {1} and {2}".format(lottonumtext3[11], lottonumtext3[12], lottonumtext3[13])                        
		except:
			webworks = False
			xchat.prnt("Variable Error")

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
	global servername
	global game_chan
	global private
	global chanmessage
	global ZNC
	global ZNCServer
	global ZNCPort
	global ZNCUser
	global ZNCPass
	global botcheck
	global interval
	global webworks
	global rank
	global offline
	global playerspagelist
	global name
	global pswd
	global level
	global fights
	global gameactive
	global chanmessagecount
	global life
	global intervaltext
	
	if intervaltext is True:
		xchat.prnt( "INTERVAL {0}".format(time.asctime()) )
	if chanmessage is True:
		chanmessagecount += 1

	botcheck = False
	chancheck = True
	intervaldisable = False

	if gameactive is True:
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
				 xchat.prnt( "Game Bot not in channel" )

	if private is True and chanmessagecount == 1:
		xchat.hook_print("Private Message", private_cb)
		xchat.hook_print("Private Message to Dialog", private_cb)
		
	if chanmessage is True and chanmessagecount == 1:
		xchat.hook_print("Channel Message", on_message)
		xchat.hook_print("Channel Msg Hilight", on_message)

	if botcheck is True:
		webdata()
		if webworks is True:
			getvariables()

	test = []
	offline = False
	rank = 0
	if webworks is True and gameactive is True and botcheck is True:
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
	if(webworks is True and offline is True):
		xchat.prnt("Player Offline")

	if gameactive is True:
		nickname = game_chan.get_info("nick")
		netname = game_chan.get_info("network")
		if game_chan.get_info("server") is None:
			xchat.prnt( "Not connected!" )
			if ZNC is False:
				game_chan.command( "server {0}".format(servername) )
			if ZNC is True:
				game_chan.command( "server {0} {1}".format(ZNCServer, ZNCPort) )
			interval = 45
			hookmain()
			intervaldisable = True

		if webworks is True and offline is True and botcheck is True:
			usecommand("login {0} {1}".format(name, pswd))
			interval = 45
			hookmain()
			intervaldisable = True

	if (webworks is True and intervaldisable is False):
		intervalcalc()
	if webworks is False:
		interval = 300
		hookmain()

	if webworks is True and offline is False and botcheck is True:
		playerarea()
		spendmoney()
		timercheck()
		if(level >= 25 and fights >= 0 and fights < 5 and life > 0):
			xchat.prnt("Fights available")
		if(level >= 25 and fights >= 0 and fights < 5 and life > 10):
			newlister()
			fight_fight()

	return True	# <- tells timer to repeat

def intervalcalc():
	global interval
	global level
	global fights
	global botcheck
	global offline
	global life
	global fightmode
	
	interval = 5
	interval *= 60			# conv from min to sec

	if botcheck is False or offline is True:
		interval = 60
	if botcheck is True:
		if(level >= 25 and life > 10 and fightmode is True):
			if(fights >= 0 and fights < 5):
				interval = 120

	hookmain()
	
def timercheck():
	global ttl
	global interval
	global atime
	global stime
	global level
	global attackslaySum
	global mana
	global powerpots
	global gold
	global life
	global buypower
	global slaysum
			
	# make sure no times are negative
	if(atime < 0):
		atime = 0
	if(stime < 0):
		stime = 0

#        xchat.prnt("atime {0}  stime {1}  ttl {2}".format(atime, stime, ttl))
	slaydisable = False
	
	if(ttl <= interval):
		timer = (ttl+10)*1000
		xchat.prnt("Set lvlup timer. Going off in {0} minutes.".format(timer // 60000))
		xchat.hook_timer(timer, lvlup)
	if(level >= 15 and atime <= interval and atime <= ttl and life > 10):
		if powerpots == 0 and gold >= 1100 and buypower is True:
			usecommand("buy power")
			gold -= 1000
			powerpots = 1

		timer = (atime+10)*1000
		xchat.prnt("Set attack timer. Going off in {0} minutes.".format(timer // 60000))
		slaydisable = True

		if powerpots == 0:
			xchat.hook_timer(timer, attack)
		if powerpots == 1:
			xchat.hook_timer(timer, attackb)

	if(level >= 30 and attackslaySum >= 1000 and stime <= interval and stime <= ttl and slaydisable is False and life > 10):
		if(mana == 0 and gold >= 1100 and attackslaySum < 6300000):
			usecommand("buy mana")
			gold -= 1000
			mana = 1
		timer = (stime+10)*1000
		if mana == 0 and attackslaySum >= slaysum:
			xchat.prnt("Set slay timer. Going off in {0} minutes.".format(timer // 60000))
			xchat.hook_timer(timer, slay)
		if mana == 1:
			xchat.prnt("Set slay timer. Going off in {0} minutes.".format(timer // 60000))
			xchat.hook_timer(timer, slayb)
	
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
	
def spendmoney():
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
	global expertitem1
	global expertitem2
	global expertitem3
	global align
	global mysum
	global blackbuyspend
	global blackbuyspend14
	global interval
	global scrolls
	global exp
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
	       
	lowestitem = worstitem()
#        xchat.prnt("Worst item {0}".format(lowestitem))

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
		usecommand("buy life")
		gold -= lifebuy
		life = 100
		
	if(level >= 15 and buyluck is True):
		if(luck == 0 and gold >= 2100):
			usecommand("buy luck")
			luck = 1
			gold -= 1000
			
	if(expbuy is True and exp < 5):
		expdiff = 5 - exp
		expcost = expdiff * 1000
		if(gold >= (expcost + 1100)):
			for i in range(expdiff):
				usecommand("buy exp")
				gold -= 1000
				exp += 1
		elif(gold >= 1000 + 1100):
			golddiff = gold - 1100
			expcalc = golddiff // 1000
			if expcalc >= 1:
				for i in range(expcalc):
					usecommand("buy exp")
					gold -= 1000
					exp += 1
		
	gembuy = True
	if(level >= 35):
		if upgradelevel == 0 and gold < 600:
			gembuy = False
		if upgradelevel == 0 and gold >= 600:
			usecommand("buy upgrade")
			gold -= 500
			upgradelevel = 1
	if(level >= 40):
		if upgradelevel == 1 and gold < 1100:
			gembuy = False
		if upgradelevel == 1 and gold >= 1100:
			usecommand("buy upgrade")
			gold -= 1000
			upgradelevel = 2
	if(level >= 45):
		if upgradelevel == 2 and gold < 2100:
			gembuy = False
		if upgradelevel == 2 and gold >= 2100:
			usecommand("buy upgrade")
			gold -= 2000
			upgradelevel = 3
	if(level >= 50):
		if upgradelevel == 3 and gold < 4100:
			gembuy = False
		if upgradelevel == 3 and gold >= 4100:
			usecommand("buy upgrade")
			gold -= 4000
			upgradelevel = 4
	if(level >= 60):
		if upgradelevel == 4 and gold < 8100:
			gembuy = False
		if upgradelevel == 4 and gold >= 8100:
			usecommand("buy upgrade")
			gold -= 8000
			upgradelevel = 5
		
#        xchat.prnt("goldsave: {0}  gembuy: {1}  level: {2}  upgradelevel: {3}  align: {4}".format(goldsave, gembuy, level, upgradelevel, align))
	
	if(level >= setbuy):
		buycost = level * 2 * 3
		buyitem = level * 2     
		buydiff = 19
		if(gold > buycost + 100):
			if(amulet < (buyitem - buydiff)):
				usecommand("buy amulet {0}".format(buyitem))
				gold -= buycost
				amulet = buyitem
		if(gold > buycost + 100):
			if(boots < (buyitem - buydiff)):
				usecommand("buy boots {0}".format(buyitem))
				gold -= buycost
				boots = buyitem
		if(gold > buycost + 100):
			if(charm < (buyitem - buydiff)):
				usecommand("buy charm {0}".format(buyitem))
				gold -= buycost
				charm = buyitem
		if(gold > buycost + 100):
			if(gloves < (buyitem - buydiff)):
				usecommand("buy gloves {0}".format(buyitem))
				gold -= buycost
				gloves = buyitem
		if(gold > buycost + 100):
			if(helm < (buyitem - buydiff)):
				usecommand("buy helm {0}".format(buyitem))
				gold -= buycost
				helm = buyitem
		if(gold > buycost + 100):
			if(leggings < (buyitem - buydiff)):
				usecommand("buy leggings {0}".format(buyitem))
				gold -= buycost
				leggings = buyitem
		if(gold > buycost + 100):
			if(ring < (buyitem - buydiff)):
				usecommand("buy ring {0}".format(buyitem))
				gold -= buycost
				ring = buyitem
		if(gold > buycost + 100):
			if(shield < (buyitem - buydiff)):
				usecommand("buy shield {0}".format(buyitem))
				gold -= buycost
				shield = buyitem
		if(gold > buycost + 100):
			if(tunic < (buyitem - buydiff)):
				usecommand("buy tunic {0}".format(buyitem))
				gold -= buycost
				tunic = buyitem
		if(gold > buycost + 100):
			if(weapon < (buyitem - buydiff)):
				usecommand("buy weapon {0}".format(buyitem))
				gold -= buycost
				weapon = buyitem

	if(level >= 25):
		if(gems < 15):
			if getgems is True and gembuy is True:
				gemdiff = 15 - gems
				gemcost = gemdiff * 150
				if gold > (goldsave + gemcost):
					usecommand("get {0} gems".format(gemdiff))
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
					usecommand("get {0} gems".format(gemdiff))
					gold -= gemcost
					gems += gemdiff
				
				moneycalc = gold - goldsave
				gemcalc = moneycalc // 150
				if(gemcalc >= 15):
					gems15 = gemcalc // 15
					if(gems15 >= 1):
						buymoney = gems15 * 150 * 15
						buygems = gems15 * 15
						usecommand("get {0} gems".format(buygems))
						gold -= buymoney
						gems += buygems

			blackbuydisable = False
			if(blackbuyspend14 is True):
				if(gems >= (15 * 14)):
					usecommand("blackbuy {0} 14".format(lowestitem[0]))
					gems -= (15 * 14) 
					if(gems >= 15):
						interval = 120
						hookmain()
						blackbuydisable = True

			if(blackbuyspend is True and blackbuydisable is False):
				if(gems >= 15):
					gemspend15 = gems // 15
					if(gemspend15 >= 1):
						usecommand("blackbuy {0} {1}".format(lowestitem[0], gemspend15))
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
					usecommand("xpget scroll")
					xp -= 20
					scrolls += 1
			elif(xp >= 20):
				xpcalc = xp // 20
				if xpcalc >= 1:
					for i in range(xpcalc):
						usecommand("xpget scroll")
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
					usecommand("xpget {0} {1}".format(lowestitem[0], xpspend))
					xp -= xpspend
       
	expertitem1 = expertcalc(expert1)
	expertitem2 = expertcalc(expert2)
	expertitem3 = expertcalc(expert3)
	   
	lifepercent = (float(life) / 100)
	itemSum = (amulet + charm + helm + boots + gloves + ring + leggings + shield + tunic + weapon)
	expertSum = expertitem1 + expertitem2 + expertitem3 
	upgradeSum1 = upgradelevel * 100
	attackslaySum = (itemSum + expertSum + upgradeSum1) * lifepercent

def lvlup(userdata):
	global name
	global level
	global interval
	global gold
	global powerpots
	global life
	global buypower

	level += 1
	
	xchat.prnt("{0} has reached level {1}!".format(name, level))

	interval = 60
	hookmain()

	if(level >= 16 and life > 10):
		if powerpots == 0 and gold >= 1100 and buypower is True:
			usecommand("buy power")
			gold -= 1000
			powerpots = 1

		if powerpots == 0:
			xchat.hook_timer(0, attack)
		if powerpots == 1:
			xchat.hook_timer(0, attackb)

def fight_fight():
	global name
	global level
	global ufightcalc
	global itemSum
	global expertSum
	global fights
	global rank
	global ability
	global upgradelevel
	global life
	global fightmode

	ufight = testfight()       

	upgradeSum1 = upgradelevel * 100
	fightSumTotal = itemSum + expertSum
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
	
	ufightcalc = fightAdj / ufight[2]

	if(level >= 25):
		xchat.prnt("Best fight for Rank {0}:  {1}  [{2}]  Opponent: Rank {3}:  {4}  [{5}], Odds {6}".format(rank, name, int(fightAdj), ufight[6], ufight[0], int(ufight[2]), ufightcalc))
		if(ufightcalc >= 0.9 and fightmode is True):
			usecommand("fight {0}".format( ufight[0] ))
			fights += 1

def testfight():
	global newlist
	global level
	global name
	global upgradelevel
	global itemSum
	global expertSum
	global ability
	global life
	global fightlevellimit
	       
	upgradeSum1 = upgradelevel * 100
	fightSumTotal = float(itemSum + expertSum)
	lifepercent = (float(life) / 100)
	test = []
	
	diff = 0
	best = ("Doctor Who?", 9999999999.0, 9999999999.0, 0, 0, "p", 0)
	newlist.sort( key=operator.itemgetter(2))
	if newlist != None:
		for entry in newlist:
			if fightlevellimit is True:
				if(entry[3] >= level and entry[0] != name):
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

			if fightlevellimit is False:
				if(entry[0] != name):
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

def attackb(userdata):
	attackmulti(2)

def attackmulti(num2):
	global creepattack
	global setcreeptarget

	if creepattack is True:
		creep = bestattack(num2)
		if creep != "CreepList Error":
			usecommand("attack " + creep)
		if creep == "CreepList Error":
			xchat.prnt("{0}".format(creep))
	if creepattack is False:
		usecommand("attack " + setcreeptarget)

def slay(userdata):
	slaymulti(1)

def slayb(userdata):
	slaymulti(2)

def slaymulti(num2):
	monster = bestslay(num2)
	if monster != "MonsterList Error":
		usecommand("slay " + monster)
	if monster == "MonsterList Error":
		xchat.prnt("{0}".format(monster))

def bestattack(num2):
	global creeps
	global attackslaySum
		
	good = creeps
	if num2 == 1:
		multi = 1
	if num2 == 2:
		multi = 2
	for thing in creeps:
		if((attackslaySum * multi) <= thing[1]):
			good = thing
	return good[0]

def bestslay(num2):
	global monsters
	global attackslaySum
		
	good = monsters
	if num2 == 1:
		multi = 1
	if num2 == 2:
		multi = 2
	for thing in monsters:
		if((attackslaySum * multi) <= thing[1]):
			good = thing
	return good[0]

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
