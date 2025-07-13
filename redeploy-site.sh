#!/bin/bash

cd /portfolio
git fetch
git reset origin/main --hard

source python3-virtual-env/bin/activate

pip3 install -r requirements.txt

systemctl daemon-reload
systemctl restart myportfolio
systemctl status myportfolio
