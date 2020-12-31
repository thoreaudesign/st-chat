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
import os
import signal
from nats.aio.client import Client as NATS

import time

from pb2 import event_pb2
from pb2 import execution_pb2

from lib.ConfigManager import ConfigManager
from lib.PostgresManager import PostgresManager

import psycopg2

# Initialize config and database managers.
cm = ConfigManager()
try:
    db = PostgresManager(cm)
except Exception as e:
    print(e)

def show_usage():
    usage = """
nats-sub SUBJECT [-s SERVER] [-q QUEUE]
Example:
nats-sub help -q workers -s nats://127.0.0.1:4222 -s nats://127.0.0.1:4223
"""
    print(usage)

def show_usage_and_die():
    show_usage()
    sys.exit(1)

async def run(loop):
    parser = argparse.ArgumentParser()

    # e.g. nats-sub hello -s nats://127.0.0.1:4222
    parser.add_argument('subject', default='hello', nargs='?')
    parser.add_argument('-s', '--servers', default=[], action='append')
    parser.add_argument('-q', '--queue', default="")
    parser.add_argument('--creds', default="")
    args = parser.parse_args()

    nc = NATS()

    async def error_cb(e):
        print("Error:", e)

    async def closed_cb():
        print("Connection to NATS is closed.")
        await asyncio.sleep(0.1, loop=loop)
        loop.stop()

    async def reconnected_cb():
        print(f"Connected to NATS at {nc.connected_url.netloc}...")

    async def subscribe_handler(msg):
        if args.subject == "sport_event":
            deser_msg = event_pb2.event()
            deser_msg.ParseFromString(msg.data)

            sport = event_pb2.sport.Name(deser_msg.sport)
            match_title = deser_msg.match_title
            data_event = deser_msg.data_event

            print("Message: {sport} | {match_title} | {data_event}".format(
                sport=sport, match_title=match_title, data_event=data_event))
            
            db.insert(PostgresManager.INSERT_EVENT,
                (str(int(time.time())), sport, match_title, data_event))

        if args.subject == "execution":
            deser_msg = execution_pb2.execution()
            deser_msg.ParseFromString(msg.data)

            print("Message: {symbol} | {market} | {price} | {quantity} | {executionEpoch} | {stateSymbol}".format(
                symbol=deser_msg.symbol, market=deser_msg.market, price=deser_msg.price,
                quantity=deser_msg.quantity, executionEpoch=deser_msg.executionEpoch, 
                stateSymbol=deser_msg.stateSymbol))

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

    try:
        if len(args.servers) > 0:
            options['servers'] = args.servers

        await nc.connect(**options)
    except Exception as e:
        print(e)
        show_usage_and_die()

    print(f"Connected to NATS at {nc.connected_url.netloc}...")
    def signal_handler():
        if nc.is_closed:
            return
        print("Disconnecting...")
        loop.create_task(nc.close())

    for sig in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, sig), signal_handler)

    await nc.subscribe(args.subject, args.queue, subscribe_handler)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    try:
        loop.run_forever()
    finally:
        loop.close()
