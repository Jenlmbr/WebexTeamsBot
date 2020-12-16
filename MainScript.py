import json 
import requests 
import time
requests.packages.urllib3.disable_warnings()
accessToken = "Bearer YzRlNTg4MTEtMzI0ZC00ZjhhLWEzMjgtZDUxMDg5YTYzZTE0NjMxODhjOGYtZGQw_PF84_consumer"

r = requests.get(   "https://api.ciscospark.com/v1/rooms",
                    headers = {"Authorization": accessToken}
                )
#######################################################################################
# Check if the response from the API call was OK (r. code 200)
#######################################################################################
if not r.status_code == 200:
    raise Exception("Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))


#######################################################################################
# Displays a list of rooms.
#
# If you want to see additional key/value pairs such as roomID:
#	print ("Room name: '" + room["title"] + "' room ID: " + room["id"])
#######################################################################################
print("List of rooms:")
rooms = r.json()["items"]
for room in rooms:
    print (room["title"])

#######################################################################################
# Searches for name of the room and displays the room
#######################################################################################

while True:
    # Input the name of the room to be searched 
    roomNameToSearch = "ISS Flyover"

    # Defines a variable that will hold the roomId 
    roomIdToGetMessages = None
    
    for room in rooms:
        # Searches for the room "title" using the variable roomNameToSearch 
        if(room["title"].find(roomNameToSearch) != -1):

            # Displays the rooms found using the variable roomNameToSearch (additional options included)
            print ("Found rooms with the word " + roomNameToSearch)
            print(room["title"])

            # Stores room id and room title into variables
            roomIdToGetMessages = room["id"]
            roomTitleToGetMessages = room["title"]
            print("Found room : " + roomTitleToGetMessages)
            break

    if(roomIdToGetMessages == None):
        print("Sorry, I didn't find any room with " + roomNameToSearch + " in it.")
        print("Please try again...")
    else:
        break
    
	
IP = messages[0]["text"]
#Description = input("what is the name of the interface?")

#set API URL
api_url = "https://10.10.20.48/restconf/data/ietf-interfaces:interfaces/interface=Loopback99"

#create dictionary variable for the keys
headers = { "Accept": "application/yang-data+json",
            "Content-type":"application/yang-data+json"
          }
			
#define authentication
basicauth = ("developer", "C1sco12345")

#config for interface
yangConfig = { 
	"ietf-interfaces:interface": { 
		"name": "Loopback99",
		"description": "Loopback99", 
		"type": "iana-if-type:softwareLoopback",
		"enabled": True,
		"ietf-ip:ipv4": { 
			"address": [
				{ "ip": IP,
				"netmask": "255.255.255.0" }
				] }, 
		"ietf-ip:ipv6": {}
			} 
		}
		
#send 'put' request
resp = requests.put(api_url, data=json.dumps(yangConfig), auth=basicauth, 
headers=headers, verify=False) 
if(resp.status_code >= 200 and resp.status_code <= 299):
	print("STATUS OK: {}".format(resp.status_code)) 
else: 
	print("Error code {}, reply: {}".format(resp.status_code, resp.json()))
