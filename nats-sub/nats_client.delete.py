# Copyright 2016-2018 The NATS Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse, sys
import asyncio
from aioconsole import ainput
import os
import signal
from nats.aio.client import Client as NATS

import time

import shlex

import psycopg2

import concurrent.futures

import signal

username=os.getpid()

print = sys.stdout.write
async def listen(loop, nc, args):

    async def error_cb(e):
        print("Error:", e)
    
    async def closed_cb():
        print("Connection to NATS is closed.")
        await asyncio.sleep(0.1, loop=loop)
        loop.stop()
    
    async def reconnected_cb():
        print(f"Connected to NATS at {nc.connected_url.netloc}...")
    

    async def subscribe_handler(msg):
        print("{username}: {message}".format(username=username, message=msg.data.decode('utf-8')))
        # display message > stdout
        # write to log > database
        return
    

    options = {
        "loop": loop,
        "error_cb": error_cb,
        "closed_cb": closed_cb,
        "reconnected_cb": reconnected_cb
    }
    
    try:
        if len(args.servers) > 0:
            options['servers'] = args.servers
    
        await nc.connect(**options)
    except Exception as e:
        print(e)
        show_usage_and_die()

    print(f"Connected to NATS at {nc.connected_url.netloc}...")

    await nc.subscribe(args.chatroom, args.queue, subscribe_handler)
    
async def speak(nc, args):
    await asyncio.sleep(1)
    while True:
        try:
            text = await ainput('> ')
        
            if text == 'exit':
                print("Disconnecting from chat...")
                os.kill(os.getpid(), signal.SIGTERM)
            else:
                await asyncio.sleep(1)
                await nc.publish(args.chatroom, text.encode('utf-8'))
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            break
        

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('chatroom', default='hello', nargs='?')
    parser.add_argument('-s', '--servers', default=[], action='append')
    parser.add_argument('-q', '--queue', default="")
    return parser.parse_args()

def main():
    args = get_args()

    nc = NATS()

    loop = asyncio.get_event_loop()

    def signal_handler():
        print("Disconnecting...")
        loop.create_task(nc.close())

    for sig in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, sig), signal_handler)

    listen_task = loop.create_task(listen(loop, nc, args))
    speak_task = loop.create_task(speak(nc, args))

    try:    
        loop.run_until_complete(speak_task)
        loop.run_forever(listen_task)
    finally:
        listen_task.cancel()
        speak_task.cancel()
        print('Goodbye!')

if __name__ == '__main__':
    main()
