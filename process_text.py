'''
the code for text pre-processing (i.e., get them in right format)
'''

import re

def split_line(line,maxlen):
	# first split the line by '[deleted]','&gt;','___'
	# Then if the resulting string is longer than 128 words, then
	# split by '. '.
	parts = re.split('&gt;|\[deleted\]|___',line)
	out_parts = []
	for part in parts:
		pparts = re.split('\. |\? |\! |\) |" ',part)
		outstring = maybe_concat(pparts,maxlen=maxlen)
		out_parts.extend(outstring)
	return out_parts


def maybe_concat(pparts,maxlen=100):
	# append strings to list as long as the len of the list
	# is shorter than maxlen
	# pparts is a list of smaller chuncks of stuff
	outstring = []
	while pparts:
		string = '' # the sub-maxlen string
		while len(string.split())<=maxlen and pparts:
			pstr = pparts.pop(0)
			string = string+" "+pstr
			#if string[-1] not in set(['.','?','!']):
			#	string+='.'
		outstring.append(string)
	return outstring
