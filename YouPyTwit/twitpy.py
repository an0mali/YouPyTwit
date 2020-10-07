import tweepy
from random import randint
import string
import time

class Twitpy(object):
	
	def __init__(self, name, omgq):
		
		 self.name = name
		 
		 self.act_t = False
		 self.act_ts = False
		 self.consume_t = False
		 self.consume_ts = False
		 self.api = False
		 
		 self.max_recent = 150
		 self.recent = []
		 self.cur_interact = {
		 'usr':'',
		 'twt': '',
		 's_n': '',
		 }
		 
		 self.bar_wrds = ['daUtoobChannel', 'rt', 'RT', 'retweet', 'Retweet']
		 
		 self.omgq = omgq
		 self.connect()
		 
		 
	def connect(self):
		if self.load_consume():
			self.load_access()
		self.twit_auth()
		 
	def get_access(self, ck, cs):
		input('Attempting to retreive keys. Press any key to continue')
		redirect_url = False
		auth = tweepy.OAuthHandler(ck,cs)
	
		try:
			redirect_url = auth.get_authorization_url()
		except tweepy.TweepError:
			print('Error! Failed to get request token.')
			
		session.set('request_token', auth.request_token['oauth_token'])

		verifier = request.GET.get('oauth_verifier')
		
		auth = tweepy.OAuthHandler(ck, cs)
		token = session.get('request_token')
		session.delete('request_token')
		
		auth.request_token = {'oauth_token': token,
			'oauth_token_secret': verifier}
		
		try:
			auth.get_access_token(verifier)
		except tweepy.TweepError:
			print('Fail to get token!')
			
		with Open('access.aut', 'w+') as out:
			out.write(auth.access_token + '\n')
			out.write(auth.access_token_secret)
			
	def load_access(self):
		secret = False
		try:
			with open('access.aut', 'r') as inf:
				for line in inf:
					line = line.strip()
					if not secret:
						self.act_t = line
					else:
						self.act_ts = line
					secret = True
					
		except FileNotFoundError:
			print('No auth file found. Retrieving.')
			get_access()
			
	def load_consume(self):
		secret = False
		try:
			with open('consume.aut', 'r') as inf:
				for line in inf:
					line = line.strip()
					#print('Setting consume: ' + line)
					if not secret:
						self.consume_t = line
					else:
						self.consume_ts = line
					secret = True
		except FileNotFoundError:
			print('No consumer file found. Ending')
			return False
		return True
		
	def twit_auth(self):
		self.auth = tweepy.OAuthHandler(self.consume_t, self.consume_ts)
		self.auth.set_access_token(self.act_t, self.act_ts)
		self.api = tweepy.API(self.auth)
		self.omgq.poutit('::Twitpy:: Authorized.', 3)
		
	def post_tweet(self, tweetstr):
		self.api.update_status(tweetstr)
		
	def retweet(self, twt, usr):
		try:
			self.omgq.poutit(':RT: Favorting!', 5)
			self.api.create_favorite(twt)
			time.sleep(5)
			self.omgq.poutit(':RT: Retweeting!', 5)
			self.api.retweet(twt)
			time.sleep(5)
			#roll = randint(0,2)
			#if roll == 2:
			#	self.omgq.poutit('Decided to follow user: ' + usr, 5)
			#	self.follow_usr(usr)
			return True
		except tweepy.TweepError:
			return False
			
	def follow_all(self):
		for follower in tweepy.Cursor(self.api.followers).items():
			follower.follow()
			
	def fav_tweet(self,twt):
		try:
			self.api.create_favorite(twt)
			return True
		except tweepy.TweepError:
			self.omgq.poutit('Error trying to favorite tweet', 15)
			return False
			
	def rate_limit(self,cur):
		while True:
			try:
				yield cur.next()
			except tweepy.error.TweepError:#tweepy.RateLimitError or 
				self.omgq.poutit('Error! Rate limit reached!', 1000)
				print('Tweep Error. Sleeping for 15 min')
				time.sleep(60 * 15)		
				
	def follow_usr(self,usr):
		try:
			self.api.create_friendship(usr)
			self.omgq.poutit('Friendship created with: ' + str(usr),15)
		except tweepy.error.TweepError:
			print('Error trying to create fwend. Maybe already fwends?')
		
	def check_bwords(self, txt, wrds):
		for i in wrds:
			if i in txt:
				return False
		return True
		
	def find_ht_tweet(self,ht):
		self.omgq.poutit('::Twitpy:: Finding tweet using hashtag: ' + ht, 3)
		tweets = tweepy.Cursor(self.api.search, q='#' + ht, lang='en', count=50, result_type="recent").items(50)
		
		twt_ls = {
		'text': [],
		'usr': [],
		'id': [],
		}
		
		sel_opts = []
		
		twt = False
		usr = False
		for i in self.rate_limit(tweets):
			usr = i.user.screen_name
			if self.check_bwords(usr,self.bar_wrds):
				if self.check_bwords(i.text,self.bar_wrds):
					if not usr in self.recent:
						twt_ls['text'].append(i.text)
						twt_ls['usr'].append(usr)
						twt_ls['id'].append(i.id)
					
		
		dlen = len(twt_ls['usr'])
		self.omgq.poutit(str(dlen) + ' tweets found!', 3)
		
		
		if dlen == 0:
			return False

		twind = randint(0,dlen) -1

		twt = twt_ls['text'][twind]
		usr = twt_ls['usr'][twind]
		self.recent.append(usr)

		if len(self.recent) > self.max_recent:
			for x in range(50):
				self.recent.pop(0)
				
		if not twt:
			return False
		else:
			ntwt = ''
			pable = set(string.printable)
			for i in twt:
				if i in pable:
					ntwt += i
			twt = ntwt
		self.omgq.poutit('Tweet found! User: "' + str(usr) + '" Tweet: ' + str(twt), 5)
		return [twt, usr, twt_ls['id'][twind]]
		
