#!/bin/bash

# 1. CD into project folder
cd /root/portfolio

# 2. Fetch latest code from GitHub
git fetch
git reset origin/main --hard

# 3. Spin down containers
docker compose -f docker-compose.prod.yml down

# 4. Rebuild and spin up containers
docker compose -f docker-compose.prod.yml up -d --build


