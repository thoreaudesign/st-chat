#!/bin/bash
/etc/init.d/nginx start &>/dev/null
python3 -u /app/chat-server.py
