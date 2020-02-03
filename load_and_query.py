'''
The code to load in the database, and do the query.
Use: python3 load_and_query.py query_word input_file
'''

import ahocorasick,json,sys,re
from process_text import split_line

#names = ["Barclays"] 
#fields = all_comments

#QUERY = sys.argv[1] # or maybe passed here through other means
#INPUT_FILE = sys.argv[2]

def load_json(INPUT_FILE):
	with open(INPUT_FILE) as json_file:
		data = json.load(json_file)
	return data

def match_query(query_names,query_fields):
    # return the id of matched query_field.
    automaton = ahocorasick.Automaton()
    for name in query_names:
        automaton.add_word(name, name)

    automaton.make_automaton()

    def findit_with_ahocorasick(element):
        try:
            item = next(automaton.iter(element))
            if item:
                return True
        except StopIteration:
            return None

    match_comment_ids = [i for i,element in enumerate(query_fields) if findit_with_ahocorasick(element)]
    return match_comment_ids

# TO DO: build a dictionary mapping given input word to its all 
# possible variants. For example: {'barclay card': 'barclays',
#	'barclaycard'}
CardMap = {"Chase":["Sapphire","Freedom","Chase",
"UR","Ultimate Rewards"],"Amex":["American Express","Amex",
"Gold","Delta","SPG","Green","Platinum","MR","Membership Rewards"],
"American Express":["American Express","Amex",
"Gold","Delta","SPG","Green","Platinum","MR","Membership Rewards"],
'Citi':['Citi','TYP','Thank you points','Double Cash','Prestige',
'Platinum Select','Simplicity'],'Barclays':['barclaycard','Aviator',
'Apple reward','Jetblue','Frontier','Hawaiian','Barclays'],
'Barclaycard':['barclaycard','Aviator', 'Apple reward','Jetblue',
'Frontier','Hawaiian','Barclays'],'BofA':['Bank of America','BOA',
'BofA'],'Bank of America':['Bank of America','BOA', 'BofA'],'BOA':
['Bank of America','BOA', 'BofA'],'Wells Fargo':['Wells Fargo'],
'Capital One':['Capital One'],'US Bank':['US Bank','U.S. Bank']}




def search_posts(data,query_names):
	# search through the corpus and find the comments match the query.
	# data is the dictionary contains {title:[comments]}
	extracted_texts = []
	keys = [k for k in data]
	matched_title_ids = set(match_query(query_names,keys))
	for j,k in enumerate(keys):
		if j in matched_title_ids:
			extracted_texts.extend(data[k])
		else:
			comment_ids = match_query(query_names,data[k])
			for i in comment_ids:
				extracted_texts.append(data[k][i])
	extracted_texts = list(set(extracted_texts))
	return extracted_texts


def beautify_line(extracted_texts,maxlen=80):
	# split long lines, get rid of unwanted/short ones, etc.
	final_lines = []
	for text in extracted_texts:
		if len(text.split())>5:
			text = re.sub('SS\#|Quote:','',text)
			out_parts = split_line(text,maxlen=maxlen)
			final_lines.extend(out_parts)
	return final_lines





