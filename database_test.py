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
import bcrypt   # INCLUDE INSTALL DEPENDENCY
import time
import random
import string
salt = '$2b$12$oipF.pNP9t4uEUUTEExH8.'  # Global salt used to hash passwords and comparisons
salt = salt.encode('utf-8')


# Drinks Data --------------->

def update_drink(drink):
    """
    This function takes a drink and decrements the amount of drink based off the type.
    Drink quantity is in Liters with 2L being the maximum amount.
    Assumes each drink has one 1.5 oz shot of alcohol and the alcohol to mixer ratio
    is 1:3.
    """
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM drinks_data')
    data = cur.fetchall()
    amount = 0
    for category in data:
        if category[0] == drink:
            active_drink = category[0]
            amount = category[1]
            if active_drink == 'coke' or 'sprite' or 'tonic' or 'orange' or 'ginger':
                amount = amount - 3.5**0.0295735  # oz/drink * L/oz to get L/drink, alc:mixer ratio is 1:3
            elif active_drink == 'vodka' or 'rum' or 'gin' or 'tequila':
                amount = amount - 1.5*0.0295735  # oz/shot * L/oz to get L/shot, each mixed drink has one 1.5oz shot of alcohol
    cur.execute('UPDATE drinks_data SET amount=? WHERE drink=?', (amount, drink))
    con.commit()
    con.close()


def get_drink_count(drink):
    """
    This function takes a drink and returns the amount of that drink that is left
    """
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM drinks_data')
    data = cur.fetchall()
    for choice in data:
        if choice[0] == drink:
            return choice[1]


def return_drink_data():
    """
    This function returns all drink inventory data.
    """
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM drinks_data')
    data = cur.fetchall()
    return data

# --------------------------->


def sync_user(username, barcode):
    """
    This function takes a username and barcode readin from a reader
    and syncs the corresponding user account with the barcode.
    """
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM account_holder')
    data = cur.fetchall()
    for person in data:
        if person[2] == username:
            person_barcode = barcode
    cur.execute('UPDATE account_holder SET barcode=? WHERE username=?', (person_barcode, username))
    con.commit()
    con.close()


def insert_user(email, username, phone, password, height, weight, age, gender):
    """
    This function creates a new username with attributes:
    -email
    -username
    -phone number
    -password
    based off of the information gathered from the sign up sheet
    """
    con = sql.connect("database.db")
    cur = con.cursor()
    password = password.encode('utf-8')
    password = bcrypt.hashpw(password, salt)
    cur.execute("INSERT INTO account_holder (email,username,phone,password,drinks,barcode,height,weight,age,gender) VALUES (?,?,?,?,?,?,?,?,?,?)", (email, username, phone, password, 0, '', height, weight, age, gender))
    con.commit()
    inst_barcode()
    con.close()


def inst_barcode():
    """

    """
    con = sql.connect("database.db")
    cur = con.cursor()
    barcode_val = 'TEMP'
    cur.execute("INSERT INTO time_drinks (barcode) VALUES ('TEMP')")
    con.commit()
    con.close()


def increase_drink_count(barcode):
    """
    This function increases the drinks count for a user based off their
    linked barcode identity
    """
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM account_holder')
    data = cur.fetchall()
    drinks = 0
    for category in data:
        if category[6] == barcode:
            drinks = category[5] + 1
    cur.execute('UPDATE account_holder SET drinks=? WHERE barcode=?', (drinks, barcode))
    con.commit()
    con.close()


def return_data():
    """
    Returns all the data in the account_holder table
    """
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM account_holder")
    row = cur.fetchall()
    return row
    con.close()


def get_party_start():
    """
    Returns the party start time.
    """
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM party_global_data")
    data = cur.fetchall()
    return data[0][0]
    con.close()


def update_password(username, password):
    """
    This function updates a username with a new password and sets them in the database
    """
    con = sql.connect('database.db')
    cur = con.cursor()
    password = password.encode('utf-8')
    password = bcrypt.hashpw(password, salt)
    cur.execute('UPDATE account_holder SET password=? WHERE username=?', (password, username))
    con.commit()
    con.close()


def update_settings(email, username, phone, height, weight, age, gender):
    """
    This function updates the users' settings
    """
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute('UPDATE account_holder SET email=? WHERE username=?', (email, username))
    con.commit()
    cur.execute('UPDATE account_holder SET phone=? WHERE username=?', (phone, username))
    con.commit()
    cur.execute('UPDATE account_holder SET height=? WHERE username=?', (height, username))
    con.commit()
    cur.execute('UPDATE account_holder SET weight=? WHERE username=?', (weight, username))
    con.commit()
    cur.execute('UPDATE account_holder SET age=? WHERE username=?', (age, username))
    con.commit()
    cur.execute('UPDATE account_holder SET gender=? WHERE username=?', (gender, username))
    con.commit()
    con.close()


def return_user(username):
    """
    This function takes a username and returns all the information about them including:
    -id
    -email
    -username
    -phone
    -password
    -number of drinks
    -barcode identifier
    -height
    -weight
    -age
    -gender
    """
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


def check_password(username, password):
    """
    This function takes a username and the entered password and checks to see if
    the password is correct. It does this by using the global salt and hashing
    the given password and checking to see if this hashed phrase is the same
    as what is in the database.
    """
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


def write_drink_timestamp(barcode):
    """
    This function increases the drinks count for a user based off their
    linked barcode identity
    """
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM time_drinks')
    data = cur.fetchall()
    for category in data:
        if category[0] == barcode:
            ts = time.time()
            #st = time.strftime("%Y%M%D%H%M%S", time.gmtime(time.time()))
            st = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
            newtime = ts
    cur.execute("ALTER TABLE time_drinks ADD COLUMN " + st + " INTEGER")
    cur.execute('UPDATE time_drinks SET ' + st + ' =? WHERE barcode=?', (newtime, barcode))
    con.commit()
    con.close()


tablesToIgnore = ["sqlite_sequence"]

outputFilename = None


def Print(msg):
    if (outputFilename!=None):
        outputFile = open(outputFilename, 'a')
        print >> outputFile, msg
        outputFile.close()
    else:
        print(msg)


def Describe(dbFile):
    connection = sql.connect(dbFile)
    cursor = connection.cursor()


    totalTables = 0
    totalColumns = 0
    totalRows = 0
    totalCells = 0
    # Get List of Tables:
    tableListQuery = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name"
    cursor.execute(tableListQuery)
    tables = map(lambda t: t[0], cursor.fetchall())
    for table in tables:
        if (table in tablesToIgnore):
            continue

        columnsQuery = "PRAGMA table_info(%s)" % table
        cursor.execute(columnsQuery)
        numberOfColumns = len(cursor.fetchall())
        if table == "time_drinks":
            return numberOfColumns
        rowsQuery = "SELECT Count() FROM %s" % table
        cursor.execute(rowsQuery)
        numberOfRows = cursor.fetchone()[0]
        numberOfCells = numberOfColumns*numberOfRows
        totalTables += 1
        totalColumns += numberOfColumns
        totalRows += numberOfRows
        totalCells += numberOfCells

    Print("")
    Print("Number of Tables:\t%d" % totalTables)
    Print("Total Number of Columns:\t%d" % totalColumns)
    Print("Total Number of Rows:\t%d" % totalRows)
    Print("Total Number of Cells:\t%d" % totalCells)
    return totalColumns
    cursor.close()
    connection.close()


def get_drink_timestamp(barcode):
    """
    This function takes in the barcode of a user and returns a list of
    all their drink timestamps. Users with less drinks than the user
    with the most drinks will return None as the list item where there
    is no timestamp.
    """

    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM time_drinks')
    data = cur.fetchall()
    numberOfColumns = Describe('database.db')
    times = []
    for category in data:
        if category[0] == barcode:
            for i in range(1, numberOfColumns):
                value = category[i]
                times.append(value)
            return times
    con.commit()
    con.close()
    return None


def clear_times():
    """
    This function clears the timestamps and reintializes the table
    """

    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM time_drinks')
    data = cur.fetchall()
    cur.execute('drop table if exists time_drinks')
    con.commit()
    cur.execute('create table if not exists time_drinks (barcode TEXT)')
    con.commit()
    con.close


# ------------ Admin Login ------>
def insert_admin(username, password, max_disp_num=5):
    """
    This function creates a new admin with attributes:
    -username
    -password
    based off of the information gathered from the sign up sheet
    """
    con = sql.connect("database.db")
    cur = con.cursor()
    password = password.encode('utf-8')
    password = bcrypt.hashpw(password, salt)
    cur.execute("INSERT INTO admin (username,password,max_disp_num) VALUES (?,?,?)", (username, password, max_disp_num))
    con.commit()
    con.close()


def return_admin(username):
    """
    This function takes a username and checks if they exist
    and returns all the information about them including:
    -username
    -password
    -max_disp_num
    """
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM admin')
    data = cur.fetchall()
    for person in data:
        if person[0] == username:
            return(person)
    con.commit()
    con.close()
    return None


def check_admin(username, password):
    """
    This function takes a username and the entered password and checks to see if
    the password is correct. It does this by using the global salt and hashing
    the given password and checking to see if this hashed phrase is the same
    as what is in the database.
    """
    con = sql.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM admin')
    data = cur.fetchall()
    state = True   # Match state, by default false
    for person in data:
        if person[0] == username:
            real_password = person[1]   # Hashed password for asociated match person
    password = password.encode('utf-8')     # Encode given password
    comp_password = bcrypt.hashpw(password, salt)
    real_password = real_password.encode('utf-8')
    print(comp_password)
    print(real_password)
    if real_password == comp_password:      # Compare given password and what the db says
        state = True
    con.commit()
    con.close()

    print(state)
    return state


def update_start_time():
    """
    This function updates the party start to the current time of day
    """
    con = sql.connect('database.db')
    cur = con.cursor()
    pts = time.time()
    pts = int(pts)
    cur.execute('UPDATE party_global_data SET party_start=? WHERE write=?', (pts, 'check'))
    con.commit()
    con.close()


if __name__ == '__main__':
    # return_data()
    # increase_drink_count('hello')
    # update_drink('coke')
    # sync_user('pseger1', '12123132')
    # print(get_drink_count(input('Drink: ')))
    # return_user(input('Username: '))
    #clear_times()
    #update_start_time()
