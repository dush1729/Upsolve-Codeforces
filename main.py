import sys
import json
import urllib.request

def checkResponse(status):
	if(status == "OK"):
		print("Successfully connected. Fetching data..")
	else:
		print("Something went wrong. Please try again after some time!")
		sys.exit(0)

def getContestList():
	url = 'https://codeforces.com/api/user.rating?handle=' + handle
	data = json.load(urllib.request.urlopen(url))
	checkResponse(data["status"])
	return [contest["contestId"] for contest in data["result"]]

#Execution starts from here
if(len(sys.argv) < 2):
	print("Please enter your codeforces handle as first argument.")
	sys.exit(0)

handle = sys.argv[1]
contests = getContestList()