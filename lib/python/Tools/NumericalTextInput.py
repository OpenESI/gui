# -*- coding: UTF-8 -*-
from enigma import eTimer
from Components.Language import language

# Dict languageCode -> array of strings
MAP_SEARCH = (
	"%_0",
	" 1",
	"abc2",
	"def3",
	"ghi4",
	"jkl5",
	"mno6",
	"pqrs7",
	"tuv8",
	"wxyz9",
	)
MAP_SEARCH_UPCASE = (
	"0%_",
	"1 ",
	"ABC2",
	"DEF3",
	"GHI4",
	"JKL5",
	"MNO6",
	"PQRS7",
	"TUV8",
	"WXYZ9",
	)
MAP_DEFAULT = (
	"0,?!&@=*'+\"()$~%#",
	" 1.:;/-_",
	"abc2ABC",
	"def3DEF",
	"ghi4GHI",
	"jkl5JKL",
	"mno6MNO",
	"pqrs7PQRS",
	"tuv8TUV",
	"wxyz9WXYZ",
	)
MAP_DE = (
	"0,?!&@=*'+\"()$~%#",
	" 1.:;/-_",
	"abcä2ABCÄ",
	"def3DEF",
	"ghi4GHI",
	"jkl5JKL",
	"mnoö6MNOÖ",
	"pqrsß7PQRSß",
	"tuvü8TUVÜ",
	"wxyz9WXYZ",
	)
MAP_ES = (
	"0,¿?¡!&@=*'+\"()€$~%#",
	" 1.:;/-_",
	"abcçáà2ABCÁÀÇ",
	"deéèf3DEFÉÈ",
	"ghiíì4GHIÍÌ",
	"jkl5JKL",
	"mnñoóò6MNÑOÓÒ",
	"pqrs7PQRS",
	"tuvúùü8TUVÚÙÜ",
	"wxyz9WXYZ",
	)
MAP_SE = (
	"0,?!&@=*'+\"()$~%#",
	" 1.:;/-_",
	"abcåä2ABCÅÄ",
	"defé3DEFÉ",
	"ghi4GHI",
	"jkl5JKL",
	"mnoö6MNOÖ",
	"pqrs7PQRS",
	"tuv8TUV",
	"wxyz9WXYZ",
	)
MAP_CZ = (
	"0,?'+\"()@$!=&*%#",
	" 1.:;/-_",
	"abc2áčABCÁČ",
	"def3ďéěDEFĎÉĚ",
	"ghi4íGHIÍ",
	"jkl5JKL",
	"mno6ňóMNOŇÓ",
	"pqrs7řšPQRSŘŠ",
	"tuv8ťúůTUVŤÚŮ",
	"wxyz9ýžWXYZÝŽ",
	)
MAP_SK = (
	"0,?'+\"()@$!=&*%",
	" 1.:;/-_",
	"abc2áäčABCÁÄČ",
	"def3ďéěDEFĎÉĚ",
	"ghi4íGHIÍ",
	"jkl5ľĺJKLĽĹ",
	"mno6ňóöôMNOŇÓÖÔ",
	"pqrs7řŕšPQRSŘŔŠ",
	"tuv8ťúůüTUVŤÚŮÜ",
	"wxyz9ýžWXYZÝŽ",
	)
MAP_PL = (
	"0,?'+\"()@$!=&*%#",
	" 1.:;/-_",
	"abcąć2ABCĄĆ",
	"defę3DEFĘ",
	"ghi4GHI",
	"jklł5JKLŁ",
	"mnońó6MNOŃÓ",
	"pqrsś7PQRSŚ",
	"tuv8TUV",
	"wxyzźż9WXYZŹŻ",
	)
MAP_RU = (
	"0,?'+\"()@$!=&*%#",
	" 1.:;/-_",
	"abcабвг2ABCАБВГ",
	"defдежз3DEFДЕЖЗ",
	"ghiийкл4GHIИЙКЛ",
	"jklмноп5JKLМНОП",
	"mnoрсту6MNOРСТУ",
	"pqrsфхцч7PQRSФХЦЧ",
	"tuvшщьы8TUVШЩЬЫ",
	"wxyzъэюя9WXYZЪЭЮЯ",
	)
MAP_LV = (
	"0,?!&@=*'+\"()$~%",
	" 1.:;/-_",
	"aābcč2AĀBCČ",
	"deēf3DEĒF",
	"gģhiī4GĢHIĪ",
	"jkķlļ5JKĶLĻ",
	"mnņo6MNŅO",
	"pqrsš7PQRSŠ",
	"tuūv8TUŪV",
	"wxyzž9WXYZŽ",
	)
MAP_NL = (
	"0,?!&@=*'+\"()$~%#",
	" 1.:;/-_",
	"abc2ABC",
	"deëf3DEËF",
	"ghiï4GHIÏ",
	"jkl5JKL",
	"mno6MNO",
	"pqrs7PQRS",
	"tuv8TUV",
	"wxyz9WXYZ",
	)
MAPPINGS = {
	'de_DE': MAP_DE,
	'es_ES': MAP_ES,
	'sv_SE': MAP_SE,
	'fi_FI': MAP_SE,
	'cs_CZ': MAP_CZ,
	'sk_SK': MAP_SK,
	'pl_PL': MAP_PL,
	'ru_RU': MAP_RU,
	'lv_LV': MAP_LV,
	'nl_NL': MAP_NL,
	}

class NumericalTextInput:
	def __init__(self, nextFunc=None, handleTimeout = True, search = False, mapping = None):
		self.useableChars=None
		self.nextFunction=nextFunc
		if handleTimeout:
			self.timer = eTimer()
			self.timer.callback.append(self.timeout)
		else:
			self.timer = None
		self.lastKey = -1
		self.pos = -1
		if mapping is not None:
			self.mapping = mapping
		elif search:
			self.mapping = MAP_SEARCH
		else:
			self.mapping = MAPPINGS.get(language.getLanguage(), MAP_DEFAULT)

	def setUseableChars(self, useable):
		self.useableChars = str(useable)

	def getKey(self, num):
		cnt=0
		if self.lastKey != num:
			if self.lastKey != -1:
				self.nextChar()
			self.lastKey = num
			self.pos = -1
		if self.timer is not None:
			self.timer.start(1000, True)
		while True:
			self.pos += 1
			if len(self.mapping[num]) <= self.pos:
				self.pos = 0
			if self.useableChars:
				pos = self.useableChars.find(self.mapping[num][self.pos])
				if pos == -1:
					cnt += 1
					if cnt < len(self.mapping[num]):
						continue
					else:
						return None
			break
		return self.mapping[num][self.pos]

	def nextKey(self):
		if self.timer is not None:
			self.timer.stop()
		self.lastKey = -1

	def nextChar(self):
		self.nextKey()
		if self.nextFunction:
			self.nextFunction()

	def timeout(self):
		if self.lastKey != -1:
			self.nextChar()
