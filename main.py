import sys
import json
import urllib.request

API = "https://codeforces.com/api/"

def checkResponse(status):
	if(status != "OK"):
		print("Something went wrong. Please try again after some time!")
		sys.exit(0)

def getContestList():
	url = API + "user.rating?handle=" + handle
	data = json.load(urllib.request.urlopen(url))
	checkResponse(data["status"])
	return [str(contest["contestId"]) for contest in data["result"]]

def getUnsolvedProblems(contests):
	parsedContest = 0
	for contestId in contests:
		# Get index of all problems in given contest like A, B, C1, C2 etc
		url = API + "contest.standings?contestId=" + contestId + "&handles=" + handle
		data = json.load(urllib.request.urlopen(url))
		checkResponse(data["status"])
		problemList = []
		for problem in data["result"]["problems"]:
			problemList.append(problem["index"])

		# Get solved problems in current contest
		url = API + "contest.status?contestId=" + contestId + "&handle=" + handle
		data = json.load(urllib.request.urlopen(url))
		checkResponse(data["status"])
		solved = set()
		for submission in data["result"]:
			if(submission["verdict"] == "OK"):
				solved.add(submission["problem"]["index"])

		# Delete solved problems
		for problem in solved:
			problemList.remove(problem)

		parsedContest += 1
		print("Parsed " + str(parsedContest) + " of " + str(len(contests)) + " contests.")

# Execution starts from here
if(len(sys.argv) < 2):
	print("Please enter your codeforces handle as first argument.")
	sys.exit(0)

handle = sys.argv[1]
contests = getContestList()
getUnsolvedProblems(contests)