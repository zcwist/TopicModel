
from gensim.utils import smart_open, simple_preprocess, file_or_filename
from gensim.corpora import TextCorpus, Dictionary
from gensim.models.ldamodel import LdaModel
from gensim.parsing.preprocessing import STOPWORDS

from os import listdir, mkdir
from os.path import isfile, join 

from HTMLProcessor import ModuleTxt
import Config

import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sub_questions = ['What are the similarities and differences among "design thinking", "positive deviance" and "lean start-up"? For example, how are the personal skills or mindsets required by each similar or different?',
'In what ways have the organizations you have worked in supported the development of these skills or mindsets? In what ways might they better support these approaches?',
'Which approaches are likely to be most valuable in the Applied Innovation course you are taking? ',
'What questions do you have about the approaches that you would like to discuss with your classmates?']


class Corpus(object):
	"""docstring for Corpus"""
	def __init__(self, path, articleNum):
		super(Corpus, self).__init__()
		self.path = path
		self.articleNum = articleNum
		self.docs = []
		self.read_data()
		self.preprocessing()
		self.tfidf()

	def read_data(self):
		readingNum = self.articleNum
		dirlist = [x for x in listdir(self.path) if x.endswith(".txt")]
		file = dirlist[readingNum]
		print file
		with file_or_filename(self.path + file) as lines:
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

		# print ("Number of unique tokens: %d", len(self.dictionary))
		# print ("Number of documents: %d", len(self.corpus))	
		

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

		self.corpus = [self.dictionary.doc2bow(doc) for doc in docs]

		self.id2word = self.dictionary.id2token

		# print ("2. Number of unique tokens: %d", len(self.dictionary))
		# print ("2. Number of documents: %d", len(self.corpus))		

class ArticleAnalysis(object):
	"""docstring for Module"""
	def __init__(self, topicNumber, moduleFile, readingNum, updateModel = False):
		super(ArticleAnalysis, self).__init__()
		self.updateModel = updateModel
		self.topicNumber = topicNumber
		self.moduleText = ModuleTxt(moduleFile)
		self.readingNum = readingNum
		self.topicTerm = {}
		self.articleName = ""
		self.lda()

	def vec(self,txt):
		return self.dictionary.doc2bow(txt.lower().split())


	def lda(self):
		topicModelFile = "ldaModel/module"+str(self.topicNumber) +  "/article" + str(self.readingNum) + "/article" + str(self.readingNum)
		if (not isfile(topicModelFile)) or self.updateModel:
			try:
				mkdir("ldaModel/module"+str(self.topicNumber) + "/article" + str(self.readingNum) + "/")
			except Exception as e:
				pass
			self.corpus = Corpus('pre-processed_data/topic'+str(self.topicNumber) + '/', self.readingNum)
			self.ldaModel= LdaModel(corpus=self.corpus.corpus,num_topics=Config.TOPIC_NUMBER,id2word=self.corpus.dictionary,passes=100,iterations=400,alpha="auto",eta=0.01,)
			self.ldaModel.save(topicModelFile)
			self.dictionary = self.corpus.dictionary
			self.dictionary.save("ldaModel/module"+str(self.topicNumber) + "/article" + str(self.readingNum) + "/dictionary")
		else:
			self.ldaModel = LdaModel.load(topicModelFile)
			self.dictionary = Dictionary.load("ldaModel/module"+str(self.topicNumber) + "/article" + str(self.readingNum)+ "/dictionary")


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

	def responsesVector(self):
		for r in range(len(self.moduleText.responseList)):
			responseTuple = self.responseAnalysis(r)
			# print self.moduleText.responseList[r]	
			# responseVec = [x[1] for x in responseTuple]
			# wordlength = len(self.moduleText.responseList[r]["responseText"].split())
			# responseVec.insert(0,wordlength)
			# print responseVec
			print self.tuple2vector(responseTuple)
	def responseLength(self):
		for response in self.moduleText.responseList:
			print len(response["responseText"].split())

	def tuple2vector(self,disttuple):
		distdict = dict((t,v) for t,v in disttuple)
		elementList = []
		for x in range(Config.TOPIC_NUMBER):
			try:
				elementList.append(distdict[x])
			except Exception as e:
				elementList.append(0)

		return elementList

	
	def questionVector(self):
		print self.tuple2vector(self.questionAnalysis())

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
		for topic in self.topicTerm:
			print ("{}:{}".format(topic,self.topicTerm[topic]))
		# print self.topicTerm

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
	module1 = "Topic_ Module 1 Discussion_ Innovation Processes - Social Sector Solutions.htm"

	articleAnalysis1 = ArticleAnalysis(1,module1,0,updateModel=False)
	articleAnalysis2 = ArticleAnalysis(1,module1,1,updateModel=False)
	articleAnalysis3 = ArticleAnalysis(1,module1,2,updateModel=False)
	seg = "With a focus on going through multiple iterations in order to arrive at the best possible products or solutions, all three practices require you to build empathy for stakeholders and be comfortable learning from failure. Instead of seeing failure as something to be avoided at all costs, designers, deviants, and lean start-ups must see failure (their own and others) as valuable opportunities to understand what does or doesn't work when addressing wicked problems. However, the lean start-up framework places a premium on efficiency that I don't think is apparent in the other two approaches."
	seg = "Although standardized testing loomed large in every classroom, Teach for America recognized that existing education solutions were not effectively addressing the gaps in education. As a result, they promoted experimentation with accountability. Teachers were encouraged to try new practices in the classroom, but had to ground their work in data so we could assess the efficacy of new programs. Additionally, teachers have a close attachment to the students and communities they serve so it was natural and easy to empathize through the process. However, this emphasis on experimentation is not seen during TFA's training and onboarding programs, but I think the focus on standardized processes is necessary during training to ensure all teachers are equipped with at least the basic tools for teaching."
	seg = "For our SSS project, I think that the most valuable approach will be applying design thinking principles. We're looking to explore how to create a leadership development program and I already find myself discarding possibilities because they don't seem realistic. That's probably not the best practice so I'm excited to hold ideation sessions with my team and client so I can learn from the wild ideas they have and hopefully expand my understanding of what might be possible."
	# seg = "I would love to hear about anyone's experiences using designing thinking to create programs rather than products. It sounds cool when I'm reading about it, but I'm not sure what it looks like in practice."
	predict_subquestion_answered(articleAnalysis1,seg,1)
	predict_subquestion_answered(articleAnalysis2,seg,1)
	predict_subquestion_answered(articleAnalysis3,seg,1)
	# articleAnalysis.printTopicTerms()
	# articleAnalysis.questionVector()
	# articleAnalysis.responsesVector()
	# articleAnalysis.responseLength()
	# articleAnalysis.subquestionVector(0)