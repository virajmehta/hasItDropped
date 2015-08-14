import json
import requests
import requests.auth
import time
import re
import subprocess

'''This module is designed to request all the new content from reddit.com/r/hiphopheads every 10 minutes.
It then matches every submission's title to a regular expression that would fit any submission of Frank's new album that fits the subreddit's rules.
If it finds the album, it sends a text with the link to everyone in the phone book in the source.
It seems to be working, but the only real test is the one that matters.
I purposely avoided PRAW here beacue I wanted to get a feel for using requests for this type of work, since it's more genrally applicable.
It was also a challenge to deal with authorizing this program'''

def getToken():
	'''Gets OAuth token from reddit and saves as the file '.token'. also returns the token.  There is no protection here for the file.'''
	f = open('.token', 'w')
	client_ID = 'LAFe-EVyQRQwJA'
	client_secret = 'Ci3byZwr0MXSqWZNrGuCFtbs_4s'
	client_auth = requests.auth.HTTPBasicAuth(client_ID, client_secret)
	post_data = {'grant_type': 'client_credentials'}
	headers = {'User-Agent': 'hasItDropped by viraj'}
	response = requests.post('https://www.reddit.com/api/v1/access_token', auth=client_auth, data=post_data, headers=headers)
	data = response.json()
	f.write(data[u'access_token'])
	f.close()
	return data[u'access_token']

def trawl(postDict, lastTime, headers):
	'''When passed a dictionary of the decoded JSON that reddit sends, it looks for Frank's album.  
	If it doesn't find it, it requests more old posts until the last one it read in the last trawl to make sure it doesn't miss any.  Then it returns false.
	If it finds the album, it returns the link to it.'''
	boys_dont_cry = re.compile('\[FRESH\].*(Frank|frank|FRANK).*(OCEAN|Ocean|ocean).*')
	reTrawl = True
	while reTrawl:
		for post in postDict['data']['children']:
			if boys_dont_cry.match(post['data']['title']):
				return post['data']['url']
			if post['data']['created_utc'] < lastTime:
				reTrawl = False
		headers['after'] = postDict['data']['after']
		postDict = request(headers).json()
		headers.pop('after', 0)
	return 0




def request(headers):
	'''This function is the wrapper for the request and reauthentication for this app'''
	new_posts = requests.get('https://oauth.reddit.com/r/hiphopheads/new/.json', headers=headers)
	if new_posts.status_code == 429 or new_posts.status_code == 401:
		print('429/401: trying again')
		headers['Authorization'] = 'bearer '+getToken()
		new_posts = requests.get('https://oauth.reddit.com/r/hiphopheads/new/.json', headers=headers)
	return new_posts




def main():

	dropped = False
	f = open('.token', 'r')
	token = f.read().splitlines()#checks for old token.  Mostly for testing purposes, since when it runs it will hold the token in memory I think
	f.close()
	headers = {'Authorization': 'bearer ' + token[0], 'User-Agent': 'hasItDropped by viraj', 'limit': '1'}
	trawlNum = 0
	lastTime = 10000000000  	#bigger than current UNIX time for forseeable future, definitely before Frank dies


	while not dropped:
		new_posts = request(headers)
		trawlNum += 1
		data = new_posts.json()
		dropped = trawl(data, lastTime, headers)
		print 'Trawl {} complete'.format(trawlNum)
		
		lastTime = data['data']['children'][0]['data']['created_utc'] #saves freshest post looked at for future endpoint
		time.sleep(600)	#wait 10 minutes
	

	phoneBook = json.load(open('phoneBook.json'))
	for name in phoneBook:
		message = "Hi, {}!  This is Viraj Mehta's hasItDropped app telling you that Frank Ocean has dropped at {}".format(name, dropped)
		subprocess.call(['osascript', 'textScript.scpt', phoneBook[name], message])	#send a text

	return

if __name__ == "__main__":
	main()