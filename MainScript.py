import json 
import requests 
import time

requests.packages.urllib3.disable_warnings()
accessToken = "Bearer YjJjNDU2NGMtMDBlYS00MzAxLTgwNTgtMjQ5NjA4NjU1MGZkMDE2ZDI4MzQtNTNm_PF84_consumer"

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
    
#while True:
    # add 1 second of delay 
    time.sleep(1)

    # the Webex Teams GET parameters
   
    #  "max": 1  limits to get only the very last message in the room
    GetParameters = {
                            "roomId": roomIdToGetMessages,
                            "max": 1
                         }
    # run the call against the messages endpoint of the Webex Teams API using the HTTP GET method
    r = requests.get("https://api.ciscospark.com/v1/messages", 
                         params = GetParameters, 
                         headers = {"Authorization": accessToken}
                    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception( "Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))
    
    # get the JSON formatted returned data
    json_data = r.json()
    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")
    
    # store the array of messages
    messages = json_data["items"]
    # store the text of the first message in the array
    message = messages[0]["text"]
    print("Received message: " + message)
    
    # check if the text of the message starts with the magic character "/" followed by a location name
    #  e.g.  "/San Jose"
    #message.find("/") == 0:
        # name of a location (city) where we check for GPS coordinates using the MapQuest APIs
        #  message[1:]  returns all letters of the message variable except the first "/" character
        #   "/San Jose" is turned to "San Jose" and stored in the location variable
    
       
 
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
				{ "ip": IP ,
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
