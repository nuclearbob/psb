#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "537598252-ST3yI9ciKmvDiNJCdgHtEohfkLjtlJFzc5pTvrkm"
access_token_secret = "pcMg2uoW4PExRgOcVnEXhQqcoORgvQSL1HPqQfaIJjLBm"
consumer_key = "2hjpzHpX1Oi6INkESCeODY8KZ"
consumer_secret = "ewuu3kWlAzoKlsGAHyCX7TknxGUTGeRwzXDKCd5gHqvy7qmG2J"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)
        return True
    def on_error(self, status):
        print(status)


l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)
stream.filter(track='@WilliamWayfarer')

