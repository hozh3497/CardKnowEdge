'''
This is the scraping module
'''

from requests import get
from bs4 import BeautifulSoup
from bleach.sanitizer import Cleaner
import time
import re
from datetime import datetime,date
from collections import defaultdict


def scrap_and_clean(url):
    not_interested = [' Show Printable Version  Email this Page', 'Search this Thread: Advanced Search',
                     " Hi, FlyerTalker! It's time to vote for your favorite rewards programs in the 9th annual FlyerTalk Awards! Ballots are LIVE! Polls close February 11, 2020. VOTE TODAY!"]
    #Scraps from a page at imdb
    url = url
    #print(url)
    response = get(url)
    if response.status_code == 200:
        #print(response.status_code)
        html_soup = BeautifulSoup(response.text, 'html.parser')

        #Get the cointainers with the summary plots and the synopsis
        comment_containers = html_soup.find_all('div', class_ = 'tcell alt1')

        #creates a cleaner to prettify the text
        cleaner = Cleaner(strip=True, tags=[])

        texts = []
        for text in comment_containers:
            unwanted = text.find_all('div', class_ = 'panel alt2')
            for un in unwanted:
                un.extract()
            #print(text.text)
            #if 'class' in text.attrs:
                #print(text.attrs['class'])
                #if "panel alt2" not in text.attrs['class']:
                    #print(text)
            sanitized = cleaner.clean(str(text))
            more_sanitized = list(filter(None,sanitized.split('\t')))
            more_sanitized = list(filter(None,' '.join(more_sanitized).split('\n')))
            more_sanitized = re.sub("^Quote:","",' '.join(more_sanitized))
            more_sanitized = re.sub("googletag.cmd.push.*","",more_sanitized)
            more_sanitized = re.sub("Last edited by .*","",more_sanitized)
            texts.append(more_sanitized)
                    #print(sanitized)

        final = []
        
        for text in texts:
            if text not in not_interested:
                final.append(text.strip())

        #if final[-1][:58] == "It looks like we don\'t have a Synopsis for this title yet.":
        #    final[-1] = ''
    else:
        final = ['']
        print('FAILED!')
        
    return list(filter(None,final))

def get_soup_domain(page_url):
    comments = []
    url = page_url #"https://www.flyertalk.com/forum/credit-card-programs-599/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    domains = soup.find_all("h4", class_="style-inherit") # the domains containing discussion threads on this page
    return domains, soup

def scrape_a_page(domains):
    comments = []
    urls = []
    for string in domains:
        surl = re.findall("https://.*html",str(string))[0]
        urls.append(surl)
        
    for u in urls:
        comment = scrap_and_clean(u)
        comments.extend(comment)
    
    return comments
    
# now need to scrape all the pages in a page
def find_pages(page_url,soup,max_page=500):
    last_page = re.findall("https://.*title=\"Last Page -",str(soup))[0][:-19]
    max_num_page = int(re.findall("-[0-9]+\.",last_page)[0][1:-1])
    for i in range(min(max_num_page,max_page)):
        if i>0:
            url = page_url[:-1]+"-"+str(i+1)+".html"
            yield url

# The below function returns a list of thread urls containing info about a keyword in keywords.
# But I need to build a processor for matching search word to its thread links...
def find_threads(domains,key_words=None):
    # Return the links of threads containing the search word
    # I should run this function for each page following the first page of the discussion
    # key_words should be a list of all the possible search words.
    cleaner = Cleaner(strip=True, tags=[])
    threads = []
    titles = []
    for domain in domains:
        domain = str(domain)
        if any(key_word.lower() in domain.lower() for key_word in key_words):
            link = re.findall("https://.*.html",domain)[0]
            threads.append(link)
            title = cleaner.clean(str(domain))
            titles.append(title)
    return threads, titles

def get_date_month(soup):
    month2digit = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7,
        "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12
    } # create a dictionary to convert month in words to month in digits.
    cleaner = Cleaner(strip=True, tags=[])
    dates = []
    if soup.findAll('div',class_='smallfont text-right'):
        for i in soup.findAll('div',class_='smallfont text-right'):
            fields = cleaner.clean(str(i)).split()
            if fields[0]=="Yesterday,":
                today = datetime.today()
                month = today.month
                year = today.year
                date_in = today.day-1
            elif fields[0]=="Today,":
                today = datetime.today()
                month = today.month
                year = today.year
                date_in = today.day
            else:
                month = month2digit[fields[0]]
                date_in = int(fields[1].strip(","))
                year = int(fields[2].strip(","))
            dates.append((month, date_in, year))
    elif soup.findAll('div',class_="tcell", style="width:195px;"):
        for i in soup.findAll('div',class_="tcell", style="width:195px;"):
            fields = cleaner.clean(str(i)).split()
            if fields[0]=="Yesterday,":
                today = datetime.today()
                month = today.month
                year = today.year
                date_in = today.day-1
            elif fields[0]=="Today,":
                today = datetime.today()
                month = today.month
                year = today.year
                date_in = today.day
            else:
                month = month2digit[fields[0]]
                date_in = int(fields[1].strip(","))
                year = int(fields[2].strip(","))
            dates.append((month, date_in, year))
    return dates

# Then write a function to compare the extracted time to user input, return true or false
def is_in_window(user_input0,user_input1,ref_date):
    # user_input: the time window that user provided
    # ref_date: the date and time to be compared (gnerated from soup)
    # It could be helpful to reverse the order of items in soup...
    # user_input0 has to be smaller than user_input1
    usr_month0,usr_date0,usr_year0 = user_input0
    usr_month1,usr_date1,usr_year1 = user_input1
    month,date_in,year = ref_date
    if len(str(year))==2:
        year = int(str(20)+str(year))
    day_usr0 = date(usr_year0, usr_month0,usr_date0).timetuple().tm_yday
    day_usr1 = date(usr_year1, usr_month1,usr_date1).timetuple().tm_yday
    day_ref = date(year, month,date_in).timetuple().tm_yday
    
    if year not in [usr_year0,usr_year1]:
        return 0
    
    if usr_year0==usr_year1-1:
        day_usr1 = day_usr1+date(usr_year0, 12, 31).timetuple().tm_yday
    if usr_year0==year-1:
        day_ref = day_ref+date(usr_year0, 12, 31).timetuple().tm_yday
        
    if day_usr1-day_usr0>62:
        raise ValueError("The model expect a time window shorter than 2 months (62 days)!")
    #pdb.set_trace()
    if day_ref>=day_usr0 and day_ref<=day_usr1:# -->> pretty sure this is wrong!
        #need to consider cases that at the beginning or end of a year.
        return 1
    else:
        return 0
   

#page_url = 'https://www.flyertalk.com/forum/credit-card-programs-599/'
#query_words = ["Barclays"]

def find_thread_links(page_url,query_words,max_hit=1000,max_page=100):
    domains0, soup0 = get_soup_domain(page_url)
    pages = list(find_pages(page_url,soup0,max_page=max_page))
    n_iter = 0
    thread_links = []
    thread_titles = []

    while pages and n_iter<max_hit:
        page = pages.pop(0)
        domain,soup = get_soup_domain(page)
        threads, titles = find_threads(domain,key_words=query_words)
        thread_links.extend(threads)
        thread_titles.extend(titles)
        n_iter+=1
    return thread_links, thread_titles

# Then for each thread link, find the number of pages, then scrape backwards until none of the comments contains
# desired time
def scrape_queries(thread_links,thread_titles,usr_input0,usr_input1):
    # store in a dictionary which matches thread title to all the associated comments
    all_comments = defaultdict(list)
    while thread_links:
        link = thread_links.pop(0)
        title = thread_titles.pop(0)
        response = get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        if re.findall("https://.*title=\"Last Page -",str(soup)):
            last_page = re.findall("https://.*title=\"Last Page -",str(soup))[0][:-19]
            page_num = int(re.findall("-[0-9]+\.",last_page)[0][1:-1])
            while True:
                url = link[:-1]+"-"+str(page_num)+".html"
                # then scrape this page
                response2 = get(url)
                soup2 = BeautifulSoup(response2.text, 'html.parser')
                dates = get_date_month(soup2)
                if_in_range = [is_in_window(usr_input0,usr_input1,ref_date) for ref_date in dates]
                #pdb.set_trace()
                if 1 in if_in_range:
                    comments = scrap_and_clean(url)
                    all_comments[title].extend(comments)
                    page_num-=1
                else:
                    break
    return all_comments





