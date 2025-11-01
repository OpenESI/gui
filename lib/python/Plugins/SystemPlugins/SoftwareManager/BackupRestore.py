from datetime import date
from glob import glob
from os import access, makedirs, listdir, stat, rename, remove, F_OK, R_OK, W_OK
from os.path import exists, isdir, join

from enigma import eTimer, eEnv, eConsoleAppContainer, eEPGCache
from Components.ActionMap import ActionMap, NumberActionMap, HelpableActionMap
from Components.Button import Button
from Components.config import NoSave, configfile, ConfigSubsection, ConfigText, ConfigLocations
from Components.config import config
from Components.ConfigList import ConfigListScreen
from Components.FileList import MultiFileSelectList
from Components.Harddisk import harddiskmanager
from Components.Label import Label
from Components.MenuList import MenuList
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Components.SystemInfo import BoxInfo, getBoxDisplayName
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.RestartNetwork import RestartNetwork
from Screens.Screen import Screen
from Tools.Directories import fileWriteLines, resolveFilename, SCOPE_GUISKIN
from Tools.LoadPixmap import LoadPixmap
from . import ShellCompatibleFunctions

MACHINEBUILD = BoxInfo.getItem("machinebuild")

def eEnv_resolve_multi(path):
    resolve = eEnv.resolve(path)
    return [] if resolve == path else resolve.split()

MANDATORY_RIGHTS = ShellCompatibleFunctions.MANDATORY_RIGHTS + " ; exit 0"
BLACKLISTED = ShellCompatibleFunctions.BLACKLISTED
def InitConfig():
    BACKUPFILES = ["/etc/enigma2/", "/etc/CCcam.cfg", "/usr/keys/",
        "/etc/davfs2/", "/etc/tuxbox/config/", "/etc/auto.network", "/etc/feeds.xml", "/etc/machine-id", "/etc/rc.local",
        "/etc/openvpn/", "/etc/ipsec.conf", "/etc/ipsec.secrets", "/etc/ipsec.user", "/etc/strongswan.conf", "/etc/vtuner.conf",
        "/etc/default/crond", "/etc/dropbear/", "/etc/default/dropbear", "/home/", "/etc/samba/", "/etc/fstab", "/etc/inadyn.conf",
        "/etc/network/interfaces", "/etc/wpa_supplicant.conf", "/etc/wpa_supplicant.ath0.conf", "/etc/ciplus/", "/etc/udev/known_devices",
        "/etc/wpa_supplicant.wlan0.conf", "/etc/wpa_supplicant.wlan1.conf", "/etc/resolv.conf", "/etc/enigma2/nameserversdns.conf", "/etc/default_gw", "/etc/hostname", "/etc/hosts", "/etc/epgimport/", "/etc/exports",
        "/etc/enigmalight.conf", "/etc/enigma2/volume.xml", "/etc/enigma2/ci_auth_slot_0.bin", "/etc/enigma2/ci_auth_slot_1.bin", "/etc/PrivateKey.key",
        "/usr/lib/enigma2/python/Plugins/Extensions/VMC/DB/",
        "/usr/lib/enigma2/python/Plugins/Extensions/VMC/youtv.pwd",
        "/usr/lib/enigma2/python/Plugins/Extensions/VMC/vod.config",
        "/usr/share/enigma2/Elgato-HD-CN/skinparts/",
        "/usr/share/enigma2/display/skin_display_usr.xml",
        "/usr/share/enigma2/display/userskin.png",
        "/usr/lib/enigma2/python/Plugins/Extensions/SpecialJump/keymap_user.xml",
        "/usr/lib/enigma2/python/Plugins/Extensions/MP3Browser/db",
        "/usr/lib/enigma2/python/Plugins/Extensions/MovieBrowser/db",
        "/usr/lib/enigma2/python/Plugins/Extensions/TVSpielfilm/db", "/etc/ConfFS",
        "/etc/rc3.d/S99tuner.sh",
        "/usr/bin/enigma2_pre_start.sh",
        "/var/lib/bluetooth/",
        eEnv.resolve("${datadir}/enigma2/keymap.usr"),
        eEnv.resolve("${datadir}/enigma2/keymap_usermod.xml")]\
        + eEnv_resolve_multi("${sysconfdir}/opkg/*-secret-feed.conf")\
        + eEnv_resolve_multi("${datadir}/enigma2/*/mySkin_off")\
        + eEnv_resolve_multi("${datadir}/enigma2/*/mySkin")\
        + eEnv_resolve_multi("${datadir}/enigma2/*/skin_user_*.xml")\
        + eEnv_resolve_multi("/etc/*.emu")\
        + eEnv_resolve_multi("${sysconfdir}/cron*")\
        + eEnv_resolve_multi("${sysconfdir}/init.d/softcam*")\
        + eEnv_resolve_multi("${sysconfdir}/init.d/cardserver*")\
        + eEnv_resolve_multi("${sysconfdir}/sundtek.*")\
        + eEnv_resolve_multi("/usr/sundtek/*")\
        + eEnv_resolve_multi("/opt/bin/*")\
        + eEnv_resolve_multi("/usr/script/*")

    backupset = [f for f in BACKUPFILES if exists(f)]

    config.plugins.configurationbackup = ConfigSubsection()
    defaultlocation = "/media/hdd/"
    if MACHINEBUILD in ("maram9", "classm", "axodin", "axodinc", "starsatlx", "genius", "evo", "galaxym6") and not exists(f"/media/hdd/backup_{MACHINEBUILD}"):
        defaultlocation = "/media/backup/"
    config.plugins.configurationbackup.backuplocation = ConfigText(default=defaultlocation, visible_width=50, fixed_size=False)
    config.plugins.configurationbackup.backupdirs_default = NoSave(ConfigLocations(default=backupset))
    config.plugins.configurationbackup.backupdirs = ConfigLocations(default=[])
    config.plugins.configurationbackup.backupdirs_exclude = ConfigLocations(default=[])
    return config.plugins.configurationbackup

config.plugins.configurationbackup = InitConfig()
def getBackupPath():
    backuppath = config.plugins.configurationbackup.backuplocation.value
    return join(backuppath, f"backup_{BoxInfo.getItem('distro')}_{MACHINEBUILD}")

def getOldBackupPath():
    backuppath = config.plugins.configurationbackup.backuplocation.value
    return join(backuppath, "backup")

def getBackupFilename():
    return "enigma2settingsbackup.tar.gz"

def SettingsEntry(name, checked):
    picture = LoadPixmap(cached=True, path=resolveFilename(SCOPE_GUISKIN, f"skin_default/icons/lock_{'on' if checked else 'off'}.png"))
    return (name, picture, checked)

class RestoreScreen(ConfigListScreen, Screen):
    skin = """
        <screen position="0,0" size="0,0" title="" >
        <widget name="config" position="10,10" size="330,250" transparent="1" scrollbarMode="showOnDemand" />
        </screen>"""

    def __init__(self, session, runRestore=False):
        Screen.__init__(self, session)
        self.setTitle(_("Restoring..."))
        self.runRestore = runRestore
        self["actions"] = ActionMap(["WizardActions", "DirectionActions"],
        {
            "ok": self.close,
            "back": self.close,
            "cancel": self.close,
        }, -1)
        self.backuppath = getBackupPath()
        if not isdir(self.backuppath):
            self.backuppath = getOldBackupPath()
        self.backupfile = getBackupFilename()
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        if runRestore:
            self.callLater(self.doRestore)

    def doRestore(self):
        fullbackupfilename = join(self.backuppath, self.backupfile)
        tarcmd = f"tar -C / -xzvf {fullbackupfilename}"
        for f in BLACKLISTED:
            tarcmd += f" --exclude {f.strip('/')}"
        restorecmdlist = ["rm -R /etc/enigma2", tarcmd, MANDATORY_RIGHTS]
        if exists("/proc/stb/vmpeg/0/dst_width"):
            restorecmdlist += [
                "echo 0 > /proc/stb/vmpeg/0/dst_height",
                "echo 0 > /proc/stb/vmpeg/0/dst_left",
                "echo 0 > /proc/stb/vmpeg/0/dst_top",
                "echo 0 > /proc/stb/vmpeg/0/dst_width"
            ]
        restorecmdlist.append("/etc/init.d/autofs restart")
        self.session.openWithCallback(self.restoreFinishedCB, Console, title=self.screenTitle, cmdlist=restorecmdlist, closeOnSuccess=True, showScripts=False)

    def restoreFinishedCB(self, retval=None):
        ShellCompatibleFunctions.restoreUserDB()
        self.session.openWithCallback(self.rebootSYS, RestartNetwork)

    def rebootSYS(self, ret=None):
        try:
            with open("/tmp/rebootSYS.sh", "w") as fd:
                fd.write("#!/bin/bash\n\nkillall -9 enigma2\nreboot\n")
            self.session.open(Console, title=_("Your %s %s will Reboot...") % getBoxDisplayName(), cmdlist=["chmod +x /tmp/rebootSYS.sh", "/tmp/rebootSYS.sh"], showScripts=False)
        except Exception:
            self.session.open(Console, title=_("Restarting GUI..."), cmdlist=["killall -9 enigma2"], showScripts=False)
class installedPlugins(Screen):
    skin = """
        <screen position="center,center" size="600,100" title="Install Plugins" >
        <widget name="label" position="10,30" size="500,50" halign="center" font="Regular;20" transparent="1" foregroundColor="white" />
        </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self.setTitle(_("Install Plugins"))
        self["label"] = Label(_("Checking installed plugins..."))
        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.runFinished)
        self.container.dataAvail.append(self.dataAvail)
        self.pluginsInstalled = []
        self.remainingdata = ""
        self.container.execute("opkg list-installed | grep enigma2-plugin")

    def dataAvail(self, strData):
        if isinstance(strData, bytes):
            strData = strData.decode("UTF-8", "ignore")
        lines = strData.strip().split("\n")
        for line in lines:
            self.pluginsInstalled.append(line.split(" - ")[0])

    def runFinished(self, retval):
        self.session.openWithCallback(self.close, MessageBox, _("Plugin check complete."), timeout=5)

class RestorePlugins(Screen):
    def __init__(self, session, pluginList):
        Screen.__init__(self, session)
        self.setTitle(_("Restore Plugins"))
        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.restoreFinished)
        self.container.execute(f"opkg install {' '.join(pluginList)}")

    def restoreFinished(self, retval):
        self.session.open(MessageBox, _("Plugin restore complete."), MessageBox.TYPE_INFO, timeout=5)
        self.close()

