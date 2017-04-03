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
import sys


def insert_user(email, username, phone, password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO account_holder (email,username,phone,password) VALUES (?,?,?,?)", (email, username, phone, password))
    con.commit()
    con.close()


def return_data():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM account_holder")
    row = cur.fetchall()
    print(row)
    con.close()


def update_info(username, password):
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute('UPDATE account_holder SET password=? WHERE username=?', (password, username))
    con.commit()
    con.close()


if __name__ == '__main__':
    # insert_account_holder('ljordan51@gmail.com', 'ljordan51', '7145107173', 'gofuckyourself')
    # insert_user('segerpeter07@gmail.com', 'pseger', '5035446599', 'suckme')
    update_info(input('username: '), input('password: '))
    return_data()
