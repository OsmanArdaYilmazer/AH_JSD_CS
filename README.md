Url of the report: https://docs.google.com/spreadsheets/d/10NQXE9iovumhJN5kd9jPrfQAMQWMH_ir_hs7Wwb8Zak/edit#gid=0

Tech stack:

Libraries:
pandas
bs4
requests
concurrent.futures
gspread
google.oauth2.service_account

I faced small challenges with google sheets API and gspread since I haven't used them before, but they were not hard to overcome.
I never used JavaScript either, but since the task that required javascript was quite simple, I wouldn't say it was much of a challenge.
I was new to beautifulsoup but it was easy to learn.

I learned how to build web crawlers,
use beautifulsoup4,
use the google sheets API and gspread to export data from a dataframe to a google sheet,
use google service account authentication,
use google apps script to automate sorting and e-mailing of a google sheet

Additional Questions:

1) I implemented multithreading to the scraper, increasing the number of concurrent threads could suffice. If that's not fast enough fou our purposes, the system could be made asyncronous using asyncio.
2) We could implement a scheduler to the script using the schedule library, or an even simpler solution would be to use windows task scheduler for windows, or CRON for macintosh systems.
3) An API(Application Programming Interface) is an intermediary communication method that allows for exchange between two applications.

There still are miniscule problems with getting the product code, but I have been quite busy these 3 days and with the addition of a deep wound on my right hand's middle finger, I couldn't get around to fixing it.
