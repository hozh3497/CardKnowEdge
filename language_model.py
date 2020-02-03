'''
code for embedding
'''

import csv
import logging
import os
import random
import sys

import numpy as np
import torch
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler, TensorDataset
from torch.utils.data.distributed import DistributedSampler
from tqdm import tqdm, trange, tqdm_notebook

#from pytorch_pretrained_bert.file_utils import PYTORCH_PRETRAINED_BERT_CACHE, WEIGHTS_NAME, CONFIG_NAME
from transformers import RobertaConfig, RobertaModel, RobertaTokenizer, RobertaForMaskedLM
#from pytorch_pretrained_bert.tokenization import BertTokenizer

class LanguageModel(object):
	"""docstri model_dir for LanguageModel"""
	def __init__(self, model_dir, cache_dir):
		super(LanguageModel, self).__init__()
		self.model_dir = model_dir
		self.cache_dir = cache_dir
		self.tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
		model_state_dict = torch.load(self.model_dir,map_location='cpu')
		self.model = RobertaModel.from_pretrained(pretrained_model_name_or_path='roberta-base', state_dict=model_state_dict, cache_dir=self.cache_dir)


# functions to prepare input sequence
def prepare_input_seq(input_seq, LM, max_len=128):
    # here prepare the input sequence for the Bert model
    tokens0 = LM.tokenizer.tokenize(input_seq)
    for j,t in enumerate(tokens0):
        if t in [".","?","!"]:
            tokens0[j] = t+" [SEP]"
    tokens = []
    for t in tokens0:
        tokens+=t.split()
    if tokens[-1]!='[SEP]':
        tokens = ['[CLS]'] + tokens + ['[SEP]']
    else:
        tokens = ['[CLS]'] + tokens
    
    if len(tokens)>max_len:
        #padded_tokens=tokens +['[PAD]' for _ in range(max_len-len(tokens))]
    #else:
        padded_tokens = tokens[:max_len]
    else:
        padded_tokens = tokens

    attn_mask=[1 if token != '[PAD]' else 0 for token in padded_tokens]

    segment_ids = []
    current_seg_id = 0
    for token in padded_tokens:
        segment_ids += [current_seg_id]
        if token=="[SEP]":
            current_seg_id += 1

    indexed_tokens = LM.tokenizer.convert_tokens_to_ids(padded_tokens)
    tokens_tensor = torch.tensor([indexed_tokens])
    segments_tensors = torch.tensor([segment_ids])
    attn_mask = torch.tensor([attn_mask])

    return tokens_tensor,segments_tensors,attn_mask

def embed_sents(sents,LM):
	# LM is the language model to be loaded separately.
	id2sent = {j:sent for j,sent in enumerate(sents)}
	emb_mat = np.zeros([len(id2sent),768])
	for j,sent in enumerate(sents):
  		input_seq = sent
  		tokens_tensor,segments_tensors,attn_mask = prepare_input_seq(input_seq,LM,max_len=150)
  		val, hidden = LM.model(tokens_tensor,segments_tensors)
  		emb_mat[j,:] = hidden.detach().numpy()

	return emb_mat



