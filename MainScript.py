import requests.packages.urllib3
import requests
import json
import route_get

requests.packages.urllib3.disable_warnings()

app = Flask(__name__)

# Set some basic variables to use for the app itself
bot_email = 'jlmbr@webex.bot' # Your bot's email
access_token = 'NjQ3OGU5ODctNWI0OS00ODIzLWJmZTItNDE5MjY0OGMwNmE2ZGVjYjRjODEtNzA1_PF84_consumer' # Your access token
base_url = 'https://api.ciscospark.com/v1/'
server = 'x.x.x.x' # Server that is running the bot
port = 10010
headers = {"Authorization": "Bearer {}".format(access_token), "Content-Type": "application/json"}