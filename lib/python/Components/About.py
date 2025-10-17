"""
OpenESI About Screen Information
Informazioni sistema e versione
"""

from .OpenESIVersion import OpenESIVersion
from enigma import eTimer, getEnigmaVersionString

def getOpenESIVersionString():
    """Restituisce stringa versione OpenESI"""
    return OpenESIVersion.getVersionString()

def getVersionString():
    """Compatibilità - restituisce versione Enigma2 + OpenESI"""
    enigma_version = getEnigmaVersionString()
    esi_version = OpenESIVersion.getVersionString()
    return f"{esi_version} ({enigma_version})"

def getAboutText():
    """Testo about per schermi di informazioni"""
    version_info = OpenESIVersion.getFullVersion()
    
    about_text = f"""
OpenESI {version_info['version']} {version_info['codename']}
{version_info['edition']} Edition - Build {version_info['build']}

Sistema multimediale open source basato su Enigma2
Architettura moderna con prestazioni ottimizzate

© OpenESI Project - https://github.com/OpenESI
Sviluppato per la community open source
"""
    return about_text

# Funzioni di compatibilità
about = type('about', (), {
    'getVersionString': getVersionString,
    'getAboutText': getAboutText
})()
