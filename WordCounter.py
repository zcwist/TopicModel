from collections import Counter
from os import listdir
from nltk.tokenize import RegexpTokenizer
class WordCounter(object):
	"""docstring for WordCounter"""
	def __init__(self, input):
		super(WordCounter, self).__init__()
		self.input = input
		self.docs = {}
		self.docsname =[]
		self.count()

	def count(self):
		tokenizer = RegexpTokenizer(r'\w+')
		for f in listdir(self.input):
			if f.endswith(".txt"):
				self.docsname.append(f)
				with open(self.input+f) as file:
					doc = (unicode(file.read(),"utf-8"))
					doc = doc.lower()
					tokens = tokenizer.tokenize(doc)
					wordcount = Counter(tokens)
					self.docs[f] = dict(wordcount)
		return self.docs

	def count_in_tm(self, tpjson):
		for topic in tpjson:
			# print ("Topic" + str(topic))
			keywords = tpjson[topic]
			for keyword in keywords:
				count = []
				for paper in self.docsname:
					try:
						count.append(self.docs[paper][keyword])
					except Exception as e:
						count.append(0)
				# print (keyword + ":" + str(count))
				print('{},{},{}'.format(count[0],count[1],count[2]))


if __name__ == '__main__':
	# tpjson = {0: [u'early', u'product', u'test', u'mvp', u'approach'], 1: [u'new', u'company', u'design', u'work', u'plan'], 2: [u'process', u'method', u'behaviour', u'step', u'change'], 3: [u'process', u'entrepreneur', u'hypothesis', u'solution', u'problem'], 4: [u'mvp', u'business', u'hypothesis', u'product', u'approach']}
	tpjson = {0: [u'startup', u'example', u'product', u'new', u'entrepreneur'], 1: [u'product', u'design', u'startup', u'entrepreneur', u'team'], 2: [u'positive', u'deviance', u'child', u'approach', u'bias'], 3: [u'test', u'product', u'entrepreneur', u'mvp', u'customer'], 4: [u'startup', u'customer', u'product', u'business', u'hypothesis']}
	tpjson = {0: [u'deviance', u'local', u'deviant', u'advantage', u'positive'], 1: [u'intervention', u'good', u'outcome', u'new', u'approach'], 2: [u'social', u'accessible', u'successful', u'enthusiasm', u'solution'], 3: [u'deviance', u'change', u'positive', u'family', u'individual'], 4: [u'approach', u'mobilisation', u'increasingly', u'intervention', u'deviance']}
	
	WordCounter("pre-processed_data/topic1/").count_in_tm(tpjson)
		