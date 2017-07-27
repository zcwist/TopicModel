from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import RegexpTokenizer
import os
import collections
from HTMLProcessor import ModuleTxt

tokenizer = RegexpTokenizer(r'\w+')
def tokenize(words):
	words = unicode(words,"utf-8").lower()
	words = tokenizer.tokenize(words)
	words = [word for word in words if not word.isdigit()]
	return words



class LabeledLineSentence(object):
	"""docstring for LabeledLineSentence"""
	def __init__(self, path, tokens_only = False):
		super(LabeledLineSentence, self).__init__()
		self.path = path
		self.tokens_only = tokens_only
		self.doc_list = [f for f in os.listdir(self.path) if f.endswith(".txt")]
	def __iter__(self):
		for fid, file in enumerate(self.doc_list):
			for uid, line in enumerate(open(os.path.join(self.path,file))):
				words = tokenize(line)
				if self.tokens_only:
					yield words
				else:
					yield TaggedDocument(words=words, tags=['Doc_%s_SENT_%s' %(fid,uid)])

class MyDoc2Vec(object):
	"""docstring for MyDoc2Vec"""
	def __init__(self, update = False):
		super(MyDoc2Vec, self).__init__()
		self.update = update
		if update:
			self.updateModel()
		else:
			self.model = Doc2Vec.load("doc2vec.model")

	def updateModel(self):
		filename = "pre-processed_data/topic1/"
		trainDoc = LabeledLineSentence(filename)
		model = Doc2Vec(size=50, min_count=1, iter=100)
		model.build_vocab(trainDoc)
		model.train(trainDoc, total_examples = model.corpus_count, epochs = model.iter)
		model.save("doc2vec.model")
		self.model = model

	def test(self):
	 	model = self.model
	 	filename = "pre-processed_data/topic1/"	
		trainDoc = LabeledLineSentence(filename)
		ranks = []
		for para in trainDoc:
			inferred_vector = model.infer_vector(para.words)
			sims = model.docvecs.most_similar([inferred_vector], topn = len(model.docvecs))
			rank = [doc_tag for doc_tag, sim in sims].index(para.tags[0])
			ranks.append(rank)
		counter = collections.Counter(ranks)
		print (counter.most_common(1),sum(counter.values()))

	def getVector(self, newPara):
		tokenized = tokenize(newPara)
		tokenized = filter(lambda x:x in self.model.wv.vocab, tokenized)
		inferred_vector = self.model.infer_vector(tokenized,steps=100)
		return inferred_vector

if __name__ == '__main__':
	score = [1,1.3,0.8,0,0.8,1.2,1.5,0.7,0.8,0.3,2,1.7,2,1.5,0.3,0.8,0.7,0,0.3,0.3,2,1.7]
	
	def cos_sim():
		from scipy import spatial
		from sklearn import linear_model
		model = MyDoc2Vec()
		topic1 = "Topic_ Module 1 Discussion_ Innovation Processes - Social Sector Solutions.htm"
		module1 = ModuleTxt(topic1)
		# print module1.question()
		questionVec = model.getVector(module1.question())
		similarities = []
		for i,response in enumerate(module1.responses()):
			responseVec = model.getVector(response["responseText"])
			# print responseVec
			similarities.append([spatial.distance.cosine(questionVec, responseVec)])
			print similarities[i]
		reg = linear_model.LinearRegression()
		reg.fit(similarities, score)

		print reg.coef_

	cos_sim()


