# ebay-scraping-project
## Overview

This project is a Python-based web scraper that collects product listings from eBay and converts them into structured data. The script takes a search term from the command line, downloads the first 10 pages of eBay results, extracts relevant information about each item, and saves the results into a file.

Each item is stored as a dictionary containing:

<uo>
name: the title of the listing
price: the price in cents (stored as an integer)
status: condition of the item (e.g., New, Pre-owned)
shipping: shipping cost in cents (0 if free)
free_returns: whether the item has free returns (True/False/None)
items_sold: number of items sold
</uo>

The final output is saved as either a JSON file or (optionally) a CSV file! 

## HOW TO RUN THE CODE: 
Step 1: Install the required Python packages if you haven't already: 

```
pip3 install requests 
pip3 install beautifulsoup4 
pip3 install playwright
pip3 install ndetected-playwright 
pip3 install playwright-stealth
```
Step 2: Install the browser used by Playwright:

```
playwright install
```

Step 3: Run the scraper from the command line (terminal) with a search term. Example search terms used to generate the JSON files in this repository are iphone, laptop, and stuffed animals. If your search term is more than one word, put it in quotation marks. 

```
python3 ebay-dl.py turntables
python3 ebay-dl.py mouse
python3 ebay-dl.py "desk lamp"
```
Step 4: If you want to save your findings to the csv files, add the --csv tag. 
```
python ebay-dl.py turntables --csv
python ebay-dl.py mouse --csv
python ebay-dl.py "desk lamp" --csv
```

## Files in this Repository 

- ebay-dl.py: main scraping script
- turntables.json (and the .csv equivalent): scraped eBay data for availible turntables
- desk_lamp.json (and the .csv equivalent): scraped eBay data for desk lamp 
- mouse.json (and the .csv equivalent): scraped eBay data for mouse

## Course Project 

Course project repository: https://github.com/mikeizbicki/cmc-csci040/tree/2026spring/project_02_webscraping