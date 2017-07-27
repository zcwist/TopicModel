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
		print self.docsname
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
				print('{},{},{},{}'.format(keyword,count[0],count[1],count[2]))


if __name__ == '__main__':
	tpjson = {0: [u'early', u'product', u'test', u'mvp', u'approach'], 1: [u'new', u'company', u'design', u'work', u'plan'], 2: [u'process', u'method', u'behaviour', u'step', u'change'], 3: [u'process', u'entrepreneur', u'hypothesis', u'solution', u'problem'], 4: [u'mvp', u'business', u'hypothesis', u'product', u'approach']}
	tpjson = {0: [u'mobilisation', u'social', u'successful', u'local', u'concept'], 1: [u'intervention', u'change', u'approach', u'social', u'deviance'], 2: [u'new', u'behaviour', u'improved', u'child', u'likely'], 3: [u'people', u'uncommon', u'example', u'identify', u'good'], 4: [u'outcome', u'deviance', u'individual', u'approach', u'factor']}
	juliaJson = {0:
				[u"complexity",u"organizational",u"culture",u"simplicity",u"humanize"],
				1:
				[u"behavior",u"behaviour",u"change",u"social",u"mobilisation",u"health",u"information",u"gathering",u"implementation",u"testing"],
				2:
				[u"falsifiable",u"mvp",u"business",u"model",u"product",u"market",u"fit",u"early",u"adopter",u"feedback",u"uncertainty",u"pivot"]}
	tpjson = {0: [u'uncommon', u'people', u'increasingly', u'deviance', u'identify'], 1: [u'change', u'deviance', u'behaviour', u'adoption', u'encourage'], 2: [u'approach', u'individual', u'local', u'deviance', u'outcome'], 3: [u'finding', u'approach', u'design', u'new', u'intervention'], 4: [u'work', u'health', u'practice', u'nutrition', u'sustainable']}
	tpjson = {0: [u'approach', u'identify', u'new', u'people', u'example'], 1: [u'deviance', u'behaviour', u'adopt', u'change', u'positive'], 2: [u'local', u'deviance', u'need', u'mobilisation', u'positive'], 3: [u'approach', u'factor', u'good', u'outcome', u'change'], 4: [u'deviance', u'intervention', u'practice', u'status', u'policy']}
	tpjson = {0: [u'health', u'individual', u'inquiry', u'behavioural', u'deviance'], 1: [u'deviance', u'uncommon', u'example', u'policy', u'people'], 2: [u'intervention', u'approach', u'child', u'practice', u'sustainable'], 3: [u'change', u'behaviour', u'deviance', u'positive', u'outcome'], 4: [u'approach', u'mobilisation', u'new', u'successful', u'non']}
	tpjson = {0: [u'logical', u'putting', u'process', u'friend', u'flash'], 1: [u'internal', u'need', u'globalize', u'established', u'developing'], 2: [u'firm', u'depended', u'melissa', u'exploration', u'iterate'], 3: [u'tougher', u'operational', u'clear', u'craze', u'predictable'], 4: [u'stance', u'success', u'encourage', u'uncovers', u'cost']}
	tpjson = {0: [u'decision', u'sense', u'partner', u'human', u'changing'], 1: [u'child', u'behaviour', u'intervention', u'deviance', u'local'], 2: [u'behaviour', u'implementation', u'deviance', u'product', u'customer'], 3: [u'positive', u'community', u'deviance', u'improve', u'identify'], 4: [u'founder', u'demand', u'uncertainty', u'data', u'big']}
	tpjson = {0: [u'positive', u'community', u'improve', u'identify', u'explain'], 1: [u'behaviour', u'conducted', u'requires', u'adoption', u'encourage'], 2: [u'bias', u'set', u'team', u'help', u'partner'], 3: [u'child', u'deviance', u'behaviour', u'intervention', u'local'], 4: [u'founder', u'demand', u'uncertainty', u'idea', u'consider']}
	tpjson = {0: [u'response', u'question', u'innovation', u'thoughtful', u'post'], 1: [u'community', u'deviance', u'identify', u'advantage', u'study'], 2: [u'skill', u'deviance', u'valuable', u'applied', u'behaviour'], 3: [u'monitor', u'evaluation', u'implementation', u'founder', u'entrepreneur'], 4: [u'positive', u'start', u'development', u'likely', u'concept']}
	tpjson = {0: [u'finding', u'conducted', u'mass', u'monitor', u'confirm'], 1: [u'technical', u'customer', u'product', u'market', u'early'], 2: [u'positive', u'community', u'improve', u'identify', u'status'], 3: [u'compared', u'effect', u'asset', u'despite', u'trial'], 4: [u'behaviour', u'child', u'deviance', u'intervention', u'local']}
	tpjson = {0: [u'response', u'question', u'innovation', u'organization', u'thoughtful'], 1: [u'technical', u'customer', u'product', u'feature', u'idea'], 2: [u'valuable', u'applied', u'deviance', u'child', u'behaviour'], 3: [u'skill', u'deviance', u'similar', u'behaviour', u'community'], 4: [u'positive', u'start', u'development', u'concept', u'likely']}
	tpjson = {0: [u'deviance', u'community', u'maker', u'effectiveness', u'university'], 1: [u'positive', u'start', u'development', u'concept', u'likely'], 2: [u'response', u'question', u'innovation', u'organization', u'thoughtful'], 3: [u'receiving', u'discover', u'observe', u'enabling', u'factor'], 4: [u'skill', u'valuable', u'applied', u'deviance', u'behaviour']}
	tpjson = {0: [u'positive', u'start', u'deviance', u'development', u'likely'], 1: [u'response', u'question', u'innovation', u'thoughtful', u'organization'], 2: [u'implementation', u'deviance', u'behaviour', u'founder', u'market'], 3: [u'behaviour', u'deviance', u'product', u'customer', u'implementation'], 4: [u'skill', u'valuable', u'applied', u'deviance', u'child']}

	# mvp = {0:[u"mvp"]};
	WordCounter("pre-processed_data/topic1/").count_in_tm(tpjson)
		