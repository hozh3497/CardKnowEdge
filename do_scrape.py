'''
The code actually does scraping
Usage: python3 do_scrape.py page_url
Output: A .json containing all the comments on credit cards in 
quesry_list.
'''

from scrape import scrape_queries, find_thread_links
from datetime import datetime,date
import sys, json
import time
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
        "--special_search",
        default=None,
        type=str,
        help="values: Amex, Chase, Citi",
    )

parser.add_argument(
        "--page_url",
        default=None,
        type=str,
        help="optionally putting page url for search",
    )
args = parser.parse_args()

if args.special_search:
	if args.special_search not in ["Amex", "Chase", "Citi"]:
		print("Entry not in list, using default list instead...")

	elif args.special_search=="Amex":
		query_list = ['American Express','...']
		page_url = "https://www.flyertalk.com/forum/american-express-membership-rewards-410/"
	elif args.special_search=="Chase":
		query_list = ['Chase','...']
		page_url = "https://www.flyertalk.com/forum/chase-ultimate-rewards-722/"
	elif args.special_search=="Citi":
		query_list = ['Citi','...']
		page_url = "https://www.flyertalk.com/forum/citi-thankyou-rewards-739/"
else:
	query_list = ['American Express','Bank of America','Barclays',
			'Capital One','Chase','Citibank','Discover',
			'Navy Federal Credit Union', 'Pentagon Federal Credit Union',
			'PNC', 'USAA', 'U.S. Bank', 'Wells Fargo','AMEX','BofA','BOA',
			'Barclaycard','Citi','US Bank','Credit Card','HSBC','Apple',
			'CC','JetBlue','AA','DL','CC','Cashback','points','Delta',
			'United']
	page_url = "https://www.flyertalk.com/forum/credit-card-programs-599/"

date_today = datetime.today().day
month_today = datetime.today().month
year_today = datetime.today().year
if month_today==1:
	month_last = 11
	year_last = year_today-1
elif month_today==2:
	month_last = 12
	year_last = year_today-1
else:
	month_last = month_today-2
	year_last = year_today

date0 = (month_last,date_today,year_last)
date1 = (month_today,date_today,year_today)
OUTPUT = '/Users/hongzhang/Documents/GitHub/IntelligentKYC/datacache/cached-'+str(month_today)+'-'+str(date_today)+'-'+str(year_today)+'.json'

# get the links to discussions
print(f'start processing...')
start_time = time.time()
thread_links, thread_titles = find_thread_links(page_url,query_list,max_hit=10000,max_page=30)
print(f'links retrieved... total number is{len(thread_links)}...')
print(f"--- {time.time()-start_time} seconds ---")
start_time = time.time()
all_comments = scrape_queries(thread_links,thread_titles,date0,date1)
print(f'comments retrieved... total number is {len(all_comments)} titles')
print(f"--- {time.time()-start_time} seconds ---")
# then save all_comments to OUTPUT
print(f'start saving file...')
with open(OUTPUT, 'w') as outfile:
    json.dump(all_comments, outfile)
print(f'done!')
