from Plugins.Plugin import PluginDescriptor
from Screens.PluginBrowser import *

def ESIpanel(menuid, **kwargs):
	if menuid == "mainmenu":
		return [("Blue Panel", main, "ESIBluePanel", 11)]
	else:
		return []

def main(session, **kwargs):
	from ESIBlue import ESIBluePanel
	session.open(ESIBluePanel)

def Plugins(**kwargs):
	return [

	#// show panel in Main Menu
	PluginDescriptor(name="Blue Panel", description="Blue panel - OpenESI", where = PluginDescriptor.WHERE_MENU, fnc = ESIpanel),
	#// show panel in EXTENSIONS Menu
	PluginDescriptor(name="Blue Panel", description="Blue panel - OpenESI", where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc = main) ]
