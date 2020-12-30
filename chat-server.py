#!/usr/bin/env python

import asyncio
import json
import logging
import websockets

logging.basicConfig()

USERS = set()

def user_join_msg():
    return json.dumps({"action": "user_join"})

def user_exit_msg():
    return json.dumps({"action": "user_exit"})

async def distribute_message(message):
    if USERS:  
        new_message = json.dumps({"action": "new_message", "message": message})
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
    await notify_user_join()

async def unregister(websocket):
    USERS.remove(websocket)
    await notify_user_exit()

async def chat(websocket, path):
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            if data["message"] is not None:
                print(data["message"])
                await distribute_message(data["message"])
            else:
                logging.error("unsupported event: {}", data)
    finally:
        await unregister(websocket)

start_server = websockets.serve(chat, "10.0.2.15", 8888)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
