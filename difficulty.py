import sys
import json
import urllib.request

API = "https://codeforces.com/api/"
PROBLEM_LINK = "https://codeforces.com/problemset/problem/"

def checkResponse(status):
	if(status != "OK"):
		print("Something went wrong. Please try again after some time!")
		sys.exit(0)

def getData(url):
	data = json.load(urllib.request.urlopen(url))
	checkResponse(data["status"])
	return data["result"]

def getParticipatedContestList():
	data = getData(API + "user.rating?handle=" + handle)
	return [str(contest["contestId"]) for contest in data]

def getUnsolvedProblems(contests):
	unsolvedDict = {}
	parsedContest = 0
	for contestId in contests:
		# Get index of all problems in given contest like A, B, C1, C2 etc
		data = getData(API + "contest.standings?contestId=" + contestId + "&handles=" + handle)
		problemList = []
		for problem in data["problems"]:
			unsolvedDict[str(contestId) + problem["index"]] = problem["rating"]
			problemList.append(problem["index"])

		# Get solved problems in current contest
		data = getData(API + "contest.status?contestId=" + contestId + "&handle=" + handle)
		solved = set()
		for submission in data:
			if(submission["verdict"] == "OK"):
				solved.add(submission["problem"]["index"])

		# Delete solved problems
		for problem in solved:
			unsolvedDict.pop(str(contestId) + problem)

		parsedContest += 1
		print("Parsed " + str(parsedContest) + " of " + str(len(contests)) + " contests.")
	print("Successfully parsed all participated contests!")
	return sorted(unsolvedDict.items(), key=lambda x:x[1])

# Execution starts from here
if(len(sys.argv) < 2):
	print("Please enter your codeforces handle as first argument.")
	sys.exit(0)

handle = sys.argv[1]
participatedContest = getParticipatedContestList()
unsolvedDict = getUnsolvedProblems(participatedContest)

file = open(handle, "w")
for problem in unsolvedDict:
	index = 0
	for i in range(0,len(problem[0])):
		if(problem[0][i].isalpha()):
			index = i + 1
			break
	line = PROBLEM_LINK + problem[0][0:i] + "/" + problem[0][i:] + " - " + str(problem[1])
	print(line)
	file.write(line+"\n")
print("Saved data to file " + handle + ". Happy upsolving! :)")