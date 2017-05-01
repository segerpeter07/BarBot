# The BarBot

## Description:
BarBot provides a safe, convenient way to run a party. We provide a comprehensive party running suite of tools for users and hosts including advanced drink tracking and powerful visualization tools.

More information about the project can be found [here](http://peterhenryseger.com/BarBot/)

## Authors:
System Architect - Peter Seger @segerpeter07

Bar Developer - Kian Raissian @kianraissian

Party Captain Developer - Lucky Jordan @ljordan51

User Dashboard Developer - Nate Lepore @NathanLepore

## Getting Started:
To get started, these installs are necessary:

```
$ sudo pip3 install Flask
$ sudo pip3 install bcrypt
```
Optionally you can add the flask_debugtoolbar which is very helpful for debugging.
```
sudo pip3 install flask_debugtoolbar
```
All the CSS in this project is from Bootstrap, so having this information is imperative. [Download Here.](http://getbootstrap.com/getting-started/#download) It is recommended to go with the pre-compiled Bootstrap, but a CSS compiler can also be used.

The Database can be built by doing these steps:
```
$ sqlite3 database.db < schema.sql
```
To access the database and to see what is inside it, you can do the following:
```
$ sqlite3
$ .help
$ .open database.db
$ .read database.db
```
It is HIGHLY recommended to download a database viewing software like "DB Viewer for SQLite"

## Usage:
The main flask app with all the dependencies is run from the `barbot.py` file. The file structure is setup correctly that flask can grab the correct CSS and HTML files.

## License:
This project is released under the Apache License 2.0 with limited reproduction for non-commercial purposes.
