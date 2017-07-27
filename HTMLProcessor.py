""" Extract posts and their reply """
from bs4 import BeautifulSoup as BS
# soup = BS(open("dataset/Topic_ Module 1 Discussion_ Innovation Processes - Social Sector Solutions.htm"),"html.parser")
# print soup.title.string

# json = {"question":question,"responses":[{"response_id":id,"response":response,"comments":[comment]}]}

class ModuleTxt(object):
	"""docstring for ModuleTxt"""
	def __init__(self, topicFile):
		super(ModuleTxt, self).__init__()
		self.topicFile = topicFile
		self.soup = BS(open("dataset/" + topicFile),"html.parser")
		self.questionTxt = self.question()
		self.responseList = self.responses()


	def question(self):
		questionHtml = self.soup.find(class_="message user_content enhanced")
		questionTxt = questionHtml.text.encode("utf-8")
		return questionTxt

	def responses(self):
		responses = []
		entries = self.soup.find(id="discussion_subentries").find('ul',class_="discussion-entries")
		# print entries

		for entry in entries.find_all('li',class_="entry",recursive=False):
			text = entry.find('div', class_="message user_content enhanced")
			if text != None:
				response = {"id":entry.get('id'),"responseText":text.text.encode('utf-8'),"comments":[]}

				#comments
				for li in entry.find('ul',class_='discussion-entries').find_all('li'):
					comment = li.find('div',class_='message user_content enhanced')
					if comment != None:
						# print comment.text.encode('utf-8')
						# print "***"
						response["comments"].append({"comment_id":li.get('id'),"comment":comment.text.encode('utf-8')})

				responses.append(response)
		return responses

	def printResponse(self,num_reponse):
		print self.responseList[num_reponse]["responseText"]

	def printComments(self,num_reponse, num_comment):
		print self.responseList[num_reponse]["comments"][num_comment]["comment"]


if __name__ == '__main__':
	topic1 = "Topic_ Module 1 Discussion_ Innovation Processes - Social Sector Solutions.htm"
	# topic2 = "PFPS Module 1/Topic_ Module 1 Discussion_ Innovation Processes - IBD Team Members page 2.html"
	# topic2 = "Topic_ Module 2 Discussion_ Redesigning Businesses - Social Sector Solutions.html"
	module1 = ModuleTxt(topic1)
	print module1.question()
	# for i,response in enumerate(module1.responses()):
	# 	print "response"+str(i)
	# 	print response["responseText"]
	# 	print "========================"




	
	# print module1.responseList[0]["responseText"]["comments"][1]["comment"]
	# print module1.responseList[14]["comments"][1]["comment"]
	# module1.printResponse(1)
	# module1.printComments(16,1)


