#!/usr/bin/env python

import asyncio
import json
import websockets
import time
import names
import pickle

from lib.PostgresManager import PostgresManager
from lib.ConfigManager import ConfigManager

# Enum emulation. 
# True Enum type doesn't support string values by default.
ACTION_JOIN = "join"
ACTION_MESSAGE = "message"
ACTION_EXIT = "exit"

# Set of open websocket connections
WEBSOCKETS = set()

# Initialize config and database managers.
cm = ConfigManager()
try:
    db = PostgresManager(cm)
except Exception as e:
    print(e)

# "Main" function to run in event loop. 
# Handles user management and message distribution. 
async def chat(websocket, path):
    # Randomly generated user name. 
    username = names.get_full_name()
    await user_change(username, websocket, ACTION_JOIN)
    try:
        async for message in websocket:
            data = json.loads(message)
            if data["message"] is not None:
                await notify_users(username, ACTION_MESSAGE, data["message"])
            else:
                print("Unsupported event: {data}".format(data=data))
    finally:
        await user_change(username, websocket, ACTION_EXIT)

# Handles connection and disconnection of users. 
async def user_change(username, websocket, action):
    message = toggle_connection(username, websocket, action)
    await notify_users(username, action, message)

# Adds or removes websocket from "users" set. 
# Returns the appropriate message to inform the users.
def toggle_connection(username, websocket, action):
    if action is ACTION_JOIN:
        WEBSOCKETS.add(websocket)
        return user_msg_join(username)

    if action is ACTION_EXIT:
        WEBSOCKETS.remove(websocket)
        return user_msg_exit(username)

# Distributes messages to all connected users. 
# No action if there are no connected users. 
async def notify_users(username, action, message):
    if WEBSOCKETS:
        if action is ACTION_MESSAGE:
            message = "{username}: {message}".format(username=username, message=message)
        payload = get_payload(ACTION_MESSAGE, message)
        print(message)
        log_message((get_epoch_str(), username, ACTION_MESSAGE, message))
        await asyncio.wait([websocket.send(payload) for websocket in WEBSOCKETS])

# Configuration file management
def get_config():
    return cm.get_config("Websocket")

# Return epoch timestamp as string. 
def get_epoch_str():
    return str(int(time.time()))

# Write chat data to Postgres database. 
def log_message(attr_list):
    try:
        db.insert(PostgresManager.INSERT_CHAT, attr_list)
    except Exception as e:
        print(e)

def get_payload(action, message):
    return json.dumps({"action": ACTION_MESSAGE, "message": message})

def user_msg_join(username):
    return username + " joined chat."

def user_msg_exit(username):
    return username + " exited chat."

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
