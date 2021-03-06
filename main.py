# -*- coding: utf-8 -*-
from twython import Twython, TwythonError
import gpt_2_simple as gpt2

from dotenv import load_dotenv
load_dotenv()

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

		# split all generated lines by newline into array, discarding last leftovers after last newline
		response_split = response.split("\n")
		if len(response_split) > 1:
			response_split = response_split[:-1]

		# clean out empty lines and split too long lines into two
		lines = []
		for line in response_split:
			if not line or line.isspace(): continue
			if len(line) > 280:
				buffer = ""
				while line:
					if len(buffer) >= 240:
						lines.append(buffer)
						buffer = ""

					split = line.split(" ", 1)
					if len(split) == 1:
						word, line = split[0], ""
					else:
						word, line = line.split(" ", 1)
					buffer += word + " "

				if buffer: lines.append(buffer)
			else:
				lines.append(line)

		# generation failure, try again
		if not lines: return False

		# save generated poem to master file to read through later
		with open("generated-poems.txt", 'a') as f:
			poem = "\n".join(lines)
			print(poem)
			f.write(poem+"\n---------------\n")

		# separate poem into 280 or less character tweets
		tweets = []
		buffer = ""
		for line_num, line in enumerate(lines):
			if len(buffer) + len(line) + 1 < 280:
				buffer += "\n" + line
			else:
				tweets.append(buffer)
				buffer = "@{} ".format(self.twitter_screen_name) + line

			# if we have 8 lines so far and we have a line that ends with punctuation,
			# terminate tweet here
			if line_num >= 8 and line[-1] in [".", "!", "?"]: break
		if buffer: tweets.append(buffer)

		# post each tweet and chain into a thread
		tweet = tweets.pop(0)
		parent_tweet = self.twitter.update_status(status=tweet)
		for tweet in tweets:
			parent_tweet = self.twitter.update_status(status=tweet, in_reply_to_status_id=parent_tweet["id"])

		print("Generated and posted.")
		return True

def main():
	client = Bot()
	while not client.generate_post(): pass

if __name__ == "__main__":
	main()