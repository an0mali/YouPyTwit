import os
import csv
import youtube.utoobpy_lte as utlte
from random import randint

class Twmkr(object):
	
	def __init__(self,name,omgq):
		
		self.name = name
		
		#self.ldata = {}
		self.dload = {}
		#self.all_htags = []
		self.mention = []
		self.gdlivetw = []
		
		self.recent = []
		self.refdat = {}

		self.ldat = {}
		self.yt_data = ''
		self.uidcnt = 0
		self.uidl = []
		
		self.max_recent = 5
		self.cats = []
		self.recent = []
		self.omgq = omgq
		
		firstrun = self.check_paths()
		
		
		
		
		if firstrun:
			print('Data directories initialied. Add data then rerun the program')
			input('Press enter to continue')
		else:
			self.load_htags()
			self.parse_yt()
			
	def load_htags(self):
		print('Loading hashtags')
		for i in self.cats:
			self.load_lsv(i,'hashtags')
		
	def check_paths(self):
		firstrun = False
		if not os.path.exists('data'):
			print('Data path not found, initializing')
			firstrun = True
			os.makedirs('data')
			
		for root,dir,files in os.walk('data'):
			for i in dir:
				self.cats.append(i)
				
		return firstrun
		
	def load_data():
		for i in self.cats:
			self.load_lsv(i)
		
	def load_lsv(self, cat, dtype):
		
		files = []
		path = 'data/' + cat
		
		dtype_exists = False
		for root,dir,files in os.walk(path):
			for fname in files:
				print(fname)
				if fname == dtype:
					dtype_exists = True
					break
					
		if not dtype_exists:
			print('Twmkr:: Failed to load ' + dtype + ' data file from path: ' + path)
			input()
			return
				
		if not cat in self.dload:
			self.dload[cat] = {}
		
		if not dtype in self.dload[cat]:
			#Prep category based dictionary
			self.dload[cat][dtype] = []
		with open(path + '/' + dtype, 'r') as fin:
			ar_ref = self.dload[cat][fname]
			for line in fin:
				line = line.strip()
				if not line in ar_ref:
					ar_ref.append(line)
					
	def parse_yt(self):
		ytd = self.yt_data
		ytd = utlte.main()
		for i in ytd['items']:
			if 'id' in i:
				if 'videoId' in i['id']:
					vidid = i['id']['videoId']
					link = 'https://youtu.be/' + vidid
					
					desc = i['snippet']['description']
					desc = desc[0:250]
					
					
					
					title = i['snippet']['title']
					start = 0
					end = title.find(' |')
					title = title[start:end]
					
					htag = self.detect_vid(desc, title)
					
					self.ldat[vidid] = {
					'url': link,
					'title': title,
					'desc': desc,
					'htag_ls': htag,
					}
					self.uidl.append(vidid)
					
	def detect_vid(self, desc, title):
		htag = 'GDLive'
		
		if 'metroidvania' in desc:
			htag = 'Metvan'
		elif 'Quig' in desc or 'Quig' in title:
			htag = 'LetsPlays'
		
		return htag
				
	def gen_id(self):
		uid = str(self.uidcnt)
		self.uidcnt += 1
	
		return uid
					
	def test(self):
		self.load_links()
		print(self.ldat)
		print('\n\n\n')
		print(self.uidl)
		
	def get_rand_link_item(self):

		cnt = 0
		uid = False
		while True:
			sel = randint(0,len(self.uidl)) - 1
			uid = ''
				
			if not sel in self.recent:
				self.recent.append(sel)
				uid = self.uidl[sel]
				if len(self.recent) > 50:
					self.recent.pop(0)
				break
			
		vidat = self.ldat[uid]

		return vidat
		
	def get_rand_hashtag(self,gdtag=True, cat='GDLive'):
		htag_ls = self.dload[cat]['hashtags']
		self.omgq.poutit('Choosing htags from list: ' + str(htag_ls),15)
		#if not gdtag:
		#	htag_ls = self.all_htags
		
		sel = randint(0,len(htag_ls)) - 1
		htag = htag_ls[sel]
		self.omgq.poutit("Selected a random hashtag: " + htag, 15)
		return htag
		
		
#a = Twmkr('a')
