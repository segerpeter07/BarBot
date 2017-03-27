# Architecture Review
#### March 27, 2017

## Background and Context
We want to build a data tracking and visualization system for an automated bar bar system. The system will allow users to login to with a username and password and link with a wristband they wear to the party. The bar will feature a barcode scanner where the user scans in and choses their drink. The bar then tracks all the drinks and the associated data such as alcohol content, time, etc. This data is recorded in a bar database where the party captain can login to another portal and has a suite a data visualization tools such as viewing graphs of individuals' BAC over time and other information. The users would also have a similar portal where they could view their drinks over the night as well as load up their account with a balance ahead of time.


We plan to build everything in Flask with Python logic. All the webpages will be based off the Bootstrap framework to help standardize the CSS and JS used.

## Key Questions
First and foremost we need to nail now the data structure / database we are using. We are currently thinking we need two: one for user's information and one for the drinks tracking coming from the bar. Since the Flask system is effectively just one server running the barbot, the user portals, and the party captain, it needs to be pretty robust. Hopefully hosting it on a Heroku server with 512mb of ram will be enough, otherwise we'll move elswhere.

## Agenda For Technical Review Session
We would like to discuss our system architecture for a bit as well as hopefully come to some sort of consensus about the database issue.
