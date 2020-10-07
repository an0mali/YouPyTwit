from threading import Thread
from threading import Timer
from random import randint
from time import sleep
import string
import twitpy
import twmkr
import csv
import os

class YouPyTwit(object):
	
	def __init__(self, name, *kwargs):
		
		self.name = name
		self.ident = 'YouPyTwit'
		self.automate = True
		self.active = False
		
		with open('log.txt', 'w+') as ofile:
			ofile.write('')
		
		self.cycle_timer = False
		
		self.c_state = 0
		self.randmult = 2
		self.c_acts = []
		
		self.sleeping = False
		self.config = {
		'sleep_cycle_len': 8 * 60, #hours
		'wake_cycle_len': 16 * 60, #hours
		#anything with _time gets * 60#
		'rt_time': 120,
		'tw_time': 180, 
		'int_time': 60.0,#how often timer pops in minutes
		'fav_time': 4,
		#'int_len': 60,#sec, units per int_time, per interval. roughly becuase i suck
		'ps_enabled': True,
		'log_enabled': False,
		'refresh_rate': 0.5,
		}
		
		self.next_time = {}
		
		self.cycles = 0
		self.time_active = 0
		self.counts = {
		'cycles': 0,
		'sleep_cycle_sw': self.config['sleep_cycle_len'],
		'cycle_time': 0,
		'time_active': 0,
		'retweets': 0,
		'follows': 0,
		'tweets': 0,
		'actions': 0,
		'screen_upd': 0,
		'cycles_till_sleep': 0,
		}
		
		
		self.gdl_recent = []
		self.timer = False
		self.screen_timer = False
		self.pause_upd = False
		self.sleeping = False
		self.pout = []
		
		self.prev_rftime = 0
		
		self.tpy = twitpy.Twitpy('a', self)
		self.twmkr = twmkr.Twmkr('a', self)
		self.load_config()
		self.start_cycle()
	
	def poutit(self, mes, dur,write=True):
		ivchars = set(string.punctuation)
		self.pout.append([mes,int(dur * 10)])
		ts_mes = str(self.time_active) + ' >>> ' + mes + '\n'
		if write:
			with open('log.txt', 'a+') as ofile:
				ofile.write(ts_mes)
		
	def load_config(self):
		kw = ''
		with open('config.cfg', 'r') as inf:
			rdr = csv.DictReader(inf)
			for row in rdr:
				val = int(row['value'])
				kw = row['keyword']
				self.config[kw] = val
		
		for i in self.config:
			if not 'int_' in i:
				if '_time' in i:
					self.next_time[i] = 0
		self.poutit('Configuration loaded',1)
		
	def start_cycle(self):
		dopts = 4

		if not self.active:
			self.dbmes('init',' Bot is not active. Initializing. ')
			self.active = True
			
			self.counts['sleep_cycle_sw'] = self.config['sleep_cycle_len']
			self.update_status()
			if self.automate:
				
				print('Bot is in automated mode!')
				try:
					self.cycle()
				except:
					input('Error')
			else:
				while True:
					inp = input()
					if inp == 'stop':
						twt.cancel()
						break
					else:
						try:
							inp = int(inp)
						except:
							print('Response must be integer or "stop"')
							continue
					if inp <= dopts and inp != 0:
						self.test_things(inp)
					else:
						input('Not a valid selection')
						continue
			

			
	def cycle(self):
		#self.update_status()
		self.timer = Timer(self.config['int_time'], self.cycle)
		self.timer.start()
		
		self.poutit('A cycle tick has occured!', 1)
		cnts = self.counts
		
		self.prev_rftime = cnts['screen_upd']
		
		cats = self.c_acts
		cnts['cycles'] += 1
		
		if cnts['cycles'] == self.counts['sleep_cycle_sw']:
			nxt_cycle_len = 0
			
			if self.sleeping:
				self.sleeping = False
				nxt_cycle_len = self.config['wake_cycle_len']
			else:
				self.sleeping = True
				nxt_cycle_len = self.config['sleep_cycle_len']
				
			self.counts['sleep_cycle_sw'] += nxt_cycle_len
			
		if not self.sleeping:
			self.check_acts()
		
		
		
		
	def check_acts(self):
		cnts = self.counts

		acts = []
		nt = self.next_time
		#self.poutit(str(nt) + str(self.config), 10)
		#self.poutit('Times for next actions : ' + str(self.next_time), 3)
		if len(nt) < 1:
			self.poutit('ERROR! NO NEXT TIME DATA', 1000)
		for i in nt:
			nt[i] += 1
			if i in self.config:
				if nt[i] >= self.config[i]:
					intv_rand = randint(-self.randmult, self.randmult)
					intv_rand *= 0.1
					base_int = self.config[i]
					intv_adj = base_int * intv_rand
					nt[i] = int(intv_adj)
					acts.append(i)
		
		self.poutit('Actions to be taken: ' + str(acts), 5)
		actcnt = 0
		for i in acts:
			actcnt += 1
			act = i.replace('_time', '')
			cnts['actions'] += 1
			methd = act + '_func'
			self.pause_upd = True
			try:
				getattr(self, methd)()
			except error as e:
				print(e.msg)
				input()
			self.pause_upd = False
			if len(acts) > actcnt:
				sleep(20)
		
		if len(acts) > 1:
			self.poutit('Actions completed', 15)
		
	
	def st_timer(self):
		self.timer = Timer(self.config['int_time'], self.cycle)
		self.timer.start()
	
	def rt_func(self):
		roll = randint(0,2)
		if roll == 0:
			twt = self.grab_rand_ht_tweet()
			chk = self.tpy.retweet(twt[2], twt[1])
			if chk:
				self.poutit('::OmegaQuig:: Retweeted: ' + twt[0], 50)
		else:
			self.poutit('Decided not to retweet anything due to roll',150)
			
	def tw_func(self):
		roll = randint(0,3)
		if roll == 1:
			twt = self.construct_tweet()
			self.poutit('::OmegaQuig:: Posted this tweet I made:' + twt, 50)
			self.tpy.post_tweet(twt)
		else:
			self.poutit('Decided not to Tweet anything due to roll',150)
			
	def fav_func(self):
		twt = self.grab_rand_ht_tweet()
		chk = self.tpy.fav_tweet(twt[2])
		if chk:
			self.poutit('::OmegaQuig:: Favorited this tweet:"' + twt[0] + '" from user: ' + twt[1], 10) 
				
	def update_status(self):
		self.time_active += self.config['refresh_rate']
		nxt = self.next_time
		cfg = self.config
		if not self.pause_upd:
			os.system('cls')
			mins = round(self.time_active / 60, 3)
			hours = round(mins / 60, 3)
			print('''
			
	Debug methods:								Status Info:
		[1]: Grab random tweet					Active: ''' + str(self.automate) + '''
		[2]: Favorite random tweet				Est. Uptime: ''' + str(hours) + ''' hrs // ''' + str(mins) + ''' mins
		[3]: Retweet random tweet				Session Actions: ''' + str(self.counts['actions']) + '''
		[4]: Create tweet					Cycles: ''' + str(self.counts['cycles']) + '''
									Sleeping: ''' + str(self.sleeping) + '''
							
		_________________________________________________________________________________________							
		State Information (Updates once per minute)
		
		Action:				Cycles Since:			Cycles Till:
		'Favorite'			''' + str(nxt['fav_time']) + '''\t\t\t\t ''' + str(cfg['fav_time'] - nxt['fav_time']) + '''
		'Retweet'			''' + str(nxt['rt_time']) + '''\t\t\t\t ''' + str(cfg['rt_time'] - nxt['rt_time']) + '''
		'Tweet'				''' + str(nxt['tw_time']) + '''\t\t\t\t ''' + str(cfg['tw_time'] - nxt['tw_time']) + '''
		_________________________________________________________________________________________
									
									
								
		[stop]: Exit program
		
		Select your choice.
		
:::Output Info:::''')
			pclr = []
			for x in range(0,len(self.pout)):
				self.pout[x][1] -= 1
				if self.pout[x][1] <= 0:
					pclr.append(self.pout[x])
				print(self.pout[x][0])
				
			for i in pclr:
				self.pout.remove(i)
				
		if self.automate:
			self.screen_timer = Timer(self.config['refresh_rate'],self.update_status)
			self.screen_timer.start()
			self.counts['screen_upd'] += 1
			

					
	def grab_rand_ht_tweet(self):
		ht = ''
		while True:
			ht = self.twmkr.get_rand_hashtag()
			twt = self.tpy.find_ht_tweet(ht)
			if twt:
				return twt
					
	def test_things(self,inp):
		if inp == 1:
			self.poutit('Grabbing HT Tweet (manual) ', 10)
			self.grab_rand_ht_tweet()
		elif inp == 2:
			twt = self.grab_rand_ht_tweet()
			self.tpy.fav_tweet(twt[2])
		elif inp == 3:
			twt = self.grab_rand_ht_tweet()
			self.tpy.retweet(twt[2])
		elif inp == 4:
			tw = self.construct_tweet()
			self.poutit('Generated tweet: ' + tw, 10)
			chk = input("Post this tweet? 'y' for yes, all other for no")
			if chk == 'y':
				self.tpy.post_tweet(tw)
		
		self.update_status()
		
	def construct_tweet(self):
		tweet = ''
		link = self.twmkr.get_rand_link_item()
		ltype = link['htag_ls']
		htagls = []
		maintags = self.twmkr.dload[ltype]['hashtags']
		
		
		lnk = link['url']
		mes = link['title']
					
		tweet = mes + ' ' + lnk
		twtcnt = len(tweet)
				
		twtcnt, mentions = self.get_mentions(twtcnt, ltype)	
		
		if twtcnt >= 280:
			self.poutit('Tweet persona too long:: ' + tweet,30)
			tweet = link
			twtcnt = len(tweet)
		
		
		for i in self.twmkr.dload['Default']['hashtags']:
			htagls.append(i)
		for i in maintags:
			htagls.append(i)
		
		fail = 0
		tagcnt = 0
		max_tags = randint(6,14)
		htag_pot = []
		if len(tweet) < 280:
			while tagcnt < max_tags:
				hind = randint(0,len(htagls)) -1
				tag = htagls[hind]
				leng = len(tag) + 2
				if twtcnt + leng >= 280:
					break
				elif not tag in htag_pot:
					htag_pot.append(tag)
					twtcnt += leng
					tagcnt += 1
				else:
					fail += 1
					if fail > 50:
						print('Failed to fill all tweet space')
						break
			
			
		for i in htag_pot:
			ht = ' #' + i
			tweet += ht
			
		if mentions:
			for i in mentions:
				men = ' ' + i
				tweet += men
		return tweet
		
	def get_mentions(self, tcnt, ltyp):
		tmkr = self.twmkr
		mention_ls = []
		return_men = []
		if ltyp in tmkr.mention:
				mention_ls = []
		else:
			return tcnt, False
			
		for x in range(len(mention_ls)):
			if randint(0,1) == 0:
				break
			rchoice = randint(0,len(mention_ls)) -1
			mention = mention_ls[rchoice]
			return_men.append(mention)
			tcnt += len(mention)
			if tcnt >= 280:
				break
				
		return tcnt, return_men
		
	def dbmes(self, func, mes):
		s = self
		out = '::' + s.ident + ':: >' + func + ' > ' + mes
		if s.config['ps_enabled']:
			print(out) 
		if s.config['log_enabled']:
			pass # Insert data storage function hereeeeeeeeee
		
a = YouPyTwit('a')
