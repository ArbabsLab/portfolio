#!/bin/bash

cd /root/portfolio
git fetch
git reset origin/main --hard

source python3-virtualenv/bin/activate

pip install -r requirements.txt
deactivate

systemctl daemon-reload
systemctl restart myportfolio
systemctl status myportfolio
