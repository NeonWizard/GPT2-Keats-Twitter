# -*- coding: utf-8 -*-
from twython import Twython, TwythonError
import gpt_2_simple as gpt2

import os

class Bot:
	def __init__(self):
		# -- initialize twython
		self.twitter = Twython(
			os.environ["CONSUMER_KEY"],
			os.environ["CONSUMER_SECRET"],
			os.environ["ACCESS_TOKEN"],
			os.environ["ACCESS_TOKEN_SECRET"]
		)

		# -- initialize gpt2
		self.gpt2_model_name = os.environ["GPT2_MODEL_NAME"]
		self.gpt2_sess = gpt2.start_tf_sess()
		gpt2.load_gpt2(self.gpt2_sess, model_name=self.gpt2_model_name)

	def generate_post(self):
		# TODO: generate up to <|endoftext|> or equivalent to make exactly one poem
		response = gpt2.generate(
			self.gpt2_sess,
			include_prefix=False,
			model_name=self.gpt2_model_name,
			return_as_list=True,
			length=256,
			temperature=1.0,
			top_k=40
		)[0]
		response = response[:response.rfind("\n")]

def main():
	client = Bot()
	client.generate_post()

if __name__ == "__main__":
	main()