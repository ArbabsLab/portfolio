#!/bin/bash

URL="http://localhost:5001/api/timeline_post"
NAME="TestBab"
EMAIL="testbab@email.com"
CONTENT="Test post"

echo "POST TEST:"
RESPONSE_POST=$(curl -s -X POST "$URL" \
  -d "name=$NAME" \
  -d "email=$EMAIL" \
  -d "content=$CONTENT")
echo "POST TEST CONCLUDED"
echo "$RESPONSE_POST"

echo "GET TEST:"
RESPONSE_GET=$(curl -s "$URL")
echo "GET TEST CONCLUDED"
echo "$RESPONSE_GET"
