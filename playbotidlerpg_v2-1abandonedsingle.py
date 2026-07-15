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
__module_version__ = "2.1"
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

website = "https://irpg.abandoned-irc.net"
website2 = "playerview.php"
website3 = "/players.php"
russweb = "http://russellb.x10.mx/"
gitweb = "https://github.com/RussellBeech/xchat-plugins"
gitweb2 = "https://raw.githubusercontent.com/RussellBeech/xchat-plugins/master/"
rawplayers3 = None
interval = 300
newlist = None
playerlist = None 
playerspage = None
playerspagelist = None
mainhook = None
myentry = None
currentversion = __module_version__
currentversion = float( currentversion )

CONFIG_FILE_LOCATION = xchat.get_info('xchatdir')+"/.playbotidlerpgabandonedsingle"
CONFIG_FILE_LOCATION2 = xchat.get_info('xchatdir')+"/.autostartsingleA"

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

# ZNC settings
ZNC = False # ZNC Server Mode - True = On, False = Off
ZNCServer = "*******" # ZNC Server Address
ZNCPort = "+8080" # ZNC Port Number - For SSL put + before and in " " "+8080"
ZNCUser = "***/***" # ZNC Username/Network
ZNCPass = "*******" # ZNC Password

# Changeable settings
servername = "irc.abandoned-irc.net"
setbuy = 15 # level to start buying items from
goldsave = 3100 # gold kept in hand
buylife = True
blackbuyspend = True
blackbuyspend14 = True
getgems = True
fightmode = True
channame = "#zw-idlerpg"
botname = "IdleRPG"
creepattack = True # True = On, False = Off - Autocreep selection
setcreeptarget = "Werewolf" # Sets creep target. creepattack needs to be False to use
scrollssum = 3000 # item score you start buying scrolls
xpupgrade = True # Upgrade Items with XP
xpspend = 20 # Amount you use with xpget to upgrade items
bottextmode = True # True = on, False = off
errortextmode = True # True = on, False = off
intervaltext = True # True = on, False = off - Text displayed every interval
townworkswitch = True # True = Town/Work Area Switching, False = Town/Forest Area Switching, None = Area Switching Off
areasum = 6000 # Sum at which you switch to Fast Town Switching
buyluck = False
buypower = False
expbuy = False
slaysum = 1000 # minimum sum you start slaying without mana from
autostartdelay = 60 #seconds delay for autostart when you have the plugin auto loaded from startup

# declare stats as global
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
online = None
botcheck = None
webworks = None 
webworks2 = None 
gameactive = None
lottonum1 = None
lottonum2 = None
lottonum3 = None
location = None
locationtime = 0

game_chan = None
botdisable1 = False
autostartmode = False

for entry in configList:
	if(entry[0] == "autostartmode"):
		autostartmode = entry[1]
	if(entry[0] == "blackbuyspend"):
		blackbuyspend = entry[1]
	if(entry[0] == "blackbuyspend14"):
		blackbuyspend14 = entry[1]
	if(entry[0] == "bottextmode"):
		bottextmode = entry[1]
	if(entry[0] == "buylife"):
		buylife = entry[1]
	if(entry[0] == "buyluck"):
		buyluck = entry[1]
	if(entry[0] == "buypower"):
		buypower = entry[1]
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

	webversion = None
	gitversion = None
	newversion = 0
	versionfilename = "playbotversionabandoned.txt"

	try:
		if python3 is False:
			text = urllib2.urlopen(russweb + versionfilename)
		if python3 is True:
			text = urllib.request.urlopen(russweb + versionfilename)
		webversion = text.read()
		webversion = float( webversion )
		text.close()

	except:
		xchat.prnt( "Could not access {0}".format(russweb))

	try:
		context = ssl._create_unverified_context()
		if python3 is False:
			text2 = urllib2.urlopen(gitweb2 + versionfilename, context=context)
		if python3 is True:
			text2 = urllib.request.urlopen(gitweb2 + versionfilename, context=context)
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
	if webversion is None and gitversion is None:
		xchat.prnt("Both Websites have failed to read.  Try again later")
		return
	if gitversion is None and webversion != None:
		newversion = webversion
	if webversion is None and gitversion != None:
		newversion = gitversion
	if webversion != None and gitversion != None:
		if webversion > gitversion:
			newversion = webversion
		if webversion < gitversion:
			newversion = gitversion
		if webversion == gitversion:
			newversion = gitversion
		
	if newversion != None:
		if(currentversion == newversion):
			xchat.prnt("You have the current version of PlayBot")
		if(currentversion < newversion):
			xchat.prnt("You have an old version of PlayBot")
			xchat.prnt("You can download a new version from {0} or {1}".format(russweb, gitweb))
		if(currentversion > newversion):
			xchat.prnt("Give me, Give me")

def configwrite():
	global autostartmode
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
	global bottextmode
	global errortextmode
	
	configList = []
	configList.append( ( "autostartmode", autostartmode ) )
	configList.append( ( "blackbuyspend", blackbuyspend ) )
	configList.append( ( "blackbuyspend14", blackbuyspend14 ) )
	configList.append( ( "bottextmode", bottextmode ) )
	configList.append( ( "buylife", buylife ) )
	configList.append( ( "buyluck", buyluck ) )
	configList.append( ( "buypower", buypower ) )
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
	global botdisable1
	
	botcount1 = 0

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
			xchat.prnt( "Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame) )

def autostart(userdata):
	global name
	global pswd
	global netname
	global nickname
	global channame
	global gameactive
	global charcount
	global game_chan
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
		gameactive = True
		netname = xchat.get_info("network")

		if netname is None:
			netname = xchat.get_info("network")
			charcount = 0
			mainhook = xchat.hook_timer(autostartdelay * 1000, autostart)  # hook_timer requires milliseconds                       
			return

		nickname = xchat.get_info("nick")
		
		# find context
		game_chan = xchat.find_context(channel=channame)
		webdata()
		webdata2()

		if(game_chan is None):
			xchat.prnt("Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame))
			charcount = 0
			gameactive = False
			xchat.prnt("Autostart Failed")
			autostartmode = False
			configwrite()
			return

		if(name != None and pswd != None):
			loginstart()

	if charcount == 0:
		gameactive = False
		xchat.prnt("Autostart Failed")
		autostartmode = False
		configwrite()

if autostartmode is False:
	xchat.prnt( "To start PlayBot use /login CharName Password" )

def login(word, word_eol, userdata):
	global name
	global pswd
	global netname
	global nickname
	global channame
	global gameactive
	global charcount
	global game_chan
	global playerspagelist
	global webworks
	global webworks2
	
	charcount += 1

	if charcount == 1:
		gameactive = True
		netname = xchat.get_info("network")
		nickname = xchat.get_info("nick")
		namecheck = False
			
		# find context
		game_chan = xchat.find_context(channel=channame)

		if "undernet" in netname.lower():
			xchat.prnt("The #irpg game on Undernet is not supported.  Expect your head to explode if you continue")
			charcount = 0
		if "quakenet" in netname.lower():
			xchat.prnt("The game on QuakeNet is not supported.  Use the QuakeNet Plugin")
			charcount = 0

		if charcount == 1:
			if(game_chan is None):
				xchat.prnt("Can not find the Game channel.  Make sure you are in the game channel {0}".format(channame))
				charcount = 0
			try:
				if(name is None or pswd is None):
					name = word[1]
					pswd = word[2]
			except IndexError:
				xchat.prnt( "LOGIN ERROR: To log in use /login CharName Password" )

			webdata()
			webdata2()
			if(name is None or pswd is None):
				charcount = 0
				xchat.prnt("Login Failed")
		if charcount == 1:
			try:
				for entry in playerspagelist:
					if ">{0}<".format(name) in entry:
						namecheck = True
			except TypeError:
				webworks2 = False
			if(namecheck is False and webworks2 is True):
				xchat.prnt("LOGIN ERROR: {0} does not exist".format(name))
				charcount = 0

		if charcount == 0:
			gameactive = False
			name = None
			pswd = None
			return

		if charcount == 1:
			if(name != None and pswd != None):
				loginstart()
	
	if charcount >= 2:
		xchat.prnt("You can only play with 1 character")
		charcount = 1
	return xchat.EAT_ALL

# hook login command
xchat.hook_command("login", login, help="/login <charname> <password> - You can use this to login your character into the game")

def loginstart():
	global name
	global pswd

	global setbuy
	global buylife
	global fightmode
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
	global buyluck
	global buypower
	global expbuy
	global slaysum
	global bottextmode
	global errortextmode

	usecommand("login {0} {1}".format(name, pswd))
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
	if bottextmode is True:
		xchat.prnt("Bot Text Mode Activated.  To turn it off use /bottextoff")
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
	xchat.prnt("Current Scroll Buy ItemScore: {0}.  If you want to change it use /setscrolls number".format(scrollssum))
	xchat.prnt("Current SlaySum Minimum ItemScore: {0}.  If you want to change it use /setslaysum number".format(slaysum))
	xchat.prnt("Current XPSpend for xpget item upgrades: {0}.  If you want to change it use /setxpspend number".format(xpspend))
	xchat.prnt("")
	xchat.prnt("For a list of PlayBot commands use /helpplaybot")
	xchat.prnt("")
	versionchecker()

	# call main directly
	main(None)

def logoutchar(word, word_eol, userdata):
	global charcount
	global netname
	global game_chan
	global name
	global pswd
	global gameactive
	global autostartmode

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
		if autostartmode is True:
			autostartmode = False
			configwrite()
			configwrite2()
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

def areaoff(word, word_eol, userdata):
	global townworkswitch
	global gameactive

	if gameactive is True:
		townworkswitch = None
		xchat.prnt("Area Switch Mode Deactivated.  To change to Town/Work use /townwork or Town/Forest use /townforest")
		configwrite()
	if gameactive is False:
		xchat.prnt("You are not logged in")
	return xchat.EAT_ALL

xchat.hook_command("areaoff", areaoff, help="/areaoff - Turns Town/Work Switching Off")

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
	xchat.prnt("Area Switching Mode Off     - /areaoff")
	xchat.prnt("Autostart Mode Off          - /autostartoff")
	xchat.prnt("Autostart Mode On           - /autostarton")
	xchat.prnt("BlackBuy Spend Mode Off     - /blackbuyoff")
	xchat.prnt("BlackBuy Spend Mode On      - /blackbuyon")
	xchat.prnt("BlackBuy 14 Spend Mode Off  - /blackbuy14off")
	xchat.prnt("BlackBuy 14 Spend Mode On   - /blackbuy14on")
	xchat.prnt("Bot Text Mode Off           - /bottextoff")
	xchat.prnt("Bot Text Mode On            - /bottexton")
	xchat.prnt("Buy Life Mode Off           - /buylifeoff")
	xchat.prnt("Buy Life Mode On            - /buylifeon")
	xchat.prnt("Buy Luck Potion Mode Off    - /buyluckoff")
	xchat.prnt("Buy Luck Potion Mode On     - /buyluckon")
	xchat.prnt("Buy Power Potion Mode Off   - /buypoweroff")
	xchat.prnt("Buy Power Potion Mode On    - /buypoweron")
	xchat.prnt("CreepAttack Mode Off        - /creepattackoff")
	xchat.prnt("CreepAttack Mode On         - /creepattackon")
	xchat.prnt("Erase Config File           - /eraseconfig")
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
	global bottextmode
	global errortextmode
	global intervaltext
	global townworkswitch
	global goldsave
	global netname
	global expbuy
	global slaysum
	global autostartmode
	
	xchat.prnt("Playbot Settings List")
	xchat.prnt("")
	if townworkswitch is True:
		xchat.prnt("Area Switch Mode - Town/Work")
	if townworkswitch is False:
		xchat.prnt("Area Switch Mode - Town/Forest")
	if townworkswitch is None:
		xchat.prnt("Area Switch Mode - Deactivated")
	xchat.prnt("Autostart Mode - {0}".format(autostartmode))
	xchat.prnt("BlackBuy Spend Mode - {0}".format(blackbuyspend))
	xchat.prnt("BlackBuy 14 Spend Mode - {0}".format(blackbuyspend14))
	xchat.prnt("Bot Text Mode - {0}".format(bottextmode))
	xchat.prnt("Buy Life Mode - {0}".format(buylife))
	xchat.prnt("Buy Luck Potion Mode - {0}".format(buyluck))
	xchat.prnt("Buy Power Potion Mode - {0}".format(buypower))
	xchat.prnt("CreepAttack Mode - {0}".format(creepattack))
	xchat.prnt("Experience Buying Mode - {0}".format(expbuy))
	xchat.prnt("Error Text Mode - {0}".format(errortextmode))
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
	return xchat.EAT_ALL

xchat.hook_command("settings", settings, help="/settings - Gives a list of settings which you can change")

def newlister2():
	global playerlist
	global newlist
	global ability
	global webworks
	global webworks2
	global playerspagelist
	global website2

	newlist = []
	count = 0
	newlistererror = False

	if webworks is True and playerlist != None:
		for player in playerlist:
			count += 1
			if count > 3:
				player = player.split(" ")
#                                xchat.prnt("{0}".format(player))
				# extract players sum
				levelIdx = None
				abilityIdx = None
				upgradelevelIdx = None
				expertIdx1 = None
				expertIdx2 = None
				expertIdx3 = None
				onlineIdx = None
				lifeIdx = None
				
				amuletIdx = None
				bootsIdx = None
				charmIdx = None
				glovesIdx = None
				helmIdx = None
				leggingsIdx = None
				ringIdx = None
				shieldIdx = None
				tunicIdx = None
				weaponIdx = None
				sumIdx = None

				for index, entry in enumerate(player):
	#                                xchat.prnt("{0}".format(entry))
					if(entry == "level"):
					   levelIdx = index + 1
					   lifeIdx = index + 3
					if(entry == "ability"):
					   abilityIdx = index + 1

					if(entry == "upgrade"):
					   upgradelevelIdx = index + 1
					if(entry == "ExpertItem01"):
					   expertIdx1 = index + 1
					if(entry == "ExpertItem02"):
					   expertIdx2 = index + 1
					if(entry == "ExpertItem03"):
					   expertIdx3 = index + 1
					if(entry == "online"):
					   onlineIdx = index + 1

					if(entry == "item_amulet"):
					   amuletIdx = index + 1
					if(entry == "item_boots"):
					   bootsIdx = index + 1
					if(entry == "item_charm"):
					   charmIdx = index + 1
					if(entry == "item_gloves"):
					   glovesIdx = index + 1
					if(entry == "item_helm"):
					   helmIdx = index + 1
					if(entry == "item_leggings"):
					   leggingsIdx = index + 1
					if(entry == "item_ring"):
					   ringIdx = index + 1
					if(entry == "item_shield"):
					   shieldIdx = index + 1
					if(entry == "item_tunic"):
					   tunicIdx = index + 1
					if(entry == "item_weapon"):
					   weaponIdx = index + 1

				try:
					online_ = 0
					online_ = int(player[onlineIdx])
					
					if online_ == 1:
						rank_ = 0
						if webworks2 is True and playerspagelist != None:
							for entry9 in playerspagelist:
								if website2 in entry9 and ">{0}<".format(player[1]) in entry9:
									try:
										test = entry9
										test = test.split(">")
										ranktext = test[2]
										ranktext = ranktext.split("</")
										rank_ = int(ranktext[0])
									except:
										rank_ = 0
									
						level_ = int(player[levelIdx])

						amulet_ = int(player[amuletIdx])
						boots_ = int(player[bootsIdx])
						charm_ = int(player[charmIdx])
						gloves_ = int(player[glovesIdx])
						helm_ = int(player[helmIdx])
						leggings_ = int(player[leggingsIdx])
						ring_ = int(player[ringIdx])
						shield_ = int(player[shieldIdx])
						tunic_ = int(player[tunicIdx])
						weapon_ = int(player[weaponIdx])
						sum_ = amulet_ + boots_ + charm_ + gloves_ + helm_ + leggings_ + ring_ + shield_ + tunic_ + weapon_

						expert1_ = player[expertIdx1]
						expert2_ = player[expertIdx2]
						expert3_ = player[expertIdx3]
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

						ability_ = player[abilityIdx]
						upgradelevel_ = int(player[upgradelevelIdx])
						ulevelcalc = upgradelevel_ * 100
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
						life_ = float(player[lifeIdx])
						lifecalc = life_ / 100
						adjSum = math.floor((sum_ + ulevelcalc + abilityadj + expertcalcsumtotal) * lifecalc)

								# char       sum          adjSum  level   life   ability   rank
						newlist.append( ( player[1], float(sum_), adjSum, level_, life_, ability_, rank_) )

				except:
					newlistererror = True

	if newlistererror is True:
		webworks = False
		if errortextmode is True:
			xchat.prnt("Newlister Error")

	newlist.sort( key=operator.itemgetter(1), reverse=True )
	newlist.sort( key=operator.itemgetter(3) )
#	xchat.prnt("{0}".format(newlist))

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
	global myentry
	global rawplayers3
	global python3
	global website
	global errortextmode
	
	webworks = True
	weberror = False

	context = ssl._create_unverified_context()
	# get raw player data from web, parse for relevant entry
	try:
		if python3 is False:
			text = urllib2.urlopen(website + "/indexraw3.html", context=context)
		if python3 is True:
			text = urllib.request.urlopen(website + "/indexraw3.html", context=context)
		rawplayers3 = text.read()
		text.close()
		if python3 is True:
			rawplayers3 = rawplayers3.decode("UTF-8")
	except:
		weberror = True
		
	if weberror is True:
		if errortextmode is True:
			xchat.prnt( "1 Could not access {0}".format(website))
		webworks = False

	# build list for player records
	if(rawplayers3 is None):
		if errortextmode is True:
			xchat.prnt( "1 Could not access {0}, unknown error.".format(website) )
		webworks = False
	else:
		playerlist = rawplayers3.split("\n")
		playerlist = playerlist[:-1]

	# extract our player's record and make list
	if webworks is True:
		for entry in playerlist:
			if "char" in entry:
				entry = entry.split(" ")
				
				try:
					if(entry[1] == name):
						myentry = entry
				except IndexError:
					webworks = False
					xchat.prnt("myentry fail")

def webdata2():
	global webworks2
	global python3
	global playerspage
	global playerspagelist
	global website
	global website3
	global errortextmode
	
	webworks2 = True
	weberror = False

	context = ssl._create_unverified_context()
	# get raw player data from web, parse for relevant entry
	try:
		if python3 is False:
			text2 = urllib2.urlopen(website + website3, context=context)
		if python3 is True:
			text2 = urllib.request.urlopen(website + website3, context=context)
		playerspage = text2.read()
		text2.close()
		if python3 is True:
			playerspage = playerspage.decode("UTF-8")
	except:
		weberror = True
	if weberror is True:
		if errortextmode is True:
			xchat.prnt( "2 Could not access {0}".format(website))
		webworks2 = False

	if(playerspage is None):
		if errortextmode is True:
			xchat.prnt( "2 Could not access {0}, unknown error.".format(website) )
		webworks2 = False
	else:
		playerspagelist = playerspage.split("\n")
		playerspagelist = playerspagelist[:-1]

def playerarea():
	global level
	global mysum
	global location
	global locationtime
	global townworkswitch
	global areasum
       
	if townworkswitch is True:
		area = "work"
	if townworkswitch is False:
		area = "forest"
	if townworkswitch is None:
		return

#	xchat.prnt("{0} Time: {1} seconds".format(location, locationtime))

	if (level <= 25):
		mintime = (3 * 60 * 60)
	if (level > 25 and level <= 40):
		mintime = (6 * 60 * 60)
	if (level > 40 and level <= 50):
		mintime = (12 * 60 * 60)
	if (level > 50):
		mintime = (24 * 60 * 60)

	if locationtime == 0:
		usecommand("goto {0}".format(area))
		
	if(location == "In Town" and locationtime >= mintime and mysum < areasum and mysum != 0):
		usecommand("goto {0}".format(area))
	if(location == "In Town" and mysum >= areasum):
		usecommand("goto {0}".format(area))
	if(location == "At Work" and locationtime >= mintime):
		usecommand("goto town")
	if(location == "In The Forest" and locationtime >= (24 * 60 * 60)):
		usecommand("goto town")
       
def getvariables():
	global myentry
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
	global webworks
	global gameactive
	global lottonum1
	global lottonum2
	global lottonum3
	global location
	global locationtime
	global errortextmode
	global online
	
	lotto11 = 0
	lotto12 = 0
	lotto13 = 0
	lotto21 = 0
	lotto22 = 0
	lotto23 = 0
	lotto31 = 0
	lotto32 = 0
	lotto33 = 0
	worktime = 0
	towntime = 0
	foresttime = 0
	locationtime = 0
	location = None
	
	# get current system time UTC
	now = int( time.time() )

#	xchat.prnt("{0}".format(myentry))
	if webworks is True and gameactive is True and myentry != None:
		for index, var in enumerate(myentry):
			i = index + 1
			if( i >= len(myentry) ):
				break
			num = myentry[i]
			if str.isdigit(num):
				num = int( num )
			if var == "ExpertItem01":
				expert1 = num
			if var == "ExpertItem02":
				expert2 = num
			if var == "ExpertItem03":
				expert3 = num
			if var == "Foresttime":
				foresttime = num
				if foresttime > 0:
					foresttime = now - foresttime
			if var == "Special01":
				stone1 = num
			if var == "Special02":
				stone2 = num
			if var == "Special03":
				stone3 = num
			if var == "Towntime":
				towntime = num
				if towntime > 0:
					towntime = now - towntime
			if var == "Worktime":
				worktime = num
				if worktime > 0:
					worktime = now - worktime
			if var == "ability":
				ability = num
			if var == "alignment":
				align = num
			if var == "dragontm":
				try:
					stime = num - now
				except:
					stime = 0
			if var == "expcount":
				try:
					exp = num
				except:
					exp = 0
			if var == "experience":
				xp = num
			if var == "ffight":
				eatused = num
			if var == "fightcount":
				fights = num
			if var == "gems":
				gems = num
			if var == "gold":
				gold = num
			if var == "item_amulet":
				amulet = num
			if var == "item_boots":
				boots = num
			if var == "item_charm":
				charm = num
			if var == "item_gloves":
				gloves = num
			if var == "item_helm":
				helm = num
			if var == "item_leggings":
				leggings = num
			if var == "item_ring":
				ring = num
			if var == "item_shield":
				shield = num
			if var == "item_tunic":
				tunic = num
			if var == "item_weapon":
				weapon = num
			if var == "level":
				level = num
			if var == "life":
				life = num
			if var == "lotto11":
				lotto11 = num
			if var == "lotto12":
				lotto12 = num
			if var == "lotto13":
				lotto13 = num
			if var == "lotto21":
				lotto21 = num
			if var == "lotto22":
				lotto22 = num
			if var == "lotto23":
				lotto23 = num
			if var == "lotto31":
				lotto31 = num
			if var == "lotto32":
				lotto32 = num
			if var == "lotto33":
				lotto33 = num
			if var == "luck":
				luck = num
			if var == "mana":
				mana = num
			if var == "online":
				online = num
			if var == "powerpotion":
				powerpots = num
			if var == "regentm":
				try:
					atime = num - now
				except:
					atime = 0
			if var == "scrolls":
				try:
					scrolls = num
				except:
					scrolls = 0
			if var == "next":
				ttl = num
			if var == "upgrade":
				upgradelevel = num

			mysum = int(amulet + boots + charm + gloves + helm + leggings + ring + shield + tunic + weapon)
			lottonum1 = "{0} {1} and {2}".format(lotto11, lotto12, lotto13)
			lottonum2 = "{0} {1} and {2}".format(lotto21, lotto22, lotto23)
			lottonum3 = "{0} {1} and {2}".format(lotto31, lotto32, lotto33)
			
			if worktime > 0:
				location = "At Work"
				locationtime = worktime
			if towntime > 0:
				location = "In Town"
				locationtime = towntime
			if foresttime > 0:
				location = "In The Forest"
				locationtime = foresttime

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
	global webworks2
	global rank
	global online
	global playerspagelist
	global name
	global pswd
	global level
	global fights
	global gameactive
	global chanmessagecount
	global life
	global intervaltext
	global bottextmode
	global errortextmode
	global botdisable1
	global website2
	global ttl
	
	if intervaltext is True:
		xchat.prnt( "INTERVAL {0}".format(time.asctime()) )
	if chanmessage is True:
		chanmessagecount += 1

	botcheck = False
	chancheck = True
	botdisable1 = False
	intervaldisable = False
	oldttl = ttl

	if gameactive is True:
		bottester()

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
				 if errortextmode is True:
					 xchat.prnt( "Game Bot not in channel" )

	if private is True and chanmessagecount == 1:
		xchat.hook_print("Private Message", private_cb)
		xchat.hook_print("Private Message to Dialog", private_cb)
		
	if chanmessage is True and chanmessagecount == 1:
		xchat.hook_print("Channel Message", on_message)
		xchat.hook_print("Channel Msg Hilight", on_message)

	online = 0
	if botcheck is True:
		webdata()
		webdata2()
		if webworks is True:
			getvariables()

	test = []
	rank = 0
	if webworks2 is True and gameactive is True and botcheck is True:
		if online == 1:
			for entry9 in playerspagelist:
				if website2 in entry9 and ">{0}<".format(name) in entry9:
					try:
						test = entry9
						test = test.split(">")
						ranktext = test[2]
						ranktext = ranktext.split("</")
						rank = int(ranktext[0])
					except:
						rank = 0
						
	if(webworks is True and online == 0 and botcheck is True):
		if errortextmode is True:
			xchat.prnt("Player Offline")

	if gameactive is True:
		nickname = game_chan.get_info("nick")
		netname = game_chan.get_info("network")
		if game_chan.get_info("server") is None:
			if errortextmode is True:
				xchat.prnt( "Not connected!" )
			if ZNC is False:
				game_chan.command( "server {0}".format(servername) )
			if ZNC is True:
				game_chan.command( "server {0} {1}".format(ZNCServer, ZNCPort) )
			interval = 45
			hookmain()
			intervaldisable = True

		if webworks is True and online == 0 and botcheck is True:
			usecommand("login {0} {1}".format(name, pswd))
			interval = 45
			hookmain()
			intervaldisable = True

	if ((webworks is False and webworks2 is True) or (webworks is True and webworks2 is False)) and intervaldisable is False:
		interval = 60
		hookmain()
		intervaldisable = True
	if webworks is False and webworks2 is False and intervaldisable is False:
		interval = 300
		hookmain()
		intervaldisable = True
	if webworks is True and webworks2 is True and intervaldisable is False:
		intervalcalc()

	if webworks is True and online == 1 and botcheck is True:
		playerarea()
		spendmoney()
		timercheck()
		if(level >= 25 and fights >= 0 and fights < 5 and life > 0):
			if bottextmode is True:
				xchat.prnt("Fights available")
		if(level >= 25 and fights >= 0 and fights < 5 and life > 10):
			newlister2()
			fight_fight()

	if(webworks is True and botcheck is True):
		if online == 1:
			if(ttl == oldttl):
				if errortextmode is True:
					xchat.prnt("TTL Frozen")
					
	return True	# <- tells timer to repeat

def intervalcalc():
	global interval
	global level
	global fights
	global botcheck
	global online
	global life
	global fightmode
	
	interval = 5
	interval *= 60			# conv from min to sec

	if botcheck is False or online == 0:
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
	global bottextmode
			
	# make sure no times are negative
	if(atime < 0):
		atime = 0
	if(stime < 0):
		stime = 0

#        xchat.prnt("atime {0}  stime {1}  ttl {2}".format(atime, stime, ttl))
	slaydisable = False
	
	if(ttl <= interval):
		timer = (ttl+10)*1000
		if bottextmode is True:
			xchat.prnt("Set lvlup timer. Going off in {0} minutes.".format(timer // 60000))
		xchat.hook_timer(timer, lvlup)
	if(level >= 15 and atime <= interval and atime <= ttl and life > 10):
		if powerpots == 0 and gold >= 1100 and buypower is True:
			usecommand("buy power")
			gold -= 1000
			powerpots = 1

		timer = (atime+10)*1000
		if bottextmode is True:
			xchat.prnt("Set attack timer. Going off in {0} minutes.".format(timer // 60000))
		slaydisable = True

		if powerpots == 0:
			xchat.hook_timer(timer, attack)
		if powerpots == 1:
			xchat.hook_timer(timer, attackb)
			powerpots = 0

	if(level >= 30 and attackslaySum >= 1000 and stime <= interval and stime <= ttl and slaydisable is False and life > 10):
		if(mana == 0 and gold >= 1100 and attackslaySum < 6300000):
			usecommand("buy mana")
			gold -= 1000
			mana = 1
		timer = (stime+10)*1000
		if mana == 0 and attackslaySum >= slaysum:
			if bottextmode is True:
				xchat.prnt("Set slay timer. Going off in {0} minutes.".format(timer // 60000))
			xchat.hook_timer(timer, slay)
		if mana == 1:
			if bottextmode is True:
				xchat.prnt("Set slay timer. Going off in {0} minutes.".format(timer // 60000))
			mana = 0
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
		
	if(gembuy is True and level >= 15 and buyluck is True):
		if(luck == 0 and gold >= 2100):
			usecommand("buy luck")
			luck = 1
			gold -= 1000
			
	if(gembuy is True and expbuy is True and exp < 5):
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
	global bottextmode

	interval = 60
	hookmain()

	level += 1
	
	if bottextmode is True:
		xchat.prnt("{0} has reached level {1}!".format(name, level))

	if(level >= 16 and life > 10):
		if powerpots == 0 and gold >= 1100 and buypower is True:
			usecommand("buy power")
			gold -= 1000
			powerpots = 1

		if powerpots == 0:
			xchat.hook_timer(0, attack)
		if powerpots == 1:
			xchat.hook_timer(0, attackb)
			powerpots = 0

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
	global bottextmode

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
		if bottextmode is True:
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
	       
	upgradeSum1 = upgradelevel * 100
	fightSumTotal = float(itemSum + expertSum)
	lifepercent = (float(life) / 100)
	test = []
	
	diff = 0
	best = ("Doctor Who?", 9999999999.0, 9999999999.0, 0, 0, "p", 0)
	newlist.sort( key=operator.itemgetter(2))
	if newlist != None:
		for entry in newlist:
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
		
	good = "CreepList Error"
	if num2 == 1:
		multi = 1
	if num2 == 2:
		multi = 2
	for thing in creeps:
		if((attackslaySum * multi) <= thing[1]):
			good = thing[0]
	return good

def bestslay(num2):
	global monsters
	global attackslaySum
		
	good = "MonsterList Error"
	if num2 == 1:
		multi = 1
	if num2 == 2:
		multi = 2
	for thing in monsters:
		if((attackslaySum * multi) <= thing[1]):
			good = thing[0]
	return good

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

if autostartmode is True:
	autostart(None)
