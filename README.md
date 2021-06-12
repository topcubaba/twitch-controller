# Twitch Chat Controller

This script let your twitch chat control your game etc. You can find required libraries on requirements.txt folder.


## Usage
Edit token, channel and nickname part with yours.
You can get your oauth token from [here](https://twitchapps.com/tmi/).
```python
    def __init__(self):
        self.server = 'irc.chat.twitch.tv'
        self.port = 6667
        self.token = 'oauth:youroauthtoken'
        self.channel = '#yourchannel'
        self.nickname = 'yournickname'
```

You can edit script for your use.

## License
[MIT](https://choosealicense.com/licenses/mit/)
