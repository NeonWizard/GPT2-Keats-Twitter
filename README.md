# John Keats GPT-2 Twitter Bot
## Find and download poem files
It took a few tries to find a repository of Keat's poems that could easily be automatically scraped. I first found some PDFs and wrote a PDF scraper, but the library I used wouldn't pull the text in any usable manner. I ended up finding a site with quite a lot of poems actually, all in plain-text in HTML.

I wrote a quick scraper in Python with BeautifulSoup which just walks over the Keat's poem directory, individually loads each page, and scrapes the text to local text files. I used basic string manipulation to clean the lines to have no weird whitespace and be formatted properly, then deleted any duplicate/excerpt files.

From there I concatenated all of the files into two files - one file where each poem region is separated by `<|endoftext|>` tokens, and one where they aren't. This token has been training into the GPT-2 base model and can be useful at times to distinguish between content in different regions, but in my case I suspect I might not want it.

## Training
I used Google's Collab to finetune my model, since they provide a free NVIDIA T4 GPU which works perfectly for anything Tensorflow. I also used the gpt-2-simple library to make finetuning easier. https://github.com/minimaxir/gpt-2-simple

I uploaded my master training text file to the Collab instance and downloaded the 355M GPT-2 model. From there the code was straightforward, just load the training set and finetune according to some parameters. I played with these parameters a bit to get a desired model, mostly with the parameter controlling the number of training cycles.

### Training Approach 1 (more cycles)
### Training Approach 2 (less cycles)

## Coding the GPT-2 driver

## Coding the Twitter bot

## Creating the systemd service and timer

-----

## Installation Instructions
1. Clone the repo into your system, then `cd` into it.
2. Ensure the proper GPT2 models are on your system, and then symlink the directory with `ln -s <path_to_models> models`.
3. Run `sudo bash install.sh` to install pip packages, and set up the systemd service and timer.
4. Copy `default.env` to `.env` and fill out the fields.
