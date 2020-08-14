# -*- coding: utf-8 -*-
from twython import Twython, TwythonError
import gpt_2_simple as gpt2

import os
import sys

class Bot:
	def __init__(self):
		# -- initialize twython
		self.twitter = Twython(
			os.environ["CONSUMER_KEY"],
			os.environ["CONSUMER_SECRET"],
			os.environ["ACCESS_TOKEN"],
			os.environ["ACCESS_TOKEN_SECRET"]
		)
		self.twitter_screen_name = self.twitter.verify_credentials()["screen_name"]

		# -- initialize gpt2
		self.gpt2_model_name = os.environ["GPT2_MODEL_NAME"]
		self.gpt2_sess = gpt2.start_tf_sess()
		gpt2.load_gpt2(self.gpt2_sess, model_name=self.gpt2_model_name)

	def generate_post(self):
		print("Generating post... ", end=""); sys.stdout.flush()
		response = gpt2.generate(
			self.gpt2_sess,
			include_prefix=False,
			model_name=self.gpt2_model_name,
			return_as_list=True,
			length=183,
			temperature=1.0,
			top_k=40,
			truncate="<|endoftext|>"
		)[0]
		print(response)

		# split all generated lines by newline into array, discarding last leftovers after last newline
		lines = response.split("\n")[:-1]

		# separate poem into 280 or less character tweets
		tweets = [[]]
		for line in lines:
			if not line or line.isspace(): continue
			if len("\n".join(tweets[-1]))+len(line) < 280:
				tweets[-1].append(line)
			else:
				tweets.append([line])

		# post each tweet and chain into a thread
		# TODO: rare error where twitter post is too long, investigate further.
		tweet_content = "\n".join(tweets.pop(0))
		parent_tweet = self.twitter.update_status(status=tweet_content)
		for tweet in tweets:
			tweet_content = "@{} {}".format(self.twitter_screen_name, "\n".join(tweet))
			parent_tweet = self.twitter.update_status(status=tweet_content, in_reply_to_status_id=parent_tweet["id"])

		print("Generated and posted.")

def main():
	client = Bot()
	client.generate_post()

if __name__ == "__main__":
	main()