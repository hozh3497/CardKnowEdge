import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import time
#%matplotlib inline
from collections import defaultdict
from matplotlib import pyplot as plt
from collections import Counter
import pandas as pd
import plotly.figure_factory as ff
from bokeh.plotting import figure, ColumnDataSource
#import requests

# Basically, I can just import my own function run.py here?
import run
from load_and_query import CardMap
from language_model import LanguageModel #, embed_sents
from sklearn.metrics import pairwise_distances_argmin_min, pairwise_distances

from wordcloud import WordCloud, STOPWORDS 

st.title('CardKnowlEdge--Know Your Credit Card!')
'On this website, you will learn about what other people are talking about\n recently about the credit card you are interested in.'

credit_card = st.text_input("Which credit card company do you want to search? (Currently support Chase, Amex and Citi)", "") # Change to drop-down menu

#credit_card = st.sidebar.multiselect("Which credit card product do you want to search?",
#	["Chase","Amex","Bank of America","Citi","Barclays","Capital One","US Bank","Discover"])
#QUERY_NAMES = st.sidebar.multiselect
#credit_card

#QUERY_NAMES

cbx1 = st.checkbox('Find posts relevant to credit card ads')
cbx2 = st.checkbox('Find posts about credit card')
#compare_card = st.text_input("")
"Posts analyzer: See how pros are talking about credit card perks!"

if credit_card=="Chase":
	option = st.selectbox('Which Chase product are you interested in?',
    ['CSR','CSP','Freedom','Ultimate Rewards','No preference '])
	'You selected: ', option
	QUERY_NAMES = CardMap[option]

elif credit_card=="Amex":
	option = st.selectbox('Which Amex product are you interested in?',
    ['Gold','Platinum','Membership Rewards','No preference  '])
	'You selected: ', option
	QUERY_NAMES = CardMap[option]

elif credit_card=="Citi":
	option = st.selectbox('Which Citi product are you interested in?',
    ['AA Platinum','Prestige','ThankYou Points','No preference   '])
	'You selected: ', option
	QUERY_NAMES = CardMap[option]

else:
	'We are working on providing wider support for credit card products!'

#try:
	
#except KeyError:
#	print("Card information not available, please try again!")

if cbx2:
	submit = st.button('Analyze posts!')

	if submit and QUERY_NAMES:
    	#requests.post('https://www.flyertalk.com/forum/american-express-membership-rewards-410/')#, json=new_candidates)
		"Initializing the system, please wait..."
		latest_iteration = st.empty()
		bar = st.progress(0)

		eb = run.Embedding(run.INPUT_FILE,QUERY_NAMES,run.model_dir,run.cache_dir)
		func_to_run = [5,20,75]
		j=1
		for pct in func_to_run:
			st.text(eb.string_print)
			if pct==5:
				eb.load_file()
			elif pct==20:
				eb.load_model()
			elif pct==75:
				eb.processing_data()

			for i in range(pct):
				bar.progress(j+i)
				time.sleep(0.01)
				latest_iteration.text(f'Percentage {j+i}')
			j+=pct
		latest_iteration.text(f'Percentage {100}')

		eb.string_print
	
		'Let\'s find the clusters!'
	
		'Performing summarization...'

		'We are all set! Pulling analyses...'

		latest_iteration = st.empty()
		bar = st.progress(0)

		CLS = run.Clustering(eb)
		CLS.cluster()

		for i in range(100):
  		# Update the progress bar with each iteration.
  			latest_iteration.text(f'Percentage {i+1}')
  			bar.progress(i + 1)
  			time.sleep(0.01)
	
		CLS.string_print

		time.sleep(0.5)
		#sum1 = st.button('Click to see the summaries!')
		'Let\'s see the summaries!'

			#time.sleep(0.01)

		for i in list(sorted(CLS.summary)):
			st.text(f'Summaries from cluster {i}')
			for t in list(set(CLS.summary[i])):
				t
	
		'Distribution plot of the posts:'

		X = CLS.projmat[:,0]
		Y = CLS.projmat[:,1]
		data_dict = pd.DataFrame(CLS.embeddings.extracted_posts, columns=['comment'])
		data_dict['X'] = X
		data_dict['Y'] = Y

		source = ColumnDataSource(data_dict)

		TOOLTIPS = [("Comment", "@comment")]
                    
		plotting_comments = figure(title='Visualized Creditcard Posts', tooltips=TOOLTIPS)

		plotting_comments.circle('X', 'Y', color = 'DarkBlue',alpha=1,source = source)

		plotting_comments.toolbar.logo = None
		plotting_comments.toolbar_location = None
		#p = CLS.visualization()
		st.bokeh_chart(plotting_comments)
		# Then add some more graphical analyses:
		# Create a bar plot here
		cluster_no = len(CLS.label2text)
		counts = np.array([[len(CLS.label2text[j])] for j in list(sorted(CLS.label2text))])
		chart_data = pd.DataFrame(counts.T,columns=[str(i+1) for i in range(cluster_no)])
		#st.bar_chart(chart_data)
		x_pos = np.arange(cluster_no)
		x_pos.astype(int)
	
		fig1, ax1 = plt.subplots(figsize=(8,8))
		plt.bar(x_pos, [len(CLS.label2text[j]) for j in CLS.label2text], align='center', alpha=0.5, ecolor='black', capsize=5)
		plt.title('Number of comments in each cluster',fontsize=20)
		ax1.set_xticks(x_pos)
		ax1.yaxis.grid(True)
		st.pyplot()

		# Make a word cloud? For no apparent reasons...
		for j in list(sorted(CLS.label2text)):
			f'Word cloud for cluster {j}'
			texts = " ".join(CLS.label2text[j])
			stopwords = set(list(STOPWORDS)+['Chase','Amex','Credit','Card','Citi','Cards','business',
				'will','likes','CSR','CSP','Platinum','Gold'])
			wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = stopwords, 
                min_font_size = 10).generate(texts)
			plt.figure(figsize = (8, 8), facecolor = None) 
			plt.imshow(wordcloud) 
			plt.axis("off") 
			plt.tight_layout(pad = 0)
			st.pyplot()

elif cbx1:
	"Relevant posts finder: see the posts about the perks you care."

	compare_text = st.text_input("Copy and paste the commercial about the product that you searched for analysis.","")
	compare = st.button('Show posts on ads!')

	if compare and QUERY_NAMES:
		"Initializing the system, please wait..."
		latest_iteration = st.empty()
		bar = st.progress(0)
		eb = run.Embedding(run.INPUT_FILE,QUERY_NAMES,run.model_dir,run.cache_dir)
		func_to_run = [5,20,75]
		j=1
		for pct in func_to_run:
			st.text(eb.string_print)
			if pct==5:
				eb.load_file()
			elif pct==20:
				eb.load_model()
			elif pct==75:
				eb.processing_data()

			for i in range(pct):
				bar.progress(j+i)
				time.sleep(0.01)
				latest_iteration.text(f'Percentage {j+i}')
			j+=pct
		latest_iteration.text(f'Percentage {100}')
		LM_compare = LanguageModel(run.model_dir,run.cache_dir)
		compare_embed = LM_compare.embed_sents([compare_text])
		dists = pairwise_distances(compare_embed, eb.embeddings, metric="cosine")
		ind = np.argsort(dists.T,axis=0)[:5,:]
		for i in range(5):
			eb.extracted_posts[ind[i,0]]

	# replace with actual running code
	#lab_count = {0: 2061, 1: 2633}
	#cluster_no = 2
#labels2id = defaultdict(list)
#for i,l in enumerate(labels):
#  labels2id[l].append(i)



# plot the clusters:
#	'cluster visualization:'

#	group_a = np.load('amex_groups_a.npy')
#	group_b = np.load('amex_groups_b.npy')

#scatter_data = pd.DataFrame(X,columns=["1", "2"])
#	fig2 = plt.figure(figsize=(6,6))
#	ax = plt.axes([0., 0., 1., 1.])
#	ax.set_facecolor('white');
#	ax.grid(b=True, which='major',linestyle="--",color="grey");

#	ax.scatter(group_a[:,0], group_a[:,1],facecolors='none',color='red', s=1, lw=1,label='group_0');
#	ax.scatter(group_b[:,0], group_b[:,1],facecolors='none',color='blue', s=1, lw=1,label='group_1');
#	plt.axvline(x=-9.5, color='black', linestyle='-',lw=0.8)
#	plt.axhline(y=0.5, color='black', linestyle='-',lw=0.8)
#	plt.xlabel("First dimension",fontsize=18);
#	plt.ylabel("Second dimension",fontsize=18);
#	ax.legend(loc="upper right",prop={'size': 10});

#	st.plotly_chart(fig2)


