import json
import urllib, urllib2
import os

BING_API_KEY = os.environ.get('BING_API_KEY')

def run_query(query):
	root_url ='https://api.datamarket.azure.com/Bing/Search/'
	source = 'Web'
	query = "'{0}'".format(query)
	query = urllib.quote(query)
	results_per_page = 10
	offset = 0
	search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
			root_url,
			source,
			results_per_page,
			offset,
			query)

	username = ''
	password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	password_mgr.add_password(None, search_url, username, BING_API_KEY)

	results = []

	try:
		handler = urllib2.HTTPBasicAuthHandler(password_mgr)
		opener = urllib2.build_opener(handler)
		urllib2.install_opener(opener)

		response = urllib2.urlopen(search_url).read()

		json_response = json.loads(response)

		for result in json_response['d']['results']:
			results.append({
				'title':result['Title'],
				'link': result['Url'],
				'summary': result['Description']
				})
	except urllib2.URLError as e:
		print search_url
		print "Error when query the bing API", e
	return results