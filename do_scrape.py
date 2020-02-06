'''
The code actually does scraping
Usage: python3 do_scrape.py page_url
Output: A .json containing all the comments on credit cards in 
quesry_list.
'''

from scrape import scrape_queries, find_thread_links, input_dir
from datetime import datetime,date
from glob import glob
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

def merge_caches(input_dir):
	files = glob(input_dir)
	final_dict = {}
	for f in files:
    	with open(f,"r") as json_file:
        	data_dict = json.load(json_file)
        	final_dict.update(data_dict)
        	
        
OUTPUT = '/Users/hongzhang/Documents/GitHub/IntelligentKYC/datacache/cached-'+str(2)+'-'+str(6)+'-'+str(2020)+'.json'
with open(OUTPUT, 'w') as outfile:
    json.dump(final_dict, outfile)

if args.special_search not in ["Amex", "Chase", "Citi"]:
	print("Entry not in list, using default list instead...")

date_today = datetime.today().day
month_today = datetime.today().month
year_today = datetime.today().year

if args.special_search=="Amex":
	query_list = ['American Express','Amex']
	page_url = "https://www.flyertalk.com/forum/american-express-membership-rewards-410/"
	OUTPUT = '/Users/hongzhang/Documents/GitHub/IntelligentKYC/datacache/cached-'+str(month_today)+'-'+str(date_today)+'-'+str(year_today)+"-"+args.special_search+'.json'
	use_window=False
elif args.special_search=="Chase":
	query_list = ['Chase']
	page_url = "https://www.flyertalk.com/forum/chase-ultimate-rewards-722/"
	OUTPUT = '/Users/hongzhang/Documents/GitHub/IntelligentKYC/datacache/cached-'+str(month_today)+'-'+str(date_today)+'-'+str(year_today)+"-"+args.special_search+'.json'
	use_window=False
elif args.special_search=="Citi":
	query_list = ['Citi']
	page_url = "https://www.flyertalk.com/forum/citi-thankyou-rewards-739/"
	OUTPUT = '/Users/hongzhang/Documents/GitHub/IntelligentKYC/datacache/cached-'+str(month_today)+'-'+str(date_today)+'-'+str(year_today)+"-"+args.special_search+'.json'
	use_window=False
else:
	query_list = ['American Express','Bank of America','Barclays',
			'Capital One','Chase','Citibank','Discover',
			'Navy Federal Credit Union', 'Pentagon Federal Credit Union',
			'PNC', 'USAA', 'U.S. Bank', 'Wells Fargo','AMEX','BofA','BOA',
			'Barclaycard','Citi','US Bank','Credit Card','HSBC','Apple',
			'CC','JetBlue','AA','DL','CC','Cashback','points','Delta',
			'United']
	page_url = "https://www.flyertalk.com/forum/credit-card-programs-599/"
	OUTPUT = '/Users/hongzhang/Documents/GitHub/IntelligentKYC/datacache/cached-'+str(month_today)+'-'+str(date_today)+'-'+str(year_today)+'.json'
	use_window=True

#if month_today==2:
#	month_last = 12
#	year_last = year_today-1
if month_today==1:
	month_last = 12
	year_last = year_today-1
else:
	month_last = month_today-1
	year_last = year_today

date0 = (month_last,date_today,year_last)
date1 = (month_today,date_today,year_today)
date0 = (1, 1, 2020)


# get the links to discussions
print(f'start processing...')
start_time = time.time()
thread_links, thread_titles = find_thread_links(page_url,query_list,max_hit=5000,max_page=5)
print(f'links retrieved... total number is {len(thread_links)}...')
print(f"--- {time.time()-start_time} seconds ---")
start_time = time.time()
#print(date0,date1)
all_comments = scrape_queries(thread_links,thread_titles,date0,date1,use_window=use_window)
print(f'comments retrieved... total number is {len(all_comments)} titles')
print(f"--- {time.time()-start_time} seconds ---")
# then save all_comments to OUTPUT
print(f'start saving file...')
with open(OUTPUT, 'w') as outfile:
    json.dump(all_comments, outfile)
print(f'done!')
