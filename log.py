#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import escape
from time import gmtime, strftime, time
import sqlite3
from traceback import format_exc
import config
import os

htime = strftime("%a %Y-%m-%d %H:%M:%S%z",gmtime())
utime = int(time())

def print_message(_body, _section, _level, _time=""):
		try:
			if _time:
				_time = _time + " "
			_stdmsg = "{0}{4}{1} - {2}: \"{3}\"" + escape.ansi_reset + "\n"
			if  _level == "debug": sys.stderr.write(_stdmsg.format(escape.ansi_fg_blue, _section, _level, _body, _time))
			elif  _level == "info": sys.stderr.write(_stdmsg.format(escape.ansi_fg_cyan, _section, _level, _body, _time))
			elif  _level == "warning": sys.stderr.write(_stdmsg.format(escape.ansi_fg_hiyellow, _section, _level, _body, _time))
			elif  _level == "error": sys.stderr.write(_stdmsg.format((escape.ansi_bg_black+escape.ansi_fg_red), _section, _level, _body, _time))
			elif  _level == "critical": sys.stderr.write(_stdmsg.format((escape.ansi_fg_hiyellow+escape.ansi_bg_red), _section, _level, _body, _time))
			else: sys.stderr.write(_stdmsg.format(escape.ansi_fg_hiyellow, _section, ("Nonstandard level: " + _level), _body, _time))
		except:
			log("Could not print from log", "log.print_message", "error")

def log(_body, _section="none", _level="info"):
	try:
		print_message(_body, _section, _level)
		import db
		db.c.execute("insert into log values (?, ?, ?, ?, ?)", (utime, htime, _section, _body, _level))
		db.dbase.commit()
	except:
		try:
			_log = open(os.path.join(config.path, "aux.log"), "at")
			_log.write("{}: {} - {}: \"{}\"\n".format(htime, _section, _level, _body))
			_log.write("log.log - critical: Could not log \"{}\" to \"{}\".\nTraceback:\n{}\n".format(_body, _section, format_exc()))
			_log.close()
			sys.stderr.write("{}Could not log \"{}\" from \"{}\" to SQLite log.\n{}{} -- Written to auxillary log.{}\n".format(escape.ansi_fg_red, _body, _section, format_exc(), escape.ansi_fg_yellow, escape.ansi_reset))
		except:
			sys.stderr.write("{}Could not log \"{}\" to \"{}\".\n{}\nAdditionally, the auxillary log could not be written to!{}\n".format(escape.ansi_fg_red, _body, _section, format_exc(), escape.ansi_reset))

def log_print(_format="plain"):
	try:
		if format == "csv":
			print "udate,hdate,name,data,level"
		import db
		db.c.execute("select * from log order by udate")
		for _row in db.c:
			_udate = _row[0]
			_hdate = _row[1]
			_section = _row[2]
			_body = _row[3]
			_level = _row[4]
			if _format == "csv":
				print "{},{},{},{},{}\n".format(str(_udate),_hdate,_name,_data,_level)
			else:
				print_message(_body, _section, _level, _hdate)

	except:
		log("Log could not be printed.\n{}".format(format_exc()), "log.log_print", "warning")

def log_delete():
	try:
		db.c.execute("delete from log")
		log("Log cleared", _name="clog", _level="information", _quiet=False)
	except:
		log("Log could not be cleared.\n{}".format(format_exc()), "log.log_delete", "error")