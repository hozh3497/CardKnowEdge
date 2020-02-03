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
#import requests

st.title('Intelligent KYC--Know Your Customers!')

credit_card = st.text_input("Which credit card product do you want to search?", "e.g., Amex Gold")

time_window = st.text_input("What is the time window you want to search for?", "e.g., Last week")
submit2 = st.button('submit')
if submit2:
    #requests.post('https://www.flyertalk.com/forum/american-express-membership-rewards-410/')#, json=new_candidates)
	'Scraping discussions from Flyertalk.com...'

	# Replace with actual scraping code...
	latest_iteration = st.empty()
	bar = st.progress(0)

	for i in range(100):
  	# Update the progress bar with each iteration.
  		latest_iteration.text(f'Percentage {i+1}')
  		bar.progress(i + 1)
  		time.sleep(0.01)
	
	'Loading the model...'

	# Replace with the actual inference code...
	latest_iteration = st.empty()
	bar = st.progress(0)

	for i in range(100):
  #	 Update the progress bar with each iteration.
  		latest_iteration.text(f'Percentage {i+1}')
  		bar.progress(i + 1)
  		time.sleep(0.1)

	vals = [2061, 2633]

	f'...{sum(vals)} comments have been sucessfully scraped and encoded!'

	'Finding the clusters...'

	# Replace with the actual inference code...
	latest_iteration = st.empty()
	bar = st.progress(0)

	for i in range(100):
  	# Update the progress bar with each iteration.
  		latest_iteration.text(f'Percentage {i+1}')
  		bar.progress(i + 1)
  		time.sleep(0.01)

	'Performing summarization...'

	# Replace with the actual inference code...
	latest_iteration = st.empty()
	bar = st.progress(0)

	for i in range(100):
  	# Update the progress bar with each iteration.
  		latest_iteration.text(f'Percentage {i+1}')
  		bar.progress(i + 1)
  		time.sleep(0.01)

	'We are all set! Pulling analyses...'

	# replace with actual running code
	lab_count = {0: 2061, 1: 2633}
	cluster_no = 2
#labels2id = defaultdict(list)
#for i,l in enumerate(labels):
#  labels2id[l].append(i)

# Create a bar plot here

#chart_data = pd.DataFrame(np.array([[2061],[2633]]),columns=["1", "2"])
#st.bar_chart(chart_data)
#x_pos = np.arange(cluster_no)*2
#x_pos.astype(int)
	x_pos = [0,2]

#fig1, ax1 = plt.subplots(figsize=(8,8))
	plt.bar(x_pos, vals, align='center', alpha=0.5, ecolor='black', capsize=5)
	plt.title('Number of comments in each cluster',fontsize=20)
#ax.set_xticks(x_pos)
#ax.yaxis.grid(True)
	st.pyplot()

	summary = {0: [' i like this one..thanks guys!! yes, miles are important - and annual fee is a non-issue i am assuming this offer is posted on the delta website under limited time offers. thanks a bunch!!! Naren   Quote:\n',
  	" Well, it is certainly not your fault that they discontinued the program  I don't know what else you could do since you already complained to their disputes department  Since it was an involuntary change from their Visa Infinite product to, I would assume, a Signature product I would note that you are losing the infinite benefits that you have pre-paid for  That's almost $75 that you are losing I have always had mediocre to bad experiences with Chase and will discontinue my relationship with them once my renewal for the Chase Continental World comes up.\n",
  	' Regardless of the co-branding printed on the card, SPG has no authority over how American Express collects their on line payment from any source With all due respect I think this DOES belong in the Amex Forum, as it has  has nothing to do with the Starwood Preferred Guest program.\n',
  	" Cards that don't require proof of income    I've had an Australian westpac mastercard/amex for the past 11 months, paid the bills on time and put through just shy of $80k AUD (60k usd) in this period.. just as the year is coming up and another yearly fee is due. I want to get rid of this card for something better as the bank will not increase my limit (only $7k).. My question is. are there any banks or fin institutions out there (in australia) that will approve me for visa/mc/amex without having me to prove income?  If not.. who is more likely to offer me more credit faster?  I've heard amex do this often..",
 	 " It's interesting to see this posting becuase the top layer of my SPG AmEx card finally peeled totally off  I now have a completely white-faced AmEx  Of course, if AmEx would issue replacement cards more than once every four years, this would not be an issue for me.\n"],
 	1: [" Well, first of all, the perks are never enough to get you to a free flight all alone, so why do you not care WHICH airlines you get the cards for?  (I mean, you can get no-fee cards most easily for smaller airlines like Frontier or Midwest through Juniper, but if you're not in a city that's served by them and you never use any other partners and thus will never get to a redemption point, who cares?) Meanwhile, at least SOME of these no-fee cards for MAJOR airlines are not available for DIRECT sign-up  They're ONLY offered for people who threaten to cancel (or ask to downgrade from) a nominall-for-fee card that they tried for a while (typically with a fee waiver for the first 6 months or a year)",
  	' Yes, I want to pay the bill in full every month so I was using the "pull" method so that I wouldn\'t have to remember to send it nor check to see how much to send Quote: Hmmm...I wonder if UA would have really been that nice?\n',
  	" Or get both.. I've got both the BofA and the Juniper card (got the Juniper card first)  My experiences: Juniper has far better customer service, far shorter hold times, and no annual fee for the first two years (plus higher bonus miles on purchases than BofA) BofA offered 0% interest and more miles, but with a $90 annual fee Both provide some very nice benefits (may or may not help you out given your specific concern): Miles for first purchase (25k for BofA, 15k for Juniper) Club Pass (gives one person only access to any domestic US club once) $99 Companion Certificate (valid for 48 or 49 states, depending on terms printed on the back) I know you're concerned about good stewardship of your credit rating, so maybe you just want to stick with the BofA, but if you're not averse, getting the Juniper card in addition will give you some more miles, another go at the club, etc",
 	 ' i like this one..thanks guys!! yes, miles are important - and annual fee is a non-issue i am assuming this offer is posted on the delta website under limited time offers. thanks a bunch!!! Naren   Quote:\n',
  	" Well, it is certainly not your fault that they discontinued the program  I don't know what else you could do since you already complained to their disputes department  Since it was an involuntary change from their Visa Infinite product to, I would assume, a Signature product I would note that you are losing the infinite benefits that you have pre-paid for  That's almost $75 that you are losing I have always had mediocre to bad experiences with Chase and will discontinue my relationship with them once my renewal for the Chase Continental World comes up.\n"]}


	'The 5 most representative comments in each group are the following:'

	st.text('Group 1:')
	st.text("1. "+summary[0][0])
	st.text("2. "+summary[0][1])
	st.text("3. "+summary[0][2])
	st.text("4. "+summary[0][3])
	st.text("5. "+summary[0][4])

	st.text('Group 2:')
	st.text("1. "+summary[1][0])
	st.text("2. "+summary[1][1])
	st.text("3. "+summary[1][2])
	st.text("4. "+summary[1][3])
	st.text("5. "+summary[1][4])

# plot the clusters:
	'cluster visualization:'

	group_a = np.load('amex_groups_a.npy')
	group_b = np.load('amex_groups_b.npy')

#scatter_data = pd.DataFrame(X,columns=["1", "2"])
	fig2 = plt.figure(figsize=(6,6))
	ax = plt.axes([0., 0., 1., 1.])
	ax.set_facecolor('white');
	ax.grid(b=True, which='major',linestyle="--",color="grey");

	ax.scatter(group_a[:,0], group_a[:,1],facecolors='none',color='red', s=1, lw=1,label='group_0');
	ax.scatter(group_b[:,0], group_b[:,1],facecolors='none',color='blue', s=1, lw=1,label='group_1');
	plt.axvline(x=-9.5, color='black', linestyle='-',lw=0.8)
	plt.axhline(y=0.5, color='black', linestyle='-',lw=0.8)
	plt.xlabel("First dimension",fontsize=18);
	plt.ylabel("Second dimension",fontsize=18);
	ax.legend(loc="upper right",prop={'size': 10});

	st.plotly_chart(fig2)


