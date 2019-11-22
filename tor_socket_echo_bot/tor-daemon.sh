#!/bin/bash
nohup /usr/bin/tor --runasdaemon 0 --defaults-torrc /usr/share/tor/defaults-torrc -f /etc/tor/torrc >/opt/tor_socket_echo_bot/tord.log 2>&1 &
