# -*- coding: utf-8 -*-
from gensim.utils import smart_open, simple_preprocess
from gensim.corpora import TextCorpus, Dictionary
from gensim.models.ldamodel import LdaModel
from gensim.parsing.preprocessing import STOPWORDS
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class MyCorpus(TextCorpus):
	"""docstring for MyCorpus"""
	stoplist = set('for a of the and to in'.split())
	def get_texts(self):
		with self.getstream() as lines:
			for lineno, line in enumerate(lines):
				texts = self.tokenize(line)
				yield texts

	def tokenize(self,text):
		return [token for token in simple_preprocess(text) if token not in STOPWORDS]


# corpus = MyCorpus('pre-processed_data/mycorpus.txt')
corpus = MyCorpus('pre-processed_data/topic1/The power of positive deviance.txt')

# print corpus.dictionary.items()

# print dictionary[doc_bow]
lda= LdaModel(corpus=corpus,num_topics=5,id2word=corpus.dictionary,passes=5)

# print lda
print lda.print_topics(5)

test_text = """
With a focus on going through multiple iterations in order to arrive at the best possible products or solutions, all three practices require you to build empathy for stakeholders and be comfortable learning from failure. Instead of seeing failure as something to be avoided at all costs, designers, deviants, and lean start-ups must see failure (their own and others) as valuable opportunities to understand what does or doesn't work when addressing wicked problems. However, the lean start-up framework places a premium on efficiency that I don't think is apparent in the other two approaches.
Although standardized testing loomed large in every classroom, Teach for America recognized that existing education solutions were not effectively addressing the gaps in education. As a result, they promoted experimentation with accountability. Teachers were encouraged to try new practices in the classroom, but had to ground their work in data so we could assess the efficacy of new programs. Additionally, teachers have a close attachment to the students and communities they serve so it was natural and easy to empathize through the process. However, this emphasis on experimentation is not seen during TFA's training and onboarding programs, but I think the focus on standardized processes is necessary during training to ensure all teachers are equipped with at least the basic tools for teaching.
For our SSS project, I think that the most valuable approach will be applying design thinking principles. We're looking to explore how to create a leadership development program and I already find myself discarding possibilities because they don't seem realistic. That's probably not the best practice so I'm excited to hold ideation sessions with my team and client so I can learn from the wild ideas they have and hopefully expand my understanding of what might be possible. 
I would love to hear about anyone's experiences using designing thinking to create programs rather than products. It sounds cool when I'm reading about it, but I'm not sure what it looks like in practice. 
"""
# test_text = """
# The most efficient way to improve health is to use locally available, sustainable, and effective approaches. In the 1970s policy developers tested the concept that public health interventions could be designed around uncommon, beneficial health behaviours that some community members already practised.This concept— known as positive deviance — was used successfully to improve the nutritional status of children in several settings in the 1990s.5–10 Recently, the approach has also been applied to newborn care, child nutrition, rates of contraception, safe sexual practices, and educational outcomes.11–13 In this article we describe how the approach works, the evidence that it is effective, and possible future applications.
# """
# test_text = """
# Some people have questioned the efficiency of the approach, given the presumed limited generalisability of findings from local inquiries and the desire to mobilise each community through self discovery. Practitioners now need to test the assumption that positive deviance is, of necessity, a small scale approach by evaluating the effectiveness of different intensities of inquiry (number per population size). Similarly we should test reformulated approaches, such as a mass media advocacy campaign featuring testimonials by individuals with positive deviant behaviour. Likewise, we should systematically describe and value the additional unintended benefits accrued by communities that have taken part in positive deviance programmes.
# """
# test_text = """Future challenges?"""


new_vec = corpus.dictionary.doc2bow(test_text.lower().split())
# print new_vec
print lda[new_vec]

# test_text2 = """
# These three concepts are all approaches to improve survival (of ideas, health, outputs). They differ, however, in terms of the resources available to the agents employing the concepts (largely, time as the resource). Hypothesis-driven entrepreneurship and its MVP-approach to building viable solutions drives towards incremental improvements using the fewest resources possible. It is a forward-looking approach that tries to anticipate market needs to save time by developing MVP solutions. Positive deviance, however, retroactively analyzes something and then reimagines how this can be improved going forward by homing in on the most successful subjects.
# I previously worked in management consulting, and found traces of each of these concepts in my various projects although they were often disguised. For example, I learned to employ an MVP-approach when doing "Phase 1" or ambiguous analysis in a short period of time. I often had to translate broad concepts such as "How Big is Market X?" into tactical next steps. My teammates conditioned me to ask, "what is the minimum amount of data that I need to prove this theory true or false?" This mindset was crucial on fast-paced projects because it limited me (the analyst) from the distraction of building a robust, seemingly-perfect analysis when the same outcome could have been achieved quicker. I still find this "MVP" / ruthless efficiency important to meeting deadlines today.
# With S3 in mind (mainly the Proposal / Scoping Letter), I am revisiting how I can employ a leaner approach to project work. For example, can our team build (aka produce a smaller, pilot deliverables), measure (aka preview them with clients), and learn (aka incorporate feedback to bolster future analysis)?
# Intrigued to how others channeled these readings in the context of S3.
# """
# new_vec2 = corpus.dictionary.doc2bow(test_text2.lower().split())
# # print new_vec
# print lda[new_vec2]
