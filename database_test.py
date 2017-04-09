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
import bcrypt
salt = '$2b$12$oipF.pNP9t4uEUUTEExH8.'
salt = salt.encode('utf-8')


def insert_user(email, username, phone, password):
    con = sql.connect("database.db")
    cur = con.cursor()
    password = password.encode('utf-8')
    password = bcrypt.hashpw(password, salt)
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
    password = password.encode('utf-8')
    password = bcrypt.hashpw(password, salt)
    cur.execute('UPDATE account_holder SET password=? WHERE username=?', (password, username))
    con.commit()
    con.close()


def return_user(username):
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM account_holder')
    data = cur.fetchall()
    for person in data:
        if person[2] == username:
            return(person)
    con.commit()
    con.close()
    return None


def chec_password(username, password):
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM account_holder')
    data = cur.fetchall()
    state = False   # Match state, by default false
    for person in data:
        if person[2] == username:
            real_password = person[4]   # Hashed password for asociated match person
    password = password.encode('utf-8')     # Encode given password
    comp_password = bcrypt.hashpw(password, salt)
    print(comp_password)
    print(real_password)
    if real_password == comp_password:      # Compare given password and what the db says
        state = True
    con.commit()
    con.close()

    print(state)
    return state


if __name__ == '__main__':
    # insert_account_holder('ljordan51@gmail.com', 'ljordan51', '7145107173', 'gofuckyourself')
    # insert_user('segerpeter07@gmail.com', 'pseger', '5035446599', 'suckme')
    # update_info(input('username: '), input('password: '))
    return_data()
    # return_user(input('Username: '))
