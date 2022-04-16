import requests

response = requests.get("https://paimordle.vercel.app/static/js/main.8df5c693.js")
print(response.status_code)
fullCode = response.content.decode("utf-8")
startindex = fullCode.index("s=[\"")
endindex = fullCode.index("],c=")
solutionWords = fullCode[startindex+3:endindex]
solutionWords = solutionWords.replace("\"", "")
words = solutionWords.split(",")
print("there are ", str(len(words)))
print(words)
todayIndex = 75
print("today's paimordle is:")
print(words[todayIndex])
print("tomorrow's paimordle is:")
print(words[todayIndex+1])
print("yesterday's paimordle was:")
print(words[todayIndex-1])