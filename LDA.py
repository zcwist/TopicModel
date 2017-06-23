# -*- coding: utf-8 -*-
from gensim.utils import smart_open, simple_preprocess, file_or_filename
from gensim.corpora import TextCorpus, Dictionary
from gensim.models.ldamodel import LdaModel
from gensim.parsing.preprocessing import STOPWORDS

from os import listdir
from os.path import isfile, join

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

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

corpus = MyCorpus('pre-processed_data/topic1/')

lda= LdaModel(corpus=corpus,num_topics=5,id2word=corpus.dictionary,passes=100,iterations=400)

# for topic in lda.print_topics(5):
# 	print topic

# test_text = """
# With a focus on going through multiple iterations in order to arrive at the best possible products or solutions, all three practices require you to build empathy for stakeholders and be comfortable learning from failure. Instead of seeing failure as something to be avoided at all costs, designers, deviants, and lean start-ups must see failure (their own and others) as valuable opportunities to understand what does or doesn't work when addressing wicked problems. However, the lean start-up framework places a premium on efficiency that I don't think is apparent in the other two approaches.
# Although standardized testing loomed large in every classroom, Teach for America recognized that existing education solutions were not effectively addressing the gaps in education. As a result, they promoted experimentation with accountability. Teachers were encouraged to try new practices in the classroom, but had to ground their work in data so we could assess the efficacy of new programs. Additionally, teachers have a close attachment to the students and communities they serve so it was natural and easy to empathize through the process. However, this emphasis on experimentation is not seen during TFA's training and onboarding programs, but I think the focus on standardized processes is necessary during training to ensure all teachers are equipped with at least the basic tools for teaching.
# For our SSS project, I think that the most valuable approach will be applying design thinking principles. We're looking to explore how to create a leadership development program and I already find myself discarding possibilities because they don't seem realistic. That's probably not the best practice so I'm excited to hold ideation sessions with my team and client so I can learn from the wild ideas they have and hopefully expand my understanding of what might be possible. 
# I would love to hear about anyone's experiences using designing thinking to create programs rather than products. It sounds cool when I'm reading about it, but I'm not sure what it looks like in practice. 
# """
# # test_text = """
# # The most efficient way to improve health is to use locally available, sustainable, and effective approaches. In the 1970s policy developers tested the concept that public health interventions could be designed around uncommon, beneficial health behaviours that some community members already practised.This concept— known as positive deviance — was used successfully to improve the nutritional status of children in several settings in the 1990s.5–10 Recently, the approach has also been applied to newborn care, child nutrition, rates of contraception, safe sexual practices, and educational outcomes.11–13 In this article we describe how the approach works, the evidence that it is effective, and possible future applications.
# # """
# # test_text = """
# # Some people have questioned the efficiency of the approach, given the presumed limited generalisability of findings from local inquiries and the desire to mobilise each community through self discovery. Practitioners now need to test the assumption that positive deviance is, of necessity, a small scale approach by evaluating the effectiveness of different intensities of inquiry (number per population size). Similarly we should test reformulated approaches, such as a mass media advocacy campaign featuring testimonials by individuals with positive deviant behaviour. Likewise, we should systematically describe and value the additional unintended benefits accrued by communities that have taken part in positive deviance programmes.
# # """
# # test_text = """Future challenges?"""
# test_text = """
# Part of innovation is taking what you experience, including what you read, and thinking about the missing pieces, the next steps, or just something you are curious about. In each module of PFPS, you will do so with one or more of the readings from that week by considering the application of the concepts in the readings to your own life and work, capturing your thoughts on the Discussions pages in bCourses and responding to your classmates’ posts.

# This week’s introductory readings ask you to consider “design thinking”, "positive deviance" and “lean start-up” (aka hypothesis-driven entrepreneurship) frameworks, the basic mindsets and capabilities that underlie them and how they might play out in your lives or the organizations you work in.  As you read, think about the parallels and differences among the three approaches to innovation.

# Compose a thoughtful answer to the questions: what are the similarities and differences among “design thinking”, "positive deviance" and “lean start-up”?  For example, how are the personal skills or mindsets required by each similar or different?  In what ways have the organizations you've worked in supported the development of these skills or mindsets? In what ways might they better support these approaches? Which approaches are likely to be most valuable in the Applied Innovation course you are taking?  What questions do you have about the approaches that you would like to discuss with your classmates?  Be specific in your responses.  

# Post your response, including questions for your classmates, on bCourses and then respond to at least two of your classmates.

# General Guidelines for Discussion: Be thoughtful, constructive and inclusive.  In your responses, be kind, present objections or different points of view open to the possibility that there may be a reasonable response, and object to the responses rather than to the people.  Objections are fine, but you can also choose to be constructive, and you needn't repeat the same objection multiple times.  Be inclusive in your contributions, acknowledging previous contributions, avoiding unnecessarily offensive examples.  It is perfectly alright to raise questions that may seem to you to be unsophisticated or uninformed.  This is a place to learn and explore.  There are no right or wrong answers.

# """


# new_vec = corpus.dictionary.doc2bow(test_text.lower().split())
# # print new_vec
# print lda[new_vec]

		