# -*- coding: utf-8 -*-
from gensim.utils import smart_open, simple_preprocess, file_or_filename
from gensim.corpora import TextCorpus, Dictionary
from gensim.models.ldamodel import LdaModel
from gensim.parsing.preprocessing import STOPWORDS

from os import listdir, mkdir
from os.path import isfile, join 

from HTMLProcessor import ModuleTxt
from Plot import exportPlot
import Config

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sub_questions = ['What are the similarities and differences among “design thinking”, "positive deviance" and “lean start-up”? For example, how are the personal skills or mindsets required by each similar or different? ',
'In what ways have the organizations you have worked in supported the development of these skills or mindsets? In what ways might they better support these approaches?',
'Which approaches are likely to be most valuable in the Applied Innovation course you are taking? ',
'What questions do you have about the approaches that you would like to discuss with your classmates?']


class MyCorpus(TextCorpus):
	"""docstring for MyCorpus"""
	def get_texts(self):
		for f in listdir(self.input):
			if f. endswith(".txt"):
				with file_or_filename(self.input + f) as lines:
					for lineno, line in enumerate(lines):
						texts = self.tokenize(line)
						yield texts

	def tokenize(self,text):
		return [token for token in simple_preprocess(text) if token not in STOPWORDS]

class NLTKCorpus(object):
	"""docstring for NLTKCorpus"""
	def __init__(self, input):
		super(NLTKCorpus, self).__init__()
		self.input = input
		self.docs = []
		self.read_data(2)
		self.preprocessing()

	def read_data(self):
		for f in listdir(self.input):
			if f.endswith(".txt"):
				with file_or_filename(self.input + f) as lines:
					for lineno, line in enumerate(lines):
						self.docs.append(unicode(line,"utf-8"))

	def read_data(self,readingNum):
		dirlist = [x for x in listdir(self.input) if x.endswith(".txt")]
		file = dirlist[readingNum]
		print file
		with file_or_filename(self.input + file) as lines:
			for lineno, line in enumerate(lines):
				self.docs.append(unicode(line,"utf-8"))

	def preprocessing(self):
		# Tokenize the documents
		docs = self.docs
		from nltk.tokenize import RegexpTokenizer


		tokenizer = RegexpTokenizer(r'\w+')
		for idx in range(len(docs)):
			docs[idx] = docs[idx].lower()
			docs[idx] = tokenizer.tokenize(docs[idx])
		# print docs[0]


		docs = [[token for token in doc if not token.isdigit()] for doc in docs]

		docs = [[token for token in doc if token not in STOPWORDS] for doc in docs]

		docs = [[token for token in doc if len(token)>1] for doc in docs]

		from nltk.stem.wordnet import WordNetLemmatizer
		lemmatizer = WordNetLemmatizer()
		docs = [[lemmatizer.lemmatize(token) for token in doc] for doc in docs]


		# # phrases detection
		# from gensim.models.phrases import Phrases, Phraser
		# bigram = Phraser(Phrases(docs,min_count=5))
		# print (len(docs))
		# for idx in range(len(docs)):
		# 	for token in bigram[docs[idx]]:
		# 		if "_" in token:
		# 			try:
		# 				docs[idx].append(token)
		# 			except Exception as e:
		# 				print idx
		# 				raise(e)

		# print docs[0]
					

		from gensim.corpora import Dictionary

		self.dictionary = Dictionary(docs)

		self.corpus = [self.dictionary.doc2bow(doc) for doc in docs]

		self.id2word = self.dictionary.id2token

		print ("Number of unique tokens: %d", len(self.dictionary))
		print ("Number of documents: %d", len(self.corpus))	

class NLTKTfidfCorpus(NLTKCorpus):
	"""docstring for NLTKTfidfCorpus"""
	def __init__(self, input):
		super(NLTKTfidfCorpus, self).__init__(input)
		self.tfidf()

	def tfidf(self):
		dictionary = self.dictionary
		corpus = self.corpus
		id2word = self.id2word

		from gensim.models.tfidfmodel import TfidfModel

		tfidf = TfidfModel(corpus)

		def topn(doc):
			import heapq
			p = 0.95
			n = int(len(doc)*p)
			topn = heapq.nlargest(n, (k for k in doc), key=lambda k: k[1])
			new_doc = []
			for t in topn:
				new_doc.append(dictionary[t[0]])
			return new_doc

		docs = []

		for doc in tfidf[corpus]:
			docs.append(topn(doc))

		self.dictionary = Dictionary(docs)

		# self.dictionary.filter_extremes(no_below=0,no_above=1,keep_n=500)

		self.corpus = [self.dictionary.doc2bow(doc) for doc in docs]

		self.id2word = self.dictionary.id2token

		print ("2. Number of unique tokens: %d", len(self.dictionary))
		print ("2. Number of documents: %d", len(self.corpus))		

class ModuleAnalysis(object):
	"""docstring for Module"""
	def __init__(self, topicNumber, moduleFile, updateModel = False):
		super(ModuleAnalysis, self).__init__()
		self.updateModel = updateModel
		self.topicNumber = topicNumber
		self.moduleText = ModuleTxt(moduleFile)
		self.topicTerm = {}
		self.lda()

	def vec(self,txt):
		return self.dictionary.doc2bow(txt.lower().split())


	def lda(self):
		topicModelFile = "ldaModel/module"+str(self.topicNumber) + "/module" + str(self.topicNumber)
		if (not isfile(topicModelFile)) or self.updateModel:
			try:
				mkdir("ldaModel/module"+str(self.topicNumber) + "/")
			except Exception as e:
				pass
			self.corpus = MyCorpus('pre-processed_data/topic'+str(self.topicNumber) + '/')
			self.ldaModel= LdaModel(corpus=self.corpus,num_topics=Config.TOPIC_NUMBER,id2word=self.corpus.dictionary,passes=100,iterations=400,alpha=0.1,eta=0.1,)
			self.ldaModel.save(topicModelFile)
			self.dictionary = self.corpus.dictionary
			self.dictionary.save(topicModelFile+"/module"+str(self.topicNumber)+".dictionary")
		else:
			self.ldaModel = LdaModel.load(topicModelFile)
			self.dictionary = Dictionary.load(topicModelFile+"/module"+str(self.topicNumber)+".dictionary")

		self.topicTerm = self.topicTermTuple2Dict()

	def topicTermTuple2Dict(self,num_words=None):
		if not num_words:
			num_words = 5
		topicTermDict = {}
		topicTuple = self.ldaModel.show_topics(num_topics=Config.TOPIC_NUMBER, num_words=num_words,formatted=False)
		for topic in topicTuple:
			terms = []
			for term in topic[1]:
				terms.append(term[0])
			topicTermDict[topic[0]] = terms
		return topicTermDict

	def readingAnalysis(self,number):
		i=0
		path = "pre-processed_data/topic"+str(self.topicNumber)+ '/'
		for f in listdir(path):
			if f.endswith(".txt"):
				i += 1
				if i == number:
					with file_or_filename(path + f) as file:
						reading = file.read()
						return self.ldaModel[self.vec(reading)]

	def questionAnalysis(self):
		questionTxt = self.moduleText.questionTxt
		return self.ldaModel[self.vec(questionTxt)]

	def subquestionAnalysis(self,number):
		subquestion = sub_questions[number]
		return self.ldaModel[self.vec(subquestion)]

	def responseAnalysis(self, number):
		response = self.moduleText.responseList[number]
		responseTxt = response["responseText"]
		return self.ldaModel[self.vec(responseTxt)]

	def commentAnalysis(self,response_num,comment_num):
		commentTxt = self.moduleText.responseList[response_num]["comments"][comment_num]['comment']
		return self.ldaModel[self.vec(commentTxt)]

	# Plot with topic terms
	def plotReading(self,number):
		exportPlot(self.readingAnalysis(number),self.topicTerm,"Reading"+str(number))

	def plotQuestion(self):
		exportPlot(self.questionAnalysis(),self.topicTerm,"Question")

	def plotResponse(self,number):
		dist = self.responseAnalysis(number)
		exportPlot(dist,self.topicTerm,"response-"+str(number))

	def plotComment(self,response_num,comment_num):
		dist = self.commentAnalysis(response_num, comment_num)
		exportPlot(dist,self.topicTerm,"comment-"+str(response_num)+"-"+str(comment_num))

	def allResponseAndComment(self):
		for r in range(len(self.moduleText.responseList)):
			self.plotResponse(r)
			for c in range(len(self.moduleText.responseList[r]["comments"])):
				self.plotComment(r,c)
	def printTopicTerms(self):
		# topicTuple = self.ldaModel.show_topics(num_topics=Config.TOPIC_NUMBER, num_words=num_words,formatted=False)
		# for topic in topicTuple:
		# 	terms = []
		# 	for term in topic[1]:
		# 		terms.append(term[0])
		# 	print "topic" + str(topic[0]) + ":" + str(terms)
		print self.topicTerm

class ModuleAnalysisNLTK(ModuleAnalysis):
	"""docstring for ModuleAnalysisNLTK"""
	def __init__(self, topicNumber, moduleFile, updateModel = False):
		super(ModuleAnalysisNLTK, self).__init__(topicNumber, moduleFile, updateModel)

	def lda(self):
		topicModelFile = "ldaModel/module"+str(self.topicNumber) + "/module" + str(self.topicNumber)
		if (not isfile(topicModelFile)) or self.updateModel:
			try:
				mkdir("ldaModel/module"+str(self.topicNumber) + "/")
			except Exception as e:
				pass
			self.corpus = NLTKTfidfCorpus('pre-processed_data/topic'+str(self.topicNumber) + '/')
			self.ldaModel= LdaModel(corpus=self.corpus.corpus,num_topics=Config.TOPIC_NUMBER,id2word=self.corpus.dictionary,passes=100,iterations=400,alpha=0.1,eta=0.1,)
			self.ldaModel.save(topicModelFile)
			self.dictionary = self.corpus.dictionary
			self.dictionary.save("ldaModel/module"+str(self.topicNumber) + "/dictionary")
		else:
			self.ldaModel = LdaModel.load(topicModelFile)
			self.dictionary = Dictionary.load("ldaModel/module"+str(self.topicNumber) + "/dictionary")


		self.topicTerm = self.topicTermTuple2Dict()

		

if __name__ == '__main__':
	module1 = "Topic_ Module 1 Discussion_ Innovation Processes - Social Sector Solutions.htm"
	
	moduleAnalysis = ModuleAnalysisNLTK(1,module1, updateModel=False)
	# moduleAnalysis.plotQuestion()
	# moduleAnalysis.allResponseAndComment()
	# print moduleAnalysis.commentAnalysis(14,1)

	moduleAnalysis.printTopicTerms()

	# moduleAnalysis = ModuleAnalysisNLTK(1,module1, updateModel=False)
	# print moduleAnalysis.subquestionAnalysis(0)
	# moduleAnalysis.plotQuestion()
	# moduleAnalysis.allResponseAndComment()
	# moduleAnalysis.printTopicTerms()
	# print moduleAnalysis.readingAnalysis(1)
	# moduleAnalysis.plotReading(1)
	# moduleAnalysis.plotReading(2)
	# moduleAnalysis.plotReading(3)

		