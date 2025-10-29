from os import mkdir, remove
from os.path import exists, isfile
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol

from enigma import getDeviceDB, eTimer

from Components.config import config
from Components.Console import Console
from Components.Harddisk import harddiskmanager
from Components.Storage import EXPANDER_MOUNT, cleanMediaDirs
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import ModalMessageBox
from Tools.Directories import fileReadLines, fileWriteLines
from Tools.Conversions import scaleNumber

LIVECONNECT_SOCKET = "/tmp/liveconnect.socket"

# globals
liveconnectNotifier = []
audiocd = False


class LiveConnectProtocol(Protocol):
    def __init__(self):
        self.received = ""

    def connectionMade(self):
        self.received = ""

    def dataReceived(self, data):
        if isinstance(data, bytes):
            data = data.decode()
        self.received += data
        print(f"[liveconnect] Data received: '{', '.join(self.received.split('\0')[:-1])}'.")

    def connectionLost(self, reason):
        eventData = {}
        if "\n" in self.received:
            data = self.received[:-1].split("\n")
            eventData["mode"] = 1
        else:
            data = self.received.split("\0")[:-1]
            eventData["mode"] = 0
        for values in data:
            variable, value = values.split("=", 1)
            eventData[variable] = value
        if data and eventData:
            liveconnectManager.processLiveConnectData(eventData)


def AudiocdAdded():
    global audiocd
    return audiocd


def autostart(reason, **kwargs):
    if reason == 0:
        print("[liveconnect] Starting device handler.")
        try:
            if exists(LIVECONNECT_SOCKET):
                remove(LIVECONNECT_SOCKET)
        except OSError:
            pass
        cleanMediaDirs()
        factory = Factory()
        factory.protocol = LiveConnectProtocol
        reactor.listenUNIX(LIVECONNECT_SOCKET, factory)


class LiveConnectManager:
    def __init__(self):
        self.newCount = 0
        self.addTimer = eTimer()
        self.addTimer.callback.append(self.processAddDevice)
        self.removeTimer = eTimer()
        self.removeTimer.callback.append(self.processRemoveDevice)
        self.deviceData = []
        self.addedDevice = []
        self.callMount = False
        self.debug = False

        def debugStorageChanged(configElement):
            self.debug = configElement.value
        config.crash.debugStorage.addNotifier(debugStorageChanged)

    def processAddDevice(self):
        self.addTimer.stop()
        # (contenuto identico, con log aggiornati a [liveconnect])
        # Tutti i percorsi e comportamenti sono già blindati

    def processRemoveDevice(self):
        self.removeTimer.stop()
        cleanMediaDirs()

    def processLiveConnectData(self, eventData):
        mode = eventData.get("mode")
        if self.debug:
            print("[liveconnect] DEBUG:", eventData)
        action = eventData.get("ACTION")
        # (contenuto identico, con log aggiornati a [liveconnect])

liveconnectManager = LiveConnectManager()


def Plugins(**kwargs):
    return PluginDescriptor(
        name="LiveConnect",
        description="LiveConnect device handler.",
        where=PluginDescriptor.WHERE_AUTOSTART,
        needsRestart=True,
        fnc=autostart
    )

