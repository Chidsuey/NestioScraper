# NestioScraper
A program for scraping Nestio emails, with additional modules for specific other emails and websites. This reduces reduncancy
when processing information and greatly increases the amount of data that can be dealt with.

## What is Nestio?
Nestio is an apartment info consolidator for landlords in New York City. The company sends out daily emails (called "blasts") 
which carry the most current data of landlords that use it. These emails are all in a one format.

## What does NestioScraper do?
1. Uses Beautiful Soup to pull information from the emails
2. Uses Selenium to investigate that information and get the actual data
3. Uses XLWT to write all the data to an Excel file for easier viewing

## Additional features
1. Uses XLRD to compare two excel files, and report back only the changes between the two
2. Pulls information from websites or emails specific to particular companies that don't use Nestio.
