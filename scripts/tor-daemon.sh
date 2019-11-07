#!/bin/bash
nohup /usr/bin/tor --runasdaemon 0 --defaults-torrc /usr/share/tor/defaults-torrc -f /etc/tor/torrc >/etc/tor/tord.log 2>&1 &
