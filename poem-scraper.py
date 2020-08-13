import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

base_url = "https://www.poemhunter.com/john-keats/poems/"

page = requests.get(base_url)
soup = BeautifulSoup(page.content, "html.parser")

links = []

while True:
	for link in soup.select("td.title a"):
		links.append(urljoin(base_url, link["href"]))

	next_buttons = soup.select(".poets-poems li.next a")
	if not next_buttons: break

	next_url = urljoin(base_url, next_buttons[0]["href"])
	page = requests.get(next_url)
	soup = BeautifulSoup(page.content, "html.parser")

with open("all-keats-poems-token.txt", 'w') as master_file:
	with open("all-keats-poems-notoken.txt", 'w') as master_file2:
		for link in links:
			page = requests.get(link)
			soup = BeautifulSoup(page.content, "html.parser")

			title = soup.select("h1.title")[0].text
			print(title)

			if title.lower() == "hyperion" or "excerpt" in title.lower(): continue # duplicates

			with open("poems/{}.txt".format(title), 'w') as f:
				element = soup.select(".poem-detail .KonaBody [itemprop='text']")[0]
				text = element.get_text("\n")

				for line in text.split("\n"):
					if not line or line.isspace(): continue
					line = " ".join(line.split())
					f.write(line + "\n")
					master_file.write(line + "\n")
					master_file2.write(line + "\n")
			master_file.write("<|endoftext|>\n")