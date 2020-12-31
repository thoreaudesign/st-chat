#!/usr/bin/env python

import asyncio
import json
import websockets

from lib.PostgresManager import PostgresManager
from lib.ConfigManager import ConfigManager

import time

# Enum emulation. 
# True Enum type doesn't support string values by default.
ACTION_JOIN = "join"
ACTION_MESSAGE = "message"
ACTION_EXIT = "exit"

# Initialize config and database managers.
cm = ConfigManager()
db = PostgresManager(cm)

# Initialize set to track websocket connections, "users"
USERS = set()

# Configuration file management
def get_config():
    section = "Websocket"
    if section in cm.parser.sections():
        return cm.parser[section]


# Return epoch timestamp as string. 
def get_epoch_str():
    return str(int(time.time()))

def notification_payload(action):
    return json.dumps({"action": action})

# Write chat data to Postgres database. 
def log_message(attr_list):
    try:
        db.insert_chat(attr_list)
    except Exception as e:
        print(e)
    
# Distributes messages to all connected users. 
# No action if there are no connected users. 
async def notify_users(action, message):
    if USERS:
        payload = None
        if action is ACTION_MESSAGE:
            username = message.split(':')[0]
            payload = json.dumps({"action": ACTION_MESSAGE, "message": message})
            print(message)
            log_message((get_epoch_str(), username, ACTION_MESSAGE, message))
        else:
            payload = notification_payload(action)
        
        await asyncio.wait([user.send(payload) for user in USERS])

# Handles connection and disconnection of users. 
async def user_change(websocket, action, message):
    username = action
    USERS.add(websocket)
    print(message)
    log_message((get_epoch_str(), username, action, message))
    await notify_users(action, message)

# "Main" function to run in event loop. 
# Handles user management and message distribution. 
async def chat(websocket, path):
    await user_change(websocket, ACTION_JOIN, "New user joined chat.")
    try:
        async for message in websocket:
            data = json.loads(message)
            if data["message"] is not None:
                await notify_users(ACTION_MESSAGE, data["message"])
            else:
                print("Unsupported event: {data}".format(data=data))
    finally:
        await user_change(websocket, ACTION_EXIT, "User exited...")

# Initialize config values from config.ini
config = get_config()
host = config['host']
port = config['port']

# Configure chat function as entrypoint for websocket and start server.
# Set host and port from config.ini. 
start_server = websockets.serve(chat, host, port)
print("ST-Chat websocket server started at {host}:{port}.".format(host=host, port=port))

# Set event loop to monitor websocket and re-run chat function infinitely.
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
