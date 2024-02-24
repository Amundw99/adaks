# install dependencies with: pip install requests sanction # install dependencies with: pip install requestssanction
#what intervals have you checked at? Information in API refreshes every 5 minutes
import requests
import sanction
import time
import datetime

CLIENT_ID = "216845"
# Denne finnes i Adax ass, konto

# replace with your client ID (see Adax WiFi app,Account Section)
CLIENT_SECRET = "XCOo7CH6CttZsbUr"

# replace with your client secret (see Adax WiFi app,Account Section)
API_URL = "https://api-1.adax.no/client-api"
oauthClinet = sanction.Client(token_endpoint = API_URL + '/auth/token')
print(oauthClinet)

def get_token():
# Authenticate and obtain JWT token
    oauthClinet.request_token(grant_type = 'password', username = CLIENT_ID, password = CLIENT_SECRET)
    print('get_token', oauthClinet.refresh_token)
    return oauthClinet.access_token

def refresh_token():
    oauthClinet.request_token(grant_type='refresh_token', refresh_token = oauthClinet.refresh_token, username =
    CLIENT_ID, password = CLIENT_SECRET)
    print('refresh ', oauthClinet.access_token)
    return oauthClinet.access_token

def set_room_target_temperature(roomId, temperature, token):

# Sets target temperature of the room
    headers = {"Authorization": "Bearer " + token }
    json = {'rooms': [{'id': roomId, 'targetTemperature': str(temperature)}]}
    response = requests.post(API_URL + '/rest/v1/control/', json = json, headers = headers)
    print("inne i set_room")

def get_energy_info(token, roomId):
    headers = { "Authorization": "Bearer " + token }
    response = requests.get(API_URL + "/rest/v1/energy_log/" + str(roomId), headers = headers)
    json = response.json()
    for log in json['points']:
        fromTime = datetime.datetime.utcfromtimestamp(int(log['fromTime']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        toTime = datetime.datetime.utcfromtimestamp(int(log['toTime']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        energy = log['energyWh'];
        print("From: %15s, To: %15s, %5dwh" % (fromTime, toTime, energy))

def get_homes_info(token):

    headers = { "Authorization": "Bearer " + token }
    response = requests.get(API_URL + "/rest/v1/content/?withEnergy=1", headers = headers)
    print(response)
    json = response.json()
    print(json)
    for room in json['rooms']:
        roomName = room['name']
        if ('targetTemperature' in room):
            targetTemperature = room['targetTemperature'] / 100.0
        else:
            targetTemperature = 0

        if ('temperature' in room):
            currentTemperature = room['temperature'] / 100.0
        else:
            currentTemperature = 0
        print("Room: %15s, Target: %5.2fC, Temperature: %5.2fC, id: %5d" % (roomName, targetTemperature, currentTemperature, room['id']))

    if ('devices' in json):
        for device in json['devices']:
            deviceName = device['name']
            energy = device['energyWh'];
            energyTime = datetime.datetime.utcfromtimestamp(int(device['energyTime']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
            print("Device: %15s, Time: %15s, Energy: %5dwh, id: %5d" % (deviceName, energyTime, energy, device ['id']))
            #token = get_token()

token = get_token()
set_room_target_temperature(488687, 550, token)

while True:
    #time.sleep(5)
# Change the temperature to 24 C in the room with an Id of 196342
    #set_room_target_temperature(488687, 600, token)
# Replace the 196342 with the room id from the get_homes_info output
    #time.sleep(5)
    #set_room_target_temperature(488687, 2400, token)
# Replace the 196342 with the room id from the  get_homes_info output
    time.sleep(150)
    get_homes_info(token)
    time.sleep(180)
    #get_energy_info(token, 488687)
    token = refresh_token()
