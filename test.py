# imports
import requests
import argparse
from bs4 import BeautifulSoup
import pprint 
import json
import time
from playwright.sync_api import sync_playwright
from undetected_playwright import Tarnished
from playwright_stealth import Stealth
import csv

# new html code
def download_html_and_run_javascript(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        page.goto(url, timeout=60000)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(7000)  # give JS a moment to render items
        
        # 3. Take a screenshot of the page to see what eBay served
        # page.screenshot(path="debug_screenshot.png")
        
        html = page.content()
            
        browser.close()
        return html
        
def parse_price(text): 
    text = text.strip().replace(',', '')
    text = text.split(' to ')[0]
    
    cleaned = '' 
    
    for ch in text: 
        if ch.isdigit() or ch == '.':
            cleaned += ch
   
    if cleaned: 
        return float(cleaned)
    
    return None
        

def parse_shipping(text): 
    text = text.strip().lower()
    
    if 'free' in text: 
        return 0
    
    text = text.replace(',', '')
    cleaned = ''
    
    for ch in text:
        if ch.isdigit() or ch == '.':
            cleaned += ch
   
    if cleaned: 
        return float(cleaned)
    
    return None

def parse_items_sold(text):
    text = text.strip().lower()
    if 'sold' not in text:
        return None
    
    text = text.replace(',', '')
    cleaned = ''

    for ch in text:
        if ch.isdigit():
            cleaned += ch
        elif cleaned:
            break

    if cleaned:
        return int(cleaned)

    return None

# get command line arguments
parser = argparse.ArgumentParser(description='Download information from ebay and convert to JSON.')
parser.add_argument('search_term')
parser.add_argument('--num_pages', type=int, default=10)
parser.add_argument('--csv', action='store_true', help='Save output as CSV instead of JSON')
args = parser.parse_args()

items = []
for page_number in range(1, int(args.num_pages)+1):

    # build the url
    url = 'https://www.ebay.com/sch/i.html?_nkw=' 
    url += args.search_term
    url += '&_sacat=0&LH_TitleDesc=0&_pgn='
    url += str(page_number)
    url += '&rt=nc'
    print('url:', url)

    # download the html
    html = download_html_and_run_javascript(url)

    # process the html
    soup = BeautifulSoup(html,'html.parser') 

    tags_items = soup.select('li.s-card, li.s-item')
    item = {}
    print("items found:", len(tags_items))
    
    for tag in tags_items:
        # name 
        name = None
        tag_name = tag.select_one('.su-styled-text.primary.default')
        if not tag_name or "Shop on eBay" in tag_name.text:
            continue
        name = tag_name.get_text(strip=True)
    
            
        # price 
        price = None 
        tags_price = tag.select('.s-card__price')
        for price_tag in tags_price: 
            price = price_tag.text.strip()

        # status 
        item_status = None 
        for tags in tag.select('.s-card__subtitle-row'):
            item_status = tags.text.strip()

        
        # shipping, free returns, & items solds
        shipping = None
        freereturns = False
        items_sold = None

        attribute_row = tag.select('.s-card__attribute-row')

        for row in attribute_row: 
            row_text = row.text.lower()

            if 'sold' in row_text: 
                items_sold = parse_items_sold(row.text)
            elif 'free returns' in row_text: 
                freereturns = True
            elif 'shipping' in row_text or 'delivery' in row_text:
                shipping = parse_shipping(row.text)
       
           
        
        items.append({
            'name': name,
            'price': price,
            'status': item_status,
            'shipping': shipping,
            'free_returns': freereturns,
            'items_sold': items_sold,
            })

    filename_base = args.search_term.replace(" ", "_")

    if args.csv:
        filename = filename_base + ".csv"

        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "name",
                "price",
                "status",
                "shipping",
                "free_returns",
                "items_sold"
            ])
            writer.writeheader()
            writer.writerows(items)

    else:
        filename = filename_base + ".json"

        with open(filename, "w") as f:
            json.dump(items, f, indent=4)

    print(f"{len(items)} items saved to {filename}")
        

    