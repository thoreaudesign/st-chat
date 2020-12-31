#!/usr/bin/env python

import asyncio
import json
import websockets

from enum import Enum

from lib.PostgresManager import PostgresManager
from lib.ConfigManager import ConfigManager

import time

ACTION_JOIN = "join"
ACTION_MESSAGE = "message"
ACTION_EXIT = "exit"

cm = ConfigManager()

#try:
db = PostgresManager(cm)
#except Exception as e:
#    print(e)

USERS = set()

def get_epoch_str():
    return str(int(time.time()))

def user_join_msg():
    return json.dumps({"action": ACTION_JOIN})

def user_exit_msg():
    return json.dumps({"action": ACTION_EXIT})

async def distribute_message(message):
    if USERS:  
        username = message.split(':')[0]
        new_message = json.dumps({"action": ACTION_MESSAGE, "message": message})
        try:
            db.insert_chat((get_epoch_str(), username, ACTION_MESSAGE, message))
        except Exception as e:
            print(e)
        print(message)
        await asyncio.wait([user.send(new_message) for user in USERS])

async def notify_user_exit():
    if USERS:
        message = user_exit_msg()
        await asyncio.wait([user.send(message) for user in USERS])

async def notify_user_join():
    if USERS:  
        message = user_join_msg()
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    username = ACTION_JOIN
    message = "New user joined chat."
    USERS.add(websocket)
    try:
        db.insert_chat((get_epoch_str(), username, ACTION_JOIN, message))
    except Exception as e:
        print(e)
    print(message)
    await notify_user_join()
async def unregister(websocket):
    username = ACTION_EXIT
    message = "User exited..."
    USERS.remove(websocket)
    try:
        db.insert_chat((get_epoch_str(), username, ACTION_EXIT, message))
    except Exception as e:
        print(e)
    print(message)
    await notify_user_exit()

async def chat(websocket, path):
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            if data["message"] is not None:
                await distribute_message(data["message"])
            else:
                print("Unsupported event: {data}".format(data=data))
    finally:
        await unregister(websocket)

section = "Websocket"
config = None
if section in cm.parser.sections():
    config = cm.parser[section]

host = config['host']
port = config['port']

start_server = websockets.serve(chat, host, port)
print("ST-Chat websocket server started at {host}:{port}.".format(host=host, port=port))

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
