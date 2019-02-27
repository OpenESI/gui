# Embedded file name: /usr/lib/enigma2/python/Plugins/SystemPlugins/PiconPathSet/__init__.py
from Components.Language import language
from os import environ as os_environ
import gettext
myPlugin = 'PiconPathSet'

def localeInit():
    os_environ['LANGUAGE'] = language.getLanguage()[:2]
    gettext.bindtextdomain(myPlugin, '/usr/lib/enigma2/python/Plugins/SystemPlugins/' + myPlugin + '/locale')


def _(txt):
    t = gettext.dgettext(myPlugin, txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t


localeInit()
language.addCallback(localeInit)