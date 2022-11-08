import joblib
import pandas as pd
import numpy as np

from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2, SelectPercentile
from sklearn.metrics import fbeta_score
from sklearn.model_selection import KFold

import classification_tools.preprocessing as prp
import classification_tools as clt


def print_progress_bar(iteration):
	"""
	Print a progress bar for command-line interface training
	"""
	percent = ("{0:.1f}").format(100 * (iteration / float(50)))
	filledLength = int(iteration)
	bar = '█' * filledLength + '-' * (50 - filledLength)
	prefix = "Progress:"
	suffix = "Complete"
	printEnd = "\r"
	print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
	if iteration == 50: 
		print()

def confidence_propagation_single(tactics_confidence_list, technique_name, technique_confidence_score):
	"""
	Modify predictions and confidence scores of one technique  using a boosting method depending on this
	technique's and its related tactics' confidence score.
	"""
	new_confidence_score = technique_confidence_score
	i = 0
	for tactic in clt.CODE_TACTICS:
		if not clt.TACTICS_TECHNIQUES_RELATIONSHIP_DF.loc[clt.TACTICS_TECHNIQUES_RELATIONSHIP_DF[tactic] == technique_name].empty:
			lambdaim = 1/(np.exp(abs(technique_confidence_score-tactics_confidence_list[tactic])))
			new_confidence_score = new_confidence_score + lambdaim * tactics_confidence_list[tactic]
		i = i+1
	return new_confidence_score

def confidence_propagation( predprob_tactics, pred_techniques, predprob_techniques):
	"""
	Modify predictions and confidences scores of all techniques of the whole set using 
	confidence_propagation_single function.
	"""
	pred_techniques_corrected = pred_techniques
	predprob_techniques_corrected = predprob_techniques
	tactics_confidence_df = pd.DataFrame(data = predprob_tactics, columns = clt.CODE_TACTICS)
	for j in range(len(predprob_techniques[0])):
		for i in range(len(predprob_techniques)):
			predprob_techniques_corrected[i][j] = confidence_propagation_single(tactics_confidence_df[i:(i+1)], clt.CODE_TECHNIQUES[j], predprob_techniques[i][j])
			if predprob_techniques_corrected[i][j] >= float(0) :
				pred_techniques_corrected[i][j] = int(1)
			else:
				pred_techniques_corrected[i][j] = int(0)
	return pred_techniques_corrected, predprob_techniques_corrected

def hanging_node(pred_tactics, predprob_tactics, pred_techniques, predprob_techniques, c, d):
	"""
	Modify prediction of techniques depending on techniques and related tactics confidence score on a
	threshold basis.
	"""
	predprob_techniques_corrected = pred_techniques
	for i in range(len(pred_techniques)):
		for j in range(len(pred_techniques[0])):
			for k in range(len(pred_tactics[0])):
				if not clt.TACTICS_TECHNIQUES_RELATIONSHIP_DF.loc[clt.TACTICS_TECHNIQUES_RELATIONSHIP_DF[clt.CODE_TACTICS[k]] == clt.CODE_TECHNIQUES[j]].empty:
					if predprob_techniques[i][j] < c and predprob_techniques[i][j] > 0 and predprob_tactics[i][k] < d:
						predprob_techniques_corrected[i][k] = 0 
	return predprob_techniques_corrected

def combinations(c, d):
	"""
	Compute all combinations possible between c and d and their derived values.
	"""
	c_list = [c-0.1, c, c+0.1]
	d_list = [d-0.1, d, d+0.1]
	possibilities = []
	for cl in c_list:
		for dl in d_list:
			possibilities.append([cl, dl])
	return possibilities

def hanging_node_threshold_comparison(pred_tactics, predprob_tactics, pred_techniques, predprob_techniques, known_pred_techniques, permutations):
	"""
	Using different combinations of thresholds retrieve all the F0.5 score macro-averaged between the
	post-processed predictions and the true labels.
	"""
	f05list = []
	for pl in permutations:
		f05list_temp = [pl]
		new_pred_techniques = hanging_node(pred_tactics, predprob_tactics, pred_techniques, predprob_techniques, pl[0], pl[1])
		f05list_temp.append(fbeta_score(known_pred_techniques, new_pred_techniques, beta=0.5, average='macro'))
		f05list.append(f05list_temp)
	return f05list

