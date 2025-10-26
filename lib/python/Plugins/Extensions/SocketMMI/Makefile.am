SUBDIRS = src

installdir = $(pkglibdir)/python/Plugins/Extensions/SocketMMI

plugin_LTLIBRARIES = socketmmi.la

socketmmi_la_SOURCES = src/socket_mmi.cpp
socketmmi_la_CPPFLAGS = $(PYTHON_CPPFLAGS)
socketmmi_la_LDFLAGS = -module -avoid-version
socketmmi_la_LIBADD = -lxml2 -ludfread

install_PYTHON = \
    __init__.py \
    plugin.py \
    SocketMMI.py
