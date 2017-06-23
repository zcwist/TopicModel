import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import Config

sns.set_style("whitegrid")

def tuple2dataframe(dist_tup, term_dict = None):
	dist = {"topic":[],"p":[]}
	new_dist = dict(dist_tup)
	for i in range(Config.TOPIC_NUMBER):
		if i not in new_dist.keys():
			new_dist[i]=0

	if not term_dict:
		for topic_num in new_dist:
			dist["topic"].append(topic_num)
			dist["p"].append(new_dist[topic_num])
	else:
		for topic_num in new_dist:
			dist["topic"].append("\n".join(term_dict[topic_num]))
			dist["p"].append(new_dist[topic_num])

	return pd.DataFrame(dist)

def printPlot(distribution,term_dict=None):
	
	ax = sns.barplot(x="topic",y="p",data=tuple2dataframe(distribution,term_dict))
	ax.set(xlabel='topic distribution', ylabel="p")
	sns.plt.subplots_adjust(bottom=0.2)
	sns.plt.show()

def exportPlot(distribution,term_dict=None, figureName = None):
	plt.figure()
	ax = sns.barplot(x="topic",y="p",data=tuple2dataframe(distribution,term_dict))
	ax.set(xlabel='topic distribution', ylabel="p")
	plt.subplots_adjust(bottom=0.2)
	if figureName != None:
		# ax.fig.suptitle(figureName)
		plt.savefig("figure/"+figureName+".png")
	else:
		plt.show()
	plt.close()

if __name__ == '__main__':
	distribution = [(0, 0.31115421546141092), (1, 0.28943865269651226), (2, 0.24663006417201064), (3, 0.12016249528886951), (4, 0.032614572381196666)]
	term_dict = {0: [u'product', u'new', u'design', u'customers', u'business'], 1: [u'startup', u'product', u'test', u'lean', u'tests'], 2: [u'product', u'feedback', u'entrepreneurs', u'entrepreneur', u'model'], 3: [u'product', u'new', u'customer', u'design', u'startup'], 4: [u'design', u'business', u'approach', u'new', u'model']}

	# printPlot(distribution,term_dict)
	exportPlot(distribution,term_dict,"figure")
	# print dict(distribution)
