import sys
import json
import urllib.request

API = "https://codeforces.com/api/"

def checkResponse(status):
	if(status != "OK"):
		print("Something went wrong. Please try again after some time!")
		sys.exit(0)

def getData(url):
	data = json.load(urllib.request.urlopen(url))
	checkResponse(data["status"])
	return data["result"]

def getAllContestProblems():
	data = getData(API + "problemset.problems")
	return [str(problem["contestId"]) + problem["index"] for problem in data["problemStatistics"]]

def getParticipatedContestList():
	data = getData(API + "user.rating?handle=" + handle)
	return [str(contest["contestId"]) for contest in data]

def getUnsolvedProblems(contests):
	unsolved = []
	parsedContest = 0
	for contestId in contests:
		# Get index of all problems in given contest like A, B, C1, C2 etc
		data = getData(API + "contest.standings?contestId=" + contestId + "&handles=" + handle)
		problemList = []
		for problem in data["problems"]:
			problemList.append(problem["index"])

		# Get solved problems in current contest
		data = getData(API + "contest.status?contestId=" + contestId + "&handle=" + handle)
		solved = set()
		for submission in data:
			if(submission["verdict"] == "OK"):
				solved.add(submission["problem"]["index"])

		# Delete solved problems
		for problem in solved:
			problemList.remove(problem)

		# Add to unsolved problem
		for problem in problemList:
			unsolved.append(problem)

		parsedContest += 1
		print("Parsed " + str(parsedContest) + " of " + str(len(contests)) + " contests.")
	print("Successfully parsed all contests!")
	return unsolved

# Execution starts from here
if(len(sys.argv) < 2):
	print("Please enter your codeforces handle as first argument.")
	sys.exit(0)

handle = sys.argv[1]
getAllContestProblems()
contests = getParticipatedContestList()
getUnsolvedProblems(contests)