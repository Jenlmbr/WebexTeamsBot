import requests
import json
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
accessToken = "Bearer ZTc0ODk0MzUtMGY3OC00N2E3LTgyMjktZWMzODgzYTU2ZDNkN2NiY2IyNDEtMTJk_PF84_consumer"

###########################################
# Get data from webex chatbox through API #
###########################################

r = requests.get(   "https://api.ciscospark.com/v1/rooms",
                    headers = {"Authorization": accessToken}
                )

if not r.status_code == 200:
    raise Exception("Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))


print("List of rooms:")
rooms = r.json()["items"]
for room in rooms:
    print (room["title"])

    # Add delay
    time.sleep(1)
	
    # Define room to search for IP + variable for roomid
    roomNameToSearch = "IP_Address"

  
    roomIdToGetMessages = None
    
    for room in rooms:
        # Room is defined in variable 
        if(room["title"].find(roomNameToSearch) != -1):

            # Displays the rooms found
            print ("Room " + roomNameToSearch + " found")
            print(room["title"])

            # Variable for roomId and message created
            roomIdToGetMessages = room["id"]
            roomTitleToGetMessages = room["title"]
            print("Found room : " + roomTitleToGetMessages)
            break

    if(roomIdToGetMessages == None):
        print("Room " + roomNameToSearch + " Not found")
       
    else:
        break



while True:
    # Add delay
    time.sleep(1)

   
    GetParameters = {
                            "roomId": roomIdToGetMessages,
                            "max": 1
                         }
    # run the call against the messages endpoint of the Webex Teams API
    r = requests.get("https://api.ciscospark.com/v1/messages", 
                         params = GetParameters, 
                         headers = {"Authorization": accessToken}
                    )
    # verify if the retuned status is ok
    if not r.status_code == 200:
        raise Exception( "Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))
    
    # get the JSON formatted returned data
    json_data = r.json()
    # check for 'items' in array
    if len(json_data["items"]) == 0:
        raise Exception("no messages")
    
    # store messages
    messages = json_data["items"]
    # store the text of the first message in the array
    ip = messages[0]["text"]
    description,ip,subnet = ip.split()
    print("The description is: " + description)
    print("The IP address is: " + ip)
    print("The subnet mask is: " + subnet)


##########################################################
# return fetched info from API Webex to Cisco Devnet API  #
##########################################################

    #set API URL
    api_url = "https://10.10.20.48/restconf/data/ietf-interfaces:interfaces/interface=Loopback01"

    #dictionary variable
    headers = { "Accept": "application/yang-data+json",
                "Content-type":"application/yang-data+json"
              }
                            
    #define authentication
    basicauth = ("developer", "C1sco12345")

    #config for interface
    yangConfig = { 
            "ietf-interfaces:interface": { 
                    "name": "Loopback01",
                    "description": description, 
                    "type": "iana-if-type:softwareLoopback",
         	    "enabled": True,
                    "ietf-ip:ipv4": { 
			"address": [
				{ "ip": ip,
				"netmask": subnet }
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
