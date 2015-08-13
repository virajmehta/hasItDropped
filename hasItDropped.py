import json
import requests
import requests.auth
import time


def getToken():
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

def main():
	#import pdb; pdb.set_trace()
	dropped = False
	f = open('.token', 'r')
	token = f.read()
	f.close()
	headers = {'Authorization': 'bearer ' + token, 'User-Agent': 'hasItDropped by viraj', 'count': 50}
	while not dropped:
		new_posts = requests.get('http://oauth.reddit.com/r/hiphopheads/new/.json', headers=headers)
		if new_posts.status_code == 429:
			print('429: trying again')
			headers['Authorization'] = 'bearer '+getToken()
			new_posts = requests.get('http://oauth.reddit.com/r/hiphopheads/new/.json', headers=headers)
		print new_posts.text

	#data = new_posts.json()

if __name__ == "__main__":
	main()