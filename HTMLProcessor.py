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
				student = ""
				try:
					studentname = entry.find('div',class_="discussion-header-content right-of-avatar").find('div',class_="pull-left span4").find('h2',class_="discussion-title").find('a',class_="author").text.strip()
				except Exception as e:
					print entry.find('div',class_="discussion-header-content right-of-avatar").find('div',class_="pull-left span4").find('h2',class_="discussion-title")
					raise e
				
				response = {"id":entry.get('id'),"student":studentname,"responseText":text.text.encode('utf-8'),"comments":[]}

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

class ModuleTxtByList(ModuleTxt):
	"""docstring for ModuleTxtByList"""
	def __init__(self, topicFile):
		#filter by good answer
		self.namelist = set(["aaya abdelshafy","sarah alsamman","lal altuner","aramis anderson","catalina biggerstaff","alexander cassidy","courtnie chan","inaara charolia","elva chen","justin chen","angela colback","dion dong","marina fraile-romero","shorya ghai","manuel gonzalez","rachel hokanson","samantha holder","iris hou","destiny hwang","reed jones","samantha lamos","akemi levine","stephanie luna-lopez","kathleen masancay","peter phan","nicola phillips","mailess phiri","abhishek punia","zoe randolph","priyanka saiprasad","neil shankar","molly simon","kate simonds","alyssa so","jake trambert","matt whittle","richard wong","irene yu","peggy zhao"])

		#filter by bad answer
		self.namelist = set(["tait adams","anam ahsani","carlos allende bres","shreya chaganti","maggie chen","andrew huang","suzi hyun","sparsh jain","brytni johnston","lauren kirkpatrick","francesca ledesma","xuanzhao li","regina madanguit","alix mcmenamy","john ospina","elmer pangilinan","arsalan qureshi","lauren silver","melissa smith","arvin villadelgado","sharon wang","katherine whitman","lucy zhang","luke zhang"])
		self.student20 =[]
		super(ModuleTxtByList, self).__init__(topicFile)
	
	def responses(self):
		responses = []
		entries = self.soup.find(id="discussion_subentries").find('ul',class_="discussion-entries")
		# print entries

		for entry in entries.find_all('li',class_="entry",recursive=False):
			# print entry
			try:
				studentname = entry.find('h2').find('a').string.strip()
				# print studentname.lower() in self.namelist
				
				if studentname.lower() not in self.namelist:
					continue
				self.student20.append(studentname)

			except Exception as e:
				pass
			

			
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


if __name__ == '__main__':
	def topic1():
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
	def module2():
		module2topic = "module 2/Collaborative Innovaiotn Topic_ Week 9 Discussion_ Framing and Reframing.html"
		module2 = ModuleTxtByList(module2topic)
		# module2 = ModuleTxt(module2topic)

		module2_2topic = "module 2/Collaborative Innovation part 2 Topic_ Week 9 Discussion_ Framing and Reframing.html"
		module2_2 = ModuleTxtByList(module2_2topic)

		from collections import Counter
		studentlist = module2.student20 + module2_2.student20
		print Counter(studentlist)
		print len(studentlist)
		print len(module2.responses())
		print len(module2_2.responses())
	def fall2017():
		module2topic = "Topic_ Week 1_ Reading Reflection.html"
		week1 = ModuleTxt(module2topic)
		for i,response in enumerate(week1.responses()):
			print "response"+str(i+1)
			print response["student"]
			print response["responseText"]
			print "========================"
	fall2017()


