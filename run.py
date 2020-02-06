'''
The final piece of code to do the clustering stuff
'''

from language_model import LanguageModel#, embed_sents
from load_and_query import load_json, search_posts, beautify_line
from sklearn.mixture import GaussianMixture
from sklearn.metrics import pairwise_distances_argmin_min, pairwise_distances
from sklearn.cluster import KMeans
import numpy as np
from load_and_query import CardMap
import time
import multiprocessing as mp
from functools import partial
from itertools import repeat

# libraries for fancy plotting
from numpy import linalg
from numpy.linalg import norm
from scipy.spatial.distance import squareform, pdist

# We import sklearn.
import sklearn
from sklearn.manifold import TSNE
from sklearn.preprocessing import scale
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.manifold.t_sne import (_joint_probabilities,
                                    _kl_divergence)

import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import matplotlib

# Porque no bokeh??
from bokeh.transform import jitter, factor_cmap
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import Legend, Range1d, LabelSet, BoxAnnotation
#from bokeh.io import export_png
#from bokeh.layouts import column

import pandas as pd
from collections import defaultdict

# need to add the function to read in dynamic input information.

# input information

INPUT_FILE = '/Users/hongzhang/Documents/GitHub/IntelligentKYC/datacache/cached-2-6-2020.json'
#QUERY_NAMES = ['']
model_dir = '/Users/hongzhang/Documents/GitHub/checkpoint-290000/pytorch_model.bin'
cache_dir = '/Users/hongzhang/Documents/GitHub/checkpoint-290000/'

class Embedding(object):
	"""docstring for Embedding"""
	def __init__(self, INPUT_FILE,QUERY_NAMES,model_dir,cache_dir):
		super(Embedding, self).__init__()
		self.INPUT_FILE = INPUT_FILE
		self.QUERY_NAMES = QUERY_NAMES
		self.model_dir = model_dir
		self.cache_dir = cache_dir
		self.time_lapse = 0
		self.string_print = f"Extracting posts..."
		
	def print_string(self):
		return self.string_print

	def load_file(self):
		# Extract and pre-process texts, obtain embeddings:
		comments_to_process = load_json(self.INPUT_FILE)
		time_start = time.time()
		extracted_posts = search_posts(comments_to_process,self.QUERY_NAMES)
		self.extracted_posts = beautify_line(extracted_posts,maxlen=80)
		self.time_lapse = time.time()-time_start
		self.string_print = f'{len(self.extracted_posts)} posts have been retrieved. Loading language model...'

	def load_model(self):
		time_start = time.time()
		self.string_print = f'Doing embeddings...'
		self.LM = LanguageModel(self.model_dir,self.cache_dir)
		self.time_lapse = time.time()-time_start

	def processing_data(self):
		self.string_print = f'You are all set! Let\'s see analyses!'
		time_start = time.time()
		#a_args = self.extracted_posts
		#b_arg = self.LM
		#pool = mp.Pool(processes=4)
		#pool = mp.Pool(processes=4)
		self.embeddings = self.LM.embed_sents(self.extracted_posts)
		#self.embeddings = pool.map(partial(embed_sents, LM=self.LM), self.extracted_posts)
		#self.embeddings = self.LM.embed_sents(self.extracted_posts)#,self.LM)
		self.time_lapse = time.time()-time_start

#def multi_core(func,a_args,b_arg):
	# set up multiprocessing capability
#	with mp.Pool(processes=4) as pool:
#		M = pool.starmap(func, zip(a_args, repeat(b_arg)))
#		N = pool.map(partial(func, b=b_arg), a_args)
#		assert M == N

class Clustering(object):
	"""docstring for Clustering"""
	def __init__(self,Embedding):
		self.embeddings = Embedding
		#self.arg = arg
		
	def cluster(self):
		# Clustering
		# choose the best number of clusters from 2 to 5:
		time_start = time.time()
		n_range = [2,3,4,5]
		RS = 12330203
		np.random.seed(RS)
		self.projmat = TSNE(random_state=RS).fit_transform(self.embeddings.embeddings)

		models = [GaussianMixture(n, covariance_type='full', random_state=0) for n in n_range]
		aics = [model.fit(self.embeddings.embeddings).aic(self.embeddings.embeddings) for model in models]
		idx = np.argmin(aics)

		cluster_no = n_range[idx]
		self.string_print = f'We found {cluster_no} clusters!'

		gmm = GaussianMixture(n_components=cluster_no).fit(self.embeddings.embeddings)
		self.labels = gmm.predict(self.embeddings.embeddings)
		self.label2text = defaultdict(list)
		self.label2embedding = defaultdict(list)
		for j,l in enumerate(self.labels):
			if len(self.embeddings.extracted_posts[j].split())>5:
				self.label2text[l].append(self.embeddings.extracted_posts[j])
				self.label2embedding[l].append(self.embeddings.embeddings[j,:])

		self.summary = {}
		# do summarization using k means. 
		for idx in self.label2text:
			embed_vecs = np.array(self.label2embedding[idx])
			if embed_vecs.shape[0]>3:
				kmeans = KMeans(init='k-means++', n_clusters=3, n_init=10).fit(embed_vecs)

				avg = []
				closest = []
				for j in range(3):
					ix = np.where(kmeans.labels_ == j)[0]
					avg.append(np.mean(ix))
				closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_,\
                                                   embed_vecs)
				ordering = sorted(range(3), key=lambda k: avg[k])
				self.summary[idx] = [self.label2text[idx][closest[ix]] for ix in ordering]
			else:
				self.summary[idx] = self.label2text[idx]

		#dists = pairwise_distances(gmm.means_, self.embeddings.embeddings, metric="cosine")
		# Do k-means to get the summaries instead

		#ind = np.argsort(dists.T,axis=0)[:5,:]
		#ind = np.argsort(d)[::-1][:50]
		#self.summary = {} 
		#for i in range(cluster_no):
  		#	self.summary[i] = [self.embeddings.extracted_posts[ind[l,i]] for l in range(5)]

		self.time_lapse = time.time()-time_start

	def visualization(self):
		# fancy plotting!
		X = self.projmat[:,0]
		Y = self.projmat[:,1]
		data_dict = pd.DataFrame(self.embeddings.extracted_posts, columns=['comment'])
		data_dict['X'] = X
		data_dict['Y'] = Y

		source = ColumnDataSource(data_dict)

		TOOLTIPS = [("Comment", "@comment")]
                    
		plotting_comments = figure(title='Visualized Creditcard Posts', tooltips=TOOLTIPS)

		plotting_comments.circle('X', 'Y', color = 'DarkBlue',alpha=1,source = source)

		plotting_comments.toolbar.logo = None
		plotting_comments.toolbar_location = None

		return plotting_comments


# 2 things to change: run k-means in each cluster to get extractive
# summarization. Figure out how to make pretty figures from here.


