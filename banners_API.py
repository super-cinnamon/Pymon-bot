import json
import requests
import os
import base64

#GET ALL BANNERS
TOKEN = os.getenv('GIT_TOKEN')
response = requests.get("https://api.github.com/repos/MadeBaruna/paimon-moe-api/contents/src/data/banners.ts", headers = {'Authorization': TOKEN})
banners64 = response.json()["content"]
dicoSTR = base64.b64decode(banners64).decode("utf-8")
startindex = dicoSTR.index("100001")
newstr = dicoSTR[startindex:-1]
bannerTypes = newstr.split("\n\n")
location = 0
beginner = {}
standard = {}
character = {}
weapon = {}
allbanners = {}
for x in bannerTypes:
    location +=1
    x = "".join(x[:-1])
    x = x.replace('true:', 'true')
    x = x.replace('{', '')
    x = x.replace('\\', '')
    x = x.replace('"', '')
    x = x.replace(':00:00', '.00.00')
    x = x.replace('\n', ' ')
    x = " ".join(x.split())
    x = x.replace('\', \'', '\'; \'')
    x = x.replace('\', ]', '\'; ]')
    x = x.replace(',', ':')
    content = x.split(": ")
    sDico = {}
    index = 1
    banIndex = 0
    while index < (len(content)):
        if(content[index] == '}' or content[index] == '} ' or content[index] == ' } ' or content[index] == ' }'):
            if(location == 1):
                beginner[content[banIndex]] = sDico
            if(location == 2):
               standard[content[banIndex]] = sDico
            if(location == 3):
                character[content[banIndex]] = sDico
            if(location == 4):
                weapon[content[banIndex]] = sDico
            sDico = {}
            index +=2
            banIndex = index-1
        else:
            sDico[content[index]] = content[index+1]
            index +=2  
allbanners.update(beginner)
allbanners.update(standard)
allbanners.update(character)
allbanners.update(weapon)


#GET CURRENT BANNERS IDS
response = requests.get("https://api.github.com/repos/MadeBaruna/paimon-moe-api/contents/src/routes/wish.ts", headers = {'Authorization': TOKEN})
currentBanners64 = response.json()["content"]
fullCode = base64.b64decode(currentBanners64).decode("utf-8")
charaIndex = fullCode.index("LATEST_CHARACTER_BANNER = ")
startCharaID = charaIndex+len("LATEST_CHARACTER_BANNER = ")
endCharaID = startCharaID + 6
currentCharaBannerID = fullCode[startCharaID:endCharaID]
weapIndex = fullCode.index("LATEST_WEAPON_BANNER = ")
startWeapID = weapIndex+len("LATEST_WEAPON_BANNER = ")
endWeapID = startWeapID + 6
currentWeapBannerID = fullCode[startWeapID:endWeapID]

print("the current character banner is :")
print(character[currentCharaBannerID]['shortName'])

print("the current weapon banner is :")
print(allbanners[currentWeapBannerID]['shortName'])
        
print(response.status_code)
