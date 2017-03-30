"""
Screwing around with databases, go to terminal and type in: sqlite3 database.db < schema.sql
before running this code otherwise it won't work
also for some reason the email is getting cut off
type in terminal: sqlite3
then type in: .help
then type in: .open database.db
then type in: .read database.db
to see what has been inserted
"""

import sqlite3 as sql


def insert_account_holder(email, username, phone, password):
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute("INSERT INTO account_holder (email,username,phone,password) VALUES (?,?,?,?)", (email, username, phone, password))
        con.commit()
        con.close()


insert_account_holder('ljordan51@gmail.com', 'ljordan51', '7145107173', 'gofuckyourself')
