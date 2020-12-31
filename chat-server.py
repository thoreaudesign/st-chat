#!/usr/bin/env python

import asyncio
import json
import websockets

from enum import Enum

from lib.PostgresManager import PostgresManager
from lib.ConfigManager import ConfigManager

ACTION_JOIN = "join"
ACTION_MESSAGE = "message"
ACTION_EXIT = "exit"

conf = ConfigManager()
db = PostgresManager(conf)

USERS = set()

def user_join_msg():
    return json.dumps({"action": ACTION_JOIN})

def user_exit_msg():
    return json.dumps({"action": ACTION_EXIT})

async def distribute_message(message):
    if USERS:  
        new_message = json.dumps({"action": ACTION_MESSAGE, "message": message})
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
    USERS.add(websocket)
    print("New user joined chat.")
    await notify_user_join()

async def unregister(websocket):
    USERS.remove(websocket)
    print("User exited chat.")
    await notify_user_exit()

async def chat(websocket, path):
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            if data["message"] is not None:
                print("Sent message: {message}".format(message=data["message"]))
                await distribute_message(data["message"])
            else:
                print("Unsupported event: {data}".format(data=data))
    finally:
        await unregister(websocket)

host = "10.0.2.15"
port = "8888"

start_server = websockets.serve(chat, host, port)
print("ST-Chat websocket server started at {host}:{port}.".format(host=host, port=port))

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
