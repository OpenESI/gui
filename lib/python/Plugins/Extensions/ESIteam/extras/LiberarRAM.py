##########################################################################
from time import *
from types import *
import sys, commands, gettext, subprocess, threading, sys, traceback, time, datetime
from os import system, remove as os_remove, rename as os_rename, popen, getcwd, chdir
##########################################################################
print ("Liberando RAM")
commands.getstatusoutput('sync ; echo 3 > /proc/sys/vm/drop_caches')
print ("RAM Liberada Correctamente")
print ("De vuelta al estado normal (no libera nada)")
