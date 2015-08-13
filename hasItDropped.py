import json
import requests

new_posts = requests.get('http://reddit.com/r/hiphopheads/new/.json')
#data = new_posts.json()

print(new_posts)