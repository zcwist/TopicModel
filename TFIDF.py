from ModuleAnalysis import *
from gensim.models.tfidfmodel import TfidfModel

def getKey(item):
	return item[1]

if __name__ == '__main__':
	topicNumber = 1
	corpus = NLTKCorpus('pre-processed_data/topic'+str(topicNumber) + '/')
	# print corpus.dictionary
	# print corpus.corpus
	tfidf = TfidfModel(corpus.corpus,id2word=corpus.dictionary)
	# print tfidf
	# doc1 = tfidf[corpus.corpus][0]
	# sorted_doc1 = sorted(doc1, key=getKey)
	# # print sorted_doc1
	# for word in sorted_doc1:
	# 	print (corpus.dictionary[word[0]],word[1])

	def topn(doc):
		# print doc
		import heapq
		p = 0.8
		n = int(len(doc)*p)
		topn = heapq.nlargest(n, (k for k in doc), key=lambda k: k[1])
		new_doc = []
		for t in topn:
			new_doc.append(corpus.dictionary[t[0]])
		return new_doc

	# print topn(tfidf[corpus.corpus][0])

	for doc in tfidf[corpus.corpus]:
		print topn(doc)
