## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Docker](#docker)

## General info
This project is a simple Twitter Bot that comment under every tweet of the target user. Plus, it will tweet a new status everyday.
You can check the bot on <a href="https://twitter.com/BotFan2Louis">Twitter</a>.

Feel free to use this code as you want.
Do not hesitate do send me any feedback.
	
## Technologies
Project is created with:
* Python version: 3.9.2
* Python-twitter library version: 3.4.2
	
## Setup
Create a '.env' file as follow and write your key from the Twitter API and the Twitter user information :
```
CONSUMER_KEY=consumer_key
CONSUMER_SECRET=consumer_secret
ACCESS_TOKEN_KEY=access_token_key
ACCESS_TOKEN_SECRET=access_token_secret
USER_ID=user_id  # check https://codeofaninja.com/tools/find-twitter-id/
SCREEN_NAME=@user  # without "@"
```

To run this project :

```
$ cd ../TwitterBot
$ python ./BotFan.py
```

## Docker
(optional) To build the docker container:
```
docker build -t pilpur/bot .
```

To run the container
```
docker run -it -d -v $PWD/.env:/app/.env --restart=always pilpur/bot
```