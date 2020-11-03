#!/bin/bash

# install pip requirements
sudo python3.7 -m pip install -r requirements.txt

# install systemd service and timer
if [ -f /etc/systemd/system/keats-twitterbot.timer ]; then
    sudo systemctl disable keats-twitterbot.timer
    sudo systemctl stop keats-twitterbot.timer
fi

eval "echo -e \"`<keats-twitterbot.service`\"" > /etc/systemd/system/keats-twitterbot.service
eval "echo -e \"`<keats-twitterbot.timer`\"" > /etc/systemd/system/keats-twitterbot.timer

sudo systemctl daemon-reload
sudo systemctl enable keats-twitterbot.timer
sudo systemctl start keats-twitterbot.timer
