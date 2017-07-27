import csv
import random

dataset = []
with open('Std_Cos.csv','rb') as csvfile:
	spamreader = csv.reader(csvfile,delimiter=',', quotechar="|")
	for row in spamreader:
		# print row
		dataset.append([float(x) for x in row])

# dataset.pop(0)
feature = []
score = []

random.shuffle(dataset)

for response in dataset:
	score.append(response[-1])
	feature.append(response[:-1])

# print feature
# print score
# print feature[0]

from sklearn import svm
train_n = 15
clf = svm.SVR()
clf.fit(feature[0:train_n],score[0:train_n])

# print clf.predict(feature)
for x in range(len(score)):
	if x==train_n:
		print "*****"
	print clf.predict([feature[x]])[0]-score[x]