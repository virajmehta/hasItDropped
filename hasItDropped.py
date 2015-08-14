import json
import requests
import requests.auth
import time
import re
import subprocess


def getToken():
	'''Gets OAuth token from reddit and saves as the file '.token'. also returns the token.  There is no protection here.'''
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
	boys_dont_cry = re.compile('\[FRESH\].*(Frank|frank|FRANK).*(OCEAN|Ocean|ocean).*')
	reTrawl = True
	while reTrawl:
		for post in postDict['data']['children']:
			if boys_dont_cry.match(post['data']['title']):
				return post['data']['url']
			if post['data']['created_utc'] < lastTime:
				reTrawl = False
		headers['after'] = postDict['data']['after']
		postDict = request(headers)
		headers.pop('after', 0)
	return 0




def request(headers):
	new_posts = requests.get('https://oauth.reddit.com/r/hiphopheads/new/.json', headers=headers)
	if new_posts.status_code == 429 or new_posts.status_code == 401:
		print('429/401: trying again')
		headers['Authorization'] = 'bearer '+getToken()
		new_posts = requests.get('https://oauth.reddit.com/r/hiphopheads/new/.json', headers=headers)
	return new_posts




def main():
	#import pdb; pdb.set_trace()
	dropped = False
	f = open('.token', 'r')
	token = f.read().splitlines()
	f.close()
	headers = {'Authorization': 'bearer ' + token[0], 'User-Agent': 'hasItDropped by viraj', 'limit': '1'}
	trawl = 0
	lastTime = 0


	while not dropped:
		new_posts = request(headers)
		trawlNum += 1

		print 'Trawl {} complete'.format(trawlNum)
		
		data = new_posts.json()
		dropped = trawl(data, lastTime, headers)
		lastTime = data['data']['children'][0]['data']['created_utc']

		time.sleep(600)

	phoneBook = {'Viraj': '5129631439', 'David': '4256477687'}
	for name in phoneBook:
		message = "Hi, {}!  This is Viraj Mehta's hasItDropped app telling you that Frank Ocean has dropped at {}".format(name, dropped)
		subprocess.call(['osascript', 'sms\ script.scpt', phoneBook[name], message])

	return

if __name__ == "__main__":
	main()