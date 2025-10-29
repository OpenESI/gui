from json import load
from os.path import exists
from urllib.request import urlopen

from enigma import eTimer

from Components.ActionMap import HelpableActionMap
from Components.config import config
from Components.Label import Label
from Components.Opkg import OpkgComponent
from Components.Pixmap import Pixmap
from Components.ScrollLabel import ScrollLabel
from Components.Slider import Slider
from Components.SystemInfo import BoxInfo, getBoxDisplayName
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Screens.MessageBox import MessageBox
from Screens.ParentalControlSetup import ProtectedScreen
from Screens.Screen import Screen, ScreenSummary
from Screens.Standby import QUIT_REBOOT, TryQuitMainloop
from Tools.Directories import SCOPE_GUISKIN, resolveFilename
from Tools.LoadPixmap import LoadPixmap
class SoftwareUpdate(Screen, ProtectedScreen):
    FEED_UNKNOWN = 0
    FEED_DISABLED = 1
    FEED_UNSTABLE = 2
    FEED_STABLE = 3

    def __init__(self, session, *args):
        Screen.__init__(self, session, enableHelp=True)
        ProtectedScreen.__init__(self)
        self.setTitle(_("OpenESI Software Update"))
        self.updateList = []
        self["list"] = List(self.updateList, enableWrapAround=True)
        self["key_red"] = StaticText(_("Cancel"))
        self["key_green"] = StaticText()
        self["key_yellow"] = StaticText()
        self["feedmessage"] = Label()
        self["package_text"] = Label(_("Updates available:"))
        self["package_count"] = Label("?")
        self["activity"] = Slider(0, 100)
        self["actions"] = HelpableActionMap(self, ["OkCancelActions", "ColorActions"], {
            "cancel": self.keyCancel,
            "red": self.keyCancel,
            "green": self.keyUpdate,
            "yellow": self.keyRefresh
        })
        self.activity = 0
        self.feedState = self.FEED_UNKNOWN
        self.updateFlag = True
        self.packageCount = 0
        self.feedOnline = False
        self.timer = eTimer()
        self.timer.callback.append(self.timeout)
        self.opkg = OpkgComponent()
        self.opkg.addCallback(self.opkgCallback)
        self.onLayoutFinish.append(self.layoutFinished)

    def timeout(self):
        if self.activity < 0:
            self.timer.stop()
            self["activity"].hide()
        else:
            self.activity += 1
            if self.activity == 100:
                self.activity = 0
            self["activity"].setValue(self.activity)
            self.timer.start(100, True)

    def layoutFinished(self):
        self.opkg.startCmd(OpkgComponent.CMD_UPDATE)
        self.timer.start(25, True)

    def opkgCallback(self, event, parameter):
        if self.updateFlag:
            if event == OpkgComponent.EVENT_UPDATED and "openesi-all" in parameter:
                self.feedOnline = True
            if event == OpkgComponent.EVENT_ERROR and self.feedOnline:
                event = OpkgComponent.EVENT_DONE
        if event == OpkgComponent.EVENT_ERROR:
            self.activity = -1
            self["feedmessage"].setText(_("Error downloading update list."))
        elif event == OpkgComponent.EVENT_DONE:
            if self.updateFlag:
                self.updateFlag = False
                self.opkg.startCmd(OpkgComponent.CMD_UPGRADE_LIST)
            else:
                self.updateList = []
                for pkg in self.opkg.getFetchedList():
                    self.updateList.append((pkg[0], pkg[1], pkg[2]))
                self.packageCount = len(self.updateList)
                self["package_count"].setText(str(self.packageCount))
                self["key_green"].setText(_("Update") if self.packageCount else "")
                self.activity = -1

    def keyCancel(self):
        if self.opkg.isRunning():
            self.opkg.stop()
        self.opkg.removeCallback(self.opkgCallback)
        self.close()

    def keyUpdate(self):
        self.opkg.removeCallback(self.opkgCallback)
        self.session.open(RunSoftwareUpdate)

    def keyRefresh(self):
        self.updateFlag = True
        self.packageCount = 0
        self["package_count"].setText("?")
        self["key_green"].setText("")
        self["feedmessage"].setText("")
        self.opkg.startCmd(OpkgComponent.CMD_UPDATE)
        self.timer.start(25, True)
class RunSoftwareUpdate(Screen):
    skin = """
    <screen name="RunSoftwareUpdate" position="center,center" size="720,435" resolution="1280,720">
        <widget name="update" position="10,10" size="700,400" font="Regular;20" halign="center" transparent="1" valign="center" />
        <widget name="activity" position="10,420" size="700,5" />
    </screen>"""

    def __init__(self, session, *args):
        Screen.__init__(self, session, enableHelp=True)
        self.setTitle(_("OpenESI Software Update"))
        self["update"] = ScrollLabel(_("Software update starting, please wait.\n\n"))
        self["activity"] = Slider(0, 100)
        self["actions"] = HelpableActionMap(self, ["OkCancelActions", "NavigationActions"], {
            "cancel": self.keyCancel,
            "ok": self.keyCancel,
            "up": self["update"].goLineUp,
            "down": self["update"].goLineDown,
            "pageUp": self["update"].goPageUp,
            "pageDown": self["update"].goPageDown,
            "top": self["update"].goTop,
            "bottom": self["update"].goBottom
        })
        self.activity = 0
        self.packageTotal = 0
        self.upgradeCount = 0
        self.timer = eTimer()
        self.timer.callback.append(self.timeout)
        self.opkg = OpkgComponent()
        self.opkg.addCallback(self.opkgCallback)
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        self.opkg.startCmd(OpkgComponent.CMD_UPGRADE_LIST)
        self.timer.start(25, True)

    def timeout(self):
        if self.activity < 0:
            self.timer.stop()
            self["activity"].hide()
        else:
            if self.packageTotal and self.upgradeCount:
                self["activity"].setValue(int(self.upgradeCount / self.packageTotal * 100))
            else:
                self.activity += 1
                if self.activity == 100:
                    self.activity = 0
                self["activity"].setValue(self.activity)
            self.timer.start(100, True)

    def opkgCallback(self, event, parameter):
        if event == OpkgComponent.EVENT_UPVERSION:
            self.upgradeCount += 1
            self["update"].appendText(f"{_('Updating')} {self.upgradeCount}/{self.packageTotal}: '{parameter}'\n")
        elif event == OpkgComponent.EVENT_DONE:
            self.activity = -1
            self["update"].appendText(f"\n{_('Update completed.')}\n")
            self["update"].appendText(f"{ngettext('%d package upgraded.', '%d packages upgraded.', self.upgradeCount) % self.upgradeCount}\n")
            self["update"].appendText(f"\n{_('Press OK to continue.')}\n")

    def keyCancel(self):
        if self.opkg.isRunning():
            self.opkg.stop()
        self.opkg.removeCallback(self.opkgCallback)
        if self.upgradeCount:
            self.session.open(TryQuitMainloop, retvalue=QUIT_REBOOT)
        else:
            self.close()
class RunSoftwareUpdateSummary(ScreenSummary):
    def __init__(self, session, parent):
        ScreenSummary.__init__(self, session, parent=parent)
        self["entry"] = StaticText()
        self["value"] = StaticText()
        self["activity"] = Slider(0, 100)
        if self.addWatcher not in self.onShow:
            self.onShow.append(self.addWatcher)
        if self.removeWatcher not in self.onHide:
            self.onHide.append(self.removeWatcher)

    def addWatcher(self):
        if self.update not in self.parent.timer.callback:
            self.parent.timer.callback.append(self.update)
        self.update()

    def removeWatcher(self):
        if self.update in self.parent.timer.callback:
            self.parent.timer.callback.remove(self.update)

    def update(self):
        self["entry"].setText(ngettext("%d package upgraded.", "%d packages upgraded.", self.parent.upgradeCount) % self.parent.upgradeCount)
        if self.parent.activity < 0:
            self["value"].setText(_("Press OK to continue."))
            self["activity"].hide()
        else:
            self["activity"].setValue(self.parent.activity)

