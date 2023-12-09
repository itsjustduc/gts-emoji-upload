# gts-emoji-upload
gotosocial emoji uploading script (from a folder) - might work on mastodon as well

this is something that i feel is kind of essential for being an admin of an instance, but i have not seen such a thing around. it's meant to be kind of straightforward. definitely not the cleanest code ever, just wanted to make something quick. i am not a professional coder, the code might suck by ur standards and u should not have high expectations. if u have complaints about this, feel free to fork. 🤷
tested on gotosocial. might work on mastodon, but the docs didn't mention the custom_emojis POST method and i am not gonna set up an instance to test lol.

## config

edit the config.py file. the 2 that are necessary are the api_token and instance. if u are on gts, [this](https://takahashim.github.io/mastodon-access-token/) is a good way of getting an api token in my experience ([source code](https://github.com/takahashim/mastodon-access-token)).

## usage

the easiest way of using this is putting the images u want to upload as emojis into the same folder as the 2 .py files, and then running the script with `python emoji-upload.py --category=categoryhere`. specifying a category isn't mandatory, without it, they will be uploaded uncategorized. if u want to choose a seperate directory of images, that can be done with the `--directory` argument. setting paths manually is a bit meh in general imo, as a warning. 
the script simply takes all image files (u can edit which extensions it looks for in the config file) in said folder, and uploads them with the name of the file as emojis (excluding the extension). there is a special case of categories: if the category argument is set as `u` (for unique), then a seperate one can be picked for each file. previous ones can be reused by typing in their number from the list.
