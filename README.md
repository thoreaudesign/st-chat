# st-chat
The goals of this application are below:
1. You are given two feeds running locally, sending messages to a local NATS broker. Catalog every message with an associated timestamp into a persistent storage. These messages are serialized via protobuf, and the spec is outlined in the repository below.
1. Implement a chat room service that allows users to send and receive messages with each other. A room can have N number of users at any given time. This service must accept/send messages over the websockets protocol (https://tools.ietf.org/html/rfc6455). This service must keep a durable record of events in a persistent storage.
1. Ensure exactly once processing semantics for our users and persistent storage.
1. You will find the feeds, NATS broker, and protobuf specs here: https://bitbucket.org/will-sumfest/edge-swe-challenge/src/master/

## Requirements
* python 3.7+ 
* pip 20.3.3+
* docker 1.13.1+
* docker-compose 1.22.0+
 
## Installation
The installation commands below assume the procedure is taking place on a linux command line with docker and docker-compose already installed. 

```
# Clone repository
git clone git@github.com:thoreaudesign/st-chat.git

# Launch containers. 
# Containers include NATS broker, feeds, nginx for chat, and postgres for persistent storage. 
cd st-chat 
docker-compose up -d
```

## Running nats-sub
The nats-sub script subscribes to the NATS broker, parses the messages (protobufs) sent by the two preconfigured subscribers, then stores each message in persistent storage. 

```
# Install python dependencies using virtualenv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Use get-ip.py to get IP addresses for the containers:
>python3 get-ip.py
nats:
 - 172.22.0.3
postgres:
 - 172.22.0.4
sports:
 - 172.22.0.6
nginx:
 - 172.22.0.2
executions:
 - 172.22.0.5
Gateway(s):
  - 172.22.0.1
 
# Update config.ini to use the postgres container IP above. Save.
[Postgres]
host = 172.22.0.4
name = st-chat
user = st-chat
port = 5432
pass = 1qaz2wsx
retries = 3

# Run nats-sub.py
# Use the Gateway IP above for the nats server: 
python3 nats-sub.py sport_event -s nats://172.22.0.1:4222
python3 nats-sub execution -s nats://172.22.0.1:4222
```
