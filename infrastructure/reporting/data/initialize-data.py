#!/usr/bin/env python3

import sqlite3

connection = sqlite3.connect('reporting.db')
c = connection.cursor()

c.execute('CREATE TABLE IF NOT EXISTS reports ([record] jsonb)')

connection.commit()
