
#!/usr/bin/env python

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
import argparse
import asyncio
import os
import signal
import sys
import time

from nats.aio.client import Client as NATS
import psycopg2

from pb2 import event_pb2
from pb2 import execution_pb2
from lib.ConfigManager import ConfigManager
from lib.PostgresManager import PostgresManager

# Initialize config and database managers.
cm = ConfigManager()
try:
    db = PostgresManager(cm)
except Exception as e:
    print(e)

async def run(loop):
    parser = argparse.ArgumentParser()
    parser.add_argument('subject', default='hello', nargs='?')
    parser.add_argument('-s', '--servers', default=[], action='append')
    parser.add_argument('-q', '--queue', default="")
    parser.add_argument('--creds', default="")
    args = parser.parse_args()

    async def error_cb(e):
        print("Error:", e)

    async def closed_cb():
        print("Connection to NATS is closed.")
        await asyncio.sleep(0.1, loop=loop)
        loop.stop()

    async def reconnected_cb():
        print(f"Connected to NATS at {nc.connected_url.netloc}...")

    # Handle messages received from NATS.
    async def subscribe_handler(msg):
        
        # Handles messages from "sport_event" subject.
        if args.subject == "sport_event":
            # Parse protobuf and deserialize the message into an object.
            deser_msg = event_pb2.event()
            deser_msg.ParseFromString(msg.data)

            sport = event_pb2.sport.Name(deser_msg.sport)
            match_title = deser_msg.match_title
            data_event = deser_msg.data_event
            
            # Print string representation of message.
            print("Message: {sport} | {match_title} | {data_event}".format(
                sport=sport, match_title=match_title, data_event=data_event))
            
            # Store message in database.
            db.insert(PostgresManager.INSERT_EVENT,
                (str(int(time.time())), sport, match_title, data_event))

        # Handles messages from "execution" subject.
        if args.subject == "execution":
            # Parse protobuf and deserialize the message into an object.
            deser_msg = execution_pb2.execution()
            deser_msg.ParseFromString(msg.data)

            # Print string representation of message.
            print("Message: {symbol} | {market} | {price} | {quantity} | {executionEpoch} | {stateSymbol}".format(
                symbol=deser_msg.symbol, market=deser_msg.market, price=deser_msg.price,
                quantity=deser_msg.quantity, executionEpoch=deser_msg.executionEpoch, 
                stateSymbol=deser_msg.stateSymbol))

            # Store message in database.
            db.insert(PostgresManager.INSERT_EXECUTION,
                (str(int(time.time())), deser_msg.symbol, deser_msg.market, str(deser_msg.price),
                 str(deser_msg.quantity), str(deser_msg.executionEpoch), deser_msg.stateSymbol))

    options = {
        "loop": loop,
        "error_cb": error_cb,
        "closed_cb": closed_cb,
        "reconnected_cb": reconnected_cb
    }

    if len(args.creds) > 0:
        options["user_credentials"] = args.creds

    # Initialize NATS object.
    nc = NATS()

    # Asynchronously connect to NATS server.
    try:
        if len(args.servers) > 0:
            options['servers'] = args.servers
        await nc.connect(**options)
    except Exception as e:
        print(e)
        show_usage_and_die()
    print(f"Connected to NATS at {nc.connected_url.netloc}...")

    # Signal handler for keyboard interrupt. 
    def signal_handler():
        if nc.is_closed:
            return
        print("Disconnecting...")
        loop.create_task(nc.close())
    
    # Handle keyboard interrupt.
    for sig in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, sig), signal_handler)

    # Subscribe to subject and queue using subscribe_handler callback 
    # to process events. 
    await nc.subscribe(args.subject, args.queue, subscribe_handler)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    try:
        loop.run_forever()
    finally:
        loop.close()
