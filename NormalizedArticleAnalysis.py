# keep the number of words from different readings the same


from gensim.utils import smart_open, simple_preprocess, file_or_filename
from gensim.corpora import TextCorpus, Dictionary
from gensim.models.ldamodel import LdaModel
from gensim.parsing.preprocessing import STOPWORDS

from os import listdir, mkdir
from os.path import isfile, join 

from HTMLProcessor import ModuleTxt, ModuleTxtByList
import Config

from gensim.models.tfidfmodel import TfidfModel

import logging

sub_questions = ['What are the similarities and differences among "design thinking", "positive deviance" and "lean start-up"? For example, how are the personal skills or mindsets required by each similar or different?',
'In what ways have the organizations you have worked in supported the development of these skills or mindsets? In what ways might they better support these approaches?',
'Which approaches are likely to be most valuable in the Applied Innovation course you are taking? ',
'What questions do you have about the approaches that you would like to discuss with your classmates?']


class Corpus(object):
	"""docstring for Corpus"""
	def __init__(self, path):
		super(Corpus, self).__init__()
		self.path = path
		self.docs = [] # a list of readings
		self.paragraphs = [] #a list of list of paragraphs
		self.read_data()
		# print self.paragraphs[0]
		### preprocess paragraph
		for x in range(len(self.paragraphs)):
			self.paragraphs[x] = self.preprocessing(self.paragraphs[x])

		self.docs = self.preprocessing(self.docs)

		self.tfidf(self.docs)

		self.build_corpus()

	def build_additional_corpus(self, doc):
		doc = self.preprocessing([unicode(doc,"utf-8")])
		return [self.dictionary.doc2bow(doc[0])]


	def read_data(self):
		dirlist = [x for x in listdir(self.path) if x.endswith(".txt")]
		for fileno, file in enumerate(dirlist):
			# print file
			with file_or_filename(self.path + file) as lines:
				self.docs.append(unicode(lines.read().replace('\n', ''),"utf-8"))
				# print lines
				# self.docs.append(unicode(lines,"utf-8"))
				lines.seek(0)
				self.paragraphs.append([])
				# self.docs.append()
				for lineno, line in enumerate(lines):
					# self.docs.append(unicode(line,"utf-8"))
					self.paragraphs[fileno].append(unicode(line,"utf-8"))
					

	def preprocessing(self,docs):
		# Tokenize the documents
		from nltk.tokenize import RegexpTokenizer
		# print docs[1]


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

		return docs
		

	def build_corpus(self):
		self.corpus_list = []
		for docno, doc in enumerate(self.paragraphs):
			corpus = [self.dictionary.doc2bow(paragraph) for paragraph in doc]
			self.corpus_list.append(corpus)

	def tfidf(self,docs):
		if len(docs) > 1:
			dictionary = Dictionary(docs)

			corpus = [dictionary.doc2bow(doc) for doc in docs]
			# print len(corpus[0])
			# print len(corpus[1])
			# print len(corpus[2])

			tfidf = TfidfModel(corpus)
			# print tfidf

			def topn(doc,n):
				import heapq
				topn = heapq.nlargest(n, (k for k in doc), key=lambda k: k[1])
				new_doc = []
				for t in topn:
					new_doc.append(dictionary[t[0]])
				return new_doc

			docs = []


			for doc in tfidf[corpus]:
				docs.append(topn(doc,505))

		self.docs = docs

		self.dictionary = Dictionary(docs)

		# self.dictionary = Dictionary(docs)
		
		# self.dictionary.filter_extremes(no_below=0,no_above=1,keep_n=500)

		# self.corpus = [self.dictionary.doc2bow(doc) for doc in docs]

		# self.id2word = self.dictionary.id2token

		# print ("2. Number of unique tokens: %d", len(self.dictionary))
		# print ("2. Number of documents: %d", len(self.corpus))		

class NormArticleAnalysis(object):
	"""docstring for Module"""
	def __init__(self, topicNumber, moduleFile, updateModel = False):
		super(NormArticleAnalysis, self).__init__()
		self.updateModel = updateModel
		self.topicNumber = topicNumber
		self.moduleText = ModuleTxtByList(moduleFile)
		self.topicTerm = {}
		self.articleName = ""
		self.lda()

	def vec(self,txt):
		return self.dictionary.doc2bow(txt.lower().split())


	def lda(self):
		article = range(3)
		topicModelFile = "ldaModel/module"+str(self.topicNumber) +  "/normalizedArticle/normalizedArticle"
		if (not isfile(topicModelFile) or self.updateModel):
			logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
			try:
				mkdir("ldaModel/module"+str(self.topicNumber) +  "/normalizedArticle/")
			except Exception as e:
				pass
			corpus= Corpus('pre-processed_data/module'+str(self.topicNumber) + '/')
			dictionary = corpus.dictionary
			# print dictionary.values()
			
			self.ldaModel = LdaModel(corpus=corpus.corpus_list[0], num_topics=Config.TOPIC_NUMBER,id2word=dictionary,passes=100,iterations=400,alpha="auto",eta=0.01)
			self.ldaModel.update(corpus.corpus_list[1])
			self.ldaModel.update(corpus.corpus_list[2])
			self.ldaModel.update(corpus.corpus_list[3])
			self.ldaModel.update(corpus.corpus_list[4])
			addtional_corpus = corpus.build_additional_corpus(self.moduleText.questionTxt)
			self.ldaModel.update(addtional_corpus)
			self.ldaModel.save(topicModelFile)

			self.dictionary = dictionary
			self.dictionary.save("ldaModel/module"+str(self.topicNumber) + "/normalizedArticle/dictionary")
		else:
			self.ldaModel = LdaModel.load(topicModelFile)
			self.dictionary = Dictionary.load("ldaModel/module"+str(self.topicNumber) + "/normalizedArticle/dictionary")

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
		# return self.ldaModel.get_document_topics(self.vec(questionTxt))
		return self.ldaModel[self.vec(questionTxt)]

	def subquestionAnalysis(self,number):
		subquestion = sub_questions[number]
		return self.ldaModel[self.vec(subquestion)]

	def responseAnalysis(self, number):
		response = self.moduleText.responseList[number]
		responseTxt = response["responseText"]
		vec = self.vec(responseTxt)
		disttuple = self.ldaModel[self.vec(responseTxt)]
		# print disttuple
		return self.tuple2vector(disttuple)

	def responsesVector(self):
		for r in range(len(self.moduleText.responseList)):
			responseList = self.responseAnalysis(r)
			# print self.tuple2vector(responseTuple)
			print responseList
	def responseLength(self):
		for response in self.moduleText.responseList:
			print len(response["responseText"].split())

	def tuple2vector(self,disttuple):
		# print disttuple
		distdict = dict((t,v) for t,v in disttuple)
		# print distdict
		elementList = []
		for x in range(Config.TOPIC_NUMBER):
			try:
				elementList.append(distdict[x])
			except Exception as e:
				elementList.append(0)
		# print elementList

		return elementList

	
	def questionVector(self):
		return self.tuple2vector(self.questionAnalysis())

	def subquestionVector(self, i):
		dist = self.subquestionAnalysis(i)
		return self.tuple2vector(dist)


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
		# for topic in self.topicTerm:
		# 	print ("{}:{}".format(topic,self.topicTerm[topic]))
		print self.topicTerm

	def text_vec(self,text):
		return self.tuple2vector(self.ldaModel[self.vec(text)])


def printVec(inlist):
	print (", ".join([str(a) for a in inlist]))

from scipy import spatial

def cos_sim(vec1, vec2):
	return 1-spatial.distance.cosine(vec1,vec2)

def predict_subquestion_answered(topicmodel, seg, questionNum):

	segVec = topicmodel.text_vec(seg)
	min_sim = 1
	subquestion_num = 0
	for x in range(4):
		subquestionVec = topicmodel.subquestionVector(x)
		sim = cos_sim(segVec,subquestionVec)
		if sim<min_sim:
			min_sim = sim
			subquestion_num = x + 1
	print subquestion_num




if __name__ == '__main__':
	def module1():
		# corpus = Corpus('pre-processed_data/topic1/')
		# print corpus.corpus_list
		# print corpus.docs
		# print corpus.paragraphs[0]


		module1 = "Topic_ Module 1 Discussion_ Innovation Processes - Social Sector Solutions.htm"

		articleAnalysis1 = NormArticleAnalysis(1,module1,updateModel=False)
		articleAnalysis1.printTopicTerms()
		# print articleAnalysis1.ldaModel.show_topics(num_topics=Config.TOPIC_NUMBER, num_words=5,formatted=True)

		questionVec = articleAnalysis1.questionVector()
		print questionVec
		print 




		for x in range(22):
			vec =  articleAnalysis1.responseAnalysis(x)
			# print vec 
			print cos_sim(vec,questionVec)

		# vec = articleAnalysis1.responseAnalysis(0)
		# print vec
		# print cos_sim(vec,questionVec)

	def module2():
		module2 = "module 2/Collaborative Innovaiotn Topic_ Week 9 Discussion_ Framing and Reframing.html"
		articleAnalysis2 = NormArticleAnalysis(2, module2,updateModel=False)

		articleAnalysis2.printTopicTerms()
		questionVec = articleAnalysis2.questionVector()
		print questionVec

		for x in range(len(articleAnalysis2.moduleText.responses())):
			vec = articleAnalysis2.responseAnalysis(x)
			print cos_sim(vec,questionVec)

		module2_2 = "module 2/Collaborative Innovation part 2 Topic_ Week 9 Discussion_ Framing and Reframing.html"
		articleAnalysis2_2 = NormArticleAnalysis(2, module2_2,updateModel=False)
		for x in range(len(articleAnalysis2_2.moduleText.responses())):
			vec = articleAnalysis2_2.responseAnalysis(x)
			print cos_sim(vec,questionVec)

		# print len(articleAnalysis2.moduleText.responses())
		# print len(articleAnalysis2_2.moduleText.responses())



	module2()

