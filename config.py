import os

from dotenv import load_dotenv
load_dotenv()

CONFIG = {
  "TWITTER_CONSUMER_KEY": "",
  "TWITTER_CONSUMER_SECRET": "",
  "TWITTER_ACCESS_TOKEN": "",
  "TWITTER_ACCESS_TOKEN_SECRET": "",

  "ODIN_USER": "",
  "ODIN_PASS": "",
  "ODIN_MODEL": "john-keats-500",
}

for key, value in CONFIG.items():
  # If key has no default value, it's required
  if value == "":
    if key not in os.environ:
      print(f"ERROR: '{key}' is a required environment variable!")
      os._exit(1)

    CONFIG[key] = os.environ[key]
  else:
    # Overwrite default values if present in environment
    if key in os.environ:
      CONFIG[key] = os.environ[key]
