#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sqlite3
from traceback import format_exc
import config
import os
import log

try:
	dbase = sqlite3.connect(os.path.join(config.path, config.dbfile))
	c = dbase.cursor()
	c.execute("create table if not exists log (udate number, hdate text, section text, body text, level text);")
	log.log("Initialized SQLite database", "db", "debug")
except:
	log.log("Failed to initialize SQLite database.\n{}".format(format_exc), "db", "critical")